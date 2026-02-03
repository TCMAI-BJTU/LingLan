import json
import random
import re
from collections import Counter
from typing import Dict, List, Optional, Set, Tuple

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


def _char_counts(s: str) -> Counter:
    """统计字符串中每个字符的出现次数"""
    return Counter(list(s or ""))


def char_f1(a: str, b: str) -> float:
    """
    计算两个字符串的字符级F1分数
    基于字符的交集计算precision和recall
    """
    
    if a in b or b in a:
        return 0.99
    
    a = (a or "").strip()
    b = (b or "").strip()
    if not a or not b:
        return 0.0
    
    a = a.rstrip("证")
    b = b.rstrip("证")
    
    ca, cb = _char_counts(a), _char_counts(b)
    # 计算交集：两个Counter的交集
    inter = sum((ca & cb).values())
    
    # Precision = 交集 / 预测集
    p = inter / max(1, sum(ca.values()))
    # Recall = 交集 / 真实集
    r = inter / max(1, sum(cb.values()))
    
    if p + r == 0:
        return 0.0
    
    # F1 = 2PR / (P+R)
    return 2 * p * r / (p + r)


def normalize_herb_name(name: str) -> str:
    """标准化中药名称，去除空格和标点符号"""
    name = (name or "").strip()
    # 保留中文字符、英文字母和数字
    name = re.sub(r"[^0-9A-Za-z\u4e00-\u9fff]", "", name)
    # 移除可能粘在名称上的单位
    name = re.sub(r"(?:[Gg克]|毫克|mg|KG|kg)$", "", name)
    return name


def parse_prescription(prescription_str: str) -> Dict[str, float]:
    """解析处方字符串，返回药名->剂量的字典"""
    herb_doses = {}
    if not prescription_str:
        return herb_doses
    
    # 支持多种分隔符
    s = prescription_str.replace("，", ",").replace("；", ",").replace("、", ",")
    herb_items = s.split(',')
    
    for item in herb_items:
        item = item.strip()
        if not item:
            continue
        
        # 尝试按冒号分割
        if "：" in item:
            name, dose_str = item.split("：", 1)
        elif ":" in item:
            name, dose_str = item.split(":", 1)
        else:
            # 尝试在第一个数字处分割
            m = re.search(r"[-+]?\d*\.?\d+", item)
            if m:
                name = item[:m.start()]
                dose_str = item[m.start():]
            else:
                name, dose_str = item, ""
        
        name = normalize_herb_name(name)
        dose = None
        
        # 提取剂量数字
        m = re.search(r"([-+]?\d*\.?\d+)", dose_str)
        if m:
            try:
                dose = min(float(m.group(1)), 1000)
            except ValueError:
                dose = None
        
        if name:
            herb_doses[name] = dose
    
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
            prescription_str = prescription_str.replace("，", ",")
            prescription = parse_prescription(prescription_str)
            break

    return syndromes, treatments, prescription


def match_items_with_char_f1(pred_items: List[str], 
                             gold_items: List[str], 
                             threshold: float = 0.8) -> Tuple[List[Tuple[str, str, float]], List[str], List[str]]:
    """
    使用字符级F1匹配元素列表
    返回：(匹配对列表[(pred, gold, f1_score)], 未匹配的预测, 未匹配的真实)
    """
    matched_pairs = []
    used_pred = set()
    used_gold = set()
    
    # 对每个预测项，找到F1最高且超过阈值的真实项
    for i, pred_item in enumerate(pred_items):
        if i in used_pred:
            continue
        
        best_match_j = -1
        best_f1 = 0.0
        
        for j, gold_item in enumerate(gold_items):
            if j in used_gold:
                continue
            
            f1_score = char_f1(pred_item, gold_item)
            if f1_score > threshold and f1_score > best_f1:
                best_f1 = f1_score
                best_match_j = j
        
        if best_match_j >= 0:
            used_pred.add(i)
            used_gold.add(best_match_j)
            matched_pairs.append((pred_item, gold_items[best_match_j], best_f1))
    
    # 统计未匹配的项
    unmatched_pred = [pred_items[i] for i in range(len(pred_items)) if i not in used_pred]
    unmatched_gold = [gold_items[j] for j in range(len(gold_items)) if j not in used_gold]
    
    return matched_pairs, unmatched_pred, unmatched_gold


