import io
import os
from collections import defaultdict
from concurrent.futures import ThreadPoolExecutor, as_completed
from multiprocessing.pool import ThreadPool
from typing import Any, Callable

import jinja2
import numpy as np
import requests
from tqdm import tqdm

from .types import EvalResult, Message, SamplerBase, SingleEvalResult

ROOT_PATH = "../simple_evals"

QUERY_TEMPLATE_MULTICHOICE = """
Answer the following multiple choice question. The last line of your response should be of the following format: 'Answer: $LETTER' (without quotes) where LETTER is one of ABCD. Think step by step before answering.

{Question}

A) {A}
B) {B}
C) {C}
D) {D}
""".strip()

ANSWER_PATTERN_MULTICHOICE = r"(?i)Answer[ \t]*:[ \t]*\$?([A-D])\$?"
ANSWER_PATTERN = r"(?i)Answer\s*:\s*([^\n]+)"
MULTILINGUAL_ANSWER_PATTERN_TEMPLATE = (
    "(?i){}[ \t]*([A-D]|[أ-د]|[অ]|[ব]|[ড]|[ঢ]|[Ａ]|[Ｂ]|[Ｃ]|[Ｄ])"
)
# All the different ways "Answer" is written in different languages
MULTILINGUAL_ANSWER_REGEXES = [
    "Answer\s*:",
    "Answer\s*:​​​​​​",  # Korean invisible character
    "উত্তর\s*:",
    "उत्तर\s*:",
    "উত্তরঃ",
    "উত্তর\s*:",
    "Antwort\s*:",
    "답변\s*:",
    "정답\s*:",
    "답\s*:",
    "答案\s*：",
    "答案\s*:",
    "答\s*：",
    "答\s*:",
    "答复\s*：",
    "答曰\s*：",
    "الإجابة:",
    "الجواب:",
    "إجابة:",
    "الإجابة النهائية:",
    "الإجابة الصحيحة:",
    "الإجابة الصحيحة هي:",
    "الإجابة هي:",
    "الجواب النهائي:",
    "Respuesta\s*:",
    "Risposta\s*:",
    "答え\s*:",
    "答え\s*：",
    "回答\s*:",
    "回答\s*：",
    "解答\s*:",
    "Jawaban\s*:",
    "Réponse\s*:",
    "Resposta\s*:",
    "Jibu\s*:",
    "Idahun\s*:",
    "Ìdáhùn\s*:",
    "Idáhùn\s*:",
    "Àmọ̀nà\s*:",
    "Àdáhùn\s*:",
    "Ànúgọ\s*:",
    "Àṣàyàn\s*:",
]


EQUALITY_TEMPLATE = r"""
Look at the following two expressions (answers to a math problem) and judge whether they are equivalent. Only perform trivial simplifications

Examples:

    Expression 1: $2x+3$
    Expression 2: $3+2x$

Yes

    Expression 1: 3/2
    Expression 2: 1.5

Yes

    Expression 1: $x^2+2x+1$
    Expression 2: $y^2+2y+1$

No

    Expression 1: $x^2+2x+1$
    Expression 2: $(x+1)^2$

Yes

    Expression 1: 3245/5
    Expression 2: 649

No
(these are actually equal, don't mark them equivalent if you need to do nontrivial simplifications)

    Expression 1: 2/(-3)
    Expression 2: -2/3

Yes
(trivial simplifications are allowed)

    Expression 1: 72 degrees
    Expression 2: 72

Yes
(give benefit of the doubt to units)

    Expression 1: 64
    Expression 2: 64 square feet

Yes
(give benefit of the doubt to units)

---

YOUR TASK


Respond with only "Yes" or "No" (without quotes). Do not include a rationale.

    Expression 1: %(expression1)s
    Expression 2: %(expression2)s
""".strip()


