# How we work with Git

## First time only

```bash
git clone https://github.com/<team-account>/student-performance-predictor.git
cd student-performance-predictor
python -m venv .venv
# Windows: .venv\Scripts\activate     Mac/Linux: source .venv/bin/activate
pip install -r requirements.txt
```

## For every task

1. **Take your issue** on the GitHub task board (it has your name on it).
2. **Get the latest code**
   ```bash
   git checkout main
   git pull
   ```
3. **Make a branch** named after your task
   ```bash
   git checkout -b samnang/eda-histograms
   ```
4. **Do the work.** Save often.
5. **Commit** with a short message that says what you did
   ```bash
   git add notebooks/01_eda.ipynb
   git commit -m "Add grade histograms and pass/fail count"
   ```
6. **Push** and open a pull request (PR) on GitHub
   ```bash
   git push -u origin samnang/eda-histograms
   ```
7. In the PR, write what you did and add your **reviewer** (see the table below).
8. The reviewer **runs your code**, comments or approves. Then merge into `main`.

## Who reviews whom

Your reviewer is the person who uses your work next, so they check it really works for them.

| Your pull request | Reviewer |
|---|---|
| Samnang (Part 1) | Rayu |
| Rayu (Part 2) | Rathana |
| Rathana (Part 3) | RithyReach |
| RithyReach (Part 4) | Sophal |
| Sophal (Part 5) | Samnang |

## Rules

- Never push directly to `main`.
- Small PRs are easier to review: one task = one PR.
- Before opening a notebook PR, use *Restart & Run All* so it runs from top to bottom.
- Don't commit big files or secrets. `data/student-por.csv` is small and OK.

## Weekly meeting (20 minutes, start of each week)

Each person answers 3 questions:
1. What did I finish?
2. What will I do this week?
3. Is anything blocking me?
