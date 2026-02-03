import json
import random
import re
from typing import Any

from ... import common
from ...common import HTML_JINJA
from ...types import Eval, EvalResult, SamplerBase, SingleEvalResult

# 治法选择题提示模板
TREATMENT_CHOICE_TEMPLATE = """
根据以下病历记录，请选择最合适的中医治法。请仔细分析患者的症状表现、辨证结果，选择最适合的治疗方法。
请在回答的最后一行使用格式'答案：$LETTER'（不带引号），其中LETTER是A、B、C、D、E中的一个。

{question}

选项：
{options_text}
""".strip()

def extract_treatment_choice_answer(response_text: str) -> str:
    """从模型回答中提取选择题答案"""
    if "</think>" in response_text:
        response_text = response_text.split("</think>")[1].strip()
    # 先查找标准格式的答案
    patterns = [
        r"答案[：:]\s*([ABCDE])",
        r"答案\s*[：:]\s*([ABCDE])",
        r"答案[：:]?([ABCDE])",
        r"选择[：:]\s*([ABCDE])",
        r"选择\s*[：:]\s*([ABCDE])",
        r"选择[：:]?([ABCDE])",
        r"我的答案是\s*([ABCDE])",
        r"答案是\s*([ABCDE])",
        r"选择\s*([ABCDE])",
        r"([ABCDE])\s*[。.]?\s*$",
        r"^([ABCDE])\s*[。.]?",
        r"[选择|答案|选项].*?([ABCDE])",
        r"^([A-E])\s*[\)）]",
        r"\b([A-E])\s*[\)）]",
        r".*?([A-E])(?=[^A-E]*$)",
    ]

    for pattern in patterns:
        matches = re.findall(pattern, response_text, re.IGNORECASE | re.MULTILINE)
        if matches:
            return matches[-1].upper()

    # 如果找不到标准格式，尝试提取所有字母
    letters = re.findall(r'[ABCDE]', response_text.upper())
    if letters:
        # 返回最后出现的字母
        return letters[-1]

    # 如果都找不到，返回空字符串
    return ""

class TreatmentChoiceEval(Eval):
    """治法选择题评测类"""

    def __init__(self, data_path: str, num_examples: int | None = None, num_threads: int = 1):
        # 读取数据
        self.samples = []
        with open(data_path, 'r', encoding='utf-8') as f:
            for line in f:
                self.samples.append(json.loads(line.strip()))

        if num_examples:
            self.samples = random.sample(self.samples, min(num_examples, len(self.samples)))

        self.num_threads = num_threads

    def __call__(self, sampler: SamplerBase) -> EvalResult:
        """执行评测"""
        def fn(row: dict[str, Any]) -> SingleEvalResult:
            # 格式化选项文本
            options_text = "\n".join(row["options"])

            # 构建提示词
            prompt_messages = [
                {
                    "role": "user",
                    "content": TREATMENT_CHOICE_TEMPLATE.format(
                        question=row["question"],
                        options_text=options_text
                    )
                }
            ]

            # 获取模型回答
            sampler_response = sampler(prompt_messages)
            response_text = sampler_response.response_text
            actual_queried_prompt_messages = sampler_response.actual_queried_message_list

            # 提取答案
            predicted_answer = extract_treatment_choice_answer(response_text)
            correct_answer = row["answer"]

            # 计算准确率
            is_correct = predicted_answer == correct_answer
            score = 1.0 if is_correct else 0.0

            # 生成HTML报告
            html = common.jinja_env.from_string(HTML_JINJA).render(
                prompt_messages=actual_queried_prompt_messages,
                next_message=dict(content=response_text, role="assistant"),
                score=score,
                correct_answer=f"正确答案: {correct_answer}",
                extracted_answer=f"预测答案: {predicted_answer}" if predicted_answer else "预测答案: 未找到",
            )

            convo = actual_queried_prompt_messages + [dict(content=response_text, role="assistant")]

            return SingleEvalResult(
                html=html,
                score=score,
                metrics={"accuracy": score},
                convo=convo,
            )

        # 执行并行评测
        results = common.map_with_progress(fn, self.samples, num_threads=self.num_threads)

        # 使用公共函数聚合结果
        return common.aggregate_results(results)
