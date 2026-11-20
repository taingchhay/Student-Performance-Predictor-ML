# Task Map: who starts first, and what waits for what

**Rule:** you can start a task only when every task in its **Needs** column is merged into `main`.
"—" means you can start right away.

## Part 1 · Study the data · Samnang

| ID | Task | Needs | Output |
|---|---|---|---|
| T01 | Data dictionary (all 33 columns) | — | `docs/data_dictionary.md` |
| T02 | Load function (both subjects, add subject, student_id, fail) | — | `src/data/load.py` |
| T03 | Grade histograms + pass/fail count | T02 | `notebooks/01_data_study/` |
| T04 | Correlation, box plots, fail-rate charts | T02 | `notebooks/01_data_study/`, `reports/figures/` |
| T05 | Cleaning rules + G3 = 0 decision (**Part 2 waits for this**) | T02 | `src/data/clean.py`, `data/processed/` |
| T06 | Key findings (5–10 factors that matter most) | T03, T04, T05 | `docs/findings.md` |

## Part 2 · Prepare the data · Rayu

| ID | Task | Needs | Output |
|---|---|---|---|
| T07 | Shared settings | — | `src/config.py` |
| T08 | Split by student (train/test + CV folds), with and without G1, G2 | T05, T07 | `src/data/split.py` |
| T09 | Preprocessing (one-hot + scaling) | T07 | `src/data/preprocess.py` |
| T10 | Prediction function | T14, T18 | `src/predict.py` |

## Part 3 · Grade model · Rathana

| ID | Task | Needs | Output |
|---|---|---|---|
| T11 | Linear Regression, with and without G1, G2 | T08, T09 | `notebooks/03_grade_model/` |
| T12 | Decision Tree + Random Forest for the grade | T11 | `notebooks/03_grade_model/` |
| T13 | Factors that raise or lower the grade | T11 | `notebooks/03_grade_model/` |
| T14 | Train + save the final grade models | T11 | `src/models/train_grade.py`, `models/grade_*.joblib` |

## Part 4 · Pass/fail model · RithyReach

| ID | Task | Needs | Output |
|---|---|---|---|
| T15 | Logistic Regression: with G1/G2, without, balanced | T08, T09 | `notebooks/04_passfail_model/` |
| T16 | Decision Tree + KNN for pass/fail | T15 | `notebooks/04_passfail_model/` |
| T17 | Threshold tuning (0.5, 0.4, 0.3, 0.2) | T15 | `notebooks/04_passfail_model/` |
| T18 | Train + save the final pass/fail models | T15 | `src/models/train_passfail.py`, `models/passfail_*.joblib` |

## Part 5 · Smart features · Sophal

| ID | Task | Needs | Output |
|---|---|---|---|
| T19 | Class risk ranking | T10 | `src/features/ranking.py` |
| T20 | Main risk factors for one student | T18 | `src/features/explain.py` |
| T21 | What-if recommendations | T10 | `src/features/recommend.py` |
| T22 | Similar students who passed (KNN) | T09 | `src/features/similar.py` |

## Web app (shared)

| ID | Task | Owner | Needs | Output |
|---|---|---|---|---|
| W1 | App structure + navigation (2 pages, load models once) | Samnang | — | `app/app.py`, `app/pages/` |
| W2 | Class overview screen with example data (upload, summary cards, table) | Samnang | W1 | `app/pages/class_overview.py` |
| W3 | Check one student form | Rayu | W1 | `app/app.py` |
| W4 | Result cards + at-risk warning, connected to `predict()` | Rayu | T10, W3 | `app/app.py` |
| W5 | Connect the ranking to the Class overview screen | Sophal | W2, T19 | `app/pages/class_overview.py` |
| W6 | Risk factors, recommendations and similar students boxes | Sophal | W3, T20, T21, T22 | `app/app.py` |

## Together (everyone)

| ID | Task | Needs |
|---|---|---|
| E1 | Evaluate all models: metrics, 5-fold cross validation, baselines, results table | T11–T18 |
| E2 | Test the app with example students, check wording and ethics note | W4, W5, W6 |
| E3 | Final report and presentation | E1, E2 |

## The chain that decides how fast we finish

```
T02 → T05 (Samnang: load + cleaning)
  → T08 (Rayu: split)  +  T09 (Rayu: preprocessing)
    → T11 / T15 (Rathana / RithyReach: first models)
      → T14 + T18 (save models)
        → T10 (Rayu: predict)
          → T19, T21 (Sophal) → W4, W5, W6 (screens)
```

If a task on this chain is late, everything after it waits. Help these people first.