HTML_JINJA = """
<h3>Prompt conversation</h3>
{% for message in prompt_messages %}
{{ message_to_html(message) | safe }}
{% endfor %}
<h3>Sampled message</h3>
{{ message_to_html(next_message) | safe }}
<h3>Results</h3>
<p>Correct Answer: {{ correct_answer }}</p>
<p>Extracted Answer: {{ extracted_answer }}</p>
<p>Score: {{ score }}</p>
"""

PRESCRIPTION_HTML_JINJA = """
<h3>Prompt conversation</h3>
{% for message in prompt_messages %}
{{ message_to_html(message) | safe }}
{% endfor %}
<h3>Sampled message</h3>
{{ message_to_html(next_message) | safe }}

<h3>Results</h3>
<p>Correct Answer: {{ correct_answer }}</p>
<p>Extracted Answer: {{ extracted_answer }}</p>

<h3>中医诊疗全流程评测结果</h3>

<div style="background-color: #f5f5f5; padding: 15px; margin: 10px 0; border-radius: 5px;">
    <h4>综合评分</h4>
    <p><strong>总体F1分数:</strong> <span style="font-size: 1.2em; color: #0066cc;">{{ "%.3f"|format(overall_f1) }}</span></p>
    <p><strong>辨证F1:</strong> {{ "%.3f"|format(syndrome_f1) }} | <strong>治法F1:</strong> {{ "%.3f"|format(treatment_f1) }} | <strong>处方F1:</strong> {{ "%.3f"|format(herb_f1) }} | <strong>剂量MAE:</strong> {{ "%.3f"|format(dose_mae) }}克</p>
</div>

<div style="display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 20px; margin: 20px 0;">
    <div style="border: 1px solid #ddd; padding: 15px; border-radius: 5px;">
        <h4>辨证分析</h4>
        
        <div style="margin: 10px 0;">
            <h5 style="color: #228B22;">✓ 预测正确的辨证</h5>
            {% if correct_syndromes %}
                {% for syndrome in correct_syndromes %}
                    <span style="background-color: #d4edda; color: #155724; padding: 3px 8px; margin: 2px; border-radius: 3px; display: inline-block;">{{ syndrome }}</span>
                {% endfor %}
            {% else %}
                <span style="color: #666;">无</span>
            {% endif %}
        </div>
        
        <div style="margin: 10px 0;">
            <h5 style="color: #DC143C;">✗ 预测错误的辨证</h5>
            {% if wrong_syndromes %}
                {% for syndrome in wrong_syndromes %}
                    <span style="background-color: #f8d7da; color: #721c24; padding: 3px 8px; margin: 2px; border-radius: 3px; display: inline-block;">{{ syndrome }}</span>
                {% endfor %}
            {% else %}
                <span style="color: #666;">无</span>
            {% endif %}
        </div>
        
        <div style="margin: 10px 0;">
            <h5 style="color: #FF8C00;">⚠ 遗漏的辨证</h5>
            {% if missed_syndromes %}
                {% for syndrome in missed_syndromes %}
                    <span style="background-color: #fff3cd; color: #856404; padding: 3px 8px; margin: 2px; border-radius: 3px; display: inline-block;">{{ syndrome }}</span>
                {% endfor %}
            {% else %}
                <span style="color: #666;">无</span>
            {% endif %}
        </div>
        
        <div style="margin-top: 15px; padding: 10px; background-color: #f8f9fa; border-radius: 3px;">
            <p><strong>标准辨证:</strong> {{ gold_syndromes|join(", ") }}</p>
            <p><strong>预测辨证:</strong> {{ pred_syndromes|join(", ") if pred_syndromes else "无" }}</p>
        </div>
    </div>
    
    <div style="border: 1px solid #ddd; padding: 15px; border-radius: 5px;">
        <h4>治法分析</h4>
        
        <div style="margin: 10px 0;">
            <h5 style="color: #228B22;">✓ 预测正确的治法</h5>
            {% if correct_treatments %}
                {% for treatment in correct_treatments %}
                    <span style="background-color: #d4edda; color: #155724; padding: 3px 8px; margin: 2px; border-radius: 3px; display: inline-block;">{{ treatment }}</span>
                {% endfor %}
            {% else %}
                <span style="color: #666;">无</span>
            {% endif %}
        </div>
        
        <div style="margin: 10px 0;">
            <h5 style="color: #DC143C;">✗ 预测错误的治法</h5>
            {% if wrong_treatments %}
                {% for treatment in wrong_treatments %}
                    <span style="background-color: #f8d7da; color: #721c24; padding: 3px 8px; margin: 2px; border-radius: 3px; display: inline-block;">{{ treatment }}</span>
                {% endfor %}
            {% else %}
                <span style="color: #666;">无</span>
            {% endif %}
        </div>
        
        <div style="margin: 10px 0;">
            <h5 style="color: #FF8C00;">⚠ 遗漏的治法</h5>
            {% if missed_treatments %}
                {% for treatment in missed_treatments %}
                    <span style="background-color: #fff3cd; color: #856404; padding: 3px 8px; margin: 2px; border-radius: 3px; display: inline-block;">{{ treatment }}</span>
                {% endfor %}
            {% else %}
                <span style="color: #666;">无</span>
            {% endif %}
        </div>
        
        <div style="margin-top: 15px; padding: 10px; background-color: #f8f9fa; border-radius: 3px;">
            <p><strong>标准治法:</strong> {{ gold_treatments|join(", ") }}</p>
            <p><strong>预测治法:</strong> {{ pred_treatments|join(", ") if pred_treatments else "无" }}</p>
        </div>
    </div>
    
    <div style="border: 1px solid #ddd; padding: 15px; border-radius: 5px;">
        <h4>处方分析</h4>
        
        <div style="margin: 10px 0;">
            <h5 style="color: #228B22;">✓ 预测正确的中药</h5>
            {% if correct_herbs %}
                {% for herb_info in correct_herbs %}
                    <div style="background-color: #d4edda; color: #155724; padding: 5px 10px; margin: 3px 0; border-radius: 3px;">
                        <strong>{{ herb_info.herb }}</strong>
                        <span style="font-size: 0.9em;">
                            (预测: {{ herb_info.pred_dose }}克, 标准: {{ herb_info.gold_dose }}克, 
                            误差: {{ "%.1f"|format(herb_info.dose_error) }}克)
                        </span>
                    </div>
                {% endfor %}
            {% else %}
                <span style="color: #666;">无</span>
            {% endif %}
        </div>
        
        <div style="margin: 10px 0;">
            <h5 style="color: #DC143C;">✗ 预测错误的中药</h5>
            {% if wrong_herbs %}
                {% for herb in wrong_herbs %}
                    <span style="background-color: #f8d7da; color: #721c24; padding: 3px 8px; margin: 2px; border-radius: 3px; display: inline-block;">{{ herb }}</span>
                {% endfor %}
            {% else %}
                <span style="color: #666;">无</span>
            {% endif %}
        </div>
        
        <div style="margin: 10px 0;">
            <h5 style="color: #FF8C00;">⚠ 遗漏的中药</h5>
            {% if missed_herbs %}
                {% for herb in missed_herbs %}
                    <span style="background-color: #fff3cd; color: #856404; padding: 3px 8px; margin: 2px; border-radius: 3px; display: inline-block;">{{ herb }}</span>
                {% endfor %}
            {% else %}
                <span style="color: #666;">无</span>
            {% endif %}
        </div>
        
        <div style="margin-top: 15px; padding: 10px; background-color: #f8f9fa; border-radius: 3px;">
            <p><strong>标准处方:</strong></p>
            <div style="font-family: monospace; font-size: 0.9em; white-space: pre-wrap;">{{ gold_prescription_text }}</div>
            <p style="margin-top: 10px;"><strong>预测处方:</strong></p>
            <div style="font-family: monospace; font-size: 0.9em; white-space: pre-wrap;">{{ pred_prescription_text if pred_prescription_text else "无" }}</div>
        </div>
    </div>
</div>

<div style="background-color: #e9ecef; padding: 15px; margin: 10px 0; border-radius: 5px;">
    <h4>详细指标</h4>
    <div style="display: grid; grid-template-columns: repeat(4, 1fr); gap: 15px;">
        <div>
            <h5>辨证指标</h5>
            <p>Precision: {{ "%.3f"|format(syndrome_precision) }}</p>
            <p>Recall: {{ "%.3f"|format(syndrome_recall) }}</p>
            <p>F1: {{ "%.3f"|format(syndrome_f1) }}</p>
        </div>
        <div>
            <h5>治法指标</h5>
            <p>Precision: {{ "%.3f"|format(treatment_precision) }}</p>
            <p>Recall: {{ "%.3f"|format(treatment_recall) }}</p>
            <p>F1: {{ "%.3f"|format(treatment_f1) }}</p>
        </div>
        <div>
            <h5>处方指标</h5>
            <p>Precision: {{ "%.3f"|format(herb_precision) }}</p>
            <p>Recall: {{ "%.3f"|format(herb_recall) }}</p>
            <p>F1: {{ "%.3f"|format(herb_f1) }}</p>
        </div>
        <div>
            <h5>剂量指标</h5>
            <p>平均绝对误差: {{ "%.3f"|format(dose_mae) }}克</p>
            <p>匹配药物数: {{ matched_herb_count }}</p>
        </div>
        <div>
            <h5>综合评分</h5>
            <p>Score: {{ "%.3f"|format(score) }}</p>
        </div>
    </div>
</div>
"""


