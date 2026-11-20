# Team Plan

The project has **5 Machine Learning parts**, done in order like a relay. Everyone owns one ML part, everyone helps build the web app, and **evaluation, testing, the report and the presentation are done together**.

- Every task, its owner and what it waits for: [`TASKS.md`](TASKS.md)
- Where every file goes: [`PROJECT_STRUCTURE.md`](PROJECT_STRUCTURE.md)
- Your own guide (concepts, steps, code hints): [`tasks/`](tasks/)

## Who does what

| Part | Member | ML work | Web work | Guide |
|---|---|---|---|---|
| 1 · Study the data | Tep Samnang | Data dictionary, charts, correlation, cleaning, G3 = 0 decision | App structure + Class overview screen | [part1-samnang-data-study.md](tasks/part1-samnang-data-study.md) |
| 2 · Prepare the data | Choeng Rayu | Shared settings, split, preprocessing, `predict()` | Check one student screen (form + result cards) | [part2-rayu-data-preparation.md](tasks/part2-rayu-data-preparation.md) |
| 3 · Grade model | Rathana Asinike | Linear Regression, Decision Tree, Random Forest, factors that raise or lower the grade | — | [part3-rathana-grade-model.md](tasks/part3-rathana-grade-model.md) |
| 4 · Pass/fail model | Ly RithyReach | Logistic Regression, Decision Tree, KNN, threshold tuning | — | [part4-rithyreach-passfail-model.md](tasks/part4-rithyreach-passfail-model.md) |
| 5 · Smart features | Sophal Taingchhay | Risk ranking, risk factors, what-if recommendations, similar students (KNN) | Plugs these into both screens | [part5-sophal-smart-features.md](tasks/part5-sophal-smart-features.md) |

Parts 1 and 2 finish first, so Samnang and Rayu build the web screens while Parts 3–5 are in progress. Parts 3–5 then plug their results into the screens.

## The flow

```
Part 1  Study the data        (Samnang)
   ↓    clean data + G3 = 0 decision
Part 2  Prepare the data      (Rayu)
   ↓    train/test split + preprocessing
Part 3  Grade model (Rathana)  ║  Part 4  Pass/fail model (RithyReach)    ← these two run at the same time
   ↓    saved models
Part 2  predict()             (Rayu)
   ↓
Part 5  Smart features        (Sophal)
   ↓
Together: evaluation · testing · report · presentation
```

**Relay with overlap:** the next person can start preparing before the previous part is finished.
Rayu can write the settings and preprocessing while Samnang is still making charts. Rathana and RithyReach can practise their model code on a quick test split. Sophal can write the feature functions using a simple practice model. Samnang and Rayu can build the screens with example numbers.

## Done together

| What | When |
|---|---|
| Repo setup | Day 1 |
| Evaluation: metrics, 5-fold cross validation, baselines, results table | After Parts 3 and 4 |
| Testing: code reviews, testing the app with example students, screen wording, ethics note | After Part 5 |
| Final report and presentation | At the end |

## Shared rules

- We use **both subjects (1,044 records, 662 students)**. Always use **seed 42** and the **shared split by student** from `src/data/split.py` (`get_split()` and `cv_splits()`), so everyone's numbers match and no student is in both train and test.
- The **test set is used only once**, for the final score. Choose settings with cross validation on the training set.
- Fail = **1** (G3 < 10). We care most about **recall for fail**: catching the students who will fail.
- Every change goes through a pull request and one teammate checks it. See [`../CONTRIBUTING.md`](../CONTRIBUTING.md).
- Stuck for more than one day? Tell the team. Whoever is free helps the person blocking the others.
