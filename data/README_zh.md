# LingLan 数据集

[English](README.md)

本目录包含已发布的 LingLan 输入数据和标准标签，采用 UTF-8 编码的 JSON Lines 格式，每行一个 JSON 对象。每条记录均包含 `id`、`task` 和 `answer`。

- [`fullset/`](fullset/)：完整的评估数据集合。
- [`hardset/`](hardset/)：对应的 Hard 子集。
- [基准概览与引用](../README_zh.md)
- [评估命令与模式](../simple-evals/README.md)

## 目录结构

两套数据采用相同的目录和文件结构：

```text
data/
├── README.md
├── fullset/
│   ├── tcm_licensing_examination/
│   ├── fundamental_tcm_knowledge/
│   ├── chinese_patent_medicine_knowledge/
│   ├── information_extraction/
│   ├── decision_recognition/
│   └── diagnostic_therapeutic_reasoning/
└── hardset/
    ├── tcm_licensing_examination/
    ├── fundamental_tcm_knowledge/
    ├── chinese_patent_medicine_knowledge/
    ├── information_extraction/
    ├── decision_recognition/
    └── diagnostic_therapeutic_reasoning/
```

这六个目录对应五个基准领域，其中诊断与治疗决策领域由 `decision_recognition` 和 `diagnostic_therapeutic_reasoning` 两个目录共同表示。

## 文件与任务名称

以下路径均相对于 `fullset/` 或 `hardset/`。文件链接指向 Full；Hard 下存在相同的相对路径。`task` 列给出了每条记录中实际存储的精确值。

| 文件 | `task` | Full 行数 | Hard 行数 |
| --- | --- | ---: | ---: |
| [tcm_licensing_examination/中医考试题.jsonl](fullset/tcm_licensing_examination/中医考试题.jsonl) | `tcm_licensing_examination` | 1,832 | 400 |
| [fundamental_tcm_knowledge/知识图谱知识问答_单选题.jsonl](fullset/fundamental_tcm_knowledge/知识图谱知识问答_单选题.jsonl) | `fundamental_tcm_knowledge_single_choice` | 1,962 | 400 |
| [fundamental_tcm_knowledge/知识图谱知识问答_多选题.jsonl](fullset/fundamental_tcm_knowledge/知识图谱知识问答_多选题.jsonl) | `fundamental_tcm_knowledge_multiple_choice` | 1,919 | 400 |
| [fundamental_tcm_knowledge/知识图谱知识问答_填空题.jsonl](fullset/fundamental_tcm_knowledge/知识图谱知识问答_填空题.jsonl) | `fundamental_tcm_knowledge_fill_blank` | 1,959 | 400 |
| [chinese_patent_medicine_knowledge/中成药知识问答_单选题.jsonl](fullset/chinese_patent_medicine_knowledge/中成药知识问答_单选题.jsonl) | `chinese_patent_medicine_knowledge_single_choice` | 1,998 | 400 |
| [chinese_patent_medicine_knowledge/中成药知识问答_多选题.jsonl](fullset/chinese_patent_medicine_knowledge/中成药知识问答_多选题.jsonl) | `chinese_patent_medicine_knowledge_multiple_choice` | 1,950 | 400 |
| [chinese_patent_medicine_knowledge/中成药知识问答_填空题.jsonl](fullset/chinese_patent_medicine_knowledge/中成药知识问答_填空题.jsonl) | `chinese_patent_medicine_knowledge_fill_blank` | 2,000 | 400 |
| [information_extraction/实体抽取_古籍.jsonl](fullset/information_extraction/实体抽取_古籍.jsonl) | `classical_text_entity_extraction` | 2,000 | 400 |
| [information_extraction/实体抽取_病历.jsonl](fullset/information_extraction/实体抽取_病历.jsonl) | `clinical_record_entity_extraction` | 2,000 | 400 |
| [decision_recognition/医家辨证_选择题.jsonl](fullset/decision_recognition/医家辨证_选择题.jsonl) | `syndrome_single_choice` | 2,000 | 400 |
| [decision_recognition/医家治法_选择题.jsonl](fullset/decision_recognition/医家治法_选择题.jsonl) | `treatment_method_single_choice` | 2,000 | 400 |
| [decision_recognition/医家处方_选择题.jsonl](fullset/decision_recognition/医家处方_选择题.jsonl) | `herbal_prescription_single_choice` | 2,000 | 400 |
| [diagnostic_therapeutic_reasoning/医家辨证.jsonl](fullset/diagnostic_therapeutic_reasoning/医家辨证.jsonl) | `syndrome` | 2,000 | 400 |
| [diagnostic_therapeutic_reasoning/医家治法.jsonl](fullset/diagnostic_therapeutic_reasoning/医家治法.jsonl) | `treatment_method` | 2,000 | 400 |
| [diagnostic_therapeutic_reasoning/医家处方.jsonl](fullset/diagnostic_therapeutic_reasoning/医家处方.jsonl) | `herbal_prescription` | 2,000 | 400 |
| **总计：每套 15 个 JSONL 文件** | | **29,620** | **6,000** |

