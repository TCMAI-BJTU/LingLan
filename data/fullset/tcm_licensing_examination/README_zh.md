# 中医执业资格考试：Full 评估结果

[English](README.md) · [返回数据说明](../../README_zh.md#论文评估结果)

以下仅展示本目录对应任务的 **Full** 成绩，覆盖论文中的 **19 个模型**。数值来自 [LingLanMiDian 论文 arXiv:2602.01779v1](https://arxiv.org/html/2602.01779v1)（2026-02-02）的表 2、表 3 和附录表 4；重复出现的对照模型合并为一行，模型名称沿用论文。

准确率、精确率、召回率和 F1 的单位为 %，数值越高越好。

## 对应数据文件

- `tcm_licensing_examination`: [中医考试题.jsonl](中医考试题.jsonl)

## 综合

| 模型 | 准确率 |
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

## 最小评估示例

每个子任务分别演示：读取一条样本、给出示例预测、打印标准答案并计算基础分数。示例均选自真实样本，`prediction` 使用该样本的完整标准答案演示回放，不是实际模型输出；使用时替换为你的模型答案。标准答案始终从 `sample["answer"]` 读取。

在当前任务目录运行，使用 Python 标准库即可。

分数范围为 0–1。以下是基础评分示例，不包含论文评估器的完整解析和匹配规则。

### `tcm_licensing_examination`

真实样本：`tcm_licensing_examination_0001`（[中医考试题.jsonl](中医考试题.jsonl)，第 1 条）。

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
