# 决策识别：Full 评估结果

[English](README.md) · [返回数据说明](../../README_zh.md#论文评估结果)

以下仅展示本目录对应任务的 **Full** 成绩，覆盖论文中的 **19 个模型**。数值来自 [LingLan 论文 arXiv:2602.01779v1](https://arxiv.org/html/2602.01779v1)（2026-02-02）的表 2、表 3 和附录表 4；重复出现的对照模型合并为一行，模型名称沿用论文。

准确率、精确率、召回率和 F1 的单位为 %，数值越高越好。

## 对应数据文件

- `herbal_prescription_single_choice`: [医家处方_选择题.jsonl](医家处方_选择题.jsonl)
- `treatment_method_single_choice`: [医家治法_选择题.jsonl](医家治法_选择题.jsonl)
- `syndrome_single_choice`: [医家辨证_选择题.jsonl](医家辨证_选择题.jsonl)

## 辨证

| 模型 | 准确率 |
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

## 治法

| 模型 | 准确率 |
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

## 处方

| 模型 | 准确率 |
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

## 最小评估示例

每个子任务分别演示：读取一条样本、给出示例预测、打印标准答案并计算基础分数。示例均选自真实样本，`prediction` 使用该样本的完整标准答案演示回放，不是实际模型输出；使用时替换为你的模型答案。标准答案始终从 `sample["answer"]` 读取。

在当前任务目录运行，使用 Python 标准库即可。

分数范围为 0–1。以下是基础评分示例，不包含论文评估器的完整解析和匹配规则。

### `herbal_prescription_single_choice`

真实样本：`herbal_prescription_single_choice_0001`（[医家处方_选择题.jsonl](医家处方_选择题.jsonl)，第 1 条）。

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

真实样本：`treatment_method_single_choice_0001`（[医家治法_选择题.jsonl](医家治法_选择题.jsonl)，第 1 条）。

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

真实样本：`syndrome_single_choice_0001`（[医家辨证_选择题.jsonl](医家辨证_选择题.jsonl)，第 1 条）。

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
