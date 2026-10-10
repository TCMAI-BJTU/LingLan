# TCM licensing examination: Full results

[中文说明](README_zh.md) · [Dataset documentation](../../README.md#paper-evaluation-results)

These tables show only **Full** results for the tasks in this directory, covering **19 models** from Tables 2, 3, and Appendix Table 4 of [LingLan, arXiv:2602.01779v1](https://arxiv.org/html/2602.01779v1) (2026-02-02). Repeated reference models are merged into one row; names follow the paper.

Accuracy, precision, recall, and F1 are percentages; higher is better.

## Data files

- `tcm_licensing_examination`: [中医考试题.jsonl](中医考试题.jsonl)

## Comprehensive

| Model | Accuracy |
| --- | ---: |
| DeepSeek-R1 | 95.0 |
| DeepSeek-V3.1 | 95.5 |
| GPT-5 | 87.6 |
| Qwen3-235B | 95.0 |
| Qwen3-32B | 91.2 |
| Baichuan-M2-32B | 89.8 |
| Qwen3-Next-80B | 93.8 |
| GPT-OSS-120B | 58.1 |
| Qwen3-30B-A3B | 88.8 |
| Qwen3-14B | 87.6 |
| Qwen3-8B | 84.6 |
| Qwen3-4B | 76.6 |
| gpt-5-mini | 76.3 |
| gpt-oss-20b | 48.3 |
| Baichuan2-13B-Chat | 50.1 |
| Lingdan-13B-TCPM | 44.3 |
| TCMChat | 31.6 |
| BianCang-7B | 88.9 |
| BianCang-14B | 91.2 |

## Minimal evaluation example

Each subtask shows how to load one example, supply an illustrative prediction, print the gold answer, and compute a basic score. Every example uses a real record. `prediction` replays its complete gold answer for demonstration, not an actual model response; replace it with your model output. The gold answer is always read from `sample["answer"]`.

Run from this task directory using the Python standard library.

Scores range from 0 to 1. These basic scoring examples do not include the paper evaluator's full parsing and matching rules.

### `tcm_licensing_examination`

Real example: `tcm_licensing_examination_0001` ([中医考试题.jsonl](中医考试题.jsonl), record 1).

```python
import json

with open('中医考试题.jsonl', encoding="utf-8") as f:
    sample = json.loads(f.readlines()[0])
assert sample["id"] == 'tcm_licensing_examination_0001'
print(sample["题目"], sample["选项"])

prediction = 'B'
gold = sample["answer"]
print("Prediction:", prediction)
print("Gold:", gold)

score = int(prediction == gold)
print('Accuracy', score)
```
