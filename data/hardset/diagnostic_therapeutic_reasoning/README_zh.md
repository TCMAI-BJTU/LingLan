# 诊疗推理：Hard 评估结果

[English](README.md) · [返回数据说明](../../README_zh.md#论文评估结果)

以下仅展示本目录对应任务的 **Hard** 成绩，覆盖论文中的 **19 个模型**。数值来自 [LingLanMedBench 论文 arXiv:2602.01779](https://arxiv.org/html/2602.01779)的表 1、表 2 和补充表 S1；重复出现的对照模型合并为一行，模型名称沿用论文。

准确率、精确率、召回率和 F1 的单位为 %，数值越高越好。

## 对应数据文件

- `herbal_prescription`: [医家处方.jsonl](医家处方.jsonl)
- `treatment_method`: [医家治法.jsonl](医家治法.jsonl)
- `syndrome`: [医家辨证.jsonl](医家辨证.jsonl)

论文成绩采用一次生成辨证、治法和处方的联合流程，不代表单独生成实验。下表分别报告包含关系匹配和字符 F1 匹配的成绩。表中的余弦相似度已乘以 100，越高越好；平均绝对误差单位为克，越低越好。论文指出，接近零的平均绝对误差可能源于药名匹配失败，不能视为剂量预测完全准确。

## 辨证 — 包含关系匹配

| 模型 | 精确率 | 召回率 | F1 |
| --- | ---: | ---: | ---: |
| DeepSeek-R1 | 1.3 | 1.7 | 1.5 |
| DeepSeek-V3.1 | 1.5 | 1.8 | 1.6 |
| GPT-5 | 0.7 | 1.1 | 0.9 |
| Qwen3-235B | 1.2 | 1.9 | 1.4 |
| Qwen3-32B | 0.6 | 0.9 | 0.7 |
| Baichuan-M2-32B | 1.2 | 1.6 | 1.4 |
| Qwen3-Next-80B | 1.5 | 1.7 | 1.6 |
| GPT-OSS-120B | 0.6 | 0.7 | 0.6 |
| Qwen3-30B-A3B | 1.4 | 2.0 | 1.6 |
| Qwen3-14B | 1.2 | 1.2 | 1.2 |
| Qwen3-8B | 1.0 | 1.1 | 1.0 |
| Qwen3-4B | 1.4 | 1.7 | 1.5 |
| gpt-5-mini | 0.3 | 0.4 | 0.3 |
| gpt-oss-20b | 1.4 | 2.1 | 1.6 |
| Baichuan2-13B-Chat | 1.5 | 1.3 | 1.3 |
| Lingdan-13B-TCPM | 0.0 | 0.0 | 0.0 |
| TCMChat | 0.2 | 0.3 | 0.3 |
| BianCang-7B | 1.5 | 0.9 | 1.1 |
| BianCang-14B | 1.7 | 1.0 | 1.2 |

## 治法 — 包含关系匹配

| 模型 | 精确率 | 召回率 | F1 |
| --- | ---: | ---: | ---: |
| DeepSeek-R1 | 1.9 | 2.3 | 1.9 |
| DeepSeek-V3.1 | 0.8 | 0.8 | 0.8 |
| GPT-5 | 2.1 | 4.6 | 2.8 |
| Qwen3-235B | 0.9 | 1.2 | 1.0 |
| Qwen3-32B | 1.3 | 1.5 | 1.3 |
| Baichuan-M2-32B | 0.6 | 0.9 | 0.7 |
| Qwen3-Next-80B | 0.6 | 0.9 | 0.7 |
| GPT-OSS-120B | 0.9 | 1.2 | 1.0 |
| Qwen3-30B-A3B | 0.8 | 1.1 | 0.9 |
| Qwen3-14B | 0.8 | 1.1 | 0.9 |
| Qwen3-8B | 0.8 | 1.0 | 0.9 |
| Qwen3-4B | 1.3 | 1.7 | 1.5 |
| gpt-5-mini | 1.3 | 1.5 | 1.2 |
| gpt-oss-20b | 0.8 | 0.9 | 0.8 |
| Baichuan2-13B-Chat | 1.5 | 1.4 | 1.3 |
| Lingdan-13B-TCPM | 0.1 | 0.1 | 0.1 |
| TCMChat | 0.8 | 0.5 | 0.6 |
| BianCang-7B | 1.3 | 1.0 | 1.1 |
| BianCang-14B | 1.8 | 1.0 | 1.2 |

## 处方 — 包含关系匹配

| 模型 | 精确率 | 召回率 | F1 |
| --- | ---: | ---: | ---: |
| DeepSeek-R1 | 19.7 | 17.9 | 18.2 |
| DeepSeek-V3.1 | 19.9 | 17.0 | 17.7 |
| GPT-5 | 17.1 | 25.9 | 20.1 |
| Qwen3-235B | 19.0 | 20.1 | 18.9 |
| Qwen3-32B | 17.0 | 16.9 | 16.4 |
| Baichuan-M2-32B | 18.0 | 17.2 | 17.0 |
| Qwen3-Next-80B | 17.4 | 16.8 | 16.4 |
| GPT-OSS-120B | 17.3 | 13.6 | 14.7 |
| Qwen3-30B-A3B | 18.1 | 14.9 | 15.8 |
| Qwen3-14B | 17.2 | 17.2 | 16.7 |
| Qwen3-8B | 17.1 | 14.7 | 15.2 |
| Qwen3-4B | 16.7 | 14.0 | 14.7 |
| gpt-5-mini | 16.1 | 19.0 | 16.9 |
| gpt-oss-20b | 15.7 | 14.0 | 14.2 |
| Baichuan2-13B-Chat | 9.5 | 8.1 | 8.3 |
| Lingdan-13B-TCPM | 0.2 | 0.2 | 0.2 |
| TCMChat | 0.0 | 0.0 | 0.0 |
| BianCang-7B | 9.8 | 10.1 | 9.1 |
| BianCang-14B | 5.4 | 5.6 | 5.1 |

## 剂量 — 包含关系匹配

| 模型 | 平均绝对误差（克） | 余弦相似度 × 100 |
| --- | ---: | ---: |
| DeepSeek-R1 | 4.0 | 16.2 |
| DeepSeek-V3.1 | 4.1 | 16.4 |
| GPT-5 | 4.9 | 19.7 |
| Qwen3-235B | 4.2 | 17.7 |
| Qwen3-32B | 4.7 | 15.5 |
| Baichuan-M2-32B | 4.1 | 15.4 |
| Qwen3-Next-80B | 3.9 | 15.2 |
| GPT-OSS-120B | 3.7 | 12.8 |
| Qwen3-30B-A3B | 4.0 | 15.3 |
| Qwen3-14B | 4.2 | 15.7 |
| Qwen3-8B | 4.1 | 14.2 |
| Qwen3-4B | 4.1 | 14.5 |
| gpt-5-mini | 5.3 | 16.0 |
| gpt-oss-20b | 4.3 | 12.4 |
| Baichuan2-13B-Chat | 2.2 | 7.5 |
| Lingdan-13B-TCPM | 0.0 | 0.1 |
| TCMChat | 0.0 | 0.0 |
| BianCang-7B | 2.0 | 8.6 |
| BianCang-14B | 1.3 | 4.9 |

## 辨证 — 字符 F1 匹配

| 模型 | 精确率 | 召回率 | F1 |
| --- | ---: | ---: | ---: |
| DeepSeek-R1 | 8.9 | 11.2 | 9.6 |
| DeepSeek-V3.1 | 10.0 | 11.2 | 10.1 |
| GPT-5 | 5.8 | 9.1 | 6.9 |
| Qwen3-235B | 9.5 | 12.3 | 10.4 |
| Qwen3-32B | 7.8 | 10.5 | 8.7 |
| Baichuan-M2-32B | 7.9 | 10.3 | 8.5 |
| Qwen3-Next-80B | 9.3 | 9.7 | 9.1 |
| GPT-OSS-120B | 5.4 | 6.8 | 5.8 |
| Qwen3-30B-A3B | 9.2 | 13.0 | 10.4 |
| Qwen3-14B | 8.3 | 11.3 | 9.2 |
| Qwen3-8B | 8.2 | 10.2 | 8.8 |
| Qwen3-4B | 8.1 | 10.7 | 8.8 |
| gpt-5-mini | 4.7 | 6.4 | 5.3 |
| gpt-oss-20b | 3.4 | 4.7 | 3.8 |
| Baichuan2-13B-Chat | 5.5 | 6.2 | 5.6 |
| Lingdan-13B-TCPM | 0.1 | 0.1 | 0.1 |
| TCMChat | 0.5 | 0.6 | 0.5 |
| BianCang-7B | 7.8 | 5.2 | 6.0 |
| BianCang-14B | 8.4 | 4.5 | 5.5 |

## 治法 — 字符 F1 匹配

| 模型 | 精确率 | 召回率 | F1 |
| --- | ---: | ---: | ---: |
| DeepSeek-R1 | 8.1 | 10.6 | 8.9 |
| DeepSeek-V3.1 | 6.2 | 7.8 | 6.7 |
| GPT-5 | 5.7 | 12.3 | 7.6 |
| Qwen3-235B | 6.4 | 8.7 | 7.2 |
| Qwen3-32B | 6.7 | 9.0 | 7.5 |
| Baichuan-M2-32B | 5.1 | 7.3 | 5.9 |
| Qwen3-Next-80B | 5.9 | 7.2 | 6.4 |
| GPT-OSS-120B | 4.3 | 5.9 | 4.9 |
| Qwen3-30B-A3B | 7.7 | 10.2 | 8.6 |
| Qwen3-14B | 6.2 | 8.8 | 7.1 |
| Qwen3-8B | 6.1 | 8.5 | 6.9 |
| Qwen3-4B | 6.2 | 8.6 | 7.1 |
| gpt-5-mini | 4.0 | 7.1 | 4.8 |
| gpt-oss-20b | 3.8 | 5.4 | 4.3 |
| Baichuan2-13B-Chat | 3.9 | 4.2 | 3.9 |
| Lingdan-13B-TCPM | 0.3 | 0.2 | 0.2 |
| TCMChat | 0.9 | 0.7 | 0.8 |
| BianCang-7B | 4.6 | 3.6 | 3.8 |
| BianCang-14B | 7.9 | 4.8 | 5.7 |

## 处方 — 字符 F1 匹配

| 模型 | 精确率 | 召回率 | F1 |
| --- | ---: | ---: | ---: |
| DeepSeek-R1 | 19.8 | 18.2 | 18.4 |
| DeepSeek-V3.1 | 20.0 | 17.1 | 17.8 |
| GPT-5 | 17.3 | 26.1 | 20.3 |
| Qwen3-235B | 19.2 | 20.2 | 19.0 |
| Qwen3-32B | 17.0 | 17.0 | 16.5 |
| Baichuan-M2-32B | 18.0 | 17.8 | 17.3 |
| Qwen3-Next-80B | 17.9 | 17.2 | 16.9 |
| GPT-OSS-120B | 17.4 | 13.7 | 14.8 |
| Qwen3-30B-A3B | 18.1 | 14.9 | 15.8 |
| Qwen3-14B | 17.1 | 17.4 | 16.8 |
| Qwen3-8B | 17.2 | 14.8 | 15.3 |
| Qwen3-4B | 16.8 | 14.1 | 14.8 |
| gpt-5-mini | 16.3 | 19.2 | 17.1 |
| gpt-oss-20b | 15.7 | 14.2 | 14.4 |
| Baichuan2-13B-Chat | 13.0 | 9.5 | 9.8 |
| Lingdan-13B-TCPM | 0.9 | 0.7 | 0.8 |
| TCMChat | 0.6 | 0.3 | 0.4 |
| BianCang-7B | 10.8 | 11.7 | 10.5 |
| BianCang-14B | 14.8 | 15.4 | 14.2 |

## 剂量 — 字符 F1 匹配

| 模型 | 平均绝对误差（克） | 余弦相似度 × 100 |
| --- | ---: | ---: |
| DeepSeek-R1 | 4.0 | 16.5 |
| DeepSeek-V3.1 | 4.2 | 16.5 |
| GPT-5 | 5.0 | 20.1 |
| Qwen3-235B | 4.2 | 17.8 |
| Qwen3-32B | 4.7 | 15.6 |
| Baichuan-M2-32B | 4.2 | 16.1 |
| Qwen3-Next-80B | 3.9 | 15.6 |
| GPT-OSS-120B | 3.8 | 12.9 |
| Qwen3-30B-A3B | 4.0 | 15.3 |
| Qwen3-14B | 4.3 | 15.8 |
| Qwen3-8B | 4.1 | 14.5 |
| Qwen3-4B | 4.1 | 14.6 |
| gpt-5-mini | 5.4 | 16.2 |
| gpt-oss-20b | 4.4 | 12.5 |
| Baichuan2-13B-Chat | 2.5 | 9.0 |
| Lingdan-13B-TCPM | 0.2 | 0.6 |
| TCMChat | 0.0 | 0.0 |
| BianCang-7B | 2.5 | 9.9 |
| BianCang-14B | 3.6 | 13.0 |

## 最小评估示例

每个子任务分别演示：读取一条样本、给出示例预测、打印标准答案并计算基础分数。示例均选自真实样本，`prediction` 使用该样本的完整标准答案演示回放，不是实际模型输出；使用时替换为你的模型答案。标准答案始终从 `sample["answer"]` 读取。

在当前任务目录运行，使用 Python 标准库即可。

分数范围为 0–1。以下是基础评分示例，不包含论文评估器的完整解析和匹配规则。

### `herbal_prescription`

真实样本：`herbal_prescription_0883`（[医家处方.jsonl](医家处方.jsonl)，第 241 条）。

只计算药名 F1，示例不计算剂量。

```python
import json

with open('医家处方.jsonl', encoding="utf-8") as f:
    sample = json.loads(f.readlines()[240])
assert sample["id"] == 'herbal_prescription_0883'
print(sample["病历文本"])

prediction = '熟地: 20g, 当归: 10g, 白芍: 15g, 肉桂: 1g, 干姜: 3g, 甘草: 12g'
gold = sample["answer"]
print("Prediction:", prediction)
print("Gold:", gold)

p = {x.split(":")[0].strip() for x in prediction.split(",") if x.strip()}
g = {x.split(":")[0].strip() for x in gold.split(",") if x.strip()}
score = 2 * len(p & g) / (len(p) + len(g)) if p or g else 1.0
print('F1', score)
```

### `treatment_method`

真实样本：`treatment_method_0883`（[医家治法.jsonl](医家治法.jsonl)，第 241 条）。

计算条目精确匹配 F1。

```python
import json

with open('医家治法.jsonl', encoding="utf-8") as f:
    sample = json.loads(f.readlines()[240])
assert sample["id"] == 'treatment_method_0883'
print(sample["病历文本"])

prediction = '补阴启阳, 水中求火'
gold = sample["answer"]
print("Prediction:", prediction)
print("Gold:", gold)

p = {x.strip() for x in prediction.split(",") if x.strip()}
g = {x.strip() for x in gold.split(",") if x.strip()}
score = 2 * len(p & g) / (len(p) + len(g)) if p or g else 1.0
print('F1', score)
```

### `syndrome`

真实样本：`syndrome_0883`（[医家辨证.jsonl](医家辨证.jsonl)，第 241 条）。

计算条目精确匹配 F1。

```python
import json

with open('医家辨证.jsonl', encoding="utf-8") as f:
    sample = json.loads(f.readlines()[240])
assert sample["id"] == 'syndrome_0883'
print(sample["病历文本"])

prediction = '阴阳两虚证'
gold = sample["answer"]
print("Prediction:", prediction)
print("Gold:", gold)

p = {x.strip() for x in prediction.split(",") if x.strip()}
g = {x.strip() for x in gold.split(",") if x.strip()}
score = 2 * len(p & g) / (len(p) + len(g)) if p or g else 1.0
print('F1', score)
```

使用 GitHub 评估器联合生成时，让模型在一个 JSON 中返回 `辨证`、`治法`、`处方`，分别对应 `syndrome`、`treatment_method`、`herbal_prescription`，再对各项分别评分。读取三个任务时，应按 ID 的四位病例编号关联，不能假定三份数据的行号始终对应。
