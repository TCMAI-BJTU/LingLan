"""将三个发布文件按病例编号关联，供现有诊疗全流程评估使用。"""

import json
from pathlib import Path
import re


COMPONENTS = (
    ("syndrome", "医家辨证.jsonl", "辨证"),
    ("treatment_method", "医家治法.jsonl", "治法"),
    ("herbal_prescription", "医家处方.jsonl", "处方"),
)


def _read_jsonl(path: Path) -> list[dict]:
    rows = []
    with path.open(encoding="utf-8") as stream:
        for line_number, line in enumerate(stream, 1):
            if not line.strip():
                continue
            try:
                row = json.loads(line)
            except json.JSONDecodeError as error:
                raise ValueError(f"{path}:{line_number}: 无效 JSON") from error
            if not isinstance(row, dict):
                raise ValueError(f"{path}:{line_number}: 每条记录必须是 JSON 对象")
            rows.append(row)
    if not rows:
        raise ValueError(f"{path}: 没有可评估的病例")
    return rows


def load_diagnostic_therapeutic_examples(data_path: str | Path) -> list[dict]:
    """读取包含辨证、治法和处方三个发布文件的目录。

    新文件使用各任务 id 的四位后缀关联，保留辨证文件的原始顺序。
    关联后每个病例仍只生成一次完整诊疗回答。
    """
    path = Path(data_path)
    if not path.is_dir():
        raise FileNotFoundError(f"诊疗推理数据目录不存在：{path}")

    components = {}
    for task, filename, _ in COMPONENTS:
        source = path / filename
        indexed = {}
        for row_number, row in enumerate(_read_jsonl(source), 1):
            location = f"{source}:记录 {row_number}"
            if row.get("task") != task:
                raise ValueError(f"{location}: task 应为 {task}")
            match = re.fullmatch(re.escape(task) + r"_([0-9]{4})", str(row.get("id", "")))
            if not match:
                raise ValueError(f"{location}: id 应为 {task}_四位数字")
            case_id = match.group(1)
            if case_id in indexed:
                raise ValueError(f"{location}: 重复病例编号 {case_id}")
            for field in ("病历文本", "answer"):
                if not isinstance(row.get(field), str) or not row[field].strip():
                    raise ValueError(f"{location}: 缺少有效的 {field} 字段")
            if "医家" not in row:
                raise ValueError(f"{location}: 缺少 医家 字段")
            physician = row["医家"]
            if physician is not None and not isinstance(physician, str):
                raise ValueError(f"{location}: 医家 必须是字符串或空值")
            row["医家"] = physician
            indexed[case_id] = row
        components[task] = indexed

    case_ids = set(components["syndrome"])
    for task, indexed in components.items():
        if set(indexed) != case_ids:
            missing = sorted(case_ids - set(indexed))
            extra = sorted(set(indexed) - case_ids)
            raise ValueError(
                f"{path}: {task} 病例编号不一致；"
                f"缺少 {len(missing)} 个 {missing[:5]}，多出 {len(extra)} 个 {extra[:5]}"
            )

    examples = []
    for case_id, syndrome in components["syndrome"].items():
        example = {
            "id": f"diagnostic_therapeutic_reasoning_{case_id}",
            "task": "diagnostic_therapeutic_reasoning",
            "医家": syndrome["医家"],
            "病历文本": syndrome["病历文本"],
            "source_ids": {},
        }
        for task, _, field in COMPONENTS:
            row = components[task][case_id]
            for shared_field in ("医家", "病历文本"):
                if row[shared_field] != syndrome[shared_field]:
                    raise ValueError(f"{path}: 病例 {case_id} 的 {task} {shared_field} 不一致")
            example[field] = row["answer"]
            example["source_ids"][task] = row["id"]
        examples.append(example)
    return examples
