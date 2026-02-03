import json
import random
import re
from collections import defaultdict
from typing import Dict, List, Set, Tuple

import numpy as np

from ... import common
from ...common import PRESCRIPTION_HTML_JINJA
from ...types import Eval, EvalResult, SamplerBase, SingleEvalResult

# 中医诊疗全流程提示模板
MEDICAL_DIAGNOSIS_TEMPLATE = """
请根据以下病历文本，进行完整的中医诊疗分析，包括辨证、治法和处方。

注意：
1. 请仔细分析患者的症状表现、舌脉象等信息
2. 辨证：给出准确的中医证型判断（如有多个，用逗号分隔）
3. 治法：根据辨证结果确定相应的治疗方法（如有多个，用逗号分隔）
4. 处方：开具具体的中药处方，格式为"药名: 剂量, 药名: 剂量"

病历文本：
{medical_record}

请按照以下JSON格式输出结果：

```json
{{
  "辨证": "证型1, 证型2, ...",
  "治法": "治法1, 治法2, ...",
  "处方": "药名1: 剂量1, 药名2: 剂量2, 药名3: 剂量3, ..."
}}
```
""".strip()

def parse_prescription(prescription_str: str) -> Dict[str, float]:
    """解析处方字符串，返回药名->剂量的字典
    严格按照数据集格式：药名: 剂量g, 药名: 剂量g, ...
    """
    herb_doses = {}
    if not prescription_str:
        return herb_doses

    # 按逗号分割
    prescription_str = prescription_str.replace("，", ",")
    herb_items = prescription_str.split(',')

    for item in herb_items:
        item = item.strip()
        if not item:
            continue

        # 严格匹配格式：药名: 剂量g
        match = re.search(r"(.+?):\s*([0-9.]+)\s*(g|克)?\s*$", item)
        if match:
            herb_name = match.group(1).strip()
            try:
                dose = float(match.group(2))
                herb_doses[herb_name] = dose
            except ValueError:
                continue

    return herb_doses

def extract_response_from_json(response_text: str) -> Tuple[List[str], List[str], Dict[str, float]]:
    """从模型回答中提取辨证、治法和处方"""
    if "</think>" in response_text:
        response_text = response_text.split("</think>")[1].strip()
    syndromes = []
    treatments = []
    prescription = {}

    try:
        # 提取JSON格式
        if "```json" in response_text:
            json_cleaned = response_text.split("```json")[1].split("```")[0]
        else:
            json_cleaned = re.findall(r"({[\s\S]*?})", response_text)
            json_cleaned = json_cleaned[0] if json_cleaned else response_text

        result = json.loads(json_cleaned)
        syndrome_str = result.get("辨证", "")
        treatment_str = result.get("治法", "")
        prescription_str = result.get("处方", "")

        # 解析辨证（可能有多个，用逗号分隔）
        if syndrome_str:
            syndrome_str = syndrome_str.replace("，", ",")
            syndromes = [s.strip() for s in syndrome_str.split(",") if s.strip()]

        # 解析治法（可能有多个，用逗号分隔）
        if treatment_str:
            treatment_str = treatment_str.replace("，", ",")
            treatments = [t.strip() for t in treatment_str.split(",") if t.strip()]

        prescription = parse_prescription(prescription_str)
        return syndromes, treatments, prescription
    except:
        pass

    # 如果没有找到JSON格式，尝试解析其他格式
    # 先尝试提取包含"注：此为基于病历信息的中医诊疗分析。"的JSON格式
    json_pattern = r'\{\s*"辨证":\s*"([^"]*)",\s*"治法":\s*"([^"]*)",\s*"处方":\s*"([^"]*)"\s*\}'
    json_match = re.search(json_pattern, response_text)
    if json_match:
        syndrome_str = json_match.group(1).strip()
        treatment_str = json_match.group(2).strip()
        prescription_str = json_match.group(3).strip()

        if syndrome_str:
            syndrome_str = syndrome_str.replace("，", ",")
            syndromes = [s.strip() for s in syndrome_str.split(",") if s.strip()]
        if treatment_str:
            treatment_str = treatment_str.replace("，", ",")
            treatments = [t.strip() for t in treatment_str.split(",") if t.strip()]
        prescription = parse_prescription(prescription_str)
        return syndromes, treatments, prescription

    # 查找辨证
    syndrome_patterns = [
        r"辨证[：:]\s*([^\n]*)",
        r"证型[：:]\s*([^\n]*)",
        r"中医证型[：:]\s*([^\n]*)"
    ]

    for pattern in syndrome_patterns:
        match = re.search(pattern, response_text)
        if match:
            syndrome_str = match.group(1).strip()
            if syndrome_str:
                syndrome_str = syndrome_str.replace("，", ",")
                syndromes = [s.strip() for s in syndrome_str.split(",") if s.strip()]
            break

    # 查找治法
    treatment_patterns = [
        r"治法[：:]\s*([^\n]*)",
        r"治疗方法[：:]\s*([^\n]*)",
        r"治疗原则[：:]\s*([^\n]*)"
    ]

    for pattern in treatment_patterns:
        match = re.search(pattern, response_text)
        if match:
            treatment_str = match.group(1).strip()
            if treatment_str:
                treatment_str = treatment_str.replace("，", ",")
                treatments = [t.strip() for t in treatment_str.split(",") if t.strip()]
            break

    # 查找处方
    prescription_patterns = [
        r"处方[：:]\s*([^\n]*)",
        r"中药处方[：:]\s*([^\n]*)",
        r"方药[：:]\s*([^\n]*)"
    ]

    for pattern in prescription_patterns:
        match = re.search(pattern, response_text)
        if match:
            prescription_str = match.group(1).strip()
            prescription = parse_prescription(prescription_str)
            break

    return syndromes, treatments, prescription

