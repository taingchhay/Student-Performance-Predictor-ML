# Part 2 · Prepare the data · Choeng Rayu

**You own:** the shared settings, the train/test split, preprocessing, and `predict()`.
**You need:** Samnang's cleaning (T05) for the split. **Parts 3 and 4 wait for your split and preprocessing.**
**Web work:** the Check one student screen (form and result cards).

## Concepts you need

- **Train/test split:** train on about 80% of the data, keep about 20% hidden to test fairly.
- **Stratified:** both parts keep the same pass/fail ratio (about 78% / 22%).
- **Split by student (grouped split):** 382 students are in both the Math and Portuguese files. If one of their rows is in training and the other in test, the model has already "seen" that student, and the score looks better than it is. `StratifiedGroupKFold` keeps all rows of a student on the same side, using `student_id`.
- **One-hot encoding:** turns a text column into 0/1 columns. `Mjob` has 5 values, so it becomes 5 columns. Yes/no columns become one 0/1 column.
- **Scaling (StandardScaler):** `(value − mean) ÷ std`, so absences (0–32) don't overpower studytime (1–4).
- **Data leakage:** learning anything from the test set (even its mean). Prevent it by fitting the scaler on training data only. Putting the preprocessor inside a pipeline does this for you.
- **Pipeline:** preprocessing + model in one object, so new students go through exactly the same steps.
- **Typical values:** the web form doesn't ask all 30 questions. Missing answers are filled with the most common value (text) or the median (numbers).

## Your tasks

### T07 · Shared settings → `src/config.py`
1. File paths for both raw files, seed 42, number of folds, pass mark 10, and the 13 `STUDENT_KEYS`. Everyone imports from here.
2. **Merge this first.** It's small and everyone needs it.

### T08 · Split → `src/data/split.py`
1. `get_split(with_grades)` splits **by student** and returns 7 parts (the last one is the training students' IDs).
2. `cv_splits(...)` gives 5 cross-validation folds inside the training set, also by student. Everyone uses it for CV.
3. Two versions: with G1/G2 and without them (the early-warning version).
4. Check: 835 train rows, 209 test rows, about 22% fail in both, and **no student_id in both**.

### T09 · Preprocessing → `src/data/preprocess.py`
1. `make_preprocessor(X)`: scale number columns, one-hot encode text columns.
2. Check: 44 columns after preprocessing without G1/G2, 46 with them (the `subject` column adds one).

### T10 · Prediction → `src/predict.py` (after Parts 3 and 4 save their models)
1. `load_models(with_grades)` loads the grade and pass/fail models.
2. `to_row(details, columns)` fills in missing answers with typical values.
3. `predict_student(details)` returns the grade (0–20), pass/fail and the chance of failing.

### W3 · Check one student form → `app/app.py`
1. A switch: Early in term (no G1, G2) or Mid-term (with G1, G2), and a subject choice (Math or Portuguese).
2. Inputs: school, age, study time, past failures, absences, going out, parents' education.
3. Checkboxes: plans university, internet at home, paid classes, school support. Then a Predict button.

### W4 · Result cards → `app/app.py`
1. Three cards with `st.metric`: predicted grade, Pass/Fail, chance of failing.
2. An at-risk warning with `st.warning` when the chance is 50% or more.

## Code hints

```python
# src/config.py
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]      # project folder
RAW_PORTUGUESE = ROOT / "data" / "raw" / "student-por.csv"
RAW_MATH = ROOT / "data" / "raw" / "student-mat.csv"
PROCESSED_DATA = ROOT / "data" / "processed" / "students_clean.csv"
MODELS_DIR = ROOT / "models"

SEED = 42
PASS_MARK = 10          # pass = G3 >= 10
N_FOLDS = 5             # 1 fold (about 20%) is the test set; 5-fold CV inside training

# The 13 columns that identify the same student in both files
STUDENT_KEYS = ["school", "sex", "age", "address", "famsize", "Pstatus", "Medu", "Fedu",
                "Mjob", "Fjob", "reason", "nursery", "internet"]
```

```python
# src/data/split.py
import pandas as pd
from sklearn.model_selection import StratifiedGroupKFold
from src.config import PROCESSED_DATA, SEED, N_FOLDS

def get_split(with_grades=True):
    """Split BY STUDENT: the same student never appears in both train and test.
    Returns X_train, X_test, grade_train, grade_test, fail_train, fail_test, groups_train."""
    df = pd.read_csv(PROCESSED_DATA)
    drop = ["G3", "fail", "student_id"] + ([] if with_grades else ["G1", "G2"])
    X, groups = df.drop(columns=drop), df["student_id"]
    cv = StratifiedGroupKFold(n_splits=N_FOLDS, shuffle=True, random_state=SEED)
    train, test = next(cv.split(X, df["fail"], groups))      # first fold = test set (~20%)
    return (X.iloc[train], X.iloc[test], df["G3"].iloc[train], df["G3"].iloc[test],
            df["fail"].iloc[train], df["fail"].iloc[test], groups.iloc[train])

def cv_splits(X_train, fail_train, groups_train):
    """5 folds for cross validation inside the training set, also split by student.
    Use as: cross_val_score(model, X_train, y, cv=cv_splits(X_train, fail_train, groups_train))"""
    cv = StratifiedGroupKFold(n_splits=N_FOLDS, shuffle=True, random_state=SEED)
    return list(cv.split(X_train, fail_train, groups_train))
```

```python
# src/data/preprocess.py
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import StandardScaler, OneHotEncoder

def make_preprocessor(X):
    text_cols = X.select_dtypes(exclude="number").columns
    num_cols = X.select_dtypes(include="number").columns
    return ColumnTransformer([
        ("num", StandardScaler(), num_cols),
        ("text", OneHotEncoder(drop="if_binary", handle_unknown="ignore"), text_cols),
    ])
```

```python
# src/predict.py
import joblib
import numpy as np
import pandas as pd
from src.config import MODELS_DIR, PROCESSED_DATA

_data = pd.read_csv(PROCESSED_DATA)
TYPICAL = {c: (_data[c].median() if pd.api.types.is_numeric_dtype(_data[c]) else _data[c].mode()[0])
           for c in _data.columns if c not in ("G3", "fail", "student_id")}

def load_models(with_grades=False):
    tag = "with_grades" if with_grades else "no_grades"
    return (joblib.load(MODELS_DIR / f"grade_{tag}.joblib"),
            joblib.load(MODELS_DIR / f"passfail_{tag}.joblib"))

def to_row(details, columns):
    row = {c: details.get(c, TYPICAL[c]) for c in columns}
    return pd.DataFrame([row])

def predict_student(details, with_grades=False):
    grade_model, passfail_model = load_models(with_grades)
    X = to_row(details, passfail_model.feature_names_in_)
    grade = float(np.clip(grade_model.predict(X)[0], 0, 20))
    p_fail = float(passfail_model.predict_proba(X)[0, 1])
    return {"grade": round(grade, 1), "fail": p_fail >= 0.5, "p_fail": round(p_fail, 3)}
```

```python
# Result cards in app/app.py
from src.predict import predict_student
result = predict_student(details, with_grades=mid_term)
c1, c2, c3 = st.columns(3)
c1.metric("Predicted final grade", f"{result['grade']} / 20")
c2.metric("Result", "Fail" if result["fail"] else "Pass")
c3.metric("Chance of failing", f"{result['p_fail']:.0%}")
if result["p_fail"] >= 0.5:
    st.warning("At risk: talk with this student this week.")
```
