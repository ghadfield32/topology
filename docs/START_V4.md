# First session — Listening to Shape Learning System v4

## What to open

Extract the entire ZIP into a new folder. Inside `listening_to_shape_lab`, open `START_HERE.html`. Do not open it inside the archive preview: relative links and notebook downloads need the extracted directories. The reader works without downloading models, installing Python, or accessing datasets online. External readings and video links need internet.

This is the complete course, not a patch. Stages 00–20 keep their numbering. Versions 1–3 documents and reader pages remain for old links; the v4 home, sessions, source ledger and verification report are the current entry points.

## Preserve your work instead of restarting

If you have already answered questions, keep that work. Back up your old folder first. Copy your own answer files into the same relative paths under `my_work/` in the new folder. Copy your existing `progress/learning_log_v3.json` into the new folder only after preserving the empty shipped log separately. Do not overwrite either file without a backup.

Version 4 deliberately retains this 21-stage log format. The `v3` filename is a compatibility choice, not a requirement to redo your assessments. The old browser progress widget is a different system and does not synchronize automatically. For a legacy 13-stage v2 log, use the documented [migration procedure](LEARNING_SYSTEM_V3.md) before continuing.

Then run `python scripts/study.py verify-evidence`. Matching hashes show that recorded files survived unchanged; they do not judge the answers. A modified file is not automatically wrong. Preserve the original and record a new attempt for a substantive revision rather than silently editing the historical record.

## A beginner's first study session

Open [Stage 00](../stages/00/README.md), then the [guided session](../sessions/00_session.md). Begin with one row of the real Iris table. Identify the specimen, four measured lengths, the label and the record identifier. Say what the two axes of the selected array mean before calculating anything.

Work the three-number mean by hand. Predict the table dimensions. Inspect or execute [the original lab](../notebooks/00_lab.ipynb), then [the consolidation lab](../consolidation/00_lab.ipynb). Write one sentence explaining why an ID and a target label should not be treated as ordinary measured features.

Copy `curriculum/response_templates/00_response.md` to a new answer file under `my_work/`. Record your prediction, actual output, explanation, and one limitation. Attempt the first coding exercise in `practice/learner/00_practice.ipynb`. The starter deliberately raises `NotImplementedError`; replace only the assigned function and run its check. Reference answers live in a different directory.

Do not mark an independent assessment because you followed the worked notebook. First try unfamiliar conceptual and transfer questions without opening the answer criteria. When a symbol or Python operation is unfamiliar, use the linked foundation primer rather than guessing.

## Install Python dependencies when ready

Use Python 3.11 or later; the executed build used Python 3.13.5 on Linux. Mac and Windows are supported by instructions, not claimed as tested platforms. A separate virtual environment keeps course packages away from other projects. The versions in `pyproject.toml` describe the course environment, not a promise of being the newest available release.

Mac or Linux, from the extracted project folder:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -e ".[notebooks,test,reader]"
python scripts/study.py doctor
python -m pytest -q -ra
python -m jupyterlab
```

Windows PowerShell, without changing execution-policy settings:

```powershell
py -3 -m venv .venv
.\.venv\Scripts\python.exe -m pip install --upgrade pip
.\.venv\Scripts\python.exe -m pip install -e ".[notebooks,test,reader]"
.\.venv\Scripts\python.exe scripts\study.py doctor
.\.venv\Scripts\python.exe -m pytest -q -ra
.\.venv\Scripts\python.exe -m jupyterlab
```

The first installation needs internet or a suitable local wheel cache. The required data are already bundled. Statsmodels was used to export the historical series during authoring but is not a required runtime dependency. No GPU, account, paid course, or model checkpoint is needed for required labs.

If a package install fails, preserve the complete error and your Python version. Do not delete work or randomly upgrade every package. Reading the offline course and inspecting saved outputs remain available.

## Navigation commands

```bash
python scripts/study.py stage 0
python scripts/study.py next
python scripts/study.py verify-evidence
python scripts/learn.py status
python scripts/learn.py handoff
```

The study navigator is read-only. `next` prioritizes declared review needs, then due reviews, then the first unfinished stage. It uses your log, not an intelligence or memory assessment. The existing `learn.py record` command writes a user-declared attempt with an evidence hash. Use its help and the [learning-system guide](COMPLETION_SYSTEM_V4.md) before recording scores. There are no background reminders.

## Reproduce a single stage

```bash
python scripts/run_notebooks.py --stages 0
python scripts/run_consolidation.py --stages 0
python scripts/run_practice_answers.py --stages 0
```

These refresh reference outputs, not your assessments. To do your own work, open the learner notebook or a copy under `my_work/`. The final consolidation capstone expects earlier consolidation reports, all of which are shipped. Do not confuse a previously shipped report with a new computation after changing its input.

Your next deliverable is a small answer file explaining Stage 00's observation unit, feature columns, predicted array shape, actual result, and one unjustified conclusion to avoid.