def format_multichoice_question(row):
    return QUERY_TEMPLATE_MULTICHOICE.format(**row)


def check_equality(sampler: SamplerBase, expr1: str, expr2: str):
    prompt = EQUALITY_TEMPLATE % {"expression1": expr1, "expression2": expr2}
    sampler_response = sampler([dict(content=prompt, role="user")])
    response_text = sampler_response.response_text
    return response_text.lower().strip() == "yes"


def _compute_stat(values: list, stat: str):
    if stat == "mean":
        return np.mean(values)
    elif stat == "std":
        return np.std(values)
    elif stat == "min":
        return np.min(values)
    elif stat == "max":
        return np.max(values)
    elif stat == "n_samples":
        return len(values)
    elif stat == "bootstrap_std":
        return np.std(
            [np.mean(np.random.choice(values, len(values))) for _ in range(1000)]
        )
    else:
        raise ValueError(f"Unknown {stat =}")


def aggregate_results(
    single_eval_results: list[SingleEvalResult],
    default_stats: tuple[str, ...] = ("mean", "std"),
    name2stats: dict[str, tuple[str]] | None = None,
) -> EvalResult:
    """
    Aggregate results from multiple evaluations into a single EvalResult.
    """
    name2stats = name2stats or {}
    name2values = defaultdict(list)
    htmls = []
    convos = []
    metadata = []
    for single_eval_result in single_eval_results:
        try:
            for name, value in single_eval_result.metrics.items():
                name2values[name].append(value)
        except:
            print()
        if single_eval_result.score is not None:
            name2values["score"].append(single_eval_result.score)
        htmls.append(single_eval_result.html)
        convos.append(single_eval_result.convo)
        metadata.append(single_eval_result.example_level_metadata)
    final_metrics = {}
    for name, values in name2values.items():
        stats = name2stats.get(name, default_stats)
        for stat in stats:
            key = name if stat == "mean" else f"{name}:{stat}"
            final_metrics[key] = _compute_stat(values, stat)
    return EvalResult(
        score=final_metrics.pop("score", None),
        metrics=final_metrics,
        htmls=htmls,
        convos=convos,
        metadata={"example_level_metadata": metadata},
    )


