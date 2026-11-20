# Part 4 · Pass/fail model · Ly RithyReach

**You own:** predicting pass or fail, and the chance of failing.
**You need:** Rayu's split (T08) and preprocessing (T09). **You work at the same time as Rathana (Part 3).**
**Your saved models are needed by:** Rayu's `predict()` (T10) and Sophal's risk factors (T20).

## Concepts you need

- **Classification:** the answer is a group: pass (0) or fail (1).
- **Logistic Regression:** gives a **probability** of failing (0 to 1). By default, 0.5 or more means "fail".
- **Confusion matrix:** a table of real answers vs predictions. It shows which mistakes the model makes.
- **Precision:** of the students we said would fail, how many really failed?
- **Recall:** of the students who really failed, how many did we catch? **This matters most for us.**
- **F1:** one number that combines precision and recall.
- **The accuracy trap:** only about 22% fail, so a model that always says "pass" gets about 78% accuracy and helps nobody.
- **Class weights (`class_weight="balanced"`):** makes the model pay more attention to the rare "fail" group.
- **Threshold:** lowering 0.5 to, say, 0.3 catches more failing students, but gives more false alarms.
- **KNN:** predicts by looking at the k most similar students in the training data.

## Your tasks

### T15 · Logistic Regression → `notebooks/04_passfail_model/01_logistic_regression.ipynb`
1. With G1/G2: `make_preprocessor` + `LogisticRegression(max_iter=2000)`.
2. Without G1/G2: same model.
3. Without G1/G2, balanced: add `class_weight="balanced"`.
4. Quick look at the confusion matrix and recall for fail for each.

### T16 · Decision Tree + KNN → `notebooks/04_passfail_model/02_tree_knn.ipynb`
1. `DecisionTreeClassifier` without G1/G2. Try `max_depth` 3, 5, 10 (and `class_weight="balanced"`).
2. `KNeighborsClassifier` without G1/G2. Try k = 3, 5, 7.
3. Use 5-fold cross validation on the **training** set to choose the settings, with `cv=cv_splits(X_train, f_train, groups)` (split by student).

### T17 · Threshold tuning → `notebooks/04_passfail_model/03_threshold.ipynb`
1. Get cross-validated probabilities on the **training** set with `cross_val_predict` and `cv_splits` (split by student).
2. For thresholds 0.5, 0.4, 0.3 and 0.2, count the failing students caught and the false alarms.
3. Suggest one threshold to the team.

### T18 · Train and save → `src/models/train_passfail.py`
1. One script that trains both final pass/fail models and saves them in `models/`:
   `passfail_with_grades.joblib` and `passfail_no_grades.joblib`.
2. Run it from the project folder: `python -m src.models.train_passfail`.

## Code hints

```python
# In a notebook
import sys; sys.path.append("../..")
from sklearn.pipeline import make_pipeline
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import confusion_matrix, classification_report
from src.data.split import get_split
from src.data.preprocess import make_preprocessor

X_train, X_test, g_train, g_test, f_train, f_test, groups = get_split(with_grades=False)
model = make_pipeline(make_preprocessor(X_train),
                      LogisticRegression(max_iter=2000, class_weight="balanced"))
model.fit(X_train, f_train)
pred = model.predict(X_test)
print(confusion_matrix(f_test, pred))   # [[pass→pass, pass→fail], [fail→pass, fail→fail]]
print(classification_report(f_test, pred, target_names=["pass", "fail"]))
```

```python
# Threshold tuning on the TRAINING set only (T17)
from sklearn.model_selection import cross_val_predict
from src.data.split import cv_splits
p_fail = cross_val_predict(model, X_train, f_train, cv=cv_splits(X_train, f_train, groups),
                           method="predict_proba")[:, 1]
for t in [0.5, 0.4, 0.3, 0.2]:
    caught = ((p_fail >= t) & (f_train == 1)).sum()
    alarms = ((p_fail >= t) & (f_train == 0)).sum()
    print(t, "caught:", caught, "false alarms:", alarms)
```

```python
# src/models/train_passfail.py
import joblib
from sklearn.pipeline import make_pipeline
from sklearn.linear_model import LogisticRegression
from src.config import MODELS_DIR
from src.data.split import get_split
from src.data.preprocess import make_preprocessor

def train_and_save():
    for with_grades, name in [(True, "passfail_with_grades"), (False, "passfail_no_grades")]:
        X_train, X_test, g_train, g_test, f_train, f_test, groups = get_split(with_grades)
        model = make_pipeline(make_preprocessor(X_train),
                              LogisticRegression(max_iter=2000, class_weight="balanced"))
        model.fit(X_train, f_train)
        joblib.dump(model, MODELS_DIR / f"{name}.joblib")

if __name__ == "__main__":
    train_and_save()
```

Keep Logistic Regression as the saved model: Sophal's risk-factor code reads its weights.
