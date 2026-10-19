# Chinese patent medicine knowledge: Full results

[中文说明](README_zh.md) · [Dataset documentation](../../README.md#paper-evaluation-results)

These tables show only **Full** results for the tasks in this directory, covering **19 models** from Tables 1, 2, and Supplementary Table S1 of [LingLanMedBench, arXiv:2602.01779](https://arxiv.org/html/2602.01779). Repeated reference models are merged into one row; names follow the paper.

Accuracy, precision, recall, and F1 are percentages; higher is better.

## Data files

- `chinese_patent_medicine_knowledge_single_choice`: [中成药知识问答_单选题.jsonl](中成药知识问答_单选题.jsonl)
- `chinese_patent_medicine_knowledge_fill_blank`: [中成药知识问答_填空题.jsonl](中成药知识问答_填空题.jsonl)
- `chinese_patent_medicine_knowledge_multiple_choice`: [中成药知识问答_多选题.jsonl](中成药知识问答_多选题.jsonl)

## Single-choice

| Model | Accuracy |
| --- | ---: |
| DeepSeek-R1 | 74.3 |
| DeepSeek-V3.1 | 73.3 |
| GPT-5 | 67.3 |
| Qwen3-235B | 68.6 |
| Qwen3-32B | 66.9 |
| Baichuan-M2-32B | 60.5 |
| Qwen3-Next-80B | 63.1 |
| GPT-OSS-120B | 44.5 |
| Qwen3-30B-A3B | 58.4 |
| Qwen3-14B | 58.9 |
| Qwen3-8B | 56.6 |
| Qwen3-4B | 51.3 |
| gpt-5-mini | 51.8 |
| gpt-oss-20b | 37.6 |
| Baichuan2-13B-Chat | 41.6 |
| Lingdan-13B-TCPM | 28.3 |
| TCMChat | 19.2 |
| BianCang-7B | 58.4 |
| BianCang-14B | 62.5 |

## Multiple-choice

| Model | Accuracy | Precision | Recall | F1 |
| --- | ---: | ---: | ---: | ---: |
| DeepSeek-R1 | 48.0 | 86.4 | 90.6 | 87.0 |
| DeepSeek-V3.1 | 42.2 | 84.3 | 91.5 | 86.3 |
| GPT-5 | 35.4 | 82.4 | 87.8 | 83.3 |
| Qwen3-235B | 44.8 | 86.1 | 87.7 | 85.4 |
| Qwen3-32B | 35.5 | 81.9 | 87.8 | 83.2 |
| Baichuan-M2-32B | 33.2 | 83.1 | 82.2 | 80.6 |
| Qwen3-Next-80B | 34.2 | 80.6 | 84.1 | 80.1 |
| GPT-OSS-120B | 24.7 | 76.0 | 82.5 | 77.3 |
| Qwen3-30B-A3B | 34.7 | 81.8 | 85.4 | 82.0 |
| Qwen3-14B | 34.4 | 82.5 | 84.9 | 82.0 |
| Qwen3-8B | 31.4 | 81.3 | 84.2 | 80.9 |
| Qwen3-4B | 28.7 | 79.3 | 84.7 | 80.0 |
| gpt-5-mini | 28.9 | 78.2 | 82.7 | 78.7 |
| gpt-oss-20b | 18.5 | 72.6 | 75.4 | 71.6 |
| Baichuan2-13B-Chat | 16.8 | 71.5 | 83.5 | 75.2 |
| Lingdan-13B-TCPM | 9.7 | 51.3 | 57.9 | 52.3 |
| TCMChat | 0.8 | 55.1 | 28.1 | 33.8 |
| BianCang-7B | 24.7 | 75.5 | 83.0 | 77.1 |
| BianCang-14B | 14.1 | 39.0 | 36.6 | 36.3 |

## Cloze

| Model | char-F1 |
| --- | ---: |
| DeepSeek-R1 | 74.0 |
| DeepSeek-V3.1 | 74.4 |
| GPT-5 | 67.6 |
| Qwen3-235B | 74.3 |
| Qwen3-32B | 67.5 |
| Baichuan-M2-32B | 64.6 |
| Qwen3-Next-80B | 70.8 |
| GPT-OSS-120B | 57.5 |
| Qwen3-30B-A3B | 66.3 |
| Qwen3-14B | 66.8 |
| Qwen3-8B | 64.1 |
| Qwen3-4B | 61.4 |
| gpt-5-mini | 65.1 |
| gpt-oss-20b | 49.9 |
| Baichuan2-13B-Chat | 37.2 |
| Lingdan-13B-TCPM | 11.7 |
| TCMChat | 13.8 |
| BianCang-7B | 54.4 |
| BianCang-14B | 58.4 |

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

Real example: `chinese_patent_medicine_knowledge_fill_blank_0084` ([中成药知识问答_填空题.jsonl](中成药知识问答_填空题.jsonl), record 84).

Predictions are answer lists; gold answers use `、` separators. Score with character-set F1.

```python
import json

with open('中成药知识问答_填空题.jsonl', encoding="utf-8") as f:
    sample = json.loads(f.readlines()[83])
assert sample["id"] == 'chinese_patent_medicine_knowledge_fill_blank_0084'
print(sample["question"], sample.get("options", []))

prediction = ['化瘀止血', '消肿止痛']
gold = sample["answer"]
print("Prediction:", prediction)
print("Gold:", gold)

p = set("".join(prediction))
g = set("".join(x.strip() for x in gold.split("、")))
score = 2 * len(p & g) / (len(p) + len(g)) if p or g else 1.0
print('Character F1', score)
```

### `chinese_patent_medicine_knowledge_multiple_choice`

Real example: `chinese_patent_medicine_knowledge_multiple_choice_0001` ([中成药知识问答_多选题.jsonl](中成药知识问答_多选题.jsonl), record 1).

Score exact option-set matches.

```python
import json

with open('中成药知识问答_多选题.jsonl', encoding="utf-8") as f:
    sample = json.loads(f.readlines()[0])
assert sample["id"] == 'chinese_patent_medicine_knowledge_multiple_choice_0001'
print(sample["question"], sample.get("options", []))

prediction = ['B', 'C', 'D']
gold = sample["answer"]
print("Prediction:", prediction)
print("Gold:", gold)

score = int(set(prediction) == set(gold))
print('Accuracy', score)
```
