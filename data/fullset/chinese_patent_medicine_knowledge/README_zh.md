# 中成药知识：Full 评估结果

[English](README.md) · [返回数据说明](../../README_zh.md#论文评估结果)

以下仅展示本目录对应任务的 **Full** 成绩，覆盖论文中的 **19 个模型**。数值来自 [LingLanMiDian 论文 arXiv:2602.01779v1](https://arxiv.org/html/2602.01779v1)（2026-02-02）的表 2、表 3 和附录表 4；重复出现的对照模型合并为一行，模型名称沿用论文。

准确率、精确率、召回率和 F1 的单位为 %，数值越高越好。

## 对应数据文件

- `chinese_patent_medicine_knowledge_single_choice`: [中成药知识问答_单选题.jsonl](中成药知识问答_单选题.jsonl)
- `chinese_patent_medicine_knowledge_fill_blank`: [中成药知识问答_填空题.jsonl](中成药知识问答_填空题.jsonl)
- `chinese_patent_medicine_knowledge_multiple_choice`: [中成药知识问答_多选题.jsonl](中成药知识问答_多选题.jsonl)

## 单选

| 模型 | 准确率 |
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

## 多选

| 模型 | 准确率 | 精确率 | 召回率 | F1 |
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

## 填空

| 模型 | 字符 F1 |
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

真实样本：`chinese_patent_medicine_knowledge_fill_blank_0084`（[中成药知识问答_填空题.jsonl](中成药知识问答_填空题.jsonl)，第 84 条）。

预测使用答案列表，标准答案使用顿号分隔；计算字符集合 F1。

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

真实样本：`chinese_patent_medicine_knowledge_multiple_choice_0001`（[中成药知识问答_多选题.jsonl](中成药知识问答_多选题.jsonl)，第 1 条）。

按选项集合完全匹配评分。

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
