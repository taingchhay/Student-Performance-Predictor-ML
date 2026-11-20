# Part 1 · Study the data · Tep Samnang

**You own:** understanding and cleaning the data. **You go first**, so Part 2 waits for your cleaning (T05).
**Web work:** the app structure and the Class overview screen, built while the others train models.

## Concepts you need

- **Combining two files:** we use the Portuguese file (649 rows) and the Math file (395 rows) together = 1,044 rows, with a `subject` column. 382 students are in both files, so each student gets a `student_id` (matched on 13 columns). Part 2 uses it to split by student.
- **EDA (Exploratory Data Analysis):** looking at the data with charts *before* building models, to find patterns and problems.
- **Histogram:** shows how values are spread, for example how many students got each grade.
- **Correlation:** a number from −1 to +1 showing how strongly two columns move together. G2 and G3 ≈ +0.92 (very strong). It shows a link, not a cause.
- **Box plot:** shows the middle, spread and outliers of a number for each group, for example G3 for each study-time level.
- **Data cleaning:** fixing problems in the data with code (duplicates, strange values), never by editing the raw file.
- **The G3 = 0 question:** 15 students have a final grade of 0. They probably left school. Decide with the team whether to keep them (they count as fail) or remove them for the grade model.

## Your tasks

### T01 · Data dictionary → `docs/data_dictionary.md`
1. Open `student.txt` from the official UCI zip (see `data/README.md`), or read the CSV header.
2. For all 33 columns write: name, meaning, type (number or text), and range or values.
3. Add the 3 columns we create: `subject`, `student_id`, `fail`.

### T02 · Load function → `src/data/load.py`
1. Write `load_raw()`: read both CSVs (separator `;`), add `subject`, stack them.
2. Add `student_id` from the 13 `STUDENT_KEYS` in `src/config.py`, and the `fail` column (1 if G3 < 10).
3. Check: 1,044 rows, 662 different students, 230 fail.
4. Use the paths from `src/config.py` (if Rayu hasn't merged it yet, agree the names with him).

### T03 · Grade charts → `notebooks/01_data_study/01_grades.ipynb`
1. Histograms of G1, G2 and G3.
2. Count pass vs fail with a bar chart, per subject. Expect 814 pass and 230 fail in total (Math 33% fail, Portuguese 15%).
3. Save the charts to `reports/figures/`.

### T04 · Relationship charts → `notebooks/01_data_study/02_relationships.ipynb`
1. Correlation heatmap of the number columns.
2. Box plots of G3 by `studytime` and by `failures`.
3. Fail rate by text columns: `subject`, `school`, `sex`, `internet`, `higher`, `Mjob` (bar charts).
4. One sentence under each chart saying what it shows.

### T05 · Cleaning → `src/data/clean.py`, `data/processed/students_clean.csv`
1. Check missing values, duplicates and out-of-range values.
2. Bring the G3 = 0 question to the team and write the decision in `clean()`.
3. `make_processed()` saves the clean file. **Merge this early: Part 2 needs it.**

### T06 · Key findings → `docs/findings.md`
1. List the 5–10 factors that matter most, one line each, with the chart that shows it.

### W1 · App structure → `app/app.py`, `app/pages/`
1. Make the two-page app: `app/app.py` (Check one student) and `app/pages/class_overview.py`.
2. Load the models once with `@st.cache_resource` so both pages reuse them.
3. Check it runs: `streamlit run app/app.py`.

### W2 · Class overview screen → `app/pages/class_overview.py`
1. CSV upload button and a "download template" button.
2. Three summary cards: number of students, number at risk, model used.
3. A table for the ranked students. Use example numbers for now. Sophal connects the real ranking later (W5).

## Code hints

```python
# src/data/load.py
import pandas as pd
from src.config import RAW_PORTUGUESE, RAW_MATH, PASS_MARK, STUDENT_KEYS

def load_raw():
    """Both subjects in one table: one row per student per subject."""
    por = pd.read_csv(RAW_PORTUGUESE, sep=";").assign(subject="portuguese")
    mat = pd.read_csv(RAW_MATH, sep=";").assign(subject="math")
    df = pd.concat([por, mat], ignore_index=True)
    # Same student in both files -> same student_id (used to split by student)
    df["student_id"] = df[STUDENT_KEYS].astype(str).agg("|".join, axis=1).factorize()[0]
    df["fail"] = (df["G3"] < PASS_MARK).astype(int)    # 1 = fail
    return df
```

```python
# src/data/clean.py
from src.config import PROCESSED_DATA
from src.data.load import load_raw

def clean(df):
    df = df.drop_duplicates()
    # Team decision on G3 = 0 goes here. Default: keep them (they count as fail).
    return df

def make_processed():
    df = clean(load_raw())
    df.to_csv(PROCESSED_DATA, index=False)
    return df
```

```python
# In a notebook (two folders below the project root)
import sys; sys.path.append("../..")
import seaborn as sns, matplotlib.pyplot as plt
from src.data.load import load_raw

df = load_raw()
sns.heatmap(df.select_dtypes("number").corr(), cmap="RdBu_r", center=0)
plt.savefig("../../reports/figures/fig_correlation.png", bbox_inches="tight")
```

```python
# app/app.py (top of the file)
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parents[1]))   # so "from src..." works
import streamlit as st

st.set_page_config(page_title="Student Performance Predictor", layout="wide")
st.title("Student Performance Predictor")
# app/pages/class_overview.py starts the same way, but with parents[2]
```
