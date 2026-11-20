# Project Structure: where everything lives

```
student-performance-predictor/
│
├── README.md                  What the project is (start here)
├── CONTRIBUTING.md            How we use Git (branch → PR → review → merge)
├── requirements.txt           Python libraries: pip install -r requirements.txt
├── .gitignore
│
├── data/
│   ├── README.md              Where the data comes from + citation
│   ├── raw/                   Original files from UCI. NEVER edit these.
│   │   ├── student-por.csv    Portuguese: 649 rows, 33 columns (separator ;)
│   │   └── student-mat.csv    Math: 395 rows, same 33 columns
│   └── processed/             Cleaned data made by code (Part 1)
│
├── notebooks/                 Experiments and charts, one folder per part
│   ├── 01_data_study/         Part 1 · charts, correlation, cleaning
│   ├── 02_preparation/        Part 2 · split and preprocessing checks
│   ├── 03_grade_model/        Part 3 · Linear Regression, Tree, Forest
│   ├── 04_passfail_model/     Part 4 · Logistic Regression, Tree, KNN, threshold
│   └── 05_smart_features/     Part 5 · ranking, risk factors, what-if, similar students
│
├── src/                       Reusable code that the app imports
│   ├── config.py              Shared settings: seed 42, test size, file paths, pass mark, column lists
│   ├── data/
│   │   ├── load.py            Read both CSVs, add subject, student_id and fail (1,044 rows)
│   │   ├── clean.py           Cleaning rules + the G3 = 0 decision
│   │   ├── split.py           Split BY STUDENT (~80/20), with / without G1, G2 + CV folds
│   │   └── preprocess.py      One-hot encoding + scaling (fit on train only)
│   ├── models/
│   │   ├── train_grade.py     Train + save the grade model
│   │   └── train_passfail.py  Train + save the pass/fail model
│   ├── features/
│   │   ├── ranking.py         Sort a class by chance of failing
│   │   ├── explain.py         Main risk factors for one student
│   │   ├── recommend.py       What-if recommendations
│   │   └── similar.py         Similar students who passed (KNN)
│   └── predict.py             One function: student details → grade, pass/fail, chance of failing
│
├── models/                    Saved trained models (.joblib). Made by code, not by hand.
│
├── app/
│   ├── app.py                 Page 1 · Check one student (run: streamlit run app/app.py)
│   └── pages/
│       └── class_overview.py  Page 2 · Class overview
│
├── reports/
│   ├── figures/               Charts saved as .png for the report and slides
│   └── results/               Results tables (.csv) from the evaluation
│
├── tests/                     Checks: split ratio, column counts, predict() output
│
├── docs/
│   ├── PROJECT_STRUCTURE.md   This file
│   ├── TASKS.md               Every task, its owner, and what it waits for
│   ├── data_dictionary.md     Meaning of all 33 columns
│   └── findings.md            Key findings from the data study
│
└── scripts/
    └── create_issues.py       Creates all tasks as GitHub issues
```

## Who works where

| Part | Owner | Notebooks | Code in `src/` | Also writes |
|---|---|---|---|---|
| 1 · Study the data | Samnang | `notebooks/01_data_study/` | `data/load.py`, `data/clean.py` | `docs/data_dictionary.md`, `docs/findings.md`, `data/processed/`, app structure + `app/pages/class_overview.py` |
| 2 · Prepare the data | Rayu | `notebooks/02_preparation/` | `config.py`, `data/split.py`, `data/preprocess.py`, `predict.py` | form + result cards in `app/app.py` |
| 3 · Grade model | Rathana | `notebooks/03_grade_model/` | `models/train_grade.py` | `models/grade_*.joblib` |
| 4 · Pass/fail model | RithyReach | `notebooks/04_passfail_model/` | `models/train_passfail.py` | `models/passfail_*.joblib` |
| 5 · Smart features | Sophal | `notebooks/05_smart_features/` | `features/ranking.py`, `explain.py`, `recommend.py`, `similar.py` | their boxes in both app pages |
| Together | Everyone | — | — | `reports/results/`, `tests/`, final report |

## Rules that keep the repo clean

1. **Never edit `data/raw/`.** All cleaning happens in code (`src/data/clean.py`).
2. **Notebooks are for trying things. `src/` is for code others use.** When something works in a notebook, move it into a function in `src/`.
3. **Name notebooks with a number and your topic:** `01_grade_charts.ipynb`, `03_linear_regression.ipynb`.
4. **Save every chart you want in the report** to `reports/figures/` as `.png`, for example `fig_correlation.png`.
5. **Saved models only go in `models/`,** made by `src/models/train_*.py`, so anyone can make them again.
6. **Use `src/config.py` for paths and settings.** Never type `"data/raw/student-por.csv"` or `42` by hand in your code.
8. **Always split by student.** Use `get_split()` for train/test and `cv_splits()` for cross validation, so the same student is never on both sides.
7. **The app only imports from `src/`.** It never trains models itself.

## How a notebook imports from `src/`

Notebooks live two folders below the project root, so add this at the top:

```python
import sys; sys.path.append("../..")
from src.data.split import get_split
from src.data.preprocess import make_preprocessor
```