def match_herbs_with_char_f1(pred_prescription: Dict[str, float], 
                             gold_prescription: Dict[str, float], 
                             threshold: float = 0.8) -> Tuple[List[Dict], List[str], List[str]]:
    """
    使用字符级F1匹配中药处方
    返回：(匹配对列表, 未匹配的预测药物, 未匹配的真实药物)
    """
    pred_herbs = list(pred_prescription.keys())
    gold_herbs = list(gold_prescription.keys())
    
    matched_pairs = []
    used_pred = set()
    used_gold = set()
    
    # 对每个预测药物，找到F1最高且超过阈值的真实药物
    for i, pred_herb in enumerate(pred_herbs):
        if i in used_pred:
            continue
        
        best_match_j = -1
        best_f1 = 0.0
        
        for j, gold_herb in enumerate(gold_herbs):
            if j in used_gold:
                continue
        
            f1_score = char_f1(pred_herb, gold_herb)
            if f1_score > threshold and f1_score > best_f1:
                best_f1 = f1_score
                best_match_j = j
        
        if best_match_j >= 0:
            gold_herb = gold_herbs[best_match_j]
            pred_dose = pred_prescription[pred_herb]
            gold_dose = gold_prescription[gold_herb]
            
            matched_pairs.append({
                'pred_herb': pred_herb,
                'gold_herb': gold_herb,
                'f1_score': best_f1,
                'pred_dose': pred_dose,
                'gold_dose': gold_dose,
                'dose_error': abs(pred_dose - gold_dose) if pred_dose and gold_dose else None
            })
            
            used_pred.add(i)
            used_gold.add(best_match_j)
    
    # 统计未匹配的药物
    unmatched_pred = [pred_herbs[i] for i in range(len(pred_herbs)) if i not in used_pred]
    unmatched_gold = [gold_herbs[j] for j in range(len(gold_herbs)) if j not in used_gold]
    
    return matched_pairs, unmatched_pred, unmatched_gold


def calculate_metrics(matched_count: int, pred_count: int, gold_count: int) -> Tuple[float, float, float]:
    """计算Precision, Recall, F1"""
    if pred_count == 0 and gold_count == 0:
        return 1.0, 1.0, 1.0
    
    if pred_count == 0:
        return 0.0, 0.0, 0.0
    
    if gold_count == 0:
        return 0.0, 0.0, 0.0
    
    precision = matched_count / pred_count
    recall = matched_count / gold_count
    
    if precision + recall == 0:
        f1 = 0.0
    else:
        f1 = 2 * precision * recall / (precision + recall)
    
    return precision, recall, f1


def calculate_dose_mae(matched_herbs: List[Dict]) -> float:
    """计算剂量的平均绝对误差"""
    valid_pairs = [h for h in matched_herbs if h['dose_error'] is not None]
    
    if len(valid_pairs) == 0:
        return 0.0
    
    total_error = sum(h['dose_error'] for h in valid_pairs)
    return total_error / len(valid_pairs)


def calculate_dose_cosine_with_char_f1(
    pred_prescription: Dict[str, float],
    gold_prescription: Dict[str, float],
    threshold: float = 0.8
) -> float:
    """
    计算基于字符F1匹配的处方剂量余弦相似度（Cosine Similarity）。
    匹配规则：使用字符级F1进行匹配，F1>threshold即视为同一味药。
    未匹配的药物剂量视为 0。
    返回值范围 [0, 1]，越高越相似。
    """
    pred_herbs = list(pred_prescription.keys())
    gold_herbs = list(gold_prescription.keys())
    
    matched_gold_herbs = set()
    matched_pred_herbs = set()
    pred_aligned = []
    gold_aligned = []

    # 一对一匹配：每个预测药物匹配一次
    for i, pred_herb in enumerate(pred_herbs):
        if i in matched_pred_herbs:
            continue
            
        best_match_j = -1
        best_f1 = 0.0
        
        for j, gold_herb in enumerate(gold_herbs):
            if j in matched_gold_herbs:
                continue
            
            f1_score = char_f1(pred_herb, gold_herb)
            if f1_score > threshold and f1_score > best_f1:
                best_f1 = f1_score
                best_match_j = j
        
        if best_match_j >= 0:
            gold_herb = gold_herbs[best_match_j]
            pred_dose = pred_prescription[pred_herb]
            gold_dose = gold_prescription[gold_herb]
            
            # 只有剂量都不为None时才算入
            if pred_dose is not None and gold_dose is not None:
                pred_aligned.append(pred_dose)
                gold_aligned.append(gold_dose)
                matched_gold_herbs.add(best_match_j)
                matched_pred_herbs.add(i)
    
    # 未匹配部分补0（多药、漏药）
    for j, gold_herb in enumerate(gold_herbs):
        if j not in matched_gold_herbs:
            gold_dose = gold_prescription[gold_herb]
            if gold_dose is not None:
                pred_aligned.append(0.0)
                gold_aligned.append(gold_dose)
                
    for i, pred_herb in enumerate(pred_herbs):
        if i not in matched_pred_herbs:
            pred_dose = pred_prescription[pred_herb]
            if pred_dose is not None:
                pred_aligned.append(pred_dose)
                gold_aligned.append(0.0)

    # 转向量计算余弦相似度
    if len(pred_aligned) == 0 or len(gold_aligned) == 0:
        return 0.0
        
    a = np.array(pred_aligned, dtype=float)
    b = np.array(gold_aligned, dtype=float)
    na = np.linalg.norm(a)
    nb = np.linalg.norm(b)
    if na == 0 and nb == 0:
        return 1.0
    if na == 0 or nb == 0:
        return 0.0
    return float(a.dot(b) / (na * nb))


