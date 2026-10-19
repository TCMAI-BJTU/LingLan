# Chinese patent medicine knowledge: Hard results

[中文说明](README_zh.md) · [Dataset documentation](../../README.md#paper-evaluation-results)

These tables show only **Hard** results for the tasks in this directory, covering **19 models** from Tables 1, 2, and Supplementary Table S1 of [LingLanMedBench, arXiv:2602.01779](https://arxiv.org/html/2602.01779). Repeated reference models are merged into one row; names follow the paper.

Accuracy, precision, recall, and F1 are percentages; higher is better.

## Data files

- `chinese_patent_medicine_knowledge_single_choice`: [中成药知识问答_单选题.jsonl](中成药知识问答_单选题.jsonl)
- `chinese_patent_medicine_knowledge_fill_blank`: [中成药知识问答_填空题.jsonl](中成药知识问答_填空题.jsonl)
- `chinese_patent_medicine_knowledge_multiple_choice`: [中成药知识问答_多选题.jsonl](中成药知识问答_多选题.jsonl)

## Single-choice

| Model | Accuracy |
| --- | ---: |
| DeepSeek-R1 | 31.0 |
| DeepSeek-V3.1 | 25.5 |
| GPT-5 | 18.0 |
| Qwen3-235B | 17.8 |
| Qwen3-32B | 16.3 |
| Baichuan-M2-32B | 12.8 |
| Qwen3-Next-80B | 8.0 |
| GPT-OSS-120B | 13.0 |
| Qwen3-30B-A3B | 5.5 |
| Qwen3-14B | 9.8 |
| Qwen3-8B | 9.0 |
| Qwen3-4B | 9.3 |
| gpt-5-mini | 9.5 |
| gpt-oss-20b | 11.8 |
| Baichuan2-13B-Chat | 24.8 |
| Lingdan-13B-TCPM | 16.3 |
| TCMChat | 18.5 |
| BianCang-7B | 31.8 |
| BianCang-14B | 35.5 |

## Multiple-choice

| Model | Accuracy | Precision | Recall | F1 |
| --- | ---: | ---: | ---: | ---: |
| DeepSeek-R1 | 24.5 | 73.5 | 76.3 | 72.4 |
| DeepSeek-V3.1 | 15.0 | 69.6 | 78.4 | 71.5 |
| GPT-5 | 6.5 | 62.7 | 72.2 | 64.6 |
| Qwen3-235B | 15.3 | 69.7 | 71.1 | 68.0 |
| Qwen3-32B | 6.5 | 62.1 | 70.0 | 63.8 |
| Baichuan-M2-32B | 5.5 | 63.5 | 59.9 | 58.6 |
| Qwen3-Next-80B | 3.8 | 58.7 | 62.0 | 57.0 |
| GPT-OSS-120B | 4.0 | 53.9 | 61.8 | 55.6 |
| Qwen3-30B-A3B | 5.8 | 60.6 | 65.1 | 60.7 |
| Qwen3-14B | 5.3 | 61.5 | 64.6 | 60.4 |
| Qwen3-8B | 7.2 | 61.6 | 66.3 | 61.6 |
| Qwen3-4B | 4.5 | 59.3 | 67.7 | 60.7 |
| gpt-5-mini | 4.0 | 54.9 | 57.9 | 54.3 |
| gpt-oss-20b | 3.8 | 51.1 | 55.4 | 50.8 |
| Baichuan2-13B-Chat | 5.3 | 60.0 | 76.5 | 65.4 |
| Lingdan-13B-TCPM | 3.5 | 48.1 | 59.2 | 51.2 |
| TCMChat | 0.8 | 46.4 | 25.2 | 29.7 |
| BianCang-7B | 11.3 | 64.1 | 77.8 | 68.3 |
| BianCang-14B | 4.5 | 31.1 | 28.3 | 27.8 |

## Cloze

| Model | char-F1 |
| --- | ---: |
| DeepSeek-R1 | 57.6 |
| DeepSeek-V3.1 | 55.7 |
| GPT-5 | 45.7 |
| Qwen3-235B | 54.9 |
| Qwen3-32B | 41.3 |
| Baichuan-M2-32B | 41.0 |
| Qwen3-Next-80B | 46.7 |
| GPT-OSS-120B | 36.6 |
| Qwen3-30B-A3B | 41.3 |
| Qwen3-14B | 39.8 |
| Qwen3-8B | 37.9 |
| Qwen3-4B | 37.0 |
| gpt-5-mini | 43.3 |
| gpt-oss-20b | 29.5 |
| Baichuan2-13B-Chat | 26.4 |
| Lingdan-13B-TCPM | 9.3 |
| TCMChat | 10.6 |
| BianCang-7B | 37.5 |
| BianCang-14B | 42.2 |

## Minimal evaluation example

Each subtask shows how to load one example, supply an illustrative prediction, print the gold answer, and compute a basic score. Every example uses a real record. `prediction` replays its complete gold answer for demonstration, not an actual model response; replace it with your model output. The gold answer is always read from `sample["answer"]`.

Run from this task directory using the Python standard library.

Scores range from 0 to 1. These basic scoring examples do not include the paper evaluator's full parsing and matching rules.

### `chinese_patent_medicine_knowledge_single_choice`

Real example: `chinese_patent_medicine_knowledge_single_choice_0001` ([中成药知识问答_单选题.jsonl](中成药知识问答_单选题.jsonl), record 1).

```python
import json

with open('中成药知识问答_单选题.jsonl', encoding="utf-8") as f:
    sample = json.loads(f.readlines()[0])
assert sample["id"] == 'chinese_patent_medicine_knowledge_single_choice_0001'
print(sample["question"], sample.get("options", []))

prediction = 'D'
gold = sample["answer"]
print("Prediction:", prediction)
print("Gold:", gold)

score = int(prediction == gold)
print('Accuracy', score)
```

### `chinese_patent_medicine_knowledge_fill_blank`

Real example: `chinese_patent_medicine_knowledge_fill_blank_1968` ([中成药知识问答_填空题.jsonl](中成药知识问答_填空题.jsonl), record 197).

Predictions are answer lists; gold answers use `、` separators. Score with character-set F1.

```python
import json

with open('中成药知识问答_填空题.jsonl', encoding="utf-8") as f:
    sample = json.loads(f.readlines()[196])
assert sample["id"] == 'chinese_patent_medicine_knowledge_fill_blank_1968'
print(sample["question"], sample.get("options", []))

prediction = ['营血不足', '气滞血瘀']
gold = sample["answer"]
print("Prediction:", prediction)
print("Gold:", gold)

p = set("".join(prediction))
g = set("".join(x.strip() for x in gold.split("、")))
score = 2 * len(p & g) / (len(p) + len(g)) if p or g else 1.0
print('Character F1', score)
```

### `chinese_patent_medicine_knowledge_multiple_choice`

Real example: `chinese_patent_medicine_knowledge_multiple_choice_1166` ([中成药知识问答_多选题.jsonl](中成药知识问答_多选题.jsonl), record 1).

Score exact option-set matches.

```python
import json

with open('中成药知识问答_多选题.jsonl', encoding="utf-8") as f:
    sample = json.loads(f.readlines()[0])
assert sample["id"] == 'chinese_patent_medicine_knowledge_multiple_choice_1166'
print(sample["question"], sample.get("options", []))

prediction = ['A', 'C', 'D']
gold = sample["answer"]
print("Prediction:", prediction)
print("Gold:", gold)

score = int(set(prediction) == set(gold))
print('Accuracy', score)
```
