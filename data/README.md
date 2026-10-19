# LingLanMedBench Traditional Chinese Medicine Benchmark Dataset

[中文说明](README_zh.md)

This directory contains the released LingLanMedBench inputs and reference labels in UTF-8 JSON Lines format: one JSON object per line. Every record includes `id`, `task`, and `answer`.

- [`fullset/`](fullset/): the full evaluation collection.
- [`hardset/`](hardset/): the corresponding Hard subsets.
- [Benchmark overview and citation](../README.md)
- [Evaluation commands and modes](../simple-evals/README.md)

[Directory structure](#directory-structure) · [Files and tasks](#files-and-task-names) · [Answer formats](#input-fields-and-answer-formats) · [Results](#paper-evaluation-results) · [License](#data-license)

## Directory structure

Both sets use the same directory and file structure:

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

The six directories implement five benchmark domains: diagnostic and therapeutic decision-making is represented by both `decision_recognition` and `diagnostic_therapeutic_reasoning`.

## Files and task names

Paths below are relative to either `fullset/` or `hardset/`. File links point to Full; the same relative paths exist under Hard. The `task` column gives the exact value stored in each record.

| File | `task` | Full rows | Hard rows |
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
| **Total: 15 JSONL files per set** | | **29,620** | **6,000** |

### Counting benchmark items and file rows

The benchmark has 13 evaluation tasks when the joint diagnostic and therapeutic reasoning case is counted once. Under this convention, the current files contain **25,620 Full items** and **5,200 Hard items**.

For release, each joint reasoning case is represented by three records: syndrome, treatment method, and herbal prescription. The same 2,000 Full cases (400 Hard cases) therefore occupy 6,000 Full rows (1,200 Hard rows). Dosages are part of `herbal_prescription`; they do not form a fourth label file. The character-F1 scoring mode reuses the same cases.

## Full and Hard

Hard records are selected from Full. Each Hard record has the same `id`, `task`, input fields, and `answer` as its Full counterpart. There is no separate `is_hard` field; Hard membership is specified by inclusion in the matching file under `hardset/`.

- Full and Hard overlap. Do not concatenate them as independent examples or treat them as disjoint training and test partitions.
- Hard keeps the original IDs. Its order is not required to match Full, and a Hard row number is not its case ID.
- Each file contains 400 Hard records. The three diagnostic and therapeutic reasoning component files share the same 400 case IDs.
- Hard membership for decision recognition is task-specific. Do not assume that its syndrome, treatment-method, and prescription files select the same cases as one another or as the Hard subset for diagnostic and therapeutic reasoning.

## IDs and shared fields

| Field | Type | Meaning |
| --- | --- | --- |
| `id` | string | Task name followed by an underscore and a four-digit sample number, for example `syndrome_0001` |
| `task` | string | Exact task identifier from the inventory above |
| `answer` | string, list, or object | Reference label in the task-specific format below |

Use the complete `id` as the record key. A shared numeric suffix does not link unrelated knowledge, examination, or extraction tasks. Within the six clinical tasks (three decision recognition tasks and three diagnostic and therapeutic reasoning components), matching suffixes identify the corresponding case in Full.

## Input fields and answer formats

### Licensing examination

- `科目`: examination subject.
- `题目`: question text.
- `选项`: an object mapping `A`–`E` to option text.
- `answer`: one uppercase option letter, such as `"B"`.

### Fundamental knowledge and Chinese patent medicine knowledge

- `question`: question text.
- `question_type`: `single_choice`, `multiple_choice`, or `fill_blank`.
- `options`: a list of letter-prefixed strings, such as `"A. ..."`; present for choice questions.
- Single-choice `answer`: one uppercase option letter.
- Multiple-choice `answer`: a sorted list of distinct uppercase letters, such as `["B", "C", "D"]`. A list can contain one letter; score it against the released label list.
- Fill-in-the-blank `answer`: a string; answer items are separated with the Chinese enumeration comma `、`, for example `"党参、黄芪"`.

### Information extraction

- `text`: the source passage.
- `entity_types`: the types requested for this passage; this list can vary between records.
- `answer`: an object mapping entity types to lists of entity strings.

The entity values are surface strings, not character offsets. Preserve their types and repeated mentions when loading or scoring; do not turn each list into a set. An empty list represents no annotated entity for that type.

See the [information extraction examples](fullset/information_extraction/README.md#minimal-evaluation-example) for complete real records and answers.

### Decision recognition

- `question`: the case-based question, including any supplied clinical context.
- `options`: five letter-prefixed option strings (`A`–`E`).
- `answer`: one uppercase option letter.

The tasks correspond to the diagnostic and therapeutic reasoning label components:

| Decision-recognition task | Diagnostic and therapeutic reasoning component task |
| --- | --- |
| `syndrome_single_choice` | `syndrome` |
| `treatment_method_single_choice` | `treatment_method` |
| `herbal_prescription_single_choice` | `herbal_prescription` |

### Diagnostic and therapeutic reasoning

- **Independent evaluation:** load `syndrome` (syndrome differentiation), `treatment_method`, or `herbal_prescription` on its own. Use `病历文本` as the case input, ask the model to generate only the selected component, and score that output against the corresponding `answer` labels.
- **Joint evaluation:** join all three components by the four-digit case ID suffix, then ask the model to generate syndrome, treatment method, and prescription in one call per case. Score each component against its own reference labels.

The bundled GitHub runner uses the joint workflow. Independent evaluation requires a component-specific prompt and scoring procedure; the three component names are not standalone `--eval` entry points. Report whether generation was independent or joint.

All three component files include:

- `医家`: physician attribution; `未记录` means it was not recorded.
- `病历文本`: the case text shared by the three component records.
- `answer`: the label for that component.

`syndrome` and `treatment_method` store comma-separated label strings. `herbal_prescription` stores drug–dose pairs in the form `药名: 剂量g`, separated by commas. Dosages in this field use grams.

The [joint-case loader](../simple-evals/evals/tcm_evals/diagnostic_therapeutic_data.py) checks that the case IDs, physician, and case text agree across the three files.

## Evaluation output format

The table below describes the GitHub evaluator's raw model-response protocol. Task-directory examples instead use parsed Python values in `prediction`, such as lists for multiple-choice and fill-in-the-blank answers.

| Evaluation | Model output |
| --- | --- |
| Single-choice | `答案：B` with an uppercase option letter |
| Multiple-choice | `答案：B,C,D` or `答案：BCD` |
| Fill-in-the-blank | `答案：党参,黄芪` with an ASCII comma between items |
| Information extraction | A JSON object mapping the requested entity types to lists of strings |
| Joint diagnostic and therapeutic reasoning | A JSON object with string values for `辨证`, `治法`, and `处方`; use `药名: 剂量g` for prescription items |

Both diagnostic and therapeutic reasoning evaluation modes read the three component files: `diagnostic_therapeutic_reasoning` and `diagnostic_therapeutic_reasoning_char_f1`. These are evaluation names, distinct from the three per-record `task` values. The other 12 evaluation names match the corresponding `task` values in the inventory.

See the [evaluation guide](../simple-evals/README.md) and [entry-point configuration](../simple-evals/config_evals.py) for commands. Record the selected set, evaluation name, and model configuration with your results.

## Paper evaluation results

Results for the paper's **19 models** are listed in the corresponding task directories: Full directories show Full results and Hard directories show Hard results. The source is Tables 1, 2, and Supplementary Table S1 of [arXiv:2602.01779](https://arxiv.org/html/2602.01779).

| Task group | Full results | Hard results |
| --- | --- | --- |
| Traditional Chinese Medicine licensing examination | [Full](fullset/tcm_licensing_examination/README.md) | [Hard](hardset/tcm_licensing_examination/README.md) |
| Fundamental Traditional Chinese Medicine knowledge | [Full](fullset/fundamental_tcm_knowledge/README.md) | [Hard](hardset/fundamental_tcm_knowledge/README.md) |
| Chinese patent medicine knowledge | [Full](fullset/chinese_patent_medicine_knowledge/README.md) | [Hard](hardset/chinese_patent_medicine_knowledge/README.md) |
| Information extraction | [Full](fullset/information_extraction/README.md) | [Hard](hardset/information_extraction/README.md) |
| Decision recognition | [Full](fullset/decision_recognition/README.md) | [Hard](hardset/decision_recognition/README.md) |
| Diagnostic and therapeutic reasoning | [Full](fullset/diagnostic_therapeutic_reasoning/README.md) | [Hard](hardset/diagnostic_therapeutic_reasoning/README.md) |


## Data license

The LingLanMedBench dataset is released under the [Creative Commons Attribution 4.0 International license](https://creativecommons.org/licenses/by/4.0/). Please credit [LingLanMedBench, its authors, and the data source](https://github.com/TCMAI-BJTU/LingLan), and cite the [paper](https://arxiv.org/abs/2602.01779) when using it. When sharing the data, retain the license link and indicate any changes. See [LICENSE](LICENSE) for the full terms.
