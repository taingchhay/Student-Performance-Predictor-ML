# Part 3 · Grade model · Rathana Asinike

**You own:** predicting the final grade (0–20).
**You need:** Rayu's split (T08) and preprocessing (T09). **You work at the same time as RithyReach (Part 4).**
**Your saved models are needed by:** Rayu's `predict()` (T10).

## Concepts you need

- **Regression:** the answer is a number (a grade from 0 to 20), not a group.
- **Linear Regression:** gives each feature a weight and adds them up: grade ≈ w₁·studytime + w₂·failures + … + b. A positive weight raises the grade, a negative weight lowers it.
- **Two versions:** with G1/G2 (accurate, but those grades come late in the year) and without (early warning, harder).
- **Decision Tree:** splits students into groups with yes/no questions ("failures > 0?"). `max_depth` limits how many questions, which stops it from memorising (overfitting).
- **Random Forest:** many trees, each trained on a random part of the data, averaged together. Usually more accurate than one tree.
- **Scores you'll see** (the team evaluates them together): MAE = average error in grade points, RMSE = like MAE but punishes big errors more, R² = how much of the grade the model explains (1 = perfect).

## Your tasks

### T11 · Linear Regression → `notebooks/03_grade_model/01_linear_regression.ipynb`
1. Get the split with G1/G2 and train `make_preprocessor` + `LinearRegression`.
2. Repeat with the split without G1/G2.
3. Limit predictions to 0–20 with `np.clip`.
4. Quick check of MAE on the test set for both versions.

### T12 · Decision Tree + Random Forest → `notebooks/03_grade_model/02_tree_forest.ipynb`
1. `DecisionTreeRegressor` without G1/G2. Try `max_depth` 3, 5, 10.
2. `RandomForestRegressor` without G1/G2. Try `n_estimators` 100 and 300.
3. Use 5-fold cross validation on the **training** set to choose the settings, with `cv=cv_splits(X_train, f_train, groups)` (split by student).

### T13 · Factors that raise or lower the grade → `notebooks/03_grade_model/03_factors.ipynb`
1. Take the Linear Regression weights and match them to column names.
2. Bar chart of the top 5 that raise and the top 5 that lower the grade. Save it to `reports/figures/`.

### T14 · Train and save → `src/models/train_grade.py`
1. One script that trains both final grade models and saves them in `models/`:
   `grade_with_grades.joblib` and `grade_no_grades.joblib`.
2. Run it from the project folder: `python -m src.models.train_grade`.

## Code hints

```python
# In a notebook
import sys; sys.path.append("../..")
import numpy as np
from sklearn.pipeline import make_pipeline
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error
from src.data.split import get_split
from src.data.preprocess import make_preprocessor

X_train, X_test, g_train, g_test, f_train, f_test, groups = get_split(with_grades=False)
model = make_pipeline(make_preprocessor(X_train), LinearRegression())
model.fit(X_train, g_train)
pred = np.clip(model.predict(X_test), 0, 20)
print("MAE:", mean_absolute_error(g_test, pred))
```

```python
# Weights matched to column names (T13)
import pandas as pd
prep, lr = model.named_steps["columntransformer"], model.named_steps["linearregression"]
weights = pd.Series(lr.coef_, index=prep.get_feature_names_out()).sort_values()
print(weights.head(5))   # lower the grade most
print(weights.tail(5))   # raise the grade most
```

```python
# src/models/train_grade.py
import joblib
from sklearn.pipeline import make_pipeline
from sklearn.linear_model import LinearRegression
from src.config import MODELS_DIR
from src.data.split import get_split
from src.data.preprocess import make_preprocessor

def train_and_save():
    for with_grades, name in [(True, "grade_with_grades"), (False, "grade_no_grades")]:
        X_train, X_test, g_train, g_test, f_train, f_test, groups = get_split(with_grades)
        model = make_pipeline(make_preprocessor(X_train), LinearRegression())
        model.fit(X_train, g_train)
        joblib.dump(model, MODELS_DIR / f"{name}.joblib")

if __name__ == "__main__":
    train_and_save()
```

```python
# Cross validation split by student (T12)
from sklearn.model_selection import cross_val_score
from src.data.split import cv_splits
scores = cross_val_score(model, X_train, g_train, cv=cv_splits(X_train, f_train, groups),
                         scoring="neg_mean_absolute_error")
print("CV MAE:", -scores.mean())
```

If Random Forest turns out clearly better after the team's evaluation, swap `LinearRegression()` for it in this script.
