import json
import random
import re

from ... import common
from ...common import (
    HTML_JINJA,
    normalize_extracted_answer,
    normalize_response,
)
from ...types import Eval, EvalResult, SamplerBase, SingleEvalResult

# 多选题提示模板
MULTI_CHOICE_TEMPLATE = """
请回答以下多选题。仔细思考后，在回答的最后一行使用格式'答案：$LETTERS'（不带引号），其中LETTERS是多个字母，如'A,C,E'或'ACE'。

{question}

{options}
""".strip()

def format_multi_choice_question(row):
    """格式化多选题"""
    options_text = "\n".join(row["options"])
    return MULTI_CHOICE_TEMPLATE.format(
        question=row["question"],
        options=options_text
    )

def extract_multi_choice_answer(response_text):
    """从回答中提取多选题答案"""
    if "</think>" in response_text:
        response_text = response_text.split("</think>")[1].strip()
    # 多选题答案提取正则表达式
    patterns = [
        r"(?i)答案\s*[：:]\s*([A-E,\s]+)",
        r"(?i)答案\s*[是为]\s*([A-E,\s]+)",
        r"(?i)选择\s*([A-E,\s]+)",
        r"(?i)Answer\s*[:\s]\s*([A-E,\s]+)",
        r"(?i)答\s*[：:]\s*([A-E,\s]+)",
    ]

    for pattern in patterns:
        matches = re.findall(pattern, response_text)
        if matches:
            answer_str = matches[-1].strip()
            # 提取所有字母，忽略逗号、空格等分隔符
            letters = re.findall(r'[A-E]', answer_str.upper())
            # 去重并排序
            letters = sorted(list(set(letters)))
            return letters

    # 如果没有找到格式化的答案，尝试在整个回答中查找字母
    letters = re.findall(r'\b([A-E])\b', response_text.upper())
    if letters:
        # 去重并排序
        letters = sorted(list(set(letters)))
        return letters

    return []

def calculate_multi_choice_metrics(predicted, actual):
    """计算多选题的精确率、召回率和F1值"""
    if not predicted and not actual:
        return 1.0, 1.0, 1.0  # 都为空，认为完全正确
    
    if not predicted:
        return 0.0, 0.0, 0.0  # 预测为空但实际不为空
    
    if not actual:
        return 0.0, 0.0, 0.0  # 实际为空但预测不为空
    
    # 转换为集合进行计算
    predicted_set = set(predicted)
    actual_set = set(actual)
    
    # 计算交集
    intersection = predicted_set & actual_set
    
    # 精确率 = 正确预测的选项数 / 预测的选项总数
    precision = len(intersection) / len(predicted_set) if predicted_set else 0.0
    
    # 召回率 = 正确预测的选项数 / 实际正确选项总数
    recall = len(intersection) / len(actual_set) if actual_set else 0.0
    
    # F1值 = 2 * (精确率 * 召回率) / (精确率 + 召回率)
    f1 = 2 * (precision * recall) / (precision + recall) if (precision + recall) > 0 else 0.0
    
    return precision, recall, f1

class TCPMQAMultiChoiceEval(Eval):
    """中成药知识问答多选题评测类"""

    def __init__(self, data_path: str, num_examples: int | None = None, num_threads: int = 1):
        examples = []
        with open(data_path, 'r', encoding='utf-8') as f:
            for line in f:
                if line.strip():
                    data = json.loads(line)
                    if data.get("question_type") == "multiple_choice":
                        examples.append(data)

        if num_examples:
            examples = random.Random(0).sample(examples, min(num_examples, len(examples)))

        self.examples = examples
        self.num_threads = num_threads
        print(f"加载了 {len(examples)} 道中成药多选题")

    def __call__(self, sampler: SamplerBase) -> EvalResult:
        def fn(row: dict):
            prompt_messages = [
                sampler._pack_message(
                    content=format_multi_choice_question(row), role="user"
                )
            ]
            sampler_response = sampler(prompt_messages)
            response_text = sampler_response.response_text
            actual_queried_prompt_messages = sampler_response.actual_queried_message_list
            response_text = normalize_response(response_text)

            # 提取模型回答的答案
            extracted_answer = extract_multi_choice_answer(response_text)

            # 标准答案，需要排序以便比较
            # 固定格式：["BCD"] -> ["B", "C", "D"]
            correct_answer = sorted(list(row["answer"][0]))

            # 计算准确率（完全匹配）
            accuracy = 1.0 if extracted_answer == correct_answer else 0.0

            # 计算精确率、召回率和F1值
            precision, recall, f1 = calculate_multi_choice_metrics(extracted_answer, correct_answer)

            # 生成HTML报告
            html = common.jinja_env.from_string(HTML_JINJA).render(
                prompt_messages=actual_queried_prompt_messages,
                next_message=dict(content=response_text, role="assistant"),
                score=f1,
                correct_answer=",".join(correct_answer),
                extracted_answer=",".join(extracted_answer) if extracted_answer else "None",
            )

            convo = actual_queried_prompt_messages + [dict(content=response_text, role="assistant")]

            return SingleEvalResult(
                html=html, 
                score=accuracy, 
                metrics={
                    "accuracy": accuracy,
                    "precision": precision,
                    "recall": recall,
                    "f1": f1
                }, 
                convo=convo
            )

        results = common.map_with_progress(fn, self.examples, num_threads=self.num_threads)
        return common.aggregate_results(results)
