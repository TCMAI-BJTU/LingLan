# Fundamental TCM knowledge: Hard results

[中文说明](README_zh.md) · [Dataset documentation](../../README.md#paper-evaluation-results)

These tables show only **Hard** results for the tasks in this directory, covering **19 models** from Tables 2, 3, and Appendix Table 4 of [LingLan, arXiv:2602.01779v1](https://arxiv.org/html/2602.01779v1) (2026-02-02). Repeated reference models are merged into one row; names follow the paper.

Accuracy, precision, recall, and F1 are percentages; higher is better.

## Data files

- `fundamental_tcm_knowledge_single_choice`: [知识图谱知识问答_单选题.jsonl](知识图谱知识问答_单选题.jsonl)
- `fundamental_tcm_knowledge_fill_blank`: [知识图谱知识问答_填空题.jsonl](知识图谱知识问答_填空题.jsonl)
- `fundamental_tcm_knowledge_multiple_choice`: [知识图谱知识问答_多选题.jsonl](知识图谱知识问答_多选题.jsonl)

## Single-choice

| Model | Accuracy |
| --- | ---: |
| DeepSeek-R1 | 46.5 |
| DeepSeek-V3.1 | 45.3 |
| GPT-5 | 44.5 |
| Qwen3-235B | 45.3 |
| Qwen3-32B | 44.3 |
| Baichuan-M2-32B | 35.8 |
| Qwen3-Next-80B | 33.3 |
| GPT-OSS-120B | 28.2 |
| Qwen3-30B-A3B | 32.0 |
| Qwen3-14B | 34.5 |
| Qwen3-8B | 33.8 |
| Qwen3-4B | 28.5 |
| gpt-5-mini | 28.7 |
| gpt-oss-20b | 29.3 |
| Baichuan2-13B-Chat | 28.5 |
| Lingdan-13B-TCPM | 26.3 |
| TCMChat | 7.5 |
| BianCang-7B | 43.3 |
| BianCang-14B | 49.3 |

## Multiple-choice

| Model | Accuracy | Precision | Recall | F1 |
| --- | ---: | ---: | ---: | ---: |
| DeepSeek-R1 | 31.5 | 82.4 | 79.3 | 77.8 |
| DeepSeek-V3.1 | 28.0 | 80.5 | 80.5 | 77.5 |
| GPT-5 | 19.3 | 75.3 | 69.8 | 69.3 |
| Qwen3-235B | 25.0 | 80.9 | 73.7 | 73.7 |
| Qwen3-32B | 23.3 | 77.5 | 78.0 | 74.8 |
| Baichuan-M2-32B | 14.0 | 75.4 | 66.1 | 66.4 |
| Qwen3-Next-80B | 14.8 | 71.6 | 65.2 | 64.2 |
| GPT-OSS-120B | 9.8 | 63.5 | 65.6 | 61.3 |
| Qwen3-30B-A3B | 17.0 | 75.2 | 73.5 | 71.0 |
| Qwen3-14B | 13.8 | 75.2 | 69.4 | 68.7 |
| Qwen3-8B | 13.0 | 71.8 | 70.2 | 67.6 |
| Qwen3-4B | 12.3 | 69.0 | 67.6 | 64.8 |
| gpt-5-mini | 10.8 | 67.7 | 69.0 | 65.3 |
| gpt-oss-20b | 6.0 | 59.5 | 58.1 | 55.0 |
| Baichuan2-13B-Chat | 12.8 | 62.0 | 79.8 | 67.7 |
| Lingdan-13B-TCPM | 9.5 | 48.8 | 56.4 | 49.0 |
| TCMChat | 0.5 | 48.2 | 29.1 | 32.4 |
| BianCang-7B | 19.5 | 70.1 | 72.7 | 68.0 |
| BianCang-14B | 13.0 | 59.8 | 48.7 | 50.3 |

## Cloze

| Model | char-F1 |
| --- | ---: |
| DeepSeek-R1 | 20.9 |
| DeepSeek-V3.1 | 19.7 |
| GPT-5 | 19.8 |
| Qwen3-235B | 23.5 |
| Qwen3-32B | 17.5 |
| Baichuan-M2-32B | 16.2 |
| Qwen3-Next-80B | 15.9 |
| GPT-OSS-120B | 14.0 |
| Qwen3-30B-A3B | 17.9 |
| Qwen3-14B | 14.3 |
| Qwen3-8B | 12.3 |
| Qwen3-4B | 15.9 |
| gpt-5-mini | 17.9 |
| gpt-oss-20b | 10.6 |
| Baichuan2-13B-Chat | 13.3 |
| Lingdan-13B-TCPM | 4.5 |
| TCMChat | 6.5 |
| BianCang-7B | 15.0 |
| BianCang-14B | 14.6 |

## Minimal evaluation example

Each subtask shows how to load one example, supply an illustrative prediction, print the gold answer, and compute a basic score. Every example uses a real record. `prediction` replays its complete gold answer for demonstration, not an actual model response; replace it with your model output. The gold answer is always read from `sample["answer"]`.

Run from this task directory using the Python standard library.

Scores range from 0 to 1. These basic scoring examples do not include the paper evaluator's full parsing and matching rules.

### `fundamental_tcm_knowledge_single_choice`

Real example: `fundamental_tcm_knowledge_single_choice_0024` ([知识图谱知识问答_单选题.jsonl](知识图谱知识问答_单选题.jsonl), record 1).

```python
import json

with open('知识图谱知识问答_单选题.jsonl', encoding="utf-8") as f:
    sample = json.loads(f.readlines()[0])
assert sample["id"] == 'fundamental_tcm_knowledge_single_choice_0024'
print(sample["question"], sample.get("options", []))

prediction = 'A'
gold = sample["answer"]
print("Prediction:", prediction)
print("Gold:", gold)

score = int(prediction == gold)
print('Accuracy', score)
```

### `fundamental_tcm_knowledge_fill_blank`

Real example: `fundamental_tcm_knowledge_fill_blank_1715` ([知识图谱知识问答_填空题.jsonl](知识图谱知识问答_填空题.jsonl), record 103).

Predictions are answer lists; gold answers use `、` separators. Score with character-set F1.

```python
import json

with open('知识图谱知识问答_填空题.jsonl', encoding="utf-8") as f:
    sample = json.loads(f.readlines()[102])
assert sample["id"] == 'fundamental_tcm_knowledge_fill_blank_1715'
print(sample["question"], sample.get("options", []))

prediction = ['脉细数', '舌绛苔少']
gold = sample["answer"]
print("Prediction:", prediction)
print("Gold:", gold)

p = set("".join(prediction))
g = set("".join(x.strip() for x in gold.split("、")))
score = 2 * len(p & g) / (len(p) + len(g)) if p or g else 1.0
print('Character F1', score)
```

### `fundamental_tcm_knowledge_multiple_choice`

Real example: `fundamental_tcm_knowledge_multiple_choice_0827` ([知识图谱知识问答_多选题.jsonl](知识图谱知识问答_多选题.jsonl), record 1).

Score exact option-set matches.

```python
import json

with open('知识图谱知识问答_多选题.jsonl', encoding="utf-8") as f:
    sample = json.loads(f.readlines()[0])
assert sample["id"] == 'fundamental_tcm_knowledge_multiple_choice_0827'
print(sample["question"], sample.get("options", []))

prediction = ['A']
gold = sample["answer"]
print("Prediction:", prediction)
print("Gold:", gold)

score = int(set(prediction) == set(gold))
print('Accuracy', score)
```