def analyze_syndrome_matches(pred_syndromes: List[str], gold_syndromes: List[str]) -> Tuple[List[str], List[str], List[str]]:
    """分析辨证匹配情况，返回(正确的，错误的，遗漏的)"""
    pred_set = set(pred_syndromes)
    gold_set = set(gold_syndromes)
    
    correct = []
    wrong = []
    missed = []
    
    # 找到正确预测的辨证
    for pred_syndrome in pred_set:
        matched = False
        for gold_syndrome in gold_set:
            if pred_syndrome in gold_syndrome or gold_syndrome in pred_syndrome:
                correct.append(pred_syndrome)
                matched = True
                break
        if not matched:
            wrong.append(pred_syndrome)
    
    # 找到遗漏的辨证
    for gold_syndrome in gold_set:
        matched = False
        for pred_syndrome in pred_set:
            if pred_syndrome in gold_syndrome or gold_syndrome in pred_syndrome:
                matched = True
                break
        if not matched:
            missed.append(gold_syndrome)
    
    return correct, wrong, missed

def analyze_treatment_matches(pred_treatments: List[str], gold_treatments: List[str]) -> Tuple[List[str], List[str], List[str]]:
    """分析治法匹配情况，返回(正确的，错误的，遗漏的)"""
    pred_set = set(pred_treatments)
    gold_set = set(gold_treatments)
    
    correct = []
    wrong = []
    missed = []
    
    # 找到正确预测的治法
    for pred_treatment in pred_set:
        matched = False
        for gold_treatment in gold_set:
            if pred_treatment in gold_treatment or gold_treatment in pred_treatment:
                correct.append(pred_treatment)
                matched = True
                break
        if not matched:
            wrong.append(pred_treatment)
    
    # 找到遗漏的治法
    for gold_treatment in gold_set:
        matched = False
        for pred_treatment in pred_set:
            if pred_treatment in gold_treatment or gold_treatment in pred_treatment:
                matched = True
                break
        if not matched:
            missed.append(gold_treatment)
    
    return correct, wrong, missed