def map_with_progress(
    f: Callable,
    xs: list[Any],
    num_threads: int = os.cpu_count() or 10,
    pbar: bool = True,
):
    """
    Apply f to each element of xs, using a ThreadPool, and show progress.
    Results are returned in the same order as input.
    """
    pbar_fn = tqdm if pbar else lambda x, *args, **kwargs: x

    if os.getenv("debug"):
        return list(map(f, pbar_fn(xs, total=len(xs))))
    else:
        # 使用 ThreadPoolExecutor 和 as_completed 来保证顺序
        with ThreadPoolExecutor(max_workers=min(num_threads, len(xs))) as executor:
            # 提交所有任务，保持索引
            future_to_index = {executor.submit(f, x): i for i, x in enumerate(xs)}

            # 创建结果列表，初始化为 None
            results = [None] * len(xs)

            # 使用 tqdm 显示进度，按完成顺序处理结果
            for future in pbar_fn(as_completed(future_to_index), total=len(xs), dynamic_ncols=True):
                index = future_to_index[future]
                if future.result():
                    results[index] = future.result()

            return results


jinja_env = jinja2.Environment(
    loader=jinja2.BaseLoader(),
    undefined=jinja2.StrictUndefined,
    autoescape=jinja2.select_autoescape(["html", "xml"]),
)
_message_template = """
<div class="message {{ role }}">
    <div class="role">
    {{ role }}
    {% if variant %}<span class="variant">({{ variant }})</span>{% endif %}
    </div>
    <div class="content">
    <pre>{{ content }}</pre>
    </div>
</div>
"""


