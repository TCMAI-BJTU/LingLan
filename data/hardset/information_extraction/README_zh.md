# 信息抽取：Hard 评估结果

[English](README.md) · [返回数据说明](../../README_zh.md#论文评估结果)

以下仅展示本目录对应任务的 **Hard** 成绩，覆盖论文中的 **19 个模型**。数值来自 [LingLanMedBench 论文 arXiv:2602.01779](https://arxiv.org/html/2602.01779)的表 1、表 2 和补充表 S1；重复出现的对照模型合并为一行，模型名称沿用论文。

准确率、精确率、召回率和 F1 的单位为 %，数值越高越好。

## 对应数据文件

- `classical_text_entity_extraction`: [实体抽取_古籍.jsonl](实体抽取_古籍.jsonl)
- `clinical_record_entity_extraction`: [实体抽取_病历.jsonl](实体抽取_病历.jsonl)

## 临床病历

| 模型 | 精确率 | 召回率 | F1 |
| --- | ---: | ---: | ---: |
| DeepSeek-R1 | 46.7 | 43.9 | 44.2 |
| DeepSeek-V3.1 | 46.7 | 42.4 | 43.4 |
| GPT-5 | 56.2 | 56.0 | 55.1 |
| Qwen3-235B | 50.5 | 49.3 | 49.1 |
| Qwen3-32B | 61.3 | 49.8 | 54.2 |
| Baichuan-M2-32B | 45.5 | 41.9 | 42.6 |
| Qwen3-Next-80B | 17.3 | 15.0 | 15.5 |
| GPT-OSS-120B | 41.4 | 41.9 | 40.6 |
| Qwen3-30B-A3B | 57.2 | 37.9 | 44.6 |
| Qwen3-14B | 62.8 | 52.0 | 55.7 |
| Qwen3-8B | 55.1 | 45.1 | 48.6 |
| Qwen3-4B | 52.7 | 41.3 | 45.4 |
| gpt-5-mini | 35.2 | 43.6 | 38.3 |
| gpt-oss-20b | 39.5 | 38.5 | 38.0 |
| Baichuan2-13B-Chat | 25.0 | 22.6 | 22.7 |
| Lingdan-13B-TCPM | 1.1 | 0.9 | 0.8 |
| TCMChat | 0.1 | 0.0 | 0.0 |
| BianCang-7B | 21.7 | 11.5 | 12.9 |
| BianCang-14B | 33.2 | 21.5 | 24.8 |

## 古籍

| 模型 | 精确率 | 召回率 | F1 |
| --- | ---: | ---: | ---: |
| DeepSeek-R1 | 40.2 | 44.7 | 41.5 |
| DeepSeek-V3.1 | 42.8 | 48.8 | 44.7 |
| GPT-5 | 11.4 | 16.3 | 13.1 |
| Qwen3-235B | 37.9 | 45.9 | 40.4 |
| Qwen3-32B | 38.1 | 37.9 | 36.9 |
| Baichuan-M2-32B | 38.0 | 42.6 | 39.2 |
| Qwen3-Next-80B | 13.8 | 14.9 | 13.8 |
| GPT-OSS-120B | 31.0 | 38.5 | 33.5 |
| Qwen3-30B-A3B | 38.9 | 37.3 | 37.0 |
| Qwen3-14B | 39.6 | 38.3 | 38.0 |
| Qwen3-8B | 35.4 | 34.4 | 34.0 |
| Qwen3-4B | 35.0 | 32.0 | 32.4 |
| gpt-5-mini | 23.9 | 35.6 | 28.0 |
| gpt-oss-20b | 26.6 | 31.8 | 28.1 |
| Baichuan2-13B-Chat | 21.5 | 18.1 | 18.7 |
| Lingdan-13B-TCPM | 2.8 | 1.5 | 1.7 |
| TCMChat | 1.8 | 0.2 | 0.4 |
| BianCang-7B | 25.2 | 26.9 | 24.5 |
| BianCang-14B | 39.0 | 32.4 | 34.0 |

## 最小评估示例

每个子任务分别演示：读取一条样本、给出示例预测、打印标准答案并计算基础分数。示例均选自真实样本，`prediction` 使用该样本的完整标准答案演示回放，不是实际模型输出；使用时替换为你的模型答案。标准答案始终从 `sample["answer"]` 读取。

在当前任务目录运行，使用 Python 标准库即可。

分数范围为 0–1。以下是基础评分示例，不包含论文评估器的完整解析和匹配规则。

### `classical_text_entity_extraction`

真实样本：`classical_text_entity_extraction_1733`（[实体抽取_古籍.jsonl](实体抽取_古籍.jsonl)，第 362 条）。

按实体类型和文本精确匹配，保留重复实体计数。

```python
import json

with open('实体抽取_古籍.jsonl', encoding="utf-8") as f:
    sample = json.loads(f.readlines()[361])
assert sample["id"] == 'classical_text_entity_extraction_1733'
print(sample["text"])

prediction = {'中药': ['天门冬', '贝母', '地黄'],
 '药味': ['味苦', '微甘', '味厚'],
 '药性': ['气大寒', '沉', '阴'],
 '归经': ['入肺、肾两经'],
 '功效': ['除虚劳内热', '定热喘', '下去热淋', '苦杀三虫', '润滋骨髓', '解渴', '除烦', '消痰', '止嗽', '降火', '保肺', '退热', '滋阴'],
 '主治': ['血热燥结'],
 '禁忌': ['虚寒假热', '脾肾溏泄'],
 '中药七情关系': ['使']}
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

真实样本：`clinical_record_entity_extraction_1798`（[实体抽取_病历.jsonl](实体抽取_病历.jsonl)，第 40 条）。

按实体类型和文本精确匹配，保留重复实体计数。

```python
import json

with open('实体抽取_病历.jsonl', encoding="utf-8") as f:
    sample = json.loads(f.readlines()[39])
assert sample["id"] == 'clinical_record_entity_extraction_1798'
print(sample["text"])

prediction = {'变化情况': ['眩晕及头部昏沉感减轻', '未再出现胸闷气短', '饮食控制较前好'],
 '阳性症状': ['偶有咳痰'],
 '阴性症状': ['睡眠可', '二便调'],
 '舌脉': ['舌暗红', '苔薄黄腻', '脉弦滑'],
 '阴性体征': ['BP120/70mmHg',
          '神志清',
          '言语清晰流利',
          '高级智能水平正常',
          '双侧瞳孔等大等圆',
          '光反射灵敏',
          '眼动各向正常',
          '无眼震及复视',
          '口舌居中',
          '软腭弓动度好',
          '悬雍垂居中',
          '双侧咽反射灵敏',
          '四肢肌力5级',
          '肌张力可',
          '腱反射（++）',
          '双侧巴氏征（-）']}
gold = sample["answer"]
print("Prediction:", prediction)
print("Gold:", gold)

from collections import Counter
p = Counter((k, x.strip()) for k, xs in prediction.items() for x in (xs or []))
g = Counter((k, x.strip()) for k, xs in gold.items() for x in (xs or []))
score = 2 * sum((p & g).values()) / (sum(p.values()) + sum(g.values())) if p or g else 1.0
print('Entity F1', score)
```