def calculate_set_metrics_with_inclusion(pred_set: Set, gold_set: Set) -> Tuple[float, float, float]:
    """计算集合的precision, recall, f1，支持包含关系匹配"""
    if len(pred_set) == 0 and len(gold_set) == 0:
        return 1.0, 1.0, 1.0
    
    if len(pred_set) == 0:
        return 0.0, 0.0, 0.0
    
    if len(gold_set) == 0:
        return 0.0, 0.0, 0.0
    
    # 计算基于包含关系的匹配
    pred_matched = 0
    gold_matched = 0
    
    # 对于每个预测项，检查是否与任何标准答案项有包含关系
    for pred_item in pred_set:
        for gold_item in gold_set:
            # 两者中的一个包含另一个即算匹配
            if pred_item in gold_item or gold_item in pred_item:
                pred_matched += 1
                break
    
    # 对于每个标准答案项，检查是否与任何预测项有包含关系
    for gold_item in gold_set:
        for pred_item in pred_set:
            # 两者中的一个包含另一个即算匹配
            if pred_item in gold_item or gold_item in pred_item:
                gold_matched += 1
                break
        
    # 计算匹配数量
    # matched_items = pred_set & gold_set
    # pred_matched = len(matched_items)
    # gold_matched = len(matched_items)
    
    precision = pred_matched / len(pred_set)
    recall = gold_matched / len(gold_set)
    
    if precision + recall == 0:
        f1 = 0.0
    else:
        f1 = 2 * precision * recall / (precision + recall)
    
    return precision, recall, f1

def calculate_dose_mae_with_inclusion(pred_prescription: Dict[str, float], 
                                    gold_prescription: Dict[str, float]) -> float:
    """计算剂量的平均绝对误差，支持包含关系匹配"""
    matched_pairs = []
    
    # 找到所有匹配的药物对（基于包含关系）
    for pred_herb, pred_dose in pred_prescription.items():
        for gold_herb, gold_dose in gold_prescription.items():
            # 两者中的一个包含另一个即算匹配
            if pred_herb in gold_herb or gold_herb in pred_herb:
                matched_pairs.append((pred_dose, gold_dose))
                break  # 每个预测药物只匹配一次
    
    if len(matched_pairs) == 0:
        return 0.0  # 没有匹配的药物时，MAE为0
    
    total_error = 0.0
    for pred_dose, gold_dose in matched_pairs:
        total_error += abs(pred_dose - gold_dose)
    
    return total_error / len(matched_pairs)


def calculate_dose_cosine_with_inclusion(
    pred_prescription: Dict[str, float],
    gold_prescription: Dict[str, float]
) -> float:
    """
    计算基于包含关系匹配的处方剂量余弦相似度（Cosine Similarity）。
    匹配规则：只要药名存在包含关系（pred_herb in gold_herb 或 gold_herb in pred_herb）即视为同一味药。
    未匹配的药物剂量视为 0。
    返回值范围 [0, 1]，越高越相似。
    """
    matched_gold_herbs = set()
    matched_pred_herbs = set()
    pred_aligned = []
    gold_aligned = []

    # 一对一匹配：每个预测药物匹配一次
    for pred_herb, pred_dose in pred_prescription.items():
        matched = None
        for gold_herb, gold_dose in gold_prescription.items():
            if gold_herb in matched_gold_herbs:
                continue
            if pred_herb in gold_herb or gold_herb in pred_herb:
                matched = gold_herb
                pred_aligned.append(pred_dose)
                gold_aligned.append(gold_dose)
                matched_gold_herbs.add(gold_herb)
                matched_pred_herbs.add(pred_herb)
                break
    
    # 未匹配部分补0（多药、漏药）
    for gold_herb, gold_dose in gold_prescription.items():
        if gold_herb not in matched_gold_herbs:
            pred_aligned.append(0.0)
            gold_aligned.append(gold_dose)
    for pred_herb, pred_dose in pred_prescription.items():
        if pred_herb not in matched_pred_herbs:
            pred_aligned.append(pred_dose)
            gold_aligned.append(0.0)

    # 转向量计算余弦相似度
    a = np.array(pred_aligned, dtype=float)
    b = np.array(gold_aligned, dtype=float)
    na = np.linalg.norm(a)
    nb = np.linalg.norm(b)
    if na == 0 and nb == 0:
        return 1.0
    if na == 0 or nb == 0:
        return 0.0
    return float(a.dot(b) / (na * nb))


