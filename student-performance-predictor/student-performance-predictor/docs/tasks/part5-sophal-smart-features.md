# Part 5 · Smart features · Sophal Taingchhay

**You own:** the ML features built on top of the models: ranking, risk factors, what-if recommendations and similar students.
**You need:** Rayu's `predict()` (T10), RithyReach's saved pass/fail model (T18), and Rayu's preprocessing (T09).
**Web work:** you plug your features into both screens (W5, W6).

**Start early:** while Parts 3 and 4 are training, write your functions against a quick practice model, then switch to the real saved models.

## Concepts you need

- **Subject matters:** Math is harder (33% fail vs 15% in Portuguese), so the same student can be at risk in Math but not in Portuguese. Always pass the subject into your functions.
- **Ranking by probability:** the pass/fail model gives each student a chance of failing. Sorting by it tells the teacher who to help first.
- **Risk factors (contributions):** in Logistic Regression, each feature's push on the risk = its weight × the student's (scaled) value. The biggest positive pushes are the main risk factors *for this student*.
- **What-if analysis:** change one thing the student can control (study time, absences…), ask the model again, and see how much the risk drops. This is how the recommendations work.
- **KNN (nearest neighbours):** after preprocessing, every student is a point. The closest points to a student are the most similar students. Looking at the closest students **who passed** shows what they did differently.
- **Correlation is not cause:** the model shows links in the data. A recommendation means "linked with lower risk", never "this will make them pass".

## Your tasks

### T19 · Class risk ranking → `src/features/ranking.py`
1. `rank_class(students)`: for every student in an uploaded table, get the chance of failing and the predicted grade.
2. Label each one high (≥ 50%), medium (25–50%) or low (< 25%).
3. Sort from highest to lowest risk.

### T20 · Main risk factors → `src/features/explain.py`
1. `top_factors(details)`: the 3–4 features pushing this student's risk up the most.
2. Turn feature names like `num__failures` into readable words for the screen ("Past failed classes").

### T21 · What-if recommendations → `src/features/recommend.py`
1. List the factors a student can change and a better value for each.
2. For each, change only that one value and get the new risk.
3. Return the top 3 changes that lower the risk most, for example "Study time 1 → 3: 68% → 49%".

### T22 · Similar students who passed → `src/features/similar.py`
1. Fit `NearestNeighbors` on the preprocessed students who passed **in the same subject**.
2. Find the 5 closest to this student.
3. Compare their habits with the student's and return 2–3 short sentences.

### W5 · Connect the ranking → `app/pages/class_overview.py`
1. Replace Samnang's example numbers with `rank_class(uploaded_csv)`.
2. Fill the summary cards (students, at risk) from the real result.

### W6 · Boxes on the Check one student screen → `app/app.py`
1. "Why: main risk factors" box from `top_factors`.
2. "Recommendations" table from `what_if`, with the note "links in the data, not promises".
3. "Similar students who passed usually…" tags from `similar_passed`.

## Code hints

```python
# src/features/ranking.py
import pandas as pd
from src.predict import load_models, to_row

def rank_class(students: pd.DataFrame, with_grades=False):
    grade_model, passfail_model = load_models(with_grades)
    rows = pd.concat([to_row(r.to_dict(), passfail_model.feature_names_in_)
                      for _, r in students.iterrows()], ignore_index=True)
    out = students.copy().reset_index(drop=True)
    out["p_fail"] = passfail_model.predict_proba(rows)[:, 1]
    out["grade"] = grade_model.predict(rows).clip(0, 20).round(1)
    out["risk"] = pd.cut(out["p_fail"], [0, 0.25, 0.5, 1.0],
                         labels=["low", "medium", "high"], include_lowest=True)
    return out.sort_values("p_fail", ascending=False)
```

```python
# src/features/explain.py
import pandas as pd
from src.predict import load_models, to_row

def top_factors(details, n=4, with_grades=False):
    _, model = load_models(with_grades)
    prep = model.named_steps["columntransformer"]
    clf = model.named_steps["logisticregression"]
    x = prep.transform(to_row(details, model.feature_names_in_))[0]
    push = pd.Series(clf.coef_[0] * x, index=prep.get_feature_names_out())
    return push[push > 0].sort_values(ascending=False).head(n)
```

```python
# src/features/recommend.py
from src.predict import load_models, to_row, TYPICAL

CHANGES = {"studytime": 3, "absences": 2, "goout": 2, "schoolsup": "yes", "paid": "yes"}

def what_if(details, n=3, with_grades=False):
    _, model = load_models(with_grades)
    cols = model.feature_names_in_
    base = model.predict_proba(to_row(details, cols))[0, 1]
    results = []
    for col, better in CHANGES.items():
        p = model.predict_proba(to_row({**details, col: better}, cols))[0, 1]
        if p < base:
            results.append((col, details.get(col, TYPICAL[col]), better, round(float(base), 2), round(float(p), 2)))
    return sorted(results, key=lambda r: r[4])[:n]
```

```python
# src/features/similar.py
import pandas as pd
from sklearn.neighbors import NearestNeighbors
from src.config import PROCESSED_DATA
from src.predict import to_row
from src.data.preprocess import make_preprocessor

def similar_passed(details, k=5):
    """The k most similar students who passed, in the same subject."""
    data = pd.read_csv(PROCESSED_DATA)
    passed = data[data["fail"] == 0]
    if "subject" in details:
        passed = passed[passed["subject"] == details["subject"]]
    passed = passed.drop(columns=["G1", "G2", "G3", "fail", "student_id"])
    prep = make_preprocessor(passed).fit(passed)
    knn = NearestNeighbors(n_neighbors=k).fit(prep.transform(passed))
    _, idx = knn.kneighbors(prep.transform(to_row(details, passed.columns)))
    return passed.iloc[idx[0]]
```

```python
# Trying it in a notebook
import sys; sys.path.append("../..")
from src.features.explain import top_factors
from src.features.recommend import what_if
student = {"subject": "math", "school": "MS", "studytime": 1, "failures": 1, "absences": 10, "higher": "no"}
print(top_factors(student))
print(what_if(student))
```
