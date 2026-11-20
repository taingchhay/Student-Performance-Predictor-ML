# Data

## Dataset

**Student Performance**, UCI Machine Learning Repository. We use **both subjects together**.

- Official page: https://archive.ics.uci.edu/dataset/320/student+performance
- Download (zip): https://archive.ics.uci.edu/static/public/320/student+performance.zip
- Collected from school reports and student questionnaires at two Portuguese secondary schools (GP and MS)
- License: CC BY 4.0

## Files in `raw/` (never edit these)

| File | Subject | Rows | Students who fail (G3 < 10) |
|---|---|---|---|
| `student-por.csv` | Portuguese | 649 | 100 (15%) |
| `student-mat.csv` | Math | 395 | 130 (33%) |
| **Combined** | both | **1,044** | **230 (22%)** |

Both files have the same 33 columns: 30 features + 3 grades (G1, G2, G3, each 0–20). Separator is `;` (not `,`). No missing values, no duplicate rows.

## How we combine them (`src/data/load.py`)

1. Read both files and add a `subject` column (`portuguese` or `math`).
2. Stack them into one table: **1,044 rows**, one row per student per subject.
3. Add `student_id`. **382 students appear in both files.** They are matched on 13 columns (school, sex, age, address, famsize, Pstatus, Medu, Fedu, Mjob, Fjob, reason, nursery, internet), so the same person gets the same ID. There are 662 different students.
4. Add `fail` = 1 when G3 < 10.

**Why `student_id` matters:** if the same student is in both the training and the test set, the test score looks better than it really is (data leakage). So we always **split by student** (`src/data/split.py`): one student's rows stay together on one side.

## `processed/`

`students_clean.csv` is made by `src/data/clean.py`. Never make or edit it by hand.

## Citation

Cortez, P. (2008). *Student Performance* [Dataset]. UCI Machine Learning Repository. https://doi.org/10.24432/C5TG7T

Cortez, P., & Silva, A. (2008). Using data mining to predict secondary school student performance. In *Proceedings of the 5th Future Business Technology Conference (FUBUTEC 2008)* (pp. 5–12). EUROSIS.