### 基准样本数与文件行数的计数方式

将每个联合诊疗推理病例计为一个样本时，基准共包含 13 个评估任务。按此口径，当前文件包含 **25,620 个 Full 样本**和 **5,200 个 Hard 样本**。

发布时，每个联合推理病例以辨证、治法和中药处方三条记录表示。因此，同一批 2,000 个 Full 病例（400 个 Hard 病例）占据 6,000 行 Full 记录（1,200 行 Hard 记录）。剂量属于 `herbal_prescription` 的一部分，不单独构成第四个标签文件。字符 F1 评分模式复用同一批病例。

## Full 与 Hard

Hard 记录选自 Full。每条 Hard 记录与其在 Full 中对应的记录具有相同的 `id`、`task`、输入字段和 `answer`。数据中没有单独的 `is_hard` 字段；记录是否属于 Hard，由其是否包含在 `hardset/` 下对应文件中确定。

- Full 与 Hard 存在重叠。请勿将二者拼接后视为相互独立的样本，也不要将其视为互不重叠的训练集和测试集。
- Hard 保留原始 ID。其顺序不必与 Full 一致，Hard 中的行号也不是病例 ID。
- 每个文件包含 400 条 Hard 记录。三个 DTR 组成文件共享相同的 400 个病例 ID。
- 决策识别任务的 Hard 样本按任务分别选取。不要假定辨证、治法和处方文件选取的病例彼此相同，或与 DTR-Hard 相同。

## ID 与公共字段

| 字段 | 类型 | 含义 |
| --- | --- | --- |
| `id` | 字符串 | 任务名称后接下划线和四位样本编号，例如 `syndrome_0001` |
| `task` | 字符串 | 上方清单中的精确任务标识 |
| `answer` | 字符串、列表或对象 | 标准标签，采用下文所述的任务专属格式 |

请使用完整的 `id` 作为记录键。相同的数字后缀不能用于关联互不相关的知识、考试或抽取任务。在六个临床任务（三个 DR 任务和三个 DTR 组成任务）内部，相同后缀标识 Full 中对应的病例。

## 输入字段与答案格式

### 执业资格考试

- `科目`：考试科目。
- `题目`：题目文本。
- `选项`：将 `A`–`E` 映射到选项文本的对象。
- `answer`：一个大写选项字母，例如 `"B"`。

### 基础知识与中成药知识

- `question`：题目文本。
- `question_type`：`single_choice`、`multiple_choice` 或 `fill_blank`。
- `options`：以字母为前缀的字符串列表，例如 `"A. ..."`；选择题包含此字段。
- 单选题的 `answer`：一个大写选项字母。
- 多选题的 `answer`：由不重复的大写字母组成的有序列表，例如 `["B", "C", "D"]`。列表可以只包含一个字母；评分时以发布的标签列表为准。
- 填空题的 `answer`：字符串；答案项之间使用中文顿号 `、` 分隔，例如 `"党参、黄芪"`。

### 信息抽取

- `text`：原文。
- `entity_types`：该段原文要求抽取的实体类型；不同记录的列表可能不同。
- `answer`：将实体类型映射到实体字符串列表的对象。

实体值为实体的文本字符串，而非字符偏移量。加载或评分时应保留实体类型及重复提及，不要将各列表转换为集合。空列表表示该类型没有标注实体。

