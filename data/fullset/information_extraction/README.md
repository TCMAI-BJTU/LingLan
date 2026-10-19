# Information extraction: Full results

[中文说明](README_zh.md) · [Dataset documentation](../../README.md#paper-evaluation-results)

These tables show only **Full** results for the tasks in this directory, covering **19 models** from Tables 1, 2, and Supplementary Table S1 of [LingLanMedBench, arXiv:2602.01779](https://arxiv.org/html/2602.01779). Repeated reference models are merged into one row; names follow the paper.

Accuracy, precision, recall, and F1 are percentages; higher is better.

## Data files

- `classical_text_entity_extraction`: [实体抽取_古籍.jsonl](实体抽取_古籍.jsonl)
- `clinical_record_entity_extraction`: [实体抽取_病历.jsonl](实体抽取_病历.jsonl)

## Clinical records

| Model | Precision | Recall | F1 |
| --- | ---: | ---: | ---: |
| DeepSeek-R1 | 66.6 | 61.3 | 63.1 |
| DeepSeek-V3.1 | 64.6 | 58.6 | 60.8 |
| GPT-5 | 72.8 | 71.9 | 71.7 |
| Qwen3-235B | 69.1 | 66.3 | 67.2 |
| Qwen3-32B | 73.3 | 62.2 | 66.7 |
| Baichuan-M2-32B | 61.8 | 56.0 | 58.1 |
| Qwen3-Next-80B | 38.1 | 33.5 | 35.2 |
| GPT-OSS-120B | 59.7 | 55.8 | 57.1 |
| Qwen3-30B-A3B | 69.3 | 48.4 | 56.2 |
| Qwen3-14B | 74.6 | 62.1 | 67.1 |
| Qwen3-8B | 67.7 | 57.6 | 61.5 |
| Qwen3-4B | 64.7 | 52.3 | 57.2 |
| gpt-5-mini | 52.1 | 57.0 | 54.0 |
| gpt-oss-20b | 55.3 | 51.6 | 52.8 |
| Baichuan2-13B-Chat | 27.0 | 25.0 | 25.1 |
| Lingdan-13B-TCPM | 1.2 | 0.8 | 0.8 |
| TCMChat | 0.0 | 0.0 | 0.0 |
| BianCang-7B | 25.5 | 15.0 | 16.8 |
| BianCang-14B | 38.1 | 26.1 | 29.5 |

## Classical Texts

| Model | Precision | Recall | F1 |
| --- | ---: | ---: | ---: |
| DeepSeek-R1 | 60.1 | 62.9 | 60.8 |
| DeepSeek-V3.1 | 61.4 | 64.4 | 62.1 |
| GPT-5 | 44.7 | 51.7 | 47.5 |
| Qwen3-235B | 57.3 | 62.6 | 59.1 |
| Qwen3-32B | 57.9 | 56.9 | 56.6 |
| Baichuan-M2-32B | 58.9 | 61.6 | 59.5 |
| Qwen3-Next-80B | 38.7 | 40.3 | 39.0 |
| GPT-OSS-120B | 51.1 | 56.6 | 53.0 |
| Qwen3-30B-A3B | 59.7 | 56.3 | 57.2 |
| Qwen3-14B | 59.8 | 56.3 | 57.3 |
| Qwen3-8B | 58.1 | 54.7 | 55.6 |
| Qwen3-4B | 54.5 | 49.2 | 51.0 |
| gpt-5-mini | 48.9 | 60.5 | 53.4 |
| gpt-oss-20b | 50.3 | 54.0 | 51.3 |
| Baichuan2-13B-Chat | 32.3 | 27.8 | 29.0 |
| Lingdan-13B-TCPM | 5.6 | 2.9 | 3.4 |
| TCMChat | 1.5 | 0.2 | 0.3 |
| BianCang-7B | 46.1 | 44.9 | 44.1 |
| BianCang-14B | 55.3 | 46.0 | 49.0 |

## Minimal evaluation example

Each subtask shows how to load one example, supply an illustrative prediction, print the gold answer, and compute a basic score. Every example uses a real record. `prediction` replays its complete gold answer for demonstration, not an actual model response; replace it with your model output. The gold answer is always read from `sample["answer"]`.

Run from this task directory using the Python standard library.

Scores range from 0 to 1. These basic scoring examples do not include the paper evaluator's full parsing and matching rules.

### `classical_text_entity_extraction`

Real example: `classical_text_entity_extraction_1964` ([实体抽取_古籍.jsonl](实体抽取_古籍.jsonl), record 1964).

Exact entity-type/text matching, retaining duplicate counts.

```python
import json

with open('实体抽取_古籍.jsonl', encoding="utf-8") as f:
    sample = json.loads(f.readlines()[1963])
assert sample["id"] == 'classical_text_entity_extraction_1964'
print(sample["text"])

prediction = {'病机': ['肝气肆横'],
 '阳性症状': ['腹痛'],
 '治则治法': ['疏泄'],
 '中药': ['青皮一钱 归须一钱 茺蔚子一钱 炒延胡一钱 郁金一钱 黑山栀一钱五分 南山楂一钱五分'],
 '中药剂量': ['青皮一钱', '归须一钱', '茺蔚子一钱', '炒延胡一钱', '郁金一钱', '黑山栀一钱五分', '南山楂一钱五分'],
 '中药名': ['青皮', '归须', '茺蔚子', '炒延胡', '郁金', '黑山栀', '南山楂']}
gold = sample["answer"]
print("Prediction:", prediction)
print("Gold:", gold)

from collections import Counter
p = Counter((k, x.strip()) for k, xs in prediction.items() for x in (xs or []))
g = Counter((k, x.strip()) for k, xs in gold.items() for x in (xs or []))
score = 2 * sum((p & g).values()) / (sum(p.values()) + sum(g.values())) if p or g else 1.0
print('Entity F1', score)
```

### `clinical_record_entity_extraction`

Real example: `clinical_record_entity_extraction_1776` ([实体抽取_病历.jsonl](实体抽取_病历.jsonl), record 1776).

Exact entity-type/text matching, retaining duplicate counts.

```python
import json

with open('实体抽取_病历.jsonl', encoding="utf-8") as f:
    sample = json.loads(f.readlines()[1775])
assert sample["id"] == 'clinical_record_entity_extraction_1776'
print(sample["text"])

prediction = {'其他检查': ['胃镜'],
 '西医疾病': ['CSG', '胃溃疡（A2）'],
 '阳性症状': ['胃胀', '胃痛', '头痛', '眼睛红', '头晕', '晨起口苦', '口苦', '胃疼', '头痛', '口苦', '胃胀'],
 '持续时间': ['5年'],
 '发作特征': ['时有', '晨起', '时有'],
 '阴性症状': ['纳可', '大便可'],
 '舌象': ['舌质淡红', '苔白', '舌质淡红', '苔白'],
 '脉象': ['脉弦实', '脉弦', '脉弦'],
 '就诊日期': ['11-06'],
 '变化情况': ['缓解', '消失']}
gold = sample["answer"]
print("Prediction:", prediction)
print("Gold:", gold)

from collections import Counter
p = Counter((k, x.strip()) for k, xs in prediction.items() for x in (xs or []))
g = Counter((k, x.strip()) for k, xs in gold.items() for x in (xs or []))
score = 2 * sum((p & g).values()) / (sum(p.values()) + sum(g.values())) if p or g else 1.0
print('Entity F1', score)
```
