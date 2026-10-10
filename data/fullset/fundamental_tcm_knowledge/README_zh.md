# 中医基础知识：Full 评估结果

[English](README.md) · [返回数据说明](../../README_zh.md#论文评估结果)

以下仅展示本目录对应任务的 **Full** 成绩，覆盖论文中的 **19 个模型**。数值来自 [LingLanMiDian 论文 arXiv:2602.01779v1](https://arxiv.org/html/2602.01779v1)（2026-02-02）的表 2、表 3 和附录表 4；重复出现的对照模型合并为一行，模型名称沿用论文。

准确率、精确率、召回率和 F1 的单位为 %，数值越高越好。

## 对应数据文件

- `fundamental_tcm_knowledge_single_choice`: [知识图谱知识问答_单选题.jsonl](知识图谱知识问答_单选题.jsonl)
- `fundamental_tcm_knowledge_fill_blank`: [知识图谱知识问答_填空题.jsonl](知识图谱知识问答_填空题.jsonl)
- `fundamental_tcm_knowledge_multiple_choice`: [知识图谱知识问答_多选题.jsonl](知识图谱知识问答_多选题.jsonl)

## 单选

| 模型 | 准确率 |
| --- | ---: |
| DeepSeek-R1 | 86.1 |
| DeepSeek-V3.1 | 86.1 |
| GPT-5 | 85.4 |
| Qwen3-235B | 85.0 |
| Qwen3-32B | 86.1 |
| Baichuan-M2-32B | 83.4 |
| Qwen3-Next-80B | 82.1 |
| GPT-OSS-120B | 70.4 |
| Qwen3-30B-A3B | 82.6 |
| Qwen3-14B | 83.0 |
| Qwen3-8B | 80.8 |
| Qwen3-4B | 76.2 |
| gpt-5-mini | 77.0 |
| gpt-oss-20b | 65.4 |
| Baichuan2-13B-Chat | 60.6 |
| Lingdan-13B-TCPM | 48.4 |
| TCMChat | 11.1 |
| BianCang-7B | 78.2 |
| BianCang-14B | 82.6 |

## 多选

| 模型 | 准确率 | 精确率 | 召回率 | F1 |
| --- | ---: | ---: | ---: | ---: |
| DeepSeek-R1 | 64.8 | 92.5 | 92.1 | 91.0 |
| DeepSeek-V3.1 | 62.4 | 91.9 | 92.0 | 90.6 |
| GPT-5 | 53.9 | 90.6 | 87.2 | 87.3 |
| Qwen3-235B | 61.3 | 93.0 | 89.1 | 89.5 |
| Qwen3-32B | 56.3 | 90.3 | 90.9 | 89.1 |
| Baichuan-M2-32B | 48.6 | 90.5 | 84.5 | 85.3 |
| Qwen3-Next-80B | 52.6 | 89.4 | 84.7 | 84.7 |
| GPT-OSS-120B | 35.3 | 81.2 | 83.2 | 80.0 |
| Qwen3-30B-A3B | 52.0 | 89.8 | 88.3 | 87.4 |
| Qwen3-14B | 49.5 | 90.6 | 85.7 | 86.3 |
| Qwen3-8B | 47.8 | 88.4 | 86.8 | 85.8 |
| Qwen3-4B | 42.4 | 86.1 | 84.9 | 83.5 |
| gpt-5-mini | 46.2 | 86.1 | 86.8 | 84.8 |
| gpt-oss-20b | 24.8 | 76.1 | 74.9 | 72.9 |
| Baichuan2-13B-Chat | 23.4 | 71.8 | 84.4 | 75.9 |
| Lingdan-13B-TCPM | 14.3 | 53.6 | 56.5 | 52.4 |
| TCMChat | 0.6 | 58.9 | 36.3 | 39.9 |
| BianCang-7B | 36.9 | 78.9 | 78.4 | 76.2 |
| BianCang-14B | 23.7 | 65.2 | 53.1 | 55.8 |

## 填空

| 模型 | 字符 F1 |
| --- | ---: |
| DeepSeek-R1 | 58.2 |
| DeepSeek-V3.1 | 58.8 |
| GPT-5 | 54.9 |
| Qwen3-235B | 59.9 |
| Qwen3-32B | 56.1 |
| Baichuan-M2-32B | 50.2 |
| Qwen3-Next-80B | 56.0 |
| GPT-OSS-120B | 42.1 |
| Qwen3-30B-A3B | 53.9 |
| Qwen3-14B | 54.1 |
| Qwen3-8B | 51.1 |
| Qwen3-4B | 49.0 |
| gpt-5-mini | 49.2 |
| gpt-oss-20b | 35.9 |
| Baichuan2-13B-Chat | 33.2 |
| Lingdan-13B-TCPM | 8.5 |
| TCMChat | 13.9 |
| BianCang-7B | 35.4 |
| BianCang-14B | 38.7 |

## 最小评估示例

每个子任务分别演示：读取一条样本、给出示例预测、打印标准答案并计算基础分数。示例均选自真实样本，`prediction` 使用该样本的完整标准答案演示回放，不是实际模型输出；使用时替换为你的模型答案。标准答案始终从 `sample["answer"]` 读取。

在当前任务目录运行，使用 Python 标准库即可。

分数范围为 0–1。以下是基础评分示例，不包含论文评估器的完整解析和匹配规则。

### `fundamental_tcm_knowledge_single_choice`

真实样本：`fundamental_tcm_knowledge_single_choice_0001`（[知识图谱知识问答_单选题.jsonl](知识图谱知识问答_单选题.jsonl)，第 1 条）。

```python
import json

with open('知识图谱知识问答_单选题.jsonl', encoding="utf-8") as f:
    sample = json.loads(f.readlines()[0])
assert sample["id"] == 'fundamental_tcm_knowledge_single_choice_0001'
print(sample["question"], sample.get("options", []))

prediction = 'C'
gold = sample["answer"]
print("Prediction:", prediction)
print("Gold:", gold)

score = int(prediction == gold)
print('Accuracy', score)
```

### `fundamental_tcm_knowledge_fill_blank`

真实样本：`fundamental_tcm_knowledge_fill_blank_0555`（[知识图谱知识问答_填空题.jsonl](知识图谱知识问答_填空题.jsonl)，第 555 条）。

预测使用答案列表，标准答案使用顿号分隔；计算字符集合 F1。

```python
import json

with open('知识图谱知识问答_填空题.jsonl', encoding="utf-8") as f:
    sample = json.loads(f.readlines()[554])
assert sample["id"] == 'fundamental_tcm_knowledge_fill_blank_0555'
print(sample["question"], sample.get("options", []))

prediction = ['养阴', '止汗']
gold = sample["answer"]
print("Prediction:", prediction)
print("Gold:", gold)

p = set("".join(prediction))
g = set("".join(x.strip() for x in gold.split("、")))
score = 2 * len(p & g) / (len(p) + len(g)) if p or g else 1.0
print('Character F1', score)
```

### `fundamental_tcm_knowledge_multiple_choice`

真实样本：`fundamental_tcm_knowledge_multiple_choice_0001`（[知识图谱知识问答_多选题.jsonl](知识图谱知识问答_多选题.jsonl)，第 1 条）。

按选项集合完全匹配评分。

```python
import json

with open('知识图谱知识问答_多选题.jsonl', encoding="utf-8") as f:
    sample = json.loads(f.readlines()[0])
assert sample["id"] == 'fundamental_tcm_knowledge_multiple_choice_0001'
print(sample["question"], sample.get("options", []))

prediction = ['A', 'C', 'E']
gold = sample["answer"]
print("Prediction:", prediction)
print("Gold:", gold)

score = int(set(prediction) == set(gold))
print('Accuracy', score)
```
