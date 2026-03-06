# Halftime to Fulltime Predictor

> **To what extent are first-half statistics predictive of the final match result?**

A football analytics project using **StatsBomb open data** for the Italian Serie A 2015/16 season (380 matches, 1.35M event rows). The analysis combines advanced metric computation from raw event data with machine learning classification to quantify how much the first half tells us about the final outcome.

---

## Key Results

| Metric | Value |
|---|---|
| Result stability (HT == FT) | **62.6%** |
| Home wins kept at FT | 81.7% |
| Away wins kept at FT | 76.1% |
| HT draws kept at FT | 41.0% — most volatile state |
| Cramér's V (HT → FT association) | **0.494** — moderate, p < 0.001 |
| Best model (SVM, all features) | **56.8% accuracy, AUC 0.757** |
| Majority-class baseline | 46.3% |

**TL;DR:** The half-time score is the dominant predictor. Process metrics (possession, pressing, progressive passes) have limited standalone power on a single-season dataset. Draws are structurally unpredictable from first-half data alone.

---

## Project Structure

```
halftime-to-fulltime-predictor/
│
├── halftime_to_fulltime_predictor.ipynb   # Main analysis notebook
│
├── data/
│   ├── download_data.py                   # Script to download StatsBomb data
│   └── README.md                          # Data documentation
│
├── visualizations/                        # All plots saved here on execution
│                            
│
├── assets/
│   └── teams_logos/                             # Optional: team logo PNGs
│
├── fonts/                                 # Optional: Teko font family (.ttf)
│
├── requirements.txt
├── .gitignore
└── README.md
```

---

## Analysis Pipeline

| Phase | Description |
|---|---|
| **1. Setup** | Libraries, global config, reproducibility seed (`RANDOM_STATE = 42`) |
| **2. Data loading** | Shape inspection, event type distribution |
| **3. Standings table** | Basic table enriched with xG, PPDA, Field Tilt, possession, progressive passes, key passes, pressure height |
| **4. Visualisations** | Goals vs xG, shot maps, passing zone heatmaps, pressing scatter |
| **5. Match results table** | Per-match HT/FT stats built with vectorised pandas groupby operations |
| **6. HT–FT analysis** | Result stability, comeback rates, transition matrix |
| **7. Modelling** | Chi-square test, majority-class baseline, SVM / Decision Tree / Naive Bayes, stratified 5-fold CV, ROC curves, feature importance |
| **8. No-goals analysis** | Full modelling pipeline repeated excluding goal-related features |
| **9. Conclusions** | Findings, per-model comparison table, limitations, implications |

---

## Advanced Metrics Computed from Raw Events

All metrics are computed from scratch using StatsBomb event coordinates — no pre-aggregated stats are used.

- **xG** — StatsBomb's `shot.statsbomb_xg` field, aggregated per team per match
- **PPDA** — Passes per Defensive Action: opponent successful passes in their own half ÷ team defensive actions in the offensive half. Lower = more intense pressing.
- **Field Tilt** — team's share of passes in the final third (x > 80)
- **Possession** — pass-based ball share per match
- **Progressive passes** — completed passes reducing distance to goal by ≥ 20%
- **Pressure height** — median x-coordinate of Pressure events
- **Key passes** — passes directly leading to a shot (`pass.shot_assist` or `pass.goal_assist`)

---

## Modelling Design Choices

**First-half features only.** All models are trained exclusively on `ht_` prefixed features. Using full-match statistics to predict the final result would constitute data leakage — the model would see second-half information that is unavailable at half-time.

**Calibrated SVM.** `CalibratedClassifierCV` is used instead of `SVC(probability=True)` to obtain better probability estimates for ROC analysis on a small dataset.

**Majority-class baseline.** A `DummyClassifier` establishes the floor any model must beat before being considered useful.

---

## Model Performance Summary

### All first-half features

| Model | CV acc | Test acc | Macro AUC | Draw F1 |
|---|---|---|---|---|
| SVM (calibrated) | 0.600 ± 0.013 | **0.568** | **0.757** | 0.00 |
| Naive Bayes | 0.533 ± 0.057 | 0.547 | 0.734 | **0.39** |
| Decision Tree | 0.502 ± 0.038 | 0.495 | 0.605 | 0.34 |
| Majority-class baseline | — | 0.463 | — | 0.00 |

### Excluding goal-related features (goals, shots, xG)

| Model | CV acc | Test acc | Macro AUC |
|---|---|---|---|
| SVM (calibrated) | 0.523 ± 0.026 | 0.484 | 0.560 |
| Naive Bayes | 0.453 ± 0.036 | 0.453 | 0.608 |
| Decision Tree | 0.407 ± 0.070 | 0.390 | 0.536 |

The sharp AUC drop (0.757 → 0.560) when removing goal features confirms that the half-time score dominates, while process metrics have limited standalone power at this dataset scale.

---

## Notable Finding: Draws

The SVM (best overall model) achieves **F1 = 0.00 on draws** — it ignores them entirely due to class imbalance (95 draws vs. 175 home wins). Naive Bayes partially recovers draw prediction (F1 = 0.39) at the cost of lower overall accuracy.

The transition matrix explains why: only **41% of HT draws remain draws at FT**, while **38.6% flip to a home win** — the single most frequent second-half transition in the dataset.

---

## Installation

```bash
git clone https://github.com/marinoalfonso/halftime-to-fulltime-predictor.git
cd halftime-to-fulltime-predictor
pip install -r requirements.txt
```

### Download the data

```bash
python data/download_data.py
```

This downloads the StatsBomb open data for Serie A 2015/16 directly via the official `statsbombpy` library. The raw CSV files are not included in the repository due to their size (~1 GB).

### Optional: custom fonts

Download the [Teko font family](https://fonts.google.com/specimen/Teko) from Google Fonts and place the `.ttf` files in a `fonts/` folder. The notebook falls back to matplotlib defaults if the folder is absent.

### Run

```bash
jupyter notebook halftime_to_fulltime_predictor.ipynb
```

---

## Data

- **Source:** [StatsBomb Open Data](https://github.com/statsbomb/open-data)
- **Competition:** Serie A 2015/16
- **Matches:** 380
- **Events:** ~1,353,739 rows × 176 columns
- **License:** StatsBomb Open Data License — free for non-commercial use with attribution

See `data/README.md` for full details on the data structure and download instructions.

---

## Known Limitations

| Limitation | Impact |
|---|---|
| Single season (380 matches) | High CV variance (DT SD up to 0.070); limited generalisation |
| Class imbalance (175 / 110 / 95) | SVM collapses draw recall to zero; accuracy alone is misleading |
| No temporal features | Second-half substitutions, fatigue, red cards not modelled |
| Single competition | Serie A 2015/16 tactical patterns may not transfer to other leagues/eras |

---

## Tech Stack

![Python](https://img.shields.io/badge/Python-3.10+-blue?logo=python)
![Jupyter](https://img.shields.io/badge/Jupyter-Notebook-orange?logo=jupyter)
![scikit-learn](https://img.shields.io/badge/scikit--learn-1.3+-F7931E?logo=scikit-learn)
![pandas](https://img.shields.io/badge/pandas-2.0+-150458?logo=pandas)
![mplsoccer](https://img.shields.io/badge/mplsoccer-1.2+-green)

---

## License

This project is released under the [MIT License](LICENSE).  
Data is provided by StatsBomb under their [Open Data License](https://github.com/statsbomb/open-data/blob/master/LICENSE.pdf) — please read it before using the data in your own work.
