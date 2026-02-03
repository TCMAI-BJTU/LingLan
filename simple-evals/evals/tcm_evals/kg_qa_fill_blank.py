import json
import random
import re
from typing import Set

from ... import common
from ...common import HTML_JINJA, normalize_response
from ...types import Eval, EvalResult, SamplerBase, SingleEvalResult

# 填空题提示模板
FILL_BLANK_TEMPLATE = """
请回答以下填空题。仔细思考后，在空白处填入合适的答案。

最终答案的输出格式如下，多个答案用逗号分隔：
答案: 

问题：
{question}
""".strip()

def calculate_char_f1(pred_str: str, gold_str: str) -> float:
    """计算字符级别的F1值"""
    if not pred_str and not gold_str:
        return 1.0
    if not pred_str or not gold_str:
        return 0.0
    
    # 转换为字符集合
    pred_chars = set(pred_str.strip())
    gold_chars = set(gold_str.strip())
    
    # 计算交集
    common_chars = pred_chars & gold_chars
    
    if len(pred_chars) == 0 and len(gold_chars) == 0:
        return 1.0
    if len(common_chars) == 0:
        return 0.0
    
    precision = len(common_chars) / len(pred_chars) if len(pred_chars) > 0 else 0.0
    recall = len(common_chars) / len(gold_chars) if len(gold_chars) > 0 else 0.0
    
    if precision + recall == 0:
        return 0.0
    
    f1 = 2 * precision * recall / (precision + recall)
    return f1

def extract_fill_blank_answer(response_text: str) -> list:
    """从回答中提取填空题答案，支持多个答案"""
    if "</think>" in response_text:
        response_text = response_text.split("</think>")[1].strip()
    response_text = response_text.strip()
    
    # 尝试不同的答案提取模式
    patterns = [
        r"答案\s*[：:]\s*(.+?)(?:\n|$)",
        r"填入\s*[：:]\s*(.+?)(?:\n|$)", 
        r"答案是\s*[：:]?\s*(.+?)(?:\n|$)",
        r"应该填\s*[：:]?\s*(.+?)(?:\n|$)",
        r"^(.+?)$",  # 整个回答作为答案
    ]

    extracted_text = ""
    for pattern in patterns:
        matches = re.findall(pattern, response_text)
        if matches:
            extracted_text = matches[-1].strip()
            break

    if not extracted_text:
        # 如果没有匹配到，返回整个回答的前50个字符
        extracted_text = response_text[:50].strip()

    # 清理一些常见的前后缀
    extracted_text = re.sub(r'^["""\'\s]*|[\"""\'\s]*$', '', extracted_text)
    extracted_text = re.sub(r'。$', '', extracted_text)

    # 按逗号分割答案
    answers = [answer.strip() for answer in extracted_text.split(',') if answer.strip()]

    # 如果没有逗号分割，返回单个答案
    if not answers:
        answers = [extracted_text] if extracted_text else [""]

    return answers

def calculate_fill_blank_f1(pred_answers: list, gold_answers: list) -> dict:
    """计算填空题的F1值，不考虑多空顺序，直接拼接计算"""
    if not pred_answers and not gold_answers:
        return {"f1_score": 1.0}
    
    # 直接将所有预测答案和标准答案拼接
    combined_pred = "".join(pred_answers)
    combined_gold = "".join(gold_answers)
    
    # 计算字符级F1值
    f1_score = calculate_char_f1(combined_pred, combined_gold)
    
    return {
        "f1_score": f1_score,
        "num_blanks": len(gold_answers)
    }

class KGQAFillBlankEval(Eval):
    """知识图谱问答填空题评测类"""

    def __init__(self, data_path:str, num_examples: int | None = None, num_threads: int = 1):
        examples = []
        with open(data_path, 'r', encoding='utf-8') as f:
            for line in f:
                if line.strip():
                    data = json.loads(line)
                    if data["question_type"] == "fill_blank":
                        examples.append(data)

        if num_examples:
            examples = random.Random(0).sample(examples, min(num_examples, len(examples)))

        self.examples = examples
        self.num_threads = num_threads
        print(f"加载了 {len(examples)} 道填空题")

    def __call__(self, sampler: SamplerBase) -> EvalResult:
        def fn(row: dict):
            prompt_messages = [
                sampler._pack_message(
                    content=FILL_BLANK_TEMPLATE.format(question=row["question"]), 
                    role="user"
                )
            ]
            sampler_response = sampler(prompt_messages)
            response_text = sampler_response.response_text
            actual_queried_prompt_messages = sampler_response.actual_queried_message_list
            response_text = normalize_response(response_text)

            # 提取模型回答的答案
            extracted_answers = extract_fill_blank_answer(response_text)

            # 标准答案，按顿号分割
            correct_answer_str = row["answer"]
            correct_answers = [answer.strip() for answer in correct_answer_str.split('、') if answer.strip()]

            # 计算填空题的F1值
            f1_result = calculate_fill_blank_f1(extracted_answers, correct_answers)
            f1_score = f1_result["f1_score"]

            # 生成HTML报告
            html = common.jinja_env.from_string(HTML_JINJA).render(
                prompt_messages=actual_queried_prompt_messages,
                next_message=dict(content=response_text, role="assistant"),
                score=f1_score,
                correct_answer=correct_answer_str,
                extracted_answer=", ".join(extracted_answers),
            )

            convo = actual_queried_prompt_messages + [dict(content=response_text, role="assistant")]

            return SingleEvalResult(
                html=html, 
                score=f1_score, 
                metrics={
                    "f1_score": f1_score,
                    "num_blanks": f1_result["num_blanks"],
                    "num_extracted": len(extracted_answers),
                    "num_correct": len(correct_answers)
                }, 
                convo=convo
            )

        results = common.map_with_progress(fn, self.examples, num_threads=self.num_threads)
        return common.aggregate_results(results)
