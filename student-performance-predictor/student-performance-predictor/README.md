# Student Performance Predictor

A machine learning project that predicts a student's **final grade** and whether they will **pass or fail**, so teachers can find students who need help early, while there is still time to help them.

*Fundamentals of Machine Learning · Software Engineering, Generation 10 · CADT Institute of Digital Technology*

## Purpose

Teachers often find out a student is failing only after the final exam, when it is too late. Schools already record attendance, study time and past grades, but rarely use this data to look ahead. This project turns that data into an early warning.

## Objectives

1. Study the data with charts to find what affects students' grades the most.
2. Clean and prepare the data so the models can use it.
3. Predict the final grade (0–20) with **Linear Regression**.
4. Predict pass (grade ≥ 10) or fail with **Logistic Regression**.
5. Test both models on unseen data, with and without the earlier grades G1 and G2, to see how early we can warn.
6. Build a simple web page where a teacher enters a student's details and sees the prediction.

## Dataset

[UCI Student Performance](https://archive.ics.uci.edu/dataset/320/student+performance) (details in [data/README.md](data/README.md)), both subjects combined: Portuguese (`student-por.csv`, 649 rows) and Math (`student-mat.csv`, 395 rows) = **1,044 records from 662 students**, 33 columns each (study time, absences, past failures, family background, and grades G1, G2, G3), plus a `subject` column. We always split by student so no one appears in both training and test.

## Tools

Python · pandas · scikit-learn · matplotlib · seaborn · Jupyter · Streamlit

## Project structure

```
data/raw/        original dataset (never edited)
data/processed/  cleaned data made by code
notebooks/       experiments, one folder per part (01–05)
src/             reusable code: data/, models/, features/, predict.py
models/          saved trained models
app/             Streamlit web page (2 pages)
reports/         figures and results tables
tests/           checks
docs/            task map, data dictionary, findings
```

Full map of every folder and who works where: [docs/PROJECT_STRUCTURE.md](docs/PROJECT_STRUCTURE.md)

## Team

| Part | Member |
|---|---|
| 1 · Study the data | Tep Samnang |
| 2 · Prepare the data | Choeng Rayu |
| 3 · Grade model | Rathana Asinike |
| 4 · Pass/fail model | Ly RithyReach |
| 5 · Smart features | Sophal Taingchhay |

- Who does what and the order of work: [docs/TEAM_PLAN.md](docs/TEAM_PLAN.md)
- Every task and what it waits for: [docs/TASKS.md](docs/TASKS.md)
- Each member's guide (concepts, steps, code hints): [docs/tasks/](docs/tasks/)
- How we use Git: [CONTRIBUTING.md](CONTRIBUTING.md)

> This tool supports teachers. A prediction is a reason to talk with a student, not a final decision.
