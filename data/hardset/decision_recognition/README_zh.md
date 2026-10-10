# 决策识别：Hard 评估结果

[English](README.md) · [返回数据说明](../../README_zh.md#论文评估结果)

以下仅展示本目录对应任务的 **Hard** 成绩，覆盖论文中的 **19 个模型**。数值来自 [LingLanMiDian 论文 arXiv:2602.01779v1](https://arxiv.org/html/2602.01779v1)（2026-02-02）的表 2、表 3 和附录表 4；重复出现的对照模型合并为一行，模型名称沿用论文。

准确率、精确率、召回率和 F1 的单位为 %，数值越高越好。

## 对应数据文件

- `herbal_prescription_single_choice`: [医家处方_选择题.jsonl](医家处方_选择题.jsonl)
- `treatment_method_single_choice`: [医家治法_选择题.jsonl](医家治法_选择题.jsonl)
- `syndrome_single_choice`: [医家辨证_选择题.jsonl](医家辨证_选择题.jsonl)

## 辨证

| 模型 | 准确率 |
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

## 治法

| 模型 | 准确率 |
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

## 处方

| 模型 | 准确率 |
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

## 最小评估示例

每个子任务分别演示：读取一条样本、给出示例预测、打印标准答案并计算基础分数。示例均选自真实样本，`prediction` 使用该样本的完整标准答案演示回放，不是实际模型输出；使用时替换为你的模型答案。标准答案始终从 `sample["answer"]` 读取。

在当前任务目录运行，使用 Python 标准库即可。

分数范围为 0–1。以下是基础评分示例，不包含论文评估器的完整解析和匹配规则。

### `herbal_prescription_single_choice`

真实样本：`herbal_prescription_single_choice_0002`（[医家处方_选择题.jsonl](医家处方_选择题.jsonl)，第 1 条）。

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

真实样本：`treatment_method_single_choice_0005`（[医家治法_选择题.jsonl](医家治法_选择题.jsonl)，第 1 条）。

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

真实样本：`syndrome_single_choice_0005`（[医家辨证_选择题.jsonl](医家辨证_选择题.jsonl)，第 1 条）。

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
