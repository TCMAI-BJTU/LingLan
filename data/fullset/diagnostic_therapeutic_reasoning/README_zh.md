# 诊疗推理：Full 评估结果

[English](README.md) · [返回数据说明](../../README_zh.md#论文评估结果)

以下仅展示本目录对应任务的 **Full** 成绩，覆盖论文中的 **19 个模型**。数值来自 [LingLanMedBench 论文 arXiv:2602.01779](https://arxiv.org/html/2602.01779)的表 1、表 2 和补充表 S1；重复出现的对照模型合并为一行，模型名称沿用论文。

准确率、精确率、召回率和 F1 的单位为 %，数值越高越好。

## 对应数据文件

- `herbal_prescription`: [医家处方.jsonl](医家处方.jsonl)
- `treatment_method`: [医家治法.jsonl](医家治法.jsonl)
- `syndrome`: [医家辨证.jsonl](医家辨证.jsonl)

论文成绩采用一次生成辨证、治法和处方的联合流程，不代表单独生成实验。下表分别报告包含关系匹配和字符 F1 匹配的成绩。表中的余弦相似度已乘以 100，越高越好；平均绝对误差单位为克，越低越好。论文指出，接近零的平均绝对误差可能源于药名匹配失败，不能视为剂量预测完全准确。

## 辨证 — 包含关系匹配

| 模型 | 精确率 | 召回率 | F1 |
| --- | ---: | ---: | ---: |
| DeepSeek-R1 | 9.9 | 13.3 | 10.9 |
| DeepSeek-V3.1 | 11.0 | 14.3 | 11.9 |
| GPT-5 | 5.0 | 8.4 | 6.0 |
| Qwen3-235B | 9.0 | 13.4 | 10.4 |
| Qwen3-32B | 7.7 | 11.2 | 8.8 |
| Baichuan-M2-32B | 9.1 | 12.6 | 10.1 |
| Qwen3-Next-80B | 10.7 | 12.6 | 11.0 |
| GPT-OSS-120B | 3.2 | 4.5 | 3.6 |
| Qwen3-30B-A3B | 8.4 | 12.9 | 9.8 |
| Qwen3-14B | 7.6 | 11.3 | 8.8 |
| Qwen3-8B | 7.5 | 9.9 | 8.2 |
| Qwen3-4B | 6.9 | 9.8 | 7.8 |
| gpt-5-mini | 3.4 | 5.6 | 4.1 |
| gpt-oss-20b | 3.3 | 5.4 | 3.9 |
| Baichuan2-13B-Chat | 4.0 | 5.2 | 4.3 |
| Lingdan-13B-TCPM | 1.0 | 0.6 | 0.7 |
| TCMChat | 0.7 | 0.8 | 0.7 |
| BianCang-7B | 5.8 | 4.7 | 4.9 |
| BianCang-14B | 9.4 | 6.5 | 7.3 |

## 治法 — 包含关系匹配

| 模型 | 精确率 | 召回率 | F1 |
| --- | ---: | ---: | ---: |
| DeepSeek-R1 | 14.2 | 17.0 | 14.8 |
| DeepSeek-V3.1 | 14.3 | 16.4 | 14.7 |
| GPT-5 | 10.5 | 19.2 | 13.1 |
| Qwen3-235B | 12.9 | 15.6 | 13.6 |
| Qwen3-32B | 11.5 | 14.4 | 12.3 |
| Baichuan-M2-32B | 11.7 | 15.0 | 12.6 |
| Qwen3-Next-80B | 13.6 | 14.5 | 13.5 |
| GPT-OSS-120B | 9.6 | 11.2 | 9.9 |
| Qwen3-30B-A3B | 13.0 | 15.4 | 13.6 |
| Qwen3-14B | 11.0 | 14.3 | 12.0 |
| Qwen3-8B | 12.0 | 14.7 | 12.8 |
| Qwen3-4B | 11.6 | 14.4 | 12.4 |
| gpt-5-mini | 13.4 | 15.7 | 12.9 |
| gpt-oss-20b | 6.5 | 7.8 | 6.7 |
| Baichuan2-13B-Chat | 7.9 | 7.6 | 7.4 |
| Lingdan-13B-TCPM | 1.3 | 0.9 | 1.0 |
| TCMChat | 3.6 | 2.6 | 2.8 |
| BianCang-7B | 9.0 | 6.3 | 7.1 |
| BianCang-14B | 12.4 | 7.8 | 9.1 |

## 处方 — 包含关系匹配

| 模型 | 精确率 | 召回率 | F1 |
| --- | ---: | ---: | ---: |
| DeepSeek-R1 | 35.7 | 30.6 | 32.3 |
| DeepSeek-V3.1 | 36.9 | 29.6 | 32.1 |
| GPT-5 | 27.6 | 39.3 | 31.9 |
| Qwen3-235B | 33.4 | 33.5 | 32.7 |
| Qwen3-32B | 31.0 | 29.3 | 29.5 |
| Baichuan-M2-32B | 32.1 | 29.4 | 30.0 |
| Qwen3-Next-80B | 32.4 | 29.9 | 30.4 |
| GPT-OSS-120B | 30.2 | 22.9 | 25.4 |
| Qwen3-30B-A3B | 32.4 | 26.0 | 28.3 |
| Qwen3-14B | 31.1 | 29.6 | 29.8 |
| Qwen3-8B | 31.7 | 26.4 | 28.2 |
| Qwen3-4B | 30.4 | 25.0 | 26.8 |
| gpt-5-mini | 27.6 | 30.8 | 28.5 |
| gpt-oss-20b | 24.8 | 21.2 | 22.2 |
| Baichuan2-13B-Chat | 15.8 | 12.7 | 13.6 |
| Lingdan-13B-TCPM | 0.3 | 0.2 | 0.2 |
| TCMChat | 0.0 | 0.0 | 0.0 |
| BianCang-7B | 15.0 | 15.4 | 14.4 |
| BianCang-14B | 8.8 | 8.3 | 8.2 |

## 剂量 — 包含关系匹配

| 模型 | 平均绝对误差（克） | 余弦相似度 × 100 |
| --- | ---: | ---: |
| DeepSeek-R1 | 4.1 | 30.9 |
| DeepSeek-V3.1 | 4.2 | 31.0 |
| GPT-5 | 4.5 | 31.4 |
| Qwen3-235B | 4.2 | 31.2 |
| Qwen3-32B | 4.4 | 29.0 |
| Baichuan-M2-32B | 4.2 | 28.7 |
| Qwen3-Next-80B | 4.0 | 29.1 |
| GPT-OSS-120B | 4.4 | 23.3 |
| Qwen3-30B-A3B | 4.4 | 28.1 |
| Qwen3-14B | 4.2 | 28.6 |
| Qwen3-8B | 4.3 | 27.2 |
| Qwen3-4B | 4.1 | 26.3 |
| gpt-5-mini | 5.3 | 27.9 |
| gpt-oss-20b | 4.5 | 20.0 |
| Baichuan2-13B-Chat | 2.3 | 12.9 |
| Lingdan-13B-TCPM | 0.1 | 0.2 |
| TCMChat | 0.0 | 0.0 |
| BianCang-7B | 2.5 | 13.5 |
| BianCang-14B | 1.4 | 7.5 |

## 辨证 — 字符 F1 匹配

| 模型 | 精确率 | 召回率 | F1 |
| --- | ---: | ---: | ---: |
| DeepSeek-R1 | 20.4 | 26.6 | 22.0 |
| DeepSeek-V3.1 | 21.5 | 27.1 | 22.9 |
| GPT-5 | 12.1 | 20.1 | 14.6 |
| Qwen3-235B | 19.0 | 27.4 | 21.6 |
| Qwen3-32B | 16.5 | 23.8 | 18.7 |
| Baichuan-M2-32B | 18.1 | 24.8 | 20.0 |
| Qwen3-Next-80B | 20.9 | 24.1 | 21.3 |
| GPT-OSS-120B | 10.6 | 14.9 | 11.9 |
| Qwen3-30B-A3B | 17.3 | 26.5 | 20.1 |
| Qwen3-14B | 16.5 | 24.1 | 18.8 |
| Qwen3-8B | 17.4 | 22.5 | 18.8 |
| Qwen3-4B | 15.5 | 21.9 | 17.5 |
| gpt-5-mini | 10.1 | 16.0 | 11.9 |
| gpt-oss-20b | 7.7 | 11.9 | 8.8 |
| Baichuan2-13B-Chat | 8.8 | 10.9 | 9.4 |
| Lingdan-13B-TCPM | 1.6 | 1.1 | 1.2 |
| TCMChat | 0.8 | 0.9 | 0.8 |
| BianCang-7B | 12.8 | 10.0 | 10.6 |
| BianCang-14B | 19.9 | 13.7 | 15.4 |

## 治法 — 字符 F1 匹配

| 模型 | 精确率 | 召回率 | F1 |
| --- | ---: | ---: | ---: |
| DeepSeek-R1 | 21.0 | 25.2 | 22.1 |
| DeepSeek-V3.1 | 21.7 | 24.9 | 22.5 |
| GPT-5 | 15.0 | 28.1 | 18.9 |
| Qwen3-235B | 19.8 | 24.1 | 21.0 |
| Qwen3-32B | 18.0 | 23.0 | 19.5 |
| Baichuan-M2-32B | 18.0 | 23.3 | 19.6 |
| Qwen3-Next-80B | 21.1 | 22.5 | 21.1 |
| GPT-OSS-120B | 14.6 | 17.7 | 15.3 |
| Qwen3-30B-A3B | 20.1 | 23.9 | 21.1 |
| Qwen3-14B | 16.8 | 22.4 | 18.6 |
| Qwen3-8B | 18.8 | 23.4 | 20.2 |
| Qwen3-4B | 17.4 | 21.8 | 18.8 |
| gpt-5-mini | 17.2 | 22.6 | 17.4 |
| gpt-oss-20b | 10.3 | 13.4 | 11.1 |
| Baichuan2-13B-Chat | 11.6 | 11.2 | 10.9 |
| Lingdan-13B-TCPM | 1.5 | 1.0 | 1.1 |
| TCMChat | 4.1 | 2.9 | 3.1 |
| BianCang-7B | 14.2 | 9.8 | 11.0 |
| BianCang-14B | 19.4 | 12.3 | 14.3 |

## 处方 — 字符 F1 匹配

| 模型 | 精确率 | 召回率 | F1 |
| --- | ---: | ---: | ---: |
| DeepSeek-R1 | 35.6 | 31.0 | 32.4 |
| DeepSeek-V3.1 | 37.0 | 29.6 | 32.2 |
| GPT-5 | 27.7 | 39.7 | 32.0 |
| Qwen3-235B | 33.4 | 33.6 | 32.7 |
| Qwen3-32B | 30.9 | 29.6 | 29.6 |
| Baichuan-M2-32B | 31.6 | 30.2 | 30.2 |
| Qwen3-Next-80B | 33.5 | 30.8 | 31.2 |
| GPT-OSS-120B | 30.1 | 23.0 | 25.5 |
| Qwen3-30B-A3B | 32.4 | 26.0 | 28.3 |
| Qwen3-14B | 30.9 | 29.9 | 29.8 |
| Qwen3-8B | 31.7 | 26.5 | 28.3 |
| Qwen3-4B | 30.4 | 25.1 | 26.9 |
| gpt-5-mini | 27.7 | 31.1 | 28.7 |
| gpt-oss-20b | 25.4 | 21.9 | 22.9 |
| Baichuan2-13B-Chat | 20.1 | 14.5 | 15.6 |
| Lingdan-13B-TCPM | 1.9 | 1.5 | 1.6 |
| TCMChat | 2.0 | 1.1 | 1.3 |
| BianCang-7B | 17.5 | 18.3 | 16.8 |
| BianCang-14B | 23.6 | 23.2 | 22.4 |

## 剂量 — 字符 F1 匹配

| 模型 | 平均绝对误差（克） | 余弦相似度 × 100 |
| --- | ---: | ---: |
| DeepSeek-R1 | 4.1 | 31.2 |
| DeepSeek-V3.1 | 4.2 | 31.1 |
| GPT-5 | 4.5 | 31.7 |
| Qwen3-235B | 4.2 | 31.3 |
| Qwen3-32B | 4.4 | 29.2 |
| Baichuan-M2-32B | 4.2 | 29.0 |
| Qwen3-Next-80B | 4.0 | 29.7 |
| GPT-OSS-120B | 4.4 | 23.5 |
| Qwen3-30B-A3B | 4.4 | 28.2 |
| Qwen3-14B | 4.2 | 28.7 |
| Qwen3-8B | 4.3 | 27.4 |
| Qwen3-4B | 4.1 | 26.3 |
| gpt-5-mini | 5.3 | 28.1 |
| gpt-oss-20b | 4.6 | 20.8 |
| Baichuan2-13B-Chat | 2.7 | 14.8 |
| Lingdan-13B-TCPM | 0.4 | 1.4 |
| TCMChat | 0.0 | 0.1 |
| BianCang-7B | 3.0 | 15.9 |
| BianCang-14B | 3.8 | 20.9 |

## 最小评估示例

每个子任务分别演示：读取一条样本、给出示例预测、打印标准答案并计算基础分数。示例均选自真实样本，`prediction` 使用该样本的完整标准答案演示回放，不是实际模型输出；使用时替换为你的模型答案。标准答案始终从 `sample["answer"]` 读取。

在当前任务目录运行，使用 Python 标准库即可。

分数范围为 0–1。以下是基础评分示例，不包含论文评估器的完整解析和匹配规则。

### `herbal_prescription`

真实样本：`herbal_prescription_0919`（[医家处方.jsonl](医家处方.jsonl)，第 919 条）。

只计算药名 F1，示例不计算剂量。

```python
import json

with open('医家处方.jsonl', encoding="utf-8") as f:
    sample = json.loads(f.readlines()[918])
assert sample["id"] == 'herbal_prescription_0919'
print(sample["病历文本"])

prediction = '红参: 10g, 制附子: 10g, 炙甘草: 10g, 炮姜: 7g, 焦白术: 10g'
gold = sample["answer"]
print("Prediction:", prediction)
print("Gold:", gold)

p = {x.split(":")[0].strip() for x in prediction.split(",") if x.strip()}
g = {x.split(":")[0].strip() for x in gold.split(",") if x.strip()}
score = 2 * len(p & g) / (len(p) + len(g)) if p or g else 1.0
print('F1', score)
```

### `treatment_method`

真实样本：`treatment_method_0919`（[医家治法.jsonl](医家治法.jsonl)，第 919 条）。

计算条目精确匹配 F1。

```python
import json

with open('医家治法.jsonl', encoding="utf-8") as f:
    sample = json.loads(f.readlines()[918])
assert sample["id"] == 'treatment_method_0919'
print(sample["病历文本"])

prediction = '温肾阳, 通心阳'
gold = sample["answer"]
print("Prediction:", prediction)
print("Gold:", gold)

p = {x.strip() for x in prediction.split(",") if x.strip()}
g = {x.strip() for x in gold.split(",") if x.strip()}
score = 2 * len(p & g) / (len(p) + len(g)) if p or g else 1.0
print('F1', score)
```

### `syndrome`

真实样本：`syndrome_0919`（[医家辨证.jsonl](医家辨证.jsonl)，第 919 条）。

计算条目精确匹配 F1。

```python
import json

with open('医家辨证.jsonl', encoding="utf-8") as f:
    sample = json.loads(f.readlines()[918])
assert sample["id"] == 'syndrome_0919'
print(sample["病历文本"])

prediction = '心肾阳虚证'
gold = sample["answer"]
print("Prediction:", prediction)
print("Gold:", gold)

p = {x.strip() for x in prediction.split(",") if x.strip()}
g = {x.strip() for x in gold.split(",") if x.strip()}
score = 2 * len(p & g) / (len(p) + len(g)) if p or g else 1.0
print('F1', score)
```

使用 GitHub 评估器联合生成时，让模型在一个 JSON 中返回 `辨证`、`治法`、`处方`，分别对应 `syndrome`、`treatment_method`、`herbal_prescription`，再对各项分别评分。读取三个任务时，应按 ID 的四位病例编号关联，不能假定三份数据的行号始终对应。
