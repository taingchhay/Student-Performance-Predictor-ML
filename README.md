# Student-Performance-Predictor-ML
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

[UCI Student Performance](https://archive.ics.uci.edu/dataset/320/student+performance), Portuguese class file (`student-por.csv`): 649 students, 33 columns (study time, absences, past failures, family background, and grades G1, G2, G3).

## Tools

Python · pandas · scikit-learn · matplotlib · seaborn · Jupyter · Streamlit

## Project structure

```
data/        dataset
notebooks/   data analysis and model experiments
src/         preprocessing, split and predict code
models/      saved models
app/         Streamlit web page
report/      final report
```

## Team

Sophal Taingchhay · Tep Samnang · Choeng Rayu · Rathana Asinike · Ly RithyReach
