# Information extraction: Hard results

[中文说明](README_zh.md) · [Dataset documentation](../../README.md#paper-evaluation-results)

These tables show only **Hard** results for the tasks in this directory, covering **19 models** from Tables 2, 3, and Appendix Table 4 of [LingLanMiDian, arXiv:2602.01779v1](https://arxiv.org/html/2602.01779v1) (2026-02-02). Repeated reference models are merged into one row; names follow the paper.

Accuracy, precision, recall, and F1 are percentages; higher is better.

## Data files

- `classical_text_entity_extraction`: [实体抽取_古籍.jsonl](实体抽取_古籍.jsonl)
- `clinical_record_entity_extraction`: [实体抽取_病历.jsonl](实体抽取_病历.jsonl)

## Clinical EMR

| Model | Precision | Recall | F1 |
| --- | ---: | ---: | ---: |
| DeepSeek-R1 | 46.7 | 43.9 | 44.2 |
| DeepSeek-V3.1 | 46.7 | 42.4 | 43.4 |
| GPT-5 | 56.2 | 56.0 | 55.1 |
| Qwen3-235B | 50.5 | 49.3 | 49.1 |
| Qwen3-32B | 61.3 | 49.8 | 54.2 |
| Baichuan-M2-32B | 45.5 | 41.9 | 42.6 |
| Qwen3-Next-80B | 17.3 | 15.0 | 15.5 |
| GPT-OSS-120B | 41.4 | 41.9 | 40.6 |
| Qwen3-30B-A3B | 57.2 | 37.9 | 44.6 |
| Qwen3-14B | 62.8 | 52.0 | 55.7 |
| Qwen3-8B | 55.1 | 45.1 | 48.6 |
| Qwen3-4B | 52.7 | 41.3 | 45.4 |
| gpt-5-mini | 35.2 | 43.6 | 38.3 |
| gpt-oss-20b | 39.5 | 38.5 | 38.0 |
| Baichuan2-13B-Chat | 25.0 | 22.6 | 22.7 |
| Lingdan-13B-TCPM | 1.1 | 0.9 | 0.8 |
| TCMChat | 0.1 | 0.0 | 0.0 |
| BianCang-7B | 21.7 | 11.5 | 12.9 |
| BianCang-14B | 33.2 | 21.5 | 24.8 |

## Classical Texts

| Model | Precision | Recall | F1 |
| --- | ---: | ---: | ---: |
| DeepSeek-R1 | 40.2 | 44.7 | 41.5 |
| DeepSeek-V3.1 | 42.8 | 48.8 | 44.7 |
| GPT-5 | 11.4 | 16.3 | 13.1 |
| Qwen3-235B | 37.9 | 45.9 | 40.4 |
| Qwen3-32B | 38.1 | 37.9 | 36.9 |
| Baichuan-M2-32B | 38.0 | 42.6 | 39.2 |
| Qwen3-Next-80B | 13.8 | 14.9 | 13.8 |
| GPT-OSS-120B | 31.0 | 38.5 | 33.5 |
| Qwen3-30B-A3B | 38.9 | 37.3 | 37.0 |
| Qwen3-14B | 39.6 | 38.3 | 38.0 |
| Qwen3-8B | 35.4 | 34.4 | 34.0 |
| Qwen3-4B | 35.0 | 32.0 | 32.4 |
| gpt-5-mini | 23.9 | 35.6 | 28.0 |
| gpt-oss-20b | 26.6 | 31.8 | 28.1 |
| Baichuan2-13B-Chat | 21.5 | 18.1 | 18.7 |
| Lingdan-13B-TCPM | 2.8 | 1.5 | 1.7 |
| TCMChat | 1.8 | 0.2 | 0.4 |
| BianCang-7B | 25.2 | 26.9 | 24.5 |
| BianCang-14B | 39.0 | 32.4 | 34.0 |

## Minimal evaluation example

Each subtask shows how to load one example, supply an illustrative prediction, print the gold answer, and compute a basic score. Every example uses a real record. `prediction` replays its complete gold answer for demonstration, not an actual model response; replace it with your model output. The gold answer is always read from `sample["answer"]`.

Run from this task directory using the Python standard library.

Scores range from 0 to 1. These basic scoring examples do not include the paper evaluator's full parsing and matching rules.

### `classical_text_entity_extraction`

Real example: `classical_text_entity_extraction_1733` ([实体抽取_古籍.jsonl](实体抽取_古籍.jsonl), record 362).

Exact entity-type/text matching, retaining duplicate counts.

```python
import json

with open('实体抽取_古籍.jsonl', encoding="utf-8") as f:
    sample = json.loads(f.readlines()[361])
assert sample["id"] == 'classical_text_entity_extraction_1733'
print(sample["text"])

prediction = {'中药': ['天门冬', '贝母', '地黄'],
 '药味': ['味苦', '微甘', '味厚'],
 '药性': ['气大寒', '沉', '阴'],
 '归经': ['入肺、肾两经'],
 '功效': ['除虚劳内热', '定热喘', '下去热淋', '苦杀三虫', '润滋骨髓', '解渴', '除烦', '消痰', '止嗽', '降火', '保肺', '退热', '滋阴'],
 '主治': ['血热燥结'],
 '禁忌': ['虚寒假热', '脾肾溏泄'],
 '中药七情关系': ['使']}
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

Real example: `clinical_record_entity_extraction_1798` ([实体抽取_病历.jsonl](实体抽取_病历.jsonl), record 40).

Exact entity-type/text matching, retaining duplicate counts.

```python
import json

with open('实体抽取_病历.jsonl', encoding="utf-8") as f:
    sample = json.loads(f.readlines()[39])
assert sample["id"] == 'clinical_record_entity_extraction_1798'
print(sample["text"])

prediction = {'变化情况': ['眩晕及头部昏沉感减轻', '未再出现胸闷气短', '饮食控制较前好'],
 '阳性症状': ['偶有咳痰'],
 '阴性症状': ['睡眠可', '二便调'],
 '舌脉': ['舌暗红', '苔薄黄腻', '脉弦滑'],
 '阴性体征': ['BP120/70mmHg',
          '神志清',
          '言语清晰流利',
          '高级智能水平正常',
          '双侧瞳孔等大等圆',
          '光反射灵敏',
          '眼动各向正常',
          '无眼震及复视',
          '口舌居中',
          '软腭弓动度好',
          '悬雍垂居中',
          '双侧咽反射灵敏',
          '四肢肌力5级',
          '肌张力可',
          '腱反射（++）',
          '双侧巴氏征（-）']}
gold = sample["answer"]
print("Prediction:", prediction)
print("Gold:", gold)

from collections import Counter
p = Counter((k, x.strip()) for k, xs in prediction.items() for x in (xs or []))
g = Counter((k, x.strip()) for k, xs in gold.items() for x in (xs or []))
score = 2 * sum((p & g).values()) / (sum(p.values()) + sum(g.values())) if p or g else 1.0
print('Entity F1', score)
```
