# 信息抽取：Full 评估结果

[English](README.md) · [返回数据说明](../../README_zh.md#论文评估结果)

以下仅展示本目录对应任务的 **Full** 成绩，覆盖论文中的 **19 个模型**。数值来自 [LingLan 论文 arXiv:2602.01779v1](https://arxiv.org/html/2602.01779v1)（2026-02-02）的表 2、表 3 和附录表 4；重复出现的对照模型合并为一行，模型名称沿用论文。

准确率、精确率、召回率和 F1 的单位为 %，数值越高越好。

## 对应数据文件

- `classical_text_entity_extraction`: [实体抽取_古籍.jsonl](实体抽取_古籍.jsonl)
- `clinical_record_entity_extraction`: [实体抽取_病历.jsonl](实体抽取_病历.jsonl)

## 临床病历

| 模型 | 精确率 | 召回率 | F1 |
| --- | ---: | ---: | ---: |
| DeepSeek-R1 | 66.6 | 61.3 | 63.1 |
| DeepSeek-V3.1 | 64.6 | 58.6 | 60.8 |
| GPT-5 | 72.8 | 71.9 | 71.7 |
| Qwen3-235B | 69.1 | 66.3 | 67.2 |
| Qwen3-32B | 73.3 | 62.2 | 66.7 |
| Baichuan-M2-32B | 61.8 | 56.0 | 58.1 |
| Qwen3-Next-80B | 38.1 | 33.5 | 35.2 |
| GPT-OSS-120B | 59.7 | 55.8 | 57.1 |
| Qwen3-30B-A3B | 69.3 | 48.4 | 56.2 |
| Qwen3-14B | 74.6 | 62.1 | 67.1 |
| Qwen3-8B | 67.7 | 57.6 | 61.5 |
| Qwen3-4B | 64.7 | 52.3 | 57.2 |
| gpt-5-mini | 52.1 | 57.0 | 54.0 |
| gpt-oss-20b | 55.3 | 51.6 | 52.8 |
| Baichuan2-13B-Chat | 27.0 | 25.0 | 25.1 |
| Lingdan-13B-TCPM | 1.2 | 0.8 | 0.8 |
| TCMChat | 0.0 | 0.0 | 0.0 |
| BianCang-7B | 25.5 | 15.0 | 16.8 |
| BianCang-14B | 38.1 | 26.1 | 29.5 |

## 古籍

| 模型 | 精确率 | 召回率 | F1 |
| --- | ---: | ---: | ---: |
| DeepSeek-R1 | 60.1 | 62.9 | 60.8 |
| DeepSeek-V3.1 | 61.4 | 64.4 | 62.1 |
| GPT-5 | 44.7 | 51.7 | 47.5 |
| Qwen3-235B | 57.3 | 62.6 | 59.1 |
| Qwen3-32B | 57.9 | 56.9 | 56.6 |
| Baichuan-M2-32B | 58.9 | 61.6 | 59.5 |
| Qwen3-Next-80B | 38.7 | 40.3 | 39.0 |
| GPT-OSS-120B | 51.1 | 56.6 | 53.0 |
| Qwen3-30B-A3B | 59.7 | 56.3 | 57.2 |
| Qwen3-14B | 59.8 | 56.3 | 57.3 |
| Qwen3-8B | 58.1 | 54.7 | 55.6 |
| Qwen3-4B | 54.5 | 49.2 | 51.0 |
| gpt-5-mini | 48.9 | 60.5 | 53.4 |
| gpt-oss-20b | 50.3 | 54.0 | 51.3 |
| Baichuan2-13B-Chat | 32.3 | 27.8 | 29.0 |
| Lingdan-13B-TCPM | 5.6 | 2.9 | 3.4 |
| TCMChat | 1.5 | 0.2 | 0.3 |
| BianCang-7B | 46.1 | 44.9 | 44.1 |
| BianCang-14B | 55.3 | 46.0 | 49.0 |

## 最小评估示例

每个子任务分别演示：读取一条样本、给出示例预测、打印标准答案并计算基础分数。示例均选自真实样本，`prediction` 使用该样本的完整标准答案演示回放，不是实际模型输出；使用时替换为你的模型答案。标准答案始终从 `sample["answer"]` 读取。

在当前任务目录运行，使用 Python 标准库即可。

分数范围为 0–1。以下是基础评分示例，不包含论文评估器的完整解析和匹配规则。

### `classical_text_entity_extraction`

真实样本：`classical_text_entity_extraction_1964`（[实体抽取_古籍.jsonl](实体抽取_古籍.jsonl)，第 1964 条）。

按实体类型和文本精确匹配，保留重复实体计数。

```python
import json

with open('实体抽取_古籍.jsonl', encoding="utf-8") as f:
    sample = json.loads(f.readlines()[1963])
assert sample["id"] == 'classical_text_entity_extraction_1964'
print(sample["text"])

prediction = {'病机': ['肝气肆横'],
 '阳性症状': ['腹痛'],
 '治则治法': ['疏泄'],
 '中药': ['青皮一钱 归须一钱 茺蔚子一钱 炒延胡一钱 郁金一钱 黑山栀一钱五分 南山楂一钱五分'],
 '中药剂量': ['青皮一钱', '归须一钱', '茺蔚子一钱', '炒延胡一钱', '郁金一钱', '黑山栀一钱五分', '南山楂一钱五分'],
 '中药名': ['青皮', '归须', '茺蔚子', '炒延胡', '郁金', '黑山栀', '南山楂']}
gold = sample["answer"]
print("Prediction:", prediction)
print("Gold:", gold)

from collections import Counter
p = Counter((k, x.strip()) for k, xs in prediction.items() for x in (xs or []))
g = Counter((k, x.strip()) for k, xs in gold.items() for x in (xs or []))
score = 2 * sum((p & g).values()) / (sum(p.values()) + sum(g.values())) if p or g else 1.0
print('Entity F1', score)
```

### `clinical_record_entity_extraction`

真实样本：`clinical_record_entity_extraction_1776`（[实体抽取_病历.jsonl](实体抽取_病历.jsonl)，第 1776 条）。

按实体类型和文本精确匹配，保留重复实体计数。

```python
import json

with open('实体抽取_病历.jsonl', encoding="utf-8") as f:
    sample = json.loads(f.readlines()[1775])
assert sample["id"] == 'clinical_record_entity_extraction_1776'
print(sample["text"])

prediction = {'其他检查': ['胃镜'],
 '西医疾病': ['CSG', '胃溃疡（A2）'],
 '阳性症状': ['胃胀', '胃痛', '头痛', '眼睛红', '头晕', '晨起口苦', '口苦', '胃疼', '头痛', '口苦', '胃胀'],
 '持续时间': ['5年'],
 '发作特征': ['时有', '晨起', '时有'],
 '阴性症状': ['纳可', '大便可'],
 '舌象': ['舌质淡红', '苔白', '舌质淡红', '苔白'],
 '脉象': ['脉弦实', '脉弦', '脉弦'],
 '就诊日期': ['11-06'],
 '变化情况': ['缓解', '消失']}
gold = sample["answer"]
print("Prediction:", prediction)
print("Gold:", gold)

from collections import Counter
p = Counter((k, x.strip()) for k, xs in prediction.items() for x in (xs or []))
g = Counter((k, x.strip()) for k, xs in gold.items() for x in (xs or []))
score = 2 * sum((p & g).values()) / (sum(p.values()) + sum(g.values())) if p or g else 1.0
print('Entity F1', score)
```
