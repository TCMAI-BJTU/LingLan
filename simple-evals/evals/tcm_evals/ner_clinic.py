import json
import random
import re
from collections import defaultdict
from typing import Dict, List, Set, Tuple

from ... import common
from ...common import HTML_JINJA
from ...types import Eval, EvalResult, SamplerBase, SingleEvalResult

# 实体抽取提示模板
NER_CLINIC_TEMPLATE = """
请从以下病历文本中抽取指定类型的实体。

注意：
1. 请先仔细分析文本内容，思考每个实体类型的识别要点，然后再输出结果
2. 如果某个实体类型在文本中没有对应实体，请返回空列表[]
3. 如果同一个实体在文本中出现多次，请在列表中按顺序重复出现

文本：
{text}

需要抽取的实体类型：
{entity_types}

请按照以下JSON格式输出结果，每个实体类型对应一个列表，如果文本中某个实体出现多次，请在列表中重复出现：

```json
{{
  "实体类型1": ["实体1", "实体2", ...],
  "实体类型2": ["实体1", "实体2", ...],
  ...
}}
```
""".strip()

def extract_entities_from_response(response_text: str, entity_types: List[str]) -> Dict[str, List[str]]:
    """从模型回答中提取实体结果"""
    try:
        if "</think>" in response_text:
            response_text = response_text.split("</think>")[1].strip()
        # 使用提供的JSON提取代码
        if "```json" in response_text:
            response_text = response_text.split("```json")[1].split("```")[0]
        result = json.loads(response_text)
        # 确保所有实体类型都有对应的键
        for entity_type in entity_types:
            if entity_type not in result:
                result[entity_type] = []

        keys_to_remove = []
        for k, v in result.items():
            if k not in entity_types:
                keys_to_remove.append(k)
            if v is None:
                result[k] = []

        for k in keys_to_remove:
            result.pop(k)

        return result
    except:
        pass

    # 使用正则表达式在response_text里查找JSON字典（{...}），返回字符串列表
    json_dict_matches = re.findall(r"({[\s\S]*?})", response_text)
    for match in json_dict_matches:
        try:
            result = json.loads(match)
            # 确保所有实体类型都有对应的键
            for entity_type in entity_types:
                if entity_type not in result:
                    result[entity_type] = []
            return result
        except Exception:
            continue

    # 如果没有找到JSON格式，尝试解析其他格式
    result = {entity_type: [] for entity_type in entity_types}

    # 尝试解析类似 "实体类型：实体1, 实体2" 的格式
    for entity_type in entity_types:
        pattern = f"{entity_type}[：:]\s*([^\n]*)"
        matches = re.findall(pattern, response_text)
        if matches:
            entities_str = matches[-1].strip()
            if entities_str and entities_str != "无" and entities_str != "[]":
                # 按逗号分割并清理
                entities = [e.strip() for e in entities_str.split(',') if e.strip()]
                result[entity_type] = entities
    return result

def calculate_ner_metrics(pred_entities: Dict[str, List[str]], 
                         gold_entities: Dict[str, List[str]]) -> Tuple[float, float, float]:
    """计算实体抽取的precision, recall, f1"""
    
    # 将实体转换为(entity_type, entity)的元组集合，考虑重复
    def entities_to_set(entities_dict):
        entity_set = []
        for entity_type, entities in entities_dict.items():
            for entity in entities:
                entity_set.append((entity_type, entity))
        return entity_set
    
    pred_set = entities_to_set(pred_entities)
    gold_set = entities_to_set(gold_entities)
    
    # 计算交集
    correct = 0
    for pred_entity in pred_set:
        if pred_entity in gold_set:
            correct += 1
            gold_set.remove(pred_entity)  # 避免重复计算
    
    total_pred = len(pred_set)
    total_gold = len(entities_to_set(gold_entities))  # 重新计算原始gold_set长度
    
    # 计算指标
    precision = correct / total_pred if total_pred > 0 else 0.0
    recall = correct / total_gold if total_gold > 0 else 0.0
    f1 = 2 * precision * recall / (precision + recall) if (precision + recall) > 0 else 0.0
    
    return precision, recall, f1

class NERClinicEval(Eval):
    """病历实体抽取评测类"""

    def __init__(self, data_path: str, num_examples: int | None = None, num_threads: int = 1):
        examples = []
        with open(data_path, 'r', encoding='utf-8') as f:
            for line in f:
                if line.strip():
                    examples.append(json.loads(line))

        if num_examples:
            examples = random.Random(0).sample(examples, min(num_examples, len(examples)))

        self.examples = examples
        self.num_threads = num_threads
        print(f"加载了 {len(examples)} 条病历实体抽取样本")

    def __call__(self, sampler: SamplerBase) -> EvalResult:
        def fn(row: dict):
            entity_types_str = "、".join(row["entity_types"])
            prompt_messages = [
                sampler._pack_message(
                    content=NER_CLINIC_TEMPLATE.format(
                        text=row["text"],
                        entity_types=entity_types_str
                    ), 
                    role="user"
                )
            ]
            sampler_response = sampler(prompt_messages)
            response_text = sampler_response.response_text
            actual_queried_prompt_messages = sampler_response.actual_queried_message_list

            # 提取模型识别的实体
            pred_entities = extract_entities_from_response(response_text, row["entity_types"])

            # 标准答案
            gold_entities = row["entities"]

            # 计算指标
            precision, recall, f1 = calculate_ner_metrics(pred_entities, gold_entities)

            # 生成HTML报告
            html = common.jinja_env.from_string(HTML_JINJA).render(
                prompt_messages=actual_queried_prompt_messages,
                next_message=dict(content=response_text, role="assistant"),
                score=f1,
                correct_answer=str(gold_entities),
                extracted_answer=str(pred_entities),
            )

            convo = actual_queried_prompt_messages + [dict(content=response_text, role="assistant")]

            result = SingleEvalResult(
                html=html, 
                score=f1, 
                metrics={
                    "precision": precision,
                    "recall": recall, 
                    "f1": f1
                }, 
                convo=convo
            )
            return result

        results = common.map_with_progress(fn, self.examples, num_threads=self.num_threads)
        return common.aggregate_results(results)
