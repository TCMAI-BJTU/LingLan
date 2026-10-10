# 中成药知识：Hard 评估结果

[English](README.md) · [返回数据说明](../../README_zh.md#论文评估结果)

以下仅展示本目录对应任务的 **Hard** 成绩，覆盖论文中的 **19 个模型**。数值来自 [LingLanMiDian 论文 arXiv:2602.01779v1](https://arxiv.org/html/2602.01779v1)（2026-02-02）的表 2、表 3 和附录表 4；重复出现的对照模型合并为一行，模型名称沿用论文。

准确率、精确率、召回率和 F1 的单位为 %，数值越高越好。

## 对应数据文件

- `chinese_patent_medicine_knowledge_single_choice`: [中成药知识问答_单选题.jsonl](中成药知识问答_单选题.jsonl)
- `chinese_patent_medicine_knowledge_fill_blank`: [中成药知识问答_填空题.jsonl](中成药知识问答_填空题.jsonl)
- `chinese_patent_medicine_knowledge_multiple_choice`: [中成药知识问答_多选题.jsonl](中成药知识问答_多选题.jsonl)

## 单选

| 模型 | 准确率 |
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

## 多选

| 模型 | 准确率 | 精确率 | 召回率 | F1 |
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

## 填空

| 模型 | 字符 F1 |
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

## 最小评估示例

每个子任务分别演示：读取一条样本、给出示例预测、打印标准答案并计算基础分数。示例均选自真实样本，`prediction` 使用该样本的完整标准答案演示回放，不是实际模型输出；使用时替换为你的模型答案。标准答案始终从 `sample["answer"]` 读取。

在当前任务目录运行，使用 Python 标准库即可。

分数范围为 0–1。以下是基础评分示例，不包含论文评估器的完整解析和匹配规则。

### `chinese_patent_medicine_knowledge_single_choice`

真实样本：`chinese_patent_medicine_knowledge_single_choice_0001`（[中成药知识问答_单选题.jsonl](中成药知识问答_单选题.jsonl)，第 1 条）。

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

真实样本：`chinese_patent_medicine_knowledge_fill_blank_1968`（[中成药知识问答_填空题.jsonl](中成药知识问答_填空题.jsonl)，第 197 条）。

预测使用答案列表，标准答案使用顿号分隔；计算字符集合 F1。

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

真实样本：`chinese_patent_medicine_knowledge_multiple_choice_1166`（[中成药知识问答_多选题.jsonl](中成药知识问答_多选题.jsonl)，第 1 条）。

按选项集合完全匹配评分。

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
