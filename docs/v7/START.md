# Start here — one continuing course, not another restart

## Your first session, with no assumed background

Extract the ZIP completely into a new folder. Open `START_HERE.html`. Choose Stage 00 and read its new entry guide. It defines observation, feature, label and table dimensions. Predict the shape of the selected data table on paper, then inspect the saved lab or run the tiny entry check. No software installation is required to read the offline lessons and saved outputs.

There are 31 core stages, ten industry cases, and two new methods laboratories. Do not start all of them simultaneously. The original stages contain the full subject progression. The new entry guides help you begin each stage; they do not replace the deeper lesson, workbook, independent practice or proof obligations. Industry cases are parallel applications, not ten new prerequisites.

A useful first answer is five sentences: what one row represents; which fields are predictors; what output you predict; what actually happened; and one conclusion the output does not justify. Save it as `my_work/00_first_session.md`. Reading the supplied answer does not mark this as independent mastery.

## Read, calculate, run, transfer, revisit

First establish the meaning of each symbol and observation. Then calculate the smallest case manually. Run the reference and investigate disagreements. Change one assumption, predicting the effect first. Implement the learner functions without copying. Finally answer a new question and return later for recall. When a prerequisite is missing, use the relevant primer rather than restarting the entire course.

The new uncertainty primer assumes no statistical background and defines training, calibration, testing, coverage and leakage. The original primers cover notation, Python, proofs, linear algebra, calculus, measurement uncertainty and dynamics. Their assignments are linked from the original stage pages.

## Setup for running code on Mac or Linux

In the extracted `listening_to_shape_lab` folder:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -e ".[notebooks,test,reader]"
python scripts/course_v7.py check 0
python scripts/course_v7.py verify-new-data
python -m jupyterlab
```

To run the full inherited physics neural laboratories, also install `python -m pip install -e ".[physics]"`. To run all tests use `python -m pytest -q -ra`. The delivered verification environment includes CPU PyTorch; a local environment without it will not have the same optional-check coverage. Initial installation needs internet or a package cache. The required data snapshots are bundled. The new cases run on CPU and require no GPU or model weights.

The exact tested Python version and library versions are in the current verification report. The retained dependency pins are not a promise that every future operating system or Python release supports every pinned package.

On Windows PowerShell, create the environment with `py -m venv .venv`. Use `.\.venv\Scripts\Activate.ps1` to activate it. If activation is restricted, invoke `.\.venv\Scripts\python.exe` directly; no execution-policy change is required. Replace only the initial environment-creation command with `py`.

## Find the right lesson and notebook

```bash
python scripts/course_v7.py stage 0
python scripts/course_v7.py case seeds
python scripts/course_v7.py check all
```

The first command prints the entry and full-stage paths. Open `notebooks/00_lab.ipynb` for the original first worked lab and `practice/learner/00_practice.ipynb` for its independent exercises. For the new agriculture case open `applications_v7/seeds/lab.ipynb`, then `applications_v7/seeds/learner.ipynb`. Materials is under `applications_v7/concrete_slump/`; the two methods labs are under `methods_v7/`.

Learner notebooks deliberately raise `NotImplementedError` until you write your answer. Reference notebooks are separate and executed. A failed learner exercise is not a broken reference package. Do not edit the checks merely to obtain green output.

## Preserve your work from v6 or earlier

Keep the old folder until migration is checked. Preserve `my_work/`, `progress/learning_log_v5.json` and `progress/industry_log_v6.json`, plus any evidence files stored elsewhere. Retain the same relative paths when a log points to them. Do not replace a used log with the empty one shipped in the new ZIP.

Version 7 retains 31 core stages and the original eight-case log unchanged. The two new cases and two methods labs have response templates and a separate unassessed checklist in `progress/v7_extension_checklist.json`; this checklist does not silently merge with old logs. It is manually editable, not an automatic grader. A source hash verifies unchanged bytes, not whether your proof is correct.

The existing commands remain valid:

```bash
python scripts/study_v5.py next
python scripts/study_v5.py verify-evidence
python scripts/learn.py handoff
python scripts/industry.py status
python scripts/industry.py verify-evidence
```

These tools calculate review dates when requested; they create no background notifications. Browser-local progress, where present in historical readers, is a separate record and is not automatically synchronized.

## Bring an answer back to this chat

State the stage/case ID, your prediction, the calculation you attempted, the actual code/output, and one point of uncertainty. Ask for a hint before opening the full answer. After correction, solve an unfamiliar variant. Preserve your wrong turn as useful evidence of what changed in your understanding.

The actual book text has not been audited. The source posts are not complete technical specifications. The course is an original learning system for the defined introductory and applied scope, not a guarantee of professional competence in every domain. The coverage map identifies what is implemented, demonstrated, source-reviewed, or still requires independent work.