def analyze_herb_matches(pred_prescription: Dict[str, float], gold_prescription: Dict[str, float]) -> Tuple[List[Dict], List[str], List[str]]:
    """分析中药匹配情况，返回(正确的，错误的，遗漏的)"""
    correct = []
    wrong = []
    missed = []
    
    # 找到正确预测的中药
    for pred_herb, pred_dose in pred_prescription.items():
        matched = False
        for gold_herb, gold_dose in gold_prescription.items():
            if pred_herb in gold_herb or gold_herb in pred_herb:
                correct.append({
                    'herb': pred_herb,
                    'pred_dose': pred_dose,
                    'gold_dose': gold_dose,
                    'dose_error': abs(pred_dose - gold_dose)
                })
                matched = True
                break
        if not matched:
            wrong.append(pred_herb)
    
    # 找到遗漏的中药
    for gold_herb, gold_dose in gold_prescription.items():
        matched = False
        for pred_herb, pred_dose in pred_prescription.items():
            if pred_herb in gold_herb or gold_herb in pred_herb:
                matched = True
                break
        if not matched:
            missed.append(gold_herb)
    
    return correct, wrong, missed

def format_prescription_text(prescription: Dict[str, float]) -> str:
    """格式化处方文本"""
    if not prescription:
        return ""
    return "; ".join([f"{herb}: {dose}克" for herb, dose in prescription.items()])