完整的真实样本和答案见[信息抽取示例](fullset/information_extraction/README_zh.md#最小评估示例)。

### 决策识别

- `question`：基于病例的题目，包含所提供的临床上下文。
- `options`：五个以字母为前缀的选项字符串（`A`–`E`）。
- `answer`：一个大写选项字母。

这些任务与 DTR 标签组成部分的对应关系如下：

| 决策识别任务 | DTR 组成任务 |
| --- | --- |
| `syndrome_single_choice` | `syndrome` |
| `treatment_method_single_choice` | `treatment_method` |
| `herbal_prescription_single_choice` | `herbal_prescription` |

### 诊疗推理

- **单独评估：**独立加载 `syndrome`（辨证）、`treatment_method`（治法）或 `herbal_prescription`（处方）。以 `病历文本` 为病例输入，要求模型仅生成所选任务的结果，并使用对应的 `answer` 标签评分。
- **联合评估：**通过 ID 的四位病例编号后缀关联三个组成部分，对每个病例调用模型一次，同时生成辨证、治法和处方，再分别使用各自的标准标签评分。

现有 GitHub 评估入口采用联合流程。单独评估需要配合相应的提示词和评分流程；三个组成任务名称不是独立的 `--eval` 入口。报告结果时，请注明采用单独生成还是联合生成。

三个组成文件均包含：

- `医家`：病例所属医家；`未记录` 表示未记载此信息。
- `病历文本`：三个组成记录共享的病例文本。
- `answer`：该组成部分的标签。

`syndrome` 和 `treatment_method` 存储以逗号分隔的标签字符串。`herbal_prescription` 存储形如 `药名: 剂量g` 的药物与剂量对，各项之间以逗号分隔。该字段中的剂量单位为克。

[联合病例加载器](../simple-evals/evals/tcm_evals/diagnostic_therapeutic_data.py)会检查三个文件中的病例 ID、医家和病例文本是否一致。

## 评估输出格式

下表描述 GitHub 评估器要求的模型原始输出格式。任务目录中的简短示例则直接使用解析后的 Python 值作为 `prediction`，例如用列表表示多选和填空答案。

| 评估任务 | 模型输出 |
| --- | --- |
| 单选 | `答案：B`，使用大写选项字母 |
| 多选 | `答案：B,C,D` 或 `答案：BCD` |
| 填空 | `答案：党参,黄芪`，答案项之间使用 ASCII 逗号 |
| 信息抽取 | 将要求的实体类型映射到字符串列表的 JSON 对象 |
| 联合 DTR | 包含 `辨证`、`治法` 和 `处方` 的 JSON 对象，各字段值为字符串；处方项采用 `药名: 剂量g` 格式 |

两种 DTR 评估模式均读取这三个组成文件：`diagnostic_therapeutic_reasoning` 和 `diagnostic_therapeutic_reasoning_char_f1`。它们是评估名称，与记录中的三个 `task` 值不同。其余 12 个评估名称与清单中对应的 `task` 值一致。

有关命令，请参阅[评估指南](../simple-evals/README.md)和[入口配置](../simple-evals/config_evals.py)。保存结果时，请同时记录所选数据集合、评估名称及模型配置。

## 论文评估结果

论文中的 **19 个模型**的成绩按具体任务目录分别列出：Full 目录展示 Full 成绩，Hard 目录展示 Hard 成绩。来源为 [arXiv:2602.01779v1](https://arxiv.org/html/2602.01779v1)（2026-02-02）的表 2、表 3 和附录表 4。

| 任务类别 | Full 成绩 | Hard 成绩 |
| --- | --- | --- |
| 中医执业资格考试 | [Full](fullset/tcm_licensing_examination/README_zh.md) | [Hard](hardset/tcm_licensing_examination/README_zh.md) |
| 中医基础知识 | [Full](fullset/fundamental_tcm_knowledge/README_zh.md) | [Hard](hardset/fundamental_tcm_knowledge/README_zh.md) |
| 中成药知识 | [Full](fullset/chinese_patent_medicine_knowledge/README_zh.md) | [Hard](hardset/chinese_patent_medicine_knowledge/README_zh.md) |
| 信息抽取 | [Full](fullset/information_extraction/README_zh.md) | [Hard](hardset/information_extraction/README_zh.md) |
| 决策识别 | [Full](fullset/decision_recognition/README_zh.md) | [Hard](hardset/decision_recognition/README_zh.md) |
| 诊疗推理 | [Full](fullset/diagnostic_therapeutic_reasoning/README_zh.md) | [Hard](hardset/diagnostic_therapeutic_reasoning/README_zh.md) |


## 数据许可

LingLan 数据集（`data/fullset/` 和 `data/hardset/` 中的输入数据及标准标签）采用 [知识共享署名 4.0 国际许可（CC BY 4.0）](https://creativecommons.org/licenses/by/4.0/deed.zh-hans)发布。许可全文见 [LICENSE](LICENSE)。

该许可允许分享、修改和商业使用。分享原始或修改后的数据时，请按许可条款适当署名、提供许可链接，并标明是否进行了修改。请注明 LingLanMiDian 数据集及其作者，并保留数据来源链接；论文中的推荐引用格式见项目引用说明。

此声明适用于数据集，不更改评估代码或第三方库的许可证。第三方材料中未获许可方授权的权利不因本声明而转授；具体授权范围以 CC BY 4.0 条款为准。
