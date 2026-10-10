<h2 align="center">
  <img width="600" src="./assets/linglan_logo_horizontal.svg" alt="灵兰标志" /><br />
  面向中医领域的大语言模型统一评估基准
</h2>

<p align="center">
  <a href="https://arxiv.org/abs/2602.01779"><b>论文</b></a>&nbsp;·&nbsp;
  <a href="data/README_zh.md"><b>数据集</b></a>&nbsp;·&nbsp;
  <a href="https://www.tcmnlp.com/"><b>排行榜</b></a>&nbsp;·&nbsp;
  <a href="README.md"><b>English</b></a>
</p>

## 简介

**LingLan** 是由专家整理构建的基准，用于评估大语言模型（LLM）在中医（TCM）五个领域的能力：执业资格考试、基础知识、中成药知识、信息抽取，以及诊断与治疗决策。最后一个领域同时包含诊疗推理（DTR）和单选形式的决策识别（DR）。

本版本提供 Full 和 Hard 评估集合，标准标签保存在 `answer` 字段中。样本数量见[数据统计](#数据统计)，字段结构与文件详情见[数据文档](data/README_zh.md)。

---

## 目录

- [什么是灵兰](#什么是灵兰)
- [数据统计](#数据统计)
- [评估指标](#评估指标)
- [下载](#下载)
- [快速开始](#快速开始)
- [排行榜](#排行榜)
- [引用 LingLan](#引用-linglan)
- [数据来源](#数据来源)
- [数据许可](#数据许可)
- [致谢](#致谢)

---

## 什么是灵兰

<p align="center">
  <img src="./assets/overview.png" alt="概览" style="max-width:100%; height:auto;">
</p>

LingLan 通过单选、多选、填空和结构化生成任务，评估事实知识、结构化信息抽取及临床决策能力。DTR 根据病例生成辨证、治法和处方结果；DR 则将相应的决策呈现为单选题。

六个数据目录按照用途对这些任务进行分组：四个知识或抽取任务组，以及 DTR 和 DR 两个临床任务组。它们对应上述五个领域的分类体系。

### DTR 的单独评估与联合评估

DTR 支持单独生成辨证、治法或处方，也支持一次生成三项结果。联合生成时按四位病例编号关联三个文件；现有 GitHub 评估入口采用联合流程。具体字段、入口名称和评分方式见[诊疗推理说明](data/README_zh.md#诊疗推理)。

---

## 数据统计

<p align="center">
  <img src="./assets/dataset_statistic.png" alt="数据集统计" style="max-width:70%; height:auto;">
</p>

| 任务组 | 基准任务数 | Full 样本数 | Hard 样本数 |
| --- | ---: | ---: | ---: |
| 中医执业资格考试 | 1 | 1,832 | 400 |
| 中医基础知识：单选、多选、填空 | 3 | 5,840 | 1,200 |
| 中成药知识：单选、多选、填空 | 3 | 5,948 | 1,200 |
| 信息抽取：古籍与病历 | 2 | 4,000 | 800 |
| 决策识别：辨证、治法、中药处方 | 3 | 6,000 | 1,200 |
| 诊疗推理：联合病例 | 1 | 2,000 | 400 |
| **总计** | **13** | **25,620** | **5,200** |

**文件层面的计数：**每套数据包含 15 个 JSONL 文件。将每个 DTR 病例拆分为三条标签记录后，**Full 共包含 29,620 行 JSONL 记录**，**Hard 共包含 6,000 行**，并未增加临床病例。剂量与处方标签一同存储。额外的字符 F1 评估模式使用同一批 DTR 病例，不会新增数据集。

**Hard 是 Full 的子集。**Hard 记录与其在 Full 中对应的记录具有相同的 ID、输入和答案；二者是相互重叠的评估集合，并非互不重叠的训练集与测试集。

逐文件数量见[数据清单](data/README_zh.md#文件与任务名称)。

---

## 评估指标

| 任务 | 报告的指标 |
| --- | --- |
| 单选与决策识别 | 准确率 |
| 多选 | 选项集合完全匹配准确率；选项级精确率、召回率和 F1 |
| 填空 | 字符级 F1 |
| 信息抽取 | 按实体类型计算实体提及的精确率、召回率和 F1，保留重复提及 |
| DTR 辨证、治法与处方 | 在所选临床标签匹配模式下计算精确率、召回率和 F1 |
| 处方剂量 | 匹配药物的平均绝对误差（MAE）；对齐剂量向量的余弦相似度，未匹配药物在缺失侧补零 |

有关当前检出版本所使用的评分规则，请参阅[评估实现](simple-evals/evals/tcm_evals/)。

---

## 下载

- [带标签的 Full 全量数据集](data/fullset/)
- [带标签的 Hard 子集](data/hardset/)
- [数据集结构、字段和答案格式](data/README_zh.md)

```bash
git clone https://github.com/TCMAI-BJTU/LingLan.git
cd LingLan
```

---

## 快速开始

请从仓库根目录运行命令。使用仓库附带的中医评估入口前，请安装其依赖：

```bash
python3 -m pip install openai anthropic pandas numpy jinja2 requests tqdm
```

请在运行环境和[模型注册配置](simple-evals/config_models.py)中配置模型端点及凭据。当前入口会在根据 `--model` 选择模型之前初始化已注册的采样器，因此服务提供商配置必须覆盖注册配置中保留的采样器。有关采样器设置及完整的评估名称列表，请参阅[评估指南](simple-evals/README.md)。

完成采样器配置后，可以先运行小规模评估，例如：

```bash
python3 -m simple-evals.simple_evals --model gpt-5 --eval tcm_licensing_examination --split fullset --examples 10
python3 -m simple-evals.simple_evals --model gpt-5 --eval clinical_record_entity_extraction --split hardset --examples 10
python3 -m simple-evals.simple_evals --model gpt-5 --eval diagnostic_therapeutic_reasoning --split hardset --examples 10
```

省略 `--examples` 即可评估所选集合的全部样本。`--split` 默认为 `fullset`；评估 LingLan-Hard 时请使用 `hardset`。报告保存至 `simple-evals/tmp/<split>/<evaluation>/<model>/`。

评估框架改编自 [OpenAI simple-evals](https://github.com/openai/simple-evals)。

---

## 排行榜

[完整的论文评估成绩（所有模型、各任务及 Full/Hard）](data/README_zh.md#论文评估结果)

### 简明排行榜

<p align="center">
  <img src="./assets/model_performance.png" alt="总体平均分" style="max-width:100%; height:auto;">
</p>

以下为 **Full** 和 **Hard** 上的总体平均分（%），采用本仓库记录的基线分数快照。各行按 Full 分数排序；Δ 为 Full 减去 Hard 的差值，单位为百分点。

| **排名** | **模型**          | **Full** | **Hard** | **Δ（百分点）** |
| -------- | ------------------ | -------- | -------- | ---------- |
| 1 | **DeepSeek-R1** | **51.1** | **31.9** | 19.2 |
| 2 | DeepSeek-V3.1 | 50.9 | 31.2 | 19.7 |
| 3 | Qwen3-235B-A22B | 50.6 | 30.8 | 19.8 |
| 4 | Qwen3-32B | 48.4 | 28.8 | 19.6 |
| 5 | GPT-5 | 48.1 | 28.0 | 20.1 |
| 6 | Qwen3-14B | 47.5 | 27.2 | 20.3 |
| 7 | Qwen3-30B-A3B | 47.2 | 26.7 | 20.5 |
| 8 | Baichuan-M2-32B | 47.1 | 26.2 | 20.9 |
| 9 | Qwen3-8B | 46.2 | 25.4 | 20.8 |
| 10 | Qwen3-Next-80B-A3B | 44.9 | 22.6 | 22.3 |
| 11 | GPT-5-mini | 43.9 | 23.3 | 20.6 |
| 12 | Qwen3-4B | 43.8 | 24.5 | 19.3 |
| 13 | GPT-OSS-120B | 40.7 | 23.1 | 17.6 |
| 14 | GPT-OSS-20B | 36.1 | 20.8 | 15.3 |

## 引用 LingLan

```bibtex
@misc{hua2026linglan,
      title={LingLan: A Unified Benchmark for Evaluating Large Language Models in Traditional Chinese Medicine},
      author={Rui Hua and Yu Wei and Zixin Shu and Kai Chang and Dengying Yan and Jianan Xia and Zeyu Liu and Hui Zhu and Shujie Song and Mingzhong Xiao and Xiaodong Li and Dongmei Jia and Zhuye Gao and Yanyan Meng and Naixuan Zhao and Yu Fu and Haibin Yu and Benman Yu and Yuanyuan Chen and Fei Dong and Zhizhou Meng and Pengcheng Yang and Songxue Zhao and Lijuan Pei and Yunhui Hu and Kan Ding and Jiayuan Duan and Wenmao Yin and Yang Gu and Runshun Zhang and Qiang Zhu and Jian Yu and Jiansheng Li and Baoyan Liu and Wenjia Wang and Xuezhong Zhou},
      year={2026},
      eprint={2602.01779},
      archivePrefix={arXiv},
      primaryClass={cs.AI},
      url={https://arxiv.org/abs/2602.01779},
}

```

---

## 数据来源

* 数据整理自去标识化的临床病历、古籍、官方考试来源及结构化知识资源。

---

## 数据许可

LingLan 数据集（`data/fullset/` 和 `data/hardset/` 中的输入数据及标准标签）采用 [知识共享署名 4.0 国际许可（CC BY 4.0）](https://creativecommons.org/licenses/by/4.0/deed.zh-hans)发布。许可全文见 [data/LICENSE](data/LICENSE)。

[许可范围与署名要求](data/README_zh.md#数据许可)。


---

## 致谢

感谢为数据集构建与核验作出贡献的数据整理人员、标注人员和领域专家。
