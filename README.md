# LLMD: LingLanMiDian

<!-- <div align=center><img width = '200' src ="./assets/LLMD Logo.png"/></div>   -->

## Introduction

**LLMD** is a large-scale, expert-curated benchmark for evaluating large language models (LLMs) in Traditional Chinese Medicine (TCM). It spans five domains (licensing exam, fundamental knowledge, Chinese patent medicine, information extraction, diagnostic–therapeutic reasoning) with **13 subtasks** and **25,624** instances. Each dataset includes a **400-item** *Hard* subset to probe robustness.

---

## Contents
- [What’s in LLMD](#whats-in-LLMD)
- [Data Statistics](#data-statistics)
- [Evaluation Metrics](#evaluation-metrics)
- [Download](#download)
- [Quick Start](#quick-start)
- [Leaderboards](#leaderboards)
  - [Concise Leaderboard (Overall Averages)](#concise-leaderboard-overall-averages)
  - [Detailed Leaderboard (Per-Task Bests)](#detailed-leaderboard-per-task-bests)
  - [Full Leaderboard (All Model Performance)](#full-leaderboard-all-model-performance)
- [Cite LLMD](#cite-LLMD)
- [Related Benchmarks](#related-benchmarks)
- [License & Ethics](#license--ethics)
- [Acknowledgements](#acknowledgements)

---

## What’s in LLMD

<p align="center">
  <img src="./assets/overview.png" alt="Overview" style="max-width:100%; height:auto;">
</p>

LLMD covers five domains with diverse formats (single-choice, multiple-choice, cloze, multi-label lists, dosage vectors) under a **unified metric system**:
- single-choice: Accuracy  
- multi-choice: instance-level Accuracy; option-level Precision/Recall/F1  
- cloze: **character-level F1**  
- extraction & multi-label: **list-level** Precision/Recall/F1  
- dosage: **cosine similarity** (primary), MAE when prescription overlap is adequate  

LLMD further introduces decision-recognition versions of clinical tasks (single-choice) for clean, reproducible comparisons.

---

## Data Statistics


<p align="center">
  <img src="./assets/dataset_statistic.png" alt="Dataset statistic" style="max-width:100%; height:auto;">
</p>

- TCM licensing exam: **1,832**  
- Fundamental TCM knowledge (single/multi-choice, cloze): **5,844**  
- Chinese patent medicine (single/multi-choice, cloze): **5,948**  
- Decision recognition (syndrome / treatment / prescription): **2,000 + 2,000 + 2,000**  
- Diagnostic–therapeutic reasoning (syndrome / treatment / prescription / dosage): **2,000**  
- Information extraction — classical: **2,000**  
- Information extraction — EMR: **2,000**  
- **Total:** 9 files, **25,624** items (each dataset includes a 400-item *Hard* subset)

---

## Evaluation Metrics
**Classification:** Accuracy (single-choice; decision recognition)  
**Multi-choice:** Accuracy; option-level Precision/Recall/F1  
**Cloze:** character-level F1  
**Extraction & multi-label clinical tasks:** list-level Precision/Recall/F1  
**Dosage:** cosine similarity (primary); MAE optionally reported when prescription overlap is reasonable

---

## Download

Waiting for release.

---

## Quick Start
```bash
git clone https://github.com/TCMAI-BJTU/LLMD
cd LLMD
pip install -r requirements.txt

# Evaluate a model
python eval/run_eval.py --model Qwen3-32B --tasks TLE
````

---

## Leaderboards

### Concise Leaderboard

<p align="center">
  <img src="./assets/model_performance.png" alt="Overall averages" style="max-width:100%; height:auto;">
</p>

Overall averages (%) on **Full** / **Hard** sets.
(*Hard* reveals a marked gap between current LLMs and expert-level TCM reasoning.)

| Rank | Model                |     Full |     Hard | Δ (pp) |
| ---- | -------------------- | -------: | -------: | -----: |
| 1    | **DeepSeek-R1**      | **58.3** | **37.6** |   20.7 |
| 2    | DeepSeek-V3.1-Think  |     57.9 |     37.0 |   20.9 |
| 3    | Qwen3-235B-A22B    |     57.8 |     36.5 |   21.3 |
| 4    | Qwen3-32B            |     55.6 |     34.6 |   21.0 |
| 5    | Qwen3-14B            |     54.5 |     32.4 |   22.1 |
| 6    | Baichuan-M2-32B      |     53.7 |     30.9 |   22.8 |
| 7    | Qwen3-8B             |     53.0 |     30.3 |   22.7 |
| 8    | Qwen3-4B             |     50.2 |     28.8 |   21.4 |
| 9    | Qwen3-Next-80B-A3B |     50.8 |     26.3 |   24.5 |
| 10   | GPT-OSS-120B         |     47.0 |     27.8 |   19.2 |
| 11   | GPT-OSS-20B          |     41.9 |     24.5 |   17.4 |

### Detailed Leaderboard (Per-Task Bests)

Best model per subtask/metric; values shown as **Full / Hard**.

| Subtask (Metric)               | Best (Full)         |           Score | Best (Hard)         |    Score |
| ------------------------------ | ------------------- | --------------: | ------------------- | -------: |
| TLE — Comprehensive (Accuracy) | DeepSeek-V3.1-Think | **95.5 / 81.5** | DeepSeek-V3.1-Think | **81.5** |
| FTK — Single-choice (Accuracy) | DeepSeek-R1         | **86.1 / 45.5** | DeepSeek-R1         | **45.5** |
| FTK — Multi-choice (F1)        | DeepSeek-R1         | **91.0 / 77.1** | DeepSeek-R1         | **77.1** |
| FTK — Cloze (char-F1)          | Qwen3-235B (A22B)   | **59.9 / 22.6** | Qwen3-235B (A22B)   | **22.6** |
| CPM — Single-choice (Accuracy) | DeepSeek-R1         | **74.3 / 28.5** | DeepSeek-R1         | **28.5** |
| CPM — Multi-choice (F1)        | DeepSeek-R1         | **87.0 / 71.7** | DeepSeek-R1         | **71.7** |
| CPM — Cloze (char-F1)          | DeepSeek-V3.1-Think | **74.4 / 55.1** | DeepSeek-R1         | **57.3** |
| IE — EMR (F1)                  | Qwen3-235B (A22B)   | **67.2 / 48.8** | Qwen3-32B           | **54.1** |
| IE — Classical (F1)            | DeepSeek-V3.1-Think | **62.1 / 44.1** | DeepSeek-V3.1-Think | **44.1** |
| DTR — Syndrome (F1, exact)     | DeepSeek-V3.1-Think |  **22.3 / 9.4** | Qwen3-235B (A22B)   | **10.4** |
| DTR — Treatment (F1, exact)    | DeepSeek-V3.1-Think |  **17.6 / 6.7** | DeepSeek-V3.1-Think |  **6.7** |
| DTR — Prescription (F1, exact) | DeepSeek-R1         | **32.3 / 18.3** | DeepSeek-R1         | **18.3** |
| DTR — Dosage (Cosine)          | Qwen3-235B (A22B)   | **31.2 / 17.9** | Qwen3-235B (A22B)   | **17.9** |
| DR — Syndrome (Accuracy)       | DeepSeek-R1         | **86.7 / 38.8** | DeepSeek-R1         | **38.8** |
| DR — Treatment (Accuracy)      | Qwen3-32B           | **80.0 / 22.5** | GPT-OSS-120B        | **33.5** |
| DR — Prescription (Accuracy)   | DeepSeek-V3.1-Think | **90.0 / 54.2** | DeepSeek-V3.1-Think | **54.2** |

### Full Leaderboard (All Model Performance)

| **Dom.** | **Subtask** | **Metric** | **DeepSeek-R1** | **DeepSeek-V3.1** | **Qwen3-235B** | **Qwen3-32B** | **Baichuan-M2-32B** | **Qwen3-Next-80B** | **GPT-OSS-120B** | **Qwen3-14B** | **Qwen3-4B** | **Qwen3-8B** | **gpt-oss-20b** |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| TLE | Comprehensive | Accuracy | 95.0 / 78.5 | **95.5** / **81.5** | 95.0 / 78.2 | 91.2 / 62.3 | 89.8 / 58.2 | 93.8 / 73.2 | 58.1 / 14.0 | 87.6 / 51.0 | 76.6 / 25.2 | 84.6 / 38.2 | 48.3 / 11.2 |
| FTK | Single-choice | Accuracy | **86.1** / **45.5** | **86.1** / 43.8 | 85.0 / 44.0 | **86.1** / 44.8 | 83.4 / 32.0 | 82.1 / 32.2 | 70.4 / 29.2 | 83.0 / 36.2 | 76.2 / 26.0 | 80.8 / 33.2 | 65.4 / 31.8 |
| FTK | Multiple-choice | Accuracy | **64.8** / **30.0** | 62.4 / 27.0 | 61.3 / 24.8 | 56.3 / 22.8 | 48.6 / 14.8 | 52.6 / 14.2 | 35.3 / 11.8 | 49.5 / 13.8 | 42.4 / 13.0 | 47.8 / 13.5 | 24.8 / 7.0 |
| FTK | Multiple-choice | Precision | 92.5 / **82.5** | 91.9 / 80.6 | **93.0** / 81.1 | 90.3 / 78.0 | 90.5 / 76.0 | 89.4 / 71.3 | 81.2 / 64.0 | 90.6 / 75.7 | 86.1 / 69.8 | 88.4 / 72.6 | 76.1 / 58.7 |
| FTK | Multiple-choice | Recall | **92.1** / 78.2 | 92.0 / **79.7** | 89.1 / 73.2 | 90.9 / 77.8 | 84.5 / 65.8 | 84.7 / 64.9 | 83.2 / 66.8 | 85.7 / 69.2 | 84.9 / 67.4 | 86.8 / 69.5 | 74.9 / 56.9 |
| FTK | Multiple-choice | F1 | **91.0** / **77.1** | 90.6 / **77.1** | 89.5 / 73.5 | 89.1 / 74.8 | 85.3 / 66.4 | 84.7 / 63.6 | 80.0 / 62.1 | 86.3 / 68.6 | 83.5 / 64.9 | 85.8 / 67.5 | 72.9 / 54.0 |
| FTK | Cloze | char-F1 | 58.2 / 20.4 | 58.8 / 19.4 | **59.9** / **22.6** | 56.1 / 16.6 | 50.2 / 15.7 | 56.0 / 15.8 | 42.1 / 14.2 | 54.1 / 13.9 | 49.0 / 15.5 | 51.1 / 12.7 | 35.9 / 11.2 |
| CPM | Single-choice | Accuracy | **74.3** / **28.5** | 73.3 / 23.5 | 68.6 / 16.2 | 66.9 / 17.0 | 60.5 / 11.2 | 63.1 / 7.2 | 44.5 / 12.5 | 58.9 / 7.2 | 51.3 / 10.5 | 56.6 / 9.5 | 37.6 / 13.8 |
| CPM | Multiple-choice | Accuracy | **48.0** / **22.8** | 42.2 / 14.8 | 44.8 / 15.2 | 35.5 / 7.0 | 33.2 / 5.2 | 34.2 / 3.5 | 24.7 / 4.0 | 34.4 / 6.0 | 28.7 / 4.8 | 31.4 / 7.8 | 18.5 / 4.0 |
| CPM | Multiple-choice | Precision | **86.4** / **73.0** | 84.3 / 69.2 | 86.1 / 69.0 | 81.9 / 62.7 | 83.1 / 63.6 | 80.6 / 58.6 | 76.0 / 54.0 | 82.5 / 61.7 | 79.3 / 59.2 | 81.3 / 62.1 | 72.6 / 51.1 |
| CPM | Multiple-choice | Recall | 90.6 / 75.7 | **91.5** / **78.0** | 87.7 / 70.5 | 87.8 / 70.4 | 82.2 / 59.1 | 84.1 / 62.4 | 82.5 / 62.3 | 84.9 / 64.2 | 84.7 / 67.2 | 84.2 / 66.4 | 75.4 / 55.1 |
| CPM | Multiple-choice | F1 | **87.0** / **71.7** | 86.3 / 71.1 | 85.4 / 67.5 | 83.2 / 64.1 | 80.6 / 58.1 | 80.1 / 57.1 | 77.3 / 55.8 | 82.0 / 60.3 | 80.0 / 60.4 | 80.9 / 61.8 | 71.6 / 50.8 |
| CPM | Cloze | char-F1 | 74.0 / **57.3** | **74.4** / 55.1 | 74.3 / 55.1 | 67.5 / 41.7 | 64.6 / 40.3 | 70.8 / 46.8 | 57.5 / 35.9 | 66.8 / 38.6 | 61.4 / 35.7 | 64.1 / 37.2 | 49.9 / 29.1 |
| IE | Clinical EMR | Precision | 66.6 / 46.5 | 64.6 / 46.8 | 69.1 / 50.4 | 73.3 / 61.6 | 61.8 / 45.6 | 38.1 / 15.6 | 59.7 / 41.5 | **74.6** / **63.2** | 64.7 / 52.6 | 67.7 / 55.6 | 55.3 / 39.5 |
| IE | Clinical EMR | Recall | 61.3 / 43.3 | 58.6 / 42.3 | **66.3** / 48.8 | 62.2 / 49.6 | 56.0 / 41.4 | 33.5 / 13.5 | 55.8 / 41.7 | 62.1 / **51.9** | 52.3 / 40.9 | 57.6 / 45.4 | 51.6 / 38.3 |
| IE | Clinical EMR | F1 | 63.1 / 43.7 | 60.8 / 43.4 | **67.2** / 48.8 | 66.7 / 54.1 | 58.1 / 42.3 | 35.2 / 13.9 | 57.1 / 40.7 | 67.1 / **55.8** | 57.2 / 45.2 | 61.5 / 49.1 | 52.8 / 37.9 |
| IE | Classical Texts | Precision | 60.1 / 39.8 | **61.4** / **42.3** | 57.3 / 37.6 | 57.9 / 38.0 | 58.9 / 37.9 | 38.7 / 12.9 | 51.1 / 31.0 | 59.8 / 39.3 | 54.5 / 34.5 | 58.1 / 34.8 | 50.3 / 27.1 |
| IE | Classical Texts | Recall | 62.9 / 44.0 | **64.4** / **48.0** | 62.6 / 45.2 | 56.9 / 37.7 | 61.6 / 42.2 | 40.3 / 13.9 | 56.6 / 38.2 | 56.3 / 37.7 | 49.2 / 31.3 | 54.7 / 33.6 | 54.0 / 32.2 |
| IE | Classical Texts | F1 | 60.8 / 40.9 | **62.1** / **44.1** | 59.1 / 40.0 | 56.6 / 36.8 | 59.5 / 39.0 | 39.0 / 12.9 | 53.0 / 33.4 | 57.3 / 37.5 | 51.0 / 31.8 | 55.6 / 33.4 | 51.3 / 28.5 |
| DTR | Syndrome | Precision | 9.9 / 1.1 | **11.0** / 1.1 | 9.0 / 0.9 | 7.7 / 0.5 | 9.1 / 1.1 | 10.7 / **1.3** | 3.2 / 0.6 | 7.6 / 0.9 | 6.9 / **1.3** | 7.5 / 0.9 | 3.3 / **1.3** |
| DTR | Syndrome | Recall | 13.3 / 1.4 | **14.3** / 1.3 | 13.4 / 1.4 | 11.2 / 0.7 | 12.6 / 1.3 | 12.6 / 1.5 | 4.5 / 0.7 | 11.3 / 1.0 | 9.8 / 1.6 | 9.9 / 1.0 | 5.4 / **1.9** |
| DTR | Syndrome | F1 | 10.9 / 1.1 | **11.9** / 1.2 | 10.4 / 1.1 | 8.8 / 0.6 | 10.1 / 1.2 | 11.0 / 1.3 | 3.6 / 0.6 | 8.8 / 0.9 | 7.8 / 1.4 | 8.2 / 0.9 | 3.9 / **1.5** |
| DTR | Treatment | Precision | 14.2 / **1.6** | **14.3** / 0.8 | 12.9 / 0.9 | 11.5 / 1.3 | 11.7 / 0.7 | 13.6 / 0.6 | 9.6 / 1.1 | 11.0 / 0.8 | 11.6 / 1.4 | 12.0 / 0.8 | 6.5 / 0.9 |
| DTR | Treatment | Recall | **17.0** / **1.9** | 16.4 / 0.8 | 15.6 / 1.1 | 14.4 / 1.5 | 15.0 / 1.1 | 14.5 / 0.9 | 11.2 / 1.5 | 14.3 / 1.2 | 14.4 / 1.8 | 14.7 / 1.0 | 7.8 / 1.1 |
| DTR | Treatment | F1 | **14.8** / **1.6** | 14.7 / 0.8 | 13.6 / 1.0 | 12.3 / 1.3 | 12.6 / 0.8 | 13.5 / 0.7 | 9.9 / 1.2 | 12.0 / 1.0 | 12.4 / **1.6** | 12.8 / 0.9 | 6.7 / 0.9 |
| DTR | Prescription | Precision | 35.7 / 20.1 | **36.9** / **20.3** | 33.4 / 19.3 | 31.0 / 17.1 | 32.1 / 18.3 | 32.4 / 17.4 | 30.2 / 17.5 | 31.1 / 17.3 | 30.4 / 17.1 | 31.7 / 17.1 | 24.8 / 15.8 |
| DTR | Prescription | Recall | 30.6 / 17.9 | 29.6 / 17.0 | **33.5** / **19.8** | 29.3 / 16.7 | 29.4 / 17.2 | 29.9 / 16.5 | 22.9 / 13.5 | 29.6 / 16.9 | 25.0 / 14.0 | 26.4 / 14.5 | 21.2 / 13.9 |
| DTR | Prescription | F1 | 32.3 / 18.3 | 32.1 / 17.9 | **32.7** / **18.9** | 29.5 / 16.3 | 30.0 / 17.1 | 30.4 / 16.3 | 25.4 / 14.7 | 29.8 / 16.6 | 26.8 / 14.8 | 28.2 / 15.1 | 22.2 / 14.2 |
| DTR | Dosage | MAE (abs) | 4.1 / 3.9 | 4.2 / 4.2 | 4.2 / 4.1 | 4.4 / 4.8 | 4.2 / 4.0 | **4.0** / **3.8** | 4.4 / **3.8** | 4.2 / 4.2 | 4.1 / 4.1 | 4.3 / 4.1 | 4.5 / 4.2 |
| DTR | Dosage | Cosine | 30.9 / 16.5 | 31.0 / 16.8 | **31.2** / **17.9** | 29.0 / 15.6 | 28.7 / 15.6 | 29.1 / 15.2 | 23.3 / 12.9 | 28.6 / 15.7 | 26.3 / 14.6 | 27.2 / 14.4 | 20.0 / 12.4 |
| DTR-F1 | Syndrome | Precision | 20.0 / 9.1 | **21.0** / 9.2 | 18.9 / **9.5** | 15.8 / 7.6 | 17.1 / 7.6 | 20.2 / 8.9 | 10.4 / 5.9 | 16.0 / 7.8 | 15.1 / 8.3 | 17.2 / 8.5 | 6.0 / 2.2 |
| DTR-F1 | Syndrome | Recall | 25.8 / 11.0 | 26.2 / 10.3 | **27.1** / **12.3** | 22.7 / 10.2 | 23.1 / 9.9 | 23.1 / 9.4 | 14.5 / 7.5 | 23.5 / 11.0 | 21.3 / 11.0 | 22.1 / 10.5 | 9.0 / 2.7 |
| DTR-F1 | Syndrome | F1 | 21.5 / 9.5 | **22.3** / 9.4 | 21.5 / **10.4** | 17.9 / 8.4 | 18.8 / 8.2 | 20.5 / 8.8 | 11.6 / 6.4 | 18.3 / 8.7 | 17.0 / 9.1 | 18.5 / 9.1 | 6.8 / 2.3 |
| DTR-F1 | Treatment | Precision | 15.5 / **6.9** | **16.3** / 6.1 | 14.8 / 6.5 | 13.3 / 6.4 | 13.3 / 5.2 | 16.2 / 5.8 | 9.2 / 4.4 | 12.0 / 6.2 | 12.4 / 6.2 | 14.0 / 5.6 | 6.4 / 3.7 |
| DTR-F1 | Treatment | Recall | **20.2** / **9.4** | 20.1 / 7.7 | 19.6 / 8.8 | 18.4 / 8.5 | 18.7 / 7.3 | 18.5 / 7.1 | 12.9 / 6.2 | 17.6 / 9.0 | 16.9 / 8.5 | 18.7 / 7.8 | 9.7 / 5.4 |
| DTR-F1 | Treatment | F1 | 17.1 / **7.8** | **17.6** / 6.7 | 16.4 / 7.3 | 15.0 / 7.1 | 15.1 / 5.9 | 16.8 / 6.3 | 10.5 / 5.0 | 13.9 / 7.2 | 14.0 / 7.0 | 15.6 / 6.4 | 7.5 / 4.3 |
| DTR-F1 | Prescription | Precision | 35.5 / 20.0 | **36.9** / **20.4** | 33.3 / 19.3 | 30.8 / 17.1 | 31.5 / 18.1 | 33.1 / 17.9 | 29.9 / 17.5 | 30.7 / 17.2 | 30.2 / 17.0 | 31.6 / 17.2 | 25.3 / 15.9 |
| DTR-F1 | Prescription | Recall | 30.9 / 18.0 | 29.5 / 17.0 | **33.5** / **19.9** | 29.5 / 16.8 | 30.1 / 17.6 | 30.6 / 16.9 | 22.9 / 13.6 | 29.8 / 17.1 | 25.0 / 13.9 | 26.4 / 14.5 | 21.8 / 14.1 |
| DTR-F1 | Prescription | F1 | 32.3 / 18.3 | 32.1 / 17.9 | **32.6** / **19.0** | 29.5 / 16.4 | 30.0 / 17.3 | 31.0 / 16.7 | 25.3 / 14.8 | 29.6 / 16.6 | 26.7 / 14.8 | 28.1 / 15.1 | 22.8 / 14.4 |
| DTR-F1 | Dosage | MAE (abs) | 4.1 / 4.0 | 4.2 / 4.2 | 4.2 / 4.2 | 4.4 / 4.7 | 4.2 / 4.1 | **4.0** / 3.9 | 4.4 / **3.8** | 4.2 / 4.2 | 4.1 / 4.1 | 4.3 / 4.1 | 4.6 / 4.3 |
| DTR-F1 | Dosage | Cosine | 31.0 / 16.8 | 30.9 / 16.8 | **31.2** / **17.9** | 29.1 / 15.6 | 28.9 / 16.2 | 29.6 / 15.5 | 23.3 / 13.0 | 28.6 / 15.7 | 26.3 / 14.7 | 27.3 / 14.6 | 20.7 / 12.5 |
| DR | Syndrome | Accuracy | **86.7** / **38.8** | 85.5 / 35.0 | 85.4 / 38.5 | 86.0 / 38.5 | 83.6 / 30.0 | 84.9 / 32.5 | 77.7 / 34.5 | 84.2 / 34.0 | 77.2 / 25.2 | 82.8 / 28.5 | 70.2 / 30.2 |
| DR | Treatment | Accuracy | 78.7 / 21.5 | 77.6 / 18.8 | 79.0 / 19.2 | **80.0** / 22.5 | 76.8 / 14.2 | 77.5 / 16.8 | 75.2 / **33.5** | 78.4 / 19.0 | 74.8 / 24.0 | 78.6 / 19.8 | 68.2 / 32.8 |
| DR | Prescription | Accuracy | 89.1 / 50.5 | **90.0** / **54.2** | 88.7 / 49.2 | 87.5 / 44.5 | 87.8 / 44.8 | 88.4 / 47.5 | 78.5 / 37.5 | 87.4 / 43.0 | 82.4 / 32.2 | 84.9 / 34.5 | 64.5 / 25.5 |
| **Overall Average** |  |  | **48.6** / **30.1** | 48.4 / 29.6 | 48.1 / 29.3 | 46.0 / 27.7 | 44.7 / 25.0 | 42.7 / 21.4 | 38.7 / 22.4 | 45.1 / 26.0 | 41.6 / 23.3 | 43.9 / 24.3 | 34.3 / 19.9 |
---

## Cite LLMD

```bibtex
@misc{LLMD2025,
  title={LLMD: Ultimate Traditional Chinese Medicine Benchmark},
  author={Ruihua},
  year={2025},
  note={https://github.com/TCMAI-BJTU/LLMD}
}
```

---

## License & Ethics

* Data are curated from de-identified clinical records, classical texts, official exam sources, and structured knowledge resources.
* See **LICENSE** and **ETHICS.md** for usage terms and citation requirements.

---

## Acknowledgements

We thank the curators, annotators, and domain experts who contributed to dataset construction and verification.
