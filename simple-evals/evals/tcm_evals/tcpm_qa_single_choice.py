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

# 单选题提示模板
SINGLE_CHOICE_TEMPLATE = """
请回答以下单选题。仔细思考后，在回答的最后一行使用格式'答案：$LETTER'（不带引号），其中LETTER是A、B、C、D、E中的一个。

{question}

{options}
""".strip()

def format_single_choice_question(row):
    """格式化单选题"""
    options_text = "\n".join(row["options"])
    return SINGLE_CHOICE_TEMPLATE.format(
        question=row["question"],
        options=options_text
    )

def extract_single_choice_answer(response_text):
    """从回答中提取单选题答案"""
    if "</think>" in response_text:
        response_text = response_text.split("</think>")[1].strip()
    # 中文答案提取正则表达式
    patterns = [
        r"(?i)答案\s*[：:]\s*([A-E])",
        r"(?i)答案\s*[是为]\s*([A-E])",
        r"(?i)选择\s*([A-E])",
        r"(?i)Answer\s*[:\s]\s*([A-E])",
        r"(?i)答\s*[：:]\s*([A-E])",
        r"\b([A-E])\b(?=\s*$)",
        r"^([A-E])\s*[\)）]",
        r"\b([A-E])\s*[\)）]",
        r".*?([A-E])(?=[^A-E]*$)",
    ]

    for pattern in patterns:
        matches = re.findall(pattern, response_text)
        if matches:
            return normalize_extracted_answer(matches[-1])

    return None

class TCPMQASingleChoiceEval(Eval):
    """中成药知识问答单选题评测类"""

    def __init__(self, data_path: str, num_examples: int | None = None, num_threads: int = 1):
        examples = []
        with open(data_path, 'r', encoding='utf-8') as f:
            for line in f:
                if line.strip():
                    data = json.loads(line)
                    if data.get("question_type") == "single_choice":
                        examples.append(data)

        if num_examples:
            examples = random.Random(0).sample(examples, min(num_examples, len(examples)))

        self.examples = examples
        self.num_threads = num_threads
        print(f"加载了 {len(examples)} 道中成药单选题")

    def __call__(self, sampler: SamplerBase) -> EvalResult:
        def fn(row: dict):
            prompt_messages = [
                sampler._pack_message(
                    content=format_single_choice_question(row), role="user"
                )
            ]
            sampler_response = sampler(prompt_messages)
            response_text = sampler_response.response_text
            actual_queried_prompt_messages = sampler_response.actual_queried_message_list
            response_text = normalize_response(response_text)

            # 提取模型回答的答案
            extracted_answer = extract_single_choice_answer(response_text)

            # 标准答案
            correct_answer = row["answer"]

            # 计算准确率
            accuracy = 1.0 if extracted_answer == correct_answer else 0.0

            # 生成HTML报告
            html = common.jinja_env.from_string(HTML_JINJA).render(
                prompt_messages=actual_queried_prompt_messages,
                next_message=dict(content=response_text, role="assistant"),
                score=accuracy,
                correct_answer=correct_answer,
                extracted_answer=extracted_answer,
            )

            convo = actual_queried_prompt_messages + [dict(content=response_text, role="assistant")]

            return SingleEvalResult(
                html=html, 
                score=accuracy, 
                metrics={"accuracy": accuracy}, 
                convo=convo
            )

        results = common.map_with_progress(fn, self.examples, num_threads=self.num_threads)
        return common.aggregate_results(results)