def message_to_html(message: Message) -> str:
    """
    Generate HTML snippet (inside a <div>) for a message.
    """
    return jinja_env.from_string(_message_template).render(
        role=message["role"],
        content=message["content"],
        variant=message.get("variant", None),
    )


jinja_env.globals["message_to_html"] = message_to_html


_report_template = """<!DOCTYPE html>
<html>
    <head>
        <style>
            .message {
                padding: 8px 16px;
                margin-bottom: 8px;
                border-radius: 4px;
            }
            .message.user {
                background-color: #B2DFDB;
                color: #00695C;
            }
            .message.assistant {
                background-color: #B39DDB;
                color: #4527A0;
            }
            .message.system {
                background-color: #EEEEEE;
                color: #212121;
            }
            .role {
                font-weight: bold;
                margin-bottom: 4px;
            }
            .variant {
                color: #795548;
            }
            table, th, td {
                border: 1px solid black;
            }
            pre {
                white-space: pre-wrap;
            }
        </style>
    </head>
    <body>
    {% if metrics %}
    <h1>Metrics</h1>
    <table>
    <tr>
        <th>Metric</th>
        <th>Value</th>
    </tr>
    <tr>
        <td><b>Score</b></td>
        <td>{{ score | float | round(3) }}</td>
    </tr>
    {% for name, value in metrics.items() %}
    <tr>
        <td>{{ name }}</td>
        <td>{{ value }}</td>
    </tr>
    {% endfor %}
    </table>
    {% endif %}
    <h1>Examples</h1>
    {% for html in htmls %}
    {{ html | safe }}
    <hr>
    {% endfor %}
    </body>
</html>
"""


def make_report(eval_result: EvalResult) -> str:
    """
    Create a standalone HTML report from an EvalResult.
    """
    return jinja_env.from_string(_report_template).render(
        score=eval_result.score,
        metrics=eval_result.metrics,
        htmls=eval_result.htmls,
    )


def make_report_from_example_htmls(htmls: list[str]):
    """
    Create a standalone HTML report from a list of example htmls
    """
    return jinja_env.from_string(_report_template).render(
        score=None, metrics={}, htmls=htmls
    )


def normalize_response(response: str) -> str:
    """
    Normalize the response by removing markdown and LaTeX formatting that may prevent a match.
    """

    return (
        response.replace("**", "")
        .replace("$\\boxed{", "")
        .replace("}$", "")
        .replace("\\$", "")
        .replace("$\\text{", "")
        .replace("$", "")
        .replace("\\mathrm{", "")
        .replace("\\{", "")
        .replace("\\text", "")
        .replace("\\(", "")
        .replace("\\mathbf{", "")
        .replace("{", "")
        .replace("\\boxed", "")
    )


