"""Create every project task as a GitHub issue, in the right order.

Each issue gets: a milestone for its part, a label with the owner's name, and a
"Blocked by #.." line so everyone can see which tasks must be done first.
The same tasks are listed in docs/TASKS.md.

Requirements: GitHub CLI installed and logged in (`gh auth login`).
Run from inside the repo folder:

    python scripts/create_issues.py --dry-run   # only print what would be created
    python scripts/create_issues.py             # create labels, milestones and issues
"""
import subprocess
import sys

# (id, milestone, owner, title, needs, output)  - ordered so every "need" is created first
TASKS = [
    ("T01", 1, "Samnang", "Data dictionary (all 33 columns)", [], "docs/data_dictionary.md"),
    ("T02", 1, "Samnang", "Load function (both subjects, add subject, student_id, fail)", [], "src/data/load.py"),
    ("T07", 2, "Rayu", "Shared settings", [], "src/config.py"),
    ("W1", 6, "Samnang", "App structure + navigation", [], "app/app.py, app/pages/"),
    ("T03", 1, "Samnang", "Grade histograms + pass/fail count", ["T02"], "notebooks/01_data_study/"),
    ("T04", 1, "Samnang", "Correlation, box plots, fail-rate charts", ["T02"], "notebooks/01_data_study/"),
    ("T05", 1, "Samnang", "Cleaning rules + G3 = 0 decision", ["T02"], "src/data/clean.py"),
    ("T06", 1, "Samnang", "Key findings", ["T03", "T04", "T05"], "docs/findings.md"),
    ("T08", 2, "Rayu", "Split by student (train/test + CV folds), with and without G1, G2", ["T05", "T07"], "src/data/split.py"),
    ("T09", 2, "Rayu", "Preprocessing (one-hot + scaling)", ["T07"], "src/data/preprocess.py"),
    ("W2", 6, "Samnang", "Class overview screen with example data", ["W1"], "app/pages/class_overview.py"),
    ("W3", 6, "Rayu", "Check one student form", ["W1"], "app/app.py"),
    ("T11", 3, "Rathana", "Linear Regression, with and without G1, G2", ["T08", "T09"], "notebooks/03_grade_model/"),
    ("T15", 4, "RithyReach", "Logistic Regression: with, without, balanced", ["T08", "T09"], "notebooks/04_passfail_model/"),
    ("T22", 5, "Sophal", "Similar students who passed (KNN)", ["T09"], "src/features/similar.py"),
    ("T12", 3, "Rathana", "Decision Tree + Random Forest for the grade", ["T11"], "notebooks/03_grade_model/"),
    ("T13", 3, "Rathana", "Factors that raise or lower the grade", ["T11"], "notebooks/03_grade_model/"),
    ("T14", 3, "Rathana", "Train + save the final grade models", ["T11"], "src/models/train_grade.py"),
    ("T16", 4, "RithyReach", "Decision Tree + KNN for pass/fail", ["T15"], "notebooks/04_passfail_model/"),
    ("T17", 4, "RithyReach", "Threshold tuning", ["T15"], "notebooks/04_passfail_model/"),
    ("T18", 4, "RithyReach", "Train + save the final pass/fail models", ["T15"], "src/models/train_passfail.py"),
    ("T10", 2, "Rayu", "Prediction function", ["T14", "T18"], "src/predict.py"),
    ("T20", 5, "Sophal", "Main risk factors for one student", ["T18"], "src/features/explain.py"),
    ("T19", 5, "Sophal", "Class risk ranking", ["T10"], "src/features/ranking.py"),
    ("T21", 5, "Sophal", "What-if recommendations", ["T10"], "src/features/recommend.py"),
    ("W4", 6, "Rayu", "Result cards + at-risk warning", ["T10", "W3"], "app/app.py"),
    ("W5", 6, "Sophal", "Connect the ranking to the Class overview screen", ["W2", "T19"], "app/pages/class_overview.py"),
    ("W6", 6, "Sophal", "Risk factors, recommendations, similar students boxes", ["W3", "T20", "T21", "T22"], "app/app.py"),
    ("E1", 7, "Team", "Evaluate all models (metrics, CV, baselines, results table)",
     ["T11", "T12", "T13", "T14", "T15", "T16", "T17", "T18"], "reports/results/"),
    ("E2", 7, "Team", "Test the app + check wording and ethics note", ["W4", "W5", "W6"], "bug issues"),
    ("E3", 7, "Team", "Final report and presentation", ["E1", "E2"], "final report"),
]

MILESTONES = {1: "Part 1 · Study the data", 2: "Part 2 · Prepare the data", 3: "Part 3 · Grade model",
              4: "Part 4 · Pass/fail model", 5: "Part 5 · Smart features", 6: "Web app", 7: "Together"}
OWNERS = ["Samnang", "Rayu", "Rathana", "RithyReach", "Sophal", "Team"]
DRY = "--dry-run" in sys.argv


def gh(*args):
    if DRY:
        print("gh", " ".join(args))
        return ""
    return subprocess.run(["gh", *args], check=True, capture_output=True, text=True).stdout.strip()


for name in OWNERS:
    gh("label", "create", name, "--color", "FF942B", "--force")
gh("label", "create", "blocked", "--color", "B60205", "--force")

for title in MILESTONES.values():
    try:
        gh("api", "repos/{owner}/{repo}/milestones", "-f", f"title={title}")
    except subprocess.CalledProcessError:
        pass  # milestone already exists

numbers = {}
for i, (tid, ms, owner, title, needs, output) in enumerate(TASKS, start=1):
    blocked = ", ".join(f"#{numbers[n]} ({n})" for n in needs) if needs else "nothing, start now"
    body = (f"**Owner:** {owner}\n\n**Output:** `{output}`\n\n"
            f"**Blocked by:** {blocked}\n\n"
            f"Details: `docs/TASKS.md` and the guide in `docs/tasks/`.")
    labels = owner + (",blocked" if needs else "")
    url = gh("issue", "create", "--title", f"[{tid}] {title}", "--body", body,
             "--label", labels, "--milestone", MILESTONES[ms])
    numbers[tid] = url.rsplit("/", 1)[-1] if url else str(i)  # dry run: assume sequential numbers
    print(f"{tid} -> #{numbers[tid]}  {title}")

print("\nDone. Remove the 'blocked' label from an issue when everything it needs is merged.")
