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

# 中医考试科目分类
subject2category = {
    "中医基础理论": "tcm_basic",
    "中医诊断学": "tcm_diagnosis", 
    "中药学": "tcm_pharmacy",
    "方剂学": "tcm_formula",
    "针灸学": "tcm_acupuncture",
    "中医内科学": "tcm_internal",
    "中医外科学": "tcm_surgery",
    "中医妇科学": "tcm_gynecology",
    "中医儿科学": "tcm_pediatrics",
    "内科学": "western_internal",
    "诊断学基础": "western_diagnosis",
    "传染病学": "infectious_disease",
    "医学伦理学": "medical_ethics",
    "卫生法规": "health_law",
}

# 中医考试5选项题目模板
QUERY_TEMPLATE_TCM = """
请回答以下中医执医考试题目。请仔细思考后，在回答的最后一行使用格式'答案：$LETTER'（不带引号），其中LETTER是A、B、C、D、E中的一个。

{题目}

A) {A}
B) {B}
C) {C}
D) {D}
E) {E}
""".strip()

# 中文答案提取正则表达式
TCM_ANSWER_PATTERN = r"(?i)答案\s*[：:]\s*([A-E])"

def format_tcm_question(row):
    """格式化中医考试题目"""
    return QUERY_TEMPLATE_TCM.format(
        题目=row["题目"],
        A=row["选项"]["A"],
        B=row["选项"]["B"], 
        C=row["选项"]["C"],
        D=row["选项"]["D"],
        E=row["选项"]["E"]
    )

def extract_tcm_answer(response_text):
    """从回答中提取中医考试题答案"""
    if "</think>" in response_text:
        response_text = response_text.split("</think>")[1].strip()
    # 首先尝试提取中文格式的答案
    matches = re.findall(TCM_ANSWER_PATTERN, response_text)
    if matches:
        return normalize_extracted_answer(matches[-1])

    # 如果没有找到中文格式，尝试使用通用的答案提取模式
    # 支持更多格式：Answer: A, 答案是A, 选择A等
    patterns = [
        r"(?i)答案\s*[是为]\s*([A-E])",
        r"(?i)选择\s*([A-E])",
        r"(?i)Answer\s*[:\s]\s*([A-E])",
        r"(?i)答\s*[：:]\s*([A-E])",
        r"\b([A-E])\b(?=\s*$)",
        r"^([A-E])\s*[\)）]",
        r"\b([A-E])\s*[\)）]",
        r"^([A-E])\s*[\)）]",
        r"\b([A-E])\s*[\)）]",
        r".*?([A-E])(?=[^A-E]*$)",
    ]

    for pattern in patterns:
        matches = re.findall(pattern, response_text)
        if matches:
            return normalize_extracted_answer(matches[-1])

    return None

def parse_tcm_answer(answer_str):
    """解析标准答案字符串，提取字母"""
    # 标准格式如"答案：B"
    matches = re.findall(r"答案\s*[：:]\s*([A-E])", answer_str)
    if matches:
        return matches[-1]
    # 备用格式，直接是字母
    matches = re.findall(r"([A-E])", answer_str)
    if matches:
        return matches[-1]
    return None


class TCPEEval(Eval):
    """中医执医考试评测类"""

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

    def __call__(self, sampler: SamplerBase) -> EvalResult:
        def fn(row: dict):
            prompt_messages = [
                sampler._pack_message(
                    content=format_tcm_question(row), role="user"
                )
            ]
            sampler_response = sampler(prompt_messages)
            response_text = sampler_response.response_text
            actual_queried_prompt_messages = sampler_response.actual_queried_message_list
            response_text = normalize_response(response_text)

            # 提取模型回答的答案
            extracted_answer = extract_tcm_answer(response_text)

            # 解析标准答案
            correct_answer = parse_tcm_answer(row["答案"])

            # 计算分数
            score = 1.0 if extracted_answer == correct_answer else 0.0

            # 生成HTML报告
            html = common.jinja_env.from_string(HTML_JINJA).render(
                prompt_messages=actual_queried_prompt_messages,
                next_message=dict(content=response_text, role="assistant"),
                score=score,
                correct_answer=correct_answer,
                extracted_answer=extracted_answer,
            )

            convo = actual_queried_prompt_messages + [dict(content=response_text, role="assistant")]
            # category = subject2category.get(row["科目"], "other")
            category = row["科目"]

            return SingleEvalResult(
                html=html, 
                score=score, 
                metrics={category: score, "overall": score}, 
                convo=convo
            )

        results = common.map_with_progress(fn, self.examples, num_threads=self.num_threads)
        return common.aggregate_results(results)
