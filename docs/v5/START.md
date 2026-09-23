# Start or continue the complete v5 course

## Reading without installing software

Extract the full ZIP into a new folder. Open `START_HERE.html`. Read Stage 00 if you are new; continue from your recorded stage if you already have independent evidence. The physics extension begins at Stage 21, not at the beginning of the course. Original stage numbers and earlier lessons remain intact.

Every new stage includes a beginner lesson, worked lab with saved outputs, three independent coding exercises, six conceptual questions with separate answers, and three delayed-recall questions. The two new primers explain rates/equations and how to interpret physical guarantees. External papers and videos require internet; saved course pages and outputs do not.

## Python setup: Mac or Linux

Open Terminal inside the extracted `listening_to_shape_lab` folder:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -e ".[notebooks,test,reader,physics]"
python -m pytest -q -ra
python -m jupyterlab
```

The new trained-model labs use PyTorch on CPU. No CUDA, GPU, cloud account, model weights or private data is required. The physics extra is optional for reading and NumPy exercises. Initial dependency installation requires network access or a local package cache; the datasets are already bundled. An installation of torch can be large. This build was tested with Python 3.13.5 and torch 2.10.0+cpu on Linux; Mac and Windows execution were not tested here. Do not interpret the allowed package range as testing every version.

## Windows PowerShell

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -e ".[notebooks,test,reader,physics]"
python -m pytest -q -ra
python -m jupyterlab
```

If local policy prevents activation, use `.\.venv\Scripts\python.exe` directly instead of changing system-wide execution policy. Keep this learning environment separate from production environments.

## A new learner's first session

Open the preserved Stage 00 lesson and lab from the home page. Read the notation/Python primer when a symbol or operation is unfamiliar. Before running a cell, write your expected shape or result. After running, explain one discrepancy. Attempt `00.C1` without the answer open. Save your explanation in `my_work/00/answer.md`.

Do not open Stage 23 and assume neural training is the prerequisite for understanding derivatives. The route is definitions and examples first, then implementation and assessment.

## A continuing learner's next session

```bash
python scripts/study_v5.py next
python scripts/study_v5.py stage 21
python scripts/learn.py status
python scripts/learn.py due
python scripts/learn.py handoff
```

The default new record is `progress/learning_log_v5.json`. It has 31 unassessed stages. A fresh log does not mean you should discard an older one.

## Migrate v2/v3/v4 work without overwriting it

Copy your `my_work/` evidence files into the same relative paths in the new project. Keep the old project as a backup. Migrate the old JSON record to a NEW filename:

```bash
python scripts/migrate_progress_v5.py \
  --source /path/to/old-course/progress/learning_log_v3.json \
  --destination progress/migrated_learning_log_v5.json

python scripts/study_v5.py --log progress/migrated_learning_log_v5.json verify-evidence
python scripts/study_v5.py --log progress/migrated_learning_log_v5.json next
python scripts/learn.py --log progress/migrated_learning_log_v5.json status
```

v4 intentionally used the v3 filename/schema; that is accepted. Thirteen-stage v2 logs are accepted too. Existing attempts are copied, not rewritten; additional stages start unassessed. Migration refuses an existing destination. Browser-local checkboxes from earlier readers are separate and are not automatically converted into grades.

Record an actual practice attempt only after creating your own evidence file:

```bash
python scripts/learn.py record --stage 21 --kind practice --score 60 \
  --evidence my_work/21/answer.md --note "Derived the secant; need to revisit derivative noise."
```

The score above is a syntax example, not a recommended grade. Use your own actual result. Assessment and recall commands have explicit independence and critical-misconception flags; do not set them without justification. Records are self-reports, not automated proof checking. Review-date calculations do not create background notifications.

## Reproduce reference work

```bash
python scripts/run_physics.py
python scripts/run_physics.py --stages 21 22 --kind lab
python scripts/run_notebooks.py
python scripts/run_practice_answers.py
python scripts/run_consolidation.py
python scripts/build_reader_v5.py
```

Each reference notebook gets a fresh kernel. The runners overwrite reference outputs, not learner files or learning records. Stage 30 reads the reports from 21–29, so run those first when rebuilding from scratch. Optional Ripser/GUDHI comparisons remain separate; do not count a skip as a pass.

## Evidence you should produce per stage

A hand calculation, a working independent function, an unfamiliar conceptual answer, an explicit data-origin statement, a failure case, and a statement of what remains unsupported. Record the particular misconception to revisit rather than restarting the whole course. The [coverage map](COVERAGE.md) distinguishes implemented teaching from full research reproduction.
