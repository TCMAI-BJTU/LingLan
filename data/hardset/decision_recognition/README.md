# Decision recognition: Hard results

[中文说明](README_zh.md) · [Dataset documentation](../../README.md#paper-evaluation-results)

These tables show only **Hard** results for the tasks in this directory, covering **19 models** from Tables 1, 2, and Supplementary Table S1 of [LingLanMedBench, arXiv:2602.01779](https://arxiv.org/html/2602.01779). Repeated reference models are merged into one row; names follow the paper.

Accuracy, precision, recall, and F1 are percentages; higher is better.

## Data files

- `herbal_prescription_single_choice`: [医家处方_选择题.jsonl](医家处方_选择题.jsonl)
- `treatment_method_single_choice`: [医家治法_选择题.jsonl](医家治法_选择题.jsonl)
- `syndrome_single_choice`: [医家辨证_选择题.jsonl](医家辨证_选择题.jsonl)

## Syndrome

| Model | Accuracy |
| --- | ---: |
| DeepSeek-R1 | 39.8 |
| DeepSeek-V3.1 | 35.5 |
| GPT-5 | 41.5 |
| Qwen3-235B | 40.8 |
| Qwen3-32B | 39.3 |
| Baichuan-M2-32B | 30.5 |
| Qwen3-Next-80B | 32.8 |
| GPT-OSS-120B | 34.8 |
| Qwen3-30B-A3B | 29.5 |
| Qwen3-14B | 34.5 |
| Qwen3-8B | 29.0 |
| Qwen3-4B | 25.3 |
| gpt-5-mini | 26.0 |
| gpt-oss-20b | 30.3 |
| Baichuan2-13B-Chat | 32.0 |
| Lingdan-13B-TCPM | 17.3 |
| TCMChat | 28.5 |
| BianCang-7B | 34.3 |
| BianCang-14B | 41.5 |

## Treatment

| Model | Accuracy |
| --- | ---: |
| DeepSeek-R1 | 22.8 |
| DeepSeek-V3.1 | 20.3 |
| GPT-5 | 22.0 |
| Qwen3-235B | 20.8 |
| Qwen3-32B | 22.3 |
| Baichuan-M2-32B | 15.3 |
| Qwen3-Next-80B | 17.8 |
| GPT-OSS-120B | 31.8 |
| Qwen3-30B-A3B | 23.8 |
| Qwen3-14B | 19.0 |
| Qwen3-8B | 20.3 |
| Qwen3-4B | 24.0 |
| gpt-5-mini | 26.0 |
| gpt-oss-20b | 33.5 |
| Baichuan2-13B-Chat | 28.5 |
| Lingdan-13B-TCPM | 20.5 |
| TCMChat | 27.5 |
| BianCang-7B | 32.3 |
| BianCang-14B | 26.5 |

## Prescription

| Model | Accuracy |
| --- | ---: |
| DeepSeek-R1 | 51.2 |
| DeepSeek-V3.1 | 55.3 |
| GPT-5 | 56.8 |
| Qwen3-235B | 49.3 |
| Qwen3-32B | 45.3 |
| Baichuan-M2-32B | 44.0 |
| Qwen3-Next-80B | 47.0 |
| GPT-OSS-120B | 37.3 |
| Qwen3-30B-A3B | 40.5 |
| Qwen3-14B | 43.3 |
| Qwen3-8B | 35.3 |
| Qwen3-4B | 36.0 |
| gpt-5-mini | 39.5 |
| gpt-oss-20b | 25.5 |
| Baichuan2-13B-Chat | 25.3 |
| Lingdan-13B-TCPM | 15.8 |
| TCMChat | 18.5 |
| BianCang-7B | 39.8 |
| BianCang-14B | 48.0 |

## Minimal evaluation example

Each subtask shows how to load one example, supply an illustrative prediction, print the gold answer, and compute a basic score. Every example uses a real record. `prediction` replays its complete gold answer for demonstration, not an actual model response; replace it with your model output. The gold answer is always read from `sample["answer"]`.

Run from this task directory using the Python standard library.

Scores range from 0 to 1. These basic scoring examples do not include the paper evaluator's full parsing and matching rules.

### `herbal_prescription_single_choice`

Real example: `herbal_prescription_single_choice_0002` ([医家处方_选择题.jsonl](医家处方_选择题.jsonl), record 1).

```python
import json

with open('医家处方_选择题.jsonl', encoding="utf-8") as f:
    sample = json.loads(f.readlines()[0])
assert sample["id"] == 'herbal_prescription_single_choice_0002'
print(sample["question"], sample.get("options", []))

prediction = 'A'
gold = sample["answer"]
print("Prediction:", prediction)
print("Gold:", gold)

score = int(prediction == gold)
print('Accuracy', score)
```

### `treatment_method_single_choice`

Real example: `treatment_method_single_choice_0005` ([医家治法_选择题.jsonl](医家治法_选择题.jsonl), record 1).

```python
import json

with open('医家治法_选择题.jsonl', encoding="utf-8") as f:
    sample = json.loads(f.readlines()[0])
assert sample["id"] == 'treatment_method_single_choice_0005'
print(sample["question"], sample.get("options", []))

prediction = 'B'
gold = sample["answer"]
print("Prediction:", prediction)
print("Gold:", gold)

score = int(prediction == gold)
print('Accuracy', score)
```

### `syndrome_single_choice`

Real example: `syndrome_single_choice_0005` ([医家辨证_选择题.jsonl](医家辨证_选择题.jsonl), record 1).

```python
import json

with open('医家辨证_选择题.jsonl', encoding="utf-8") as f:
    sample = json.loads(f.readlines()[0])
assert sample["id"] == 'syndrome_single_choice_0005'
print(sample["question"], sample.get("options", []))

prediction = 'B'
gold = sample["answer"]
print("Prediction:", prediction)
print("Gold:", gold)

score = int(prediction == gold)
print('Accuracy', score)
```