def format_prescription_text(prescription: Dict[str, float]) -> str:
    """格式化处方文本"""
    if not prescription:
        return ""
    return "; ".join([f"{herb}: {dose}克" if dose else f"{herb}: 未知剂量" 
                      for herb, dose in prescription.items()])


class PresDigEvalCharF1(Eval):
    """中医诊疗全流程评测类 - 字符级F1版本"""

    def __init__(self, data_path: str, num_examples: int | None = None, 
                 num_threads: int = 1, threshold: float = 0.7):
        examples = []
        with open(data_path, 'r', encoding='utf-8') as f:
            for line in f:
                if line.strip():
                    examples.append(json.loads(line))

        if num_examples:
            examples = random.Random(0).sample(examples, min(num_examples, len(examples)))

        self.examples = examples
        self.num_threads = num_threads
        self.threshold = threshold  # 字符F1匹配阈值
        print(f"加载了 {len(examples)} 条中医诊疗样本 (字符F1阈值: {threshold})")

    def __call__(self, sampler: SamplerBase) -> EvalResult:
        def fn(row: dict):
            prompt_messages = [sampler._pack_message(
                content=MEDICAL_DIAGNOSIS_TEMPLATE.format(medical_record=row["病历文本"]), 
                role="user"
            )]
            sampler_response = sampler(prompt_messages)
            response_text = sampler_response.response_text
            actual_queried_prompt_messages = sampler_response.actual_queried_message_list

            # 提取模型预测的辨证、治法和处方
            pred_syndromes, pred_treatments, pred_prescription = extract_response_from_json(response_text)

            # 标准答案
            gold_syndromes = [s.strip() for s in row["辨证"].split(",") if s.strip()]
            gold_treatments = [t.strip() for t in row["治法"].split(",") if t.strip()]
            gold_prescription = parse_prescription(row["处方"])

            # 使用字符级F1匹配辨证
            syndrome_matches, wrong_syndromes, missed_syndromes = match_items_with_char_f1(
                pred_syndromes, gold_syndromes, self.threshold
            )
            syndrome_precision, syndrome_recall, syndrome_f1 = calculate_metrics(
                len(syndrome_matches), len(pred_syndromes), len(gold_syndromes)
            )
            correct_syndromes = [m[0] for m in syndrome_matches]

            # 使用字符级F1匹配治法
            treatment_matches, wrong_treatments, missed_treatments = match_items_with_char_f1(
                pred_treatments, gold_treatments, self.threshold
            )
            treatment_precision, treatment_recall, treatment_f1 = calculate_metrics(
                len(treatment_matches), len(pred_treatments), len(gold_treatments)
            )
            correct_treatments = [m[0] for m in treatment_matches]

            # 使用字符级F1匹配中药
            herb_matches, wrong_herbs, missed_herbs = match_herbs_with_char_f1(
                pred_prescription, gold_prescription, self.threshold
            )
            herb_precision, herb_recall, herb_f1 = calculate_metrics(
                len(herb_matches), len(pred_prescription), len(gold_prescription)
            )
            
            # 计算剂量MAE
            dose_mae = calculate_dose_mae(herb_matches)
            
            # 计算剂量余弦相似度（基于字符F1匹配）
            dose_cosine = calculate_dose_cosine_with_char_f1(
                pred_prescription, gold_prescription, self.threshold
            )

            # 综合F1分数（辨证、治法、处方的平均）
            overall_f1 = (syndrome_f1 + treatment_f1 + herb_f1) / 3

            # 格式化处方文本
            gold_prescription_text = format_prescription_text(gold_prescription)
            pred_prescription_text = format_prescription_text(pred_prescription)
            
            # 匹配的中药数量
            matched_herb_count = len(herb_matches)
            
            # 转换为原格式的correct_herbs（用于HTML渲染）
            correct_herbs = [{
                'herb': h['pred_herb'],
                'pred_dose': h['pred_dose'],
                'gold_dose': h['gold_dose'],
                'dose_error': h['dose_error'] or 0.0
            } for h in herb_matches]

            # 生成HTML报告
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
                correct_answer=f"辨证: {', '.join(gold_syndromes)}; 治法: {', '.join(gold_treatments)}; 处方: {gold_prescription_text}",
                extracted_answer=f"辨证: {', '.join(pred_syndromes) if pred_syndromes else '无'}; 治法: {', '.join(pred_treatments) if pred_treatments else '无'}; 处方: {pred_prescription_text if pred_prescription_text else '无'}",
            )

            convo = actual_queried_prompt_messages + [dict(content=response_text, role="assistant")]
            
            if str(dose_cosine) == "nan":
                print()

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
                    "overall_f1": overall_f1,
                    "char_f1_threshold": self.threshold
                }, 
                convo=convo
            )

        results = common.map_with_progress(fn, self.examples, num_threads=self.num_threads)
        return common.aggregate_results(results)