class PresDigEval(Eval):
    """中医诊疗全流程评测类"""

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
        print(f"加载了 {len(examples)} 条中医诊疗样本")

    def __call__(self, sampler: SamplerBase) -> EvalResult:
        def fn(row: dict):
            prompt_messages = [sampler._pack_message(content=MEDICAL_DIAGNOSIS_TEMPLATE.format(medical_record=row["病历文本"]), role="user")]
            sampler_response = sampler(prompt_messages)
            response_text = sampler_response.response_text
            actual_queried_prompt_messages = sampler_response.actual_queried_message_list

            # 提取模型预测的辨证、治法和处方
            pred_syndromes, pred_treatments, pred_prescription = extract_response_from_json(response_text)

            # 标准答案
            gold_syndromes = [s.strip() for s in row["辨证"].split(",") if s.strip()]
            gold_treatments = [t.strip() for t in row["治法"].split(",") if t.strip()]
            gold_prescription = parse_prescription(row["处方"])

            # 计算辨证指标（支持包含关系）
            pred_syndrome_set = set(pred_syndromes)
            gold_syndrome_set = set(gold_syndromes)
            syndrome_precision, syndrome_recall, syndrome_f1 = calculate_set_metrics_with_inclusion(
                pred_syndrome_set, gold_syndrome_set
            )
            
            # 计算治法指标（支持包含关系）
            pred_treatment_set = set(pred_treatments)
            gold_treatment_set = set(gold_treatments)
            treatment_precision, treatment_recall, treatment_f1 = calculate_set_metrics_with_inclusion(
                pred_treatment_set, gold_treatment_set
            )

            # 计算中药名称指标（支持包含关系）
            pred_herb_set = set(pred_prescription.keys())
            gold_herb_set = set(gold_prescription.keys())
            herb_precision, herb_recall, herb_f1 = calculate_set_metrics_with_inclusion(
                pred_herb_set, gold_herb_set
            )

            # 计算剂量MAE（支持包含关系）
            dose_mae = calculate_dose_mae_with_inclusion(pred_prescription, gold_prescription)
            
            # 计算剂量余弦相似度（支持包含关系）
            dose_cosine = calculate_dose_cosine_with_inclusion(pred_prescription, gold_prescription)

            # 综合F1分数（辨证、治法、处方的平均）
            overall_f1 = (syndrome_f1 + treatment_f1 + herb_f1) / 3

            # 分析处方匹配情况
            correct_herbs, wrong_herbs, missed_herbs = analyze_herb_matches(pred_prescription, gold_prescription)
            
            # 格式化处方文本
            gold_prescription_text = format_prescription_text(gold_prescription)
            pred_prescription_text = format_prescription_text(pred_prescription)
            
            # 计算匹配的中药数量
            matched_herb_count = len(correct_herbs)

            # 分析辨证和治法匹配情况
            correct_syndromes, wrong_syndromes, missed_syndromes = analyze_syndrome_matches(pred_syndromes, gold_syndromes)
            correct_treatments, wrong_treatments, missed_treatments = analyze_treatment_matches(pred_treatments, gold_treatments)

            # 生成专属的中医诊疗HTML报告
            html = common.jinja_env.from_string(PRESCRIPTION_HTML_JINJA).render(
                prompt_messages=actual_queried_prompt_messages,
                next_message=dict(content=response_text, role="assistant"),
                score=overall_f1,
                overall_f1=overall_f1,
                syndrome_precision=syndrome_precision,
                syndrome_recall=syndrome_recall,
                syndrome_f1=syndrome_f1,
                treatment_precision=treatment_precision,
                treatment_recall=treatment_recall,
                treatment_f1=treatment_f1,
                herb_precision=herb_precision,
                herb_recall=herb_recall,
                herb_f1=herb_f1,
                dose_mae=dose_mae,
                dose_cosine=dose_cosine,
                pred_syndromes=pred_syndromes,
                gold_syndromes=gold_syndromes,
                pred_treatments=pred_treatments,
                gold_treatments=gold_treatments,
                correct_syndromes=correct_syndromes,
                wrong_syndromes=wrong_syndromes,
                missed_syndromes=missed_syndromes,
                correct_treatments=correct_treatments,
                wrong_treatments=wrong_treatments,
                missed_treatments=missed_treatments,
                correct_herbs=correct_herbs,
                wrong_herbs=wrong_herbs,
                missed_herbs=missed_herbs,
                gold_prescription_text=gold_prescription_text,
                pred_prescription_text=pred_prescription_text,
                matched_herb_count=matched_herb_count,
                # 添加correct_answer和extracted_answer用于Excel导出
                correct_answer=f"辨证: {', '.join(gold_syndromes)}; 治法: {', '.join(gold_treatments)}; 处方: {gold_prescription_text}",
                extracted_answer=f"辨证: {', '.join(pred_syndromes) if pred_syndromes else '无'}; 治法: {', '.join(pred_treatments) if pred_treatments else '无'}; 处方: {pred_prescription_text if pred_prescription_text else '无'}",
            )

            convo = actual_queried_prompt_messages + [dict(content=response_text, role="assistant")]

            return SingleEvalResult(
                html=html, 
                score=overall_f1,
                metrics={
                    "syndrome_precision": syndrome_precision,
                    "syndrome_recall": syndrome_recall,
                    "syndrome_f1": syndrome_f1,
                    "treatment_precision": treatment_precision,
                    "treatment_recall": treatment_recall,
                    "treatment_f1": treatment_f1,
                    "herb_precision": herb_precision,
                    "herb_recall": herb_recall,
                    "herb_f1": herb_f1,
                    "dose_mae": dose_mae,
                    "dose_cosine": dose_cosine,
                    "overall_f1": overall_f1
                }, 
                convo=convo
            )

        results = common.map_with_progress(fn, self.examples, num_threads=self.num_threads)
        return common.aggregate_results(results)