def normalize_extracted_answer(extracted_answer: str) -> str:
    return (
        # In arabic these are the letters used for A-D in multiple choice questions
        extracted_answer.replace("أ", " A")
        .replace("ب", " B")
        .replace("ج", " C")
        .replace("د", " D")
        # In Bengali these are the letters used for A-D in multiple choice questions
        .replace("অ", " A")
        .replace("ব", " B")
        .replace("ড", " C")
        .replace("ঢ", " D")
        # In Japanese these are the letters sometimes used for A-D in multiple choice questions
        .replace("Ａ", " A")
        .replace("Ｂ", " B")
        .replace("Ｃ", " C")
        .replace("Ｄ", " D")
        .strip()
    )


def url_to_fileobj(url: str, binary=False) -> Any:
    response = requests.get(url)
    response.raise_for_status()
    return io.BytesIO(response.content) if binary else io.StringIO(response.text)


def has_only_user_assistant_messages(messages: list[Message]) -> bool:
    """
    Check if the messages only contain user and assistant messages.
    """
    return all(m["role"] in ("user", "assistant") for m in messages)

try:
    import html

    def html_unescape(text):
        return html.unescape(text) if text else text

except ImportError:
    # 兼容旧版本Python
    try:
        from html.parser import HTMLParser

        html_parser = HTMLParser()

        def html_unescape(text):
            return html_parser.unescape(text) if text else text

    except ImportError:
        # 如果都不可用，则不进行解码
        def html_unescape(text):
            return text

import re
def extract_sample_details(result, eval_name, model_name):
    """从EvalResult中提取每个样本的详细信息"""
    sample_results = []

    if not result.htmls or not result.convos:
        return sample_results

    for i, (html, convo) in enumerate(zip(result.htmls, result.convos)):
        try:
            # 从对话中提取问题和回答
            question = ""
            model_response = ""

            for message in convo:
                if message.get("role") == "user":
                    question = message.get("content", "")
                    question = html_unescape(question)  # 解码HTML实体
                elif message.get("role") == "assistant":
                    model_response = message.get("content", "")
                    model_response = html_unescape(model_response)  # 解码HTML实体

            # 从HTML中提取评分信息 - 根据实际HTML格式
            score_match = re.search(r"<p>Score:\s*([\d.]+)</p>", html)
            score = float(score_match.group(1)) if score_match else 0.0

            # 提取正确答案和预测答案 - 根据实际HTML格式
            correct_answer_match = re.search(r"<p>Correct Answer:\s*([^<]+)</p>", html)
            correct_answer = correct_answer_match.group(1).strip() if correct_answer_match else ""
            correct_answer = html_unescape(correct_answer)  # 解码HTML实体

            extracted_answer_match = re.search(r"<p>Extracted Answer:\s*([^<]+)</p>", html)
            extracted_answer = extracted_answer_match.group(1).strip() if extracted_answer_match else ""
            extracted_answer = html_unescape(extracted_answer)  # 解码HTML实体

            # 尝试提取其他评估指标（如precision, recall, f1等）
            additional_metrics = {}

            # 从HTML中提取其他可能的指标
            for metric_name in ["precision", "recall", "f1", "accuracy"]:
                metric_pattern = rf"<p>{metric_name.title()}:\s*([\d.]+)</p>"
                metric_match = re.search(metric_pattern, html, re.IGNORECASE)
                if metric_match:
                    additional_metrics[metric_name] = float(metric_match.group(1))

            sample_result = {
                "eval_name": eval_name,
                "model_name": model_name,
                "sample_id": i + 1,
                "question": question,
                "correct_answer": correct_answer,
                "extracted_answer": extracted_answer,
                "model_response": model_response,
                "score": score,
                **additional_metrics,  # 展开其他指标
            }

            sample_results.append(sample_result)

        except Exception as e:
            print(f"解析样本 {i} 时出错: {e}")
            continue

    return sample_results
