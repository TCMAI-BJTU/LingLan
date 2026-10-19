# Decision recognition: Full results

[中文说明](README_zh.md) · [Dataset documentation](../../README.md#paper-evaluation-results)

These tables show only **Full** results for the tasks in this directory, covering **19 models** from Tables 1, 2, and Supplementary Table S1 of [LingLanMedBench, arXiv:2602.01779](https://arxiv.org/html/2602.01779). Repeated reference models are merged into one row; names follow the paper.

Accuracy, precision, recall, and F1 are percentages; higher is better.

## Data files

- `herbal_prescription_single_choice`: [医家处方_选择题.jsonl](医家处方_选择题.jsonl)
- `treatment_method_single_choice`: [医家治法_选择题.jsonl](医家治法_选择题.jsonl)
- `syndrome_single_choice`: [医家辨证_选择题.jsonl](医家辨证_选择题.jsonl)

## Syndrome

| Model | Accuracy |
| --- | ---: |
| DeepSeek-R1 | 86.7 |
| DeepSeek-V3.1 | 85.6 |
| GPT-5 | 86.9 |
| Qwen3-235B | 85.4 |
| Qwen3-32B | 86.0 |
| Baichuan-M2-32B | 83.6 |
| Qwen3-Next-80B | 84.9 |
| GPT-OSS-120B | 77.7 |
| Qwen3-30B-A3B | 84.1 |
| Qwen3-14B | 84.2 |
| Qwen3-8B | 82.8 |
| Qwen3-4B | 77.3 |
| gpt-5-mini | 80.7 |
| gpt-oss-20b | 70.3 |
| Baichuan2-13B-Chat | 64.6 |
| Lingdan-13B-TCPM | 32.5 |
| TCMChat | 47.2 |
| BianCang-7B | 73.8 |
| BianCang-14B | 80.7 |

## Treatment

| Model | Accuracy |
| --- | ---: |
| DeepSeek-R1 | 78.7 |
| DeepSeek-V3.1 | 77.6 |
| GPT-5 | 78.1 |
| Qwen3-235B | 79.0 |
| Qwen3-32B | 80.0 |
| Baichuan-M2-32B | 76.8 |
| Qwen3-Next-80B | 77.6 |
| GPT-OSS-120B | 75.3 |
| Qwen3-30B-A3B | 80.4 |
| Qwen3-14B | 78.4 |
| Qwen3-8B | 78.6 |
| Qwen3-4B | 74.8 |
| gpt-5-mini | 78.1 |
| gpt-oss-20b | 68.2 |
| Baichuan2-13B-Chat | 62.6 |
| Lingdan-13B-TCPM | 38.5 |
| TCMChat | 48.3 |
| BianCang-7B | 72.0 |
| BianCang-14B | 72.7 |

## Prescription

| Model | Accuracy |
| --- | ---: |
| DeepSeek-R1 | 89.1 |
| DeepSeek-V3.1 | 90.0 |
| GPT-5 | 90.6 |
| Qwen3-235B | 88.7 |
| Qwen3-32B | 87.5 |
| Baichuan-M2-32B | 87.9 |
| Qwen3-Next-80B | 88.4 |
| GPT-OSS-120B | 78.5 |
| Qwen3-30B-A3B | 86.7 |
| Qwen3-14B | 87.4 |
| Qwen3-8B | 84.9 |
| Qwen3-4B | 82.4 |
| gpt-5-mini | 84.4 |
| gpt-oss-20b | 64.5 |
| Baichuan2-13B-Chat | 36.2 |
| Lingdan-13B-TCPM | 18.1 |
| TCMChat | 23.0 |
| BianCang-7B | 65.6 |
| BianCang-14B | 80.5 |

## Minimal evaluation example

Each subtask shows how to load one example, supply an illustrative prediction, print the gold answer, and compute a basic score. Every example uses a real record. `prediction` replays its complete gold answer for demonstration, not an actual model response; replace it with your model output. The gold answer is always read from `sample["answer"]`.

Run from this task directory using the Python standard library.

Scores range from 0 to 1. These basic scoring examples do not include the paper evaluator's full parsing and matching rules.

### `herbal_prescription_single_choice`

Real example: `herbal_prescription_single_choice_0001` ([医家处方_选择题.jsonl](医家处方_选择题.jsonl), record 1).

```python
import json

with open('医家处方_选择题.jsonl', encoding="utf-8") as f:
    sample = json.loads(f.readlines()[0])
assert sample["id"] == 'herbal_prescription_single_choice_0001'
print(sample["question"], sample.get("options", []))

prediction = 'A'
gold = sample["answer"]
print("Prediction:", prediction)
print("Gold:", gold)

score = int(prediction == gold)
print('Accuracy', score)
```

### `treatment_method_single_choice`

Real example: `treatment_method_single_choice_0001` ([医家治法_选择题.jsonl](医家治法_选择题.jsonl), record 1).

```python
import json

with open('医家治法_选择题.jsonl', encoding="utf-8") as f:
    sample = json.loads(f.readlines()[0])
assert sample["id"] == 'treatment_method_single_choice_0001'
print(sample["question"], sample.get("options", []))

prediction = 'A'
gold = sample["answer"]
print("Prediction:", prediction)
print("Gold:", gold)

score = int(prediction == gold)
print('Accuracy', score)
```

### `syndrome_single_choice`

Real example: `syndrome_single_choice_0001` ([医家辨证_选择题.jsonl](医家辨证_选择题.jsonl), record 1).

```python
import json

with open('医家辨证_选择题.jsonl', encoding="utf-8") as f:
    sample = json.loads(f.readlines()[0])
assert sample["id"] == 'syndrome_single_choice_0001'
print(sample["question"], sample.get("options", []))

prediction = 'A'
gold = sample["answer"]
print("Prediction:", prediction)
print("Gold:", gold)

score = int(prediction == gold)
print('Accuracy', score)
```
