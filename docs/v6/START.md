# Start here: one course, eight optional industry cases

## Completely new to the subject

Extract the full ZIP into a new folder. Open `START_HERE.html`. Start at Stage 00; you need no coding environment to read lessons or inspect saved outputs. The existing primers explain notation and Python. The new [data primer](BEGINNER_DATA_PRIMER.md) explains observations, units, missing values, splits and elementary model measures.

After the first two stages, use only the **opening sections** of one industry case: [Wine](../../industry/lessons/wine.md) or [Stackloss](../../industry/lessons/stackloss.md) is a manageable first table. You do not need to understand the barcode cell yet. Return to that section after homology and persistence. You are learning one concept in two contexts, not eight new subjects simultaneously.

For every stage, the [31-stage transfer map](STAGE_MAP.md) identifies a concrete case, an exact small calculation, a run/check task and an unsupported conclusion. The ordinary course remains sequential; industry cases are optional parallel practice. Geometry keeps using genuine geometric controls and the included stereo observations rather than pretending a table is a camera dataset.

## Read, predict, calculate, run, explain

Read the lesson and small example. Predict an output in writing. Calculate an easy case by hand. Run the reference notebook and reconcile the result. Change exactly one assumption. Then implement the learner functions and attempt the conceptual questions without solutions. After a delay, answer the recall prompts. An honest “not yet” becomes a targeted prerequisite exercise, not a restart.

A useful first answer file is `my_work/00_first_session.md`: define a row and a column, predict an array's dimensions, report the result, and explain why a repeated row is not necessarily an independent observation. Use your own words.

## Python setup: Mac and Linux

From the extracted `listening_to_shape_lab` folder:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -e ".[notebooks,test,reader]"
python scripts/industry.py verify
python -m pytest -q -ra
python -m jupyterlab
```

The required new industry cases use NumPy, SciPy, pandas, matplotlib and scikit-learn on CPU. Install `python -m pip install -e ".[physics]"` when you reach the earlier physics neural examples (stages 21–30); without PyTorch, physics-specific checks may skip. All reference notebooks in the delivered build were executed with CPU PyTorch installed. Initial dependency installation needs internet or an existing package cache. No dataset download is needed for these cases.

On **Windows PowerShell**, create the environment with `py -m venv .venv` and activate with `.\.venv\Scripts\Activate.ps1`. When activation is restricted, invoke `.\.venv\Scripts\python.exe` directly for the remaining commands; no execution-policy change is required. Replace `python3` with `py` only at the initial creation step.

Open `notebooks/00_lab.ipynb` first. Industry notebooks live in `industry/notebooks/`; independent assignments are in `industry/learner/`; reference code and conceptual answers are in `industry/answers/`. Deliberate `NotImplementedError` functions in learner notebooks are exercises, not broken reference implementations.

## Preserve earlier learning

Do not extract over your only copy of earlier work. Copy `my_work/` and any other personal evidence files into the same relative paths in the new folder. Preserve **`progress/learning_log_v5.json`** unchanged: version 6 still has the same 31 core stages, so the schema and filename are intentionally retained. The old `study_v5.py` and `learn.py` commands remain valid. Do not replace a used log with the empty one supplied in this ZIP.

The eight cases have a separate new `progress/industry_log_v6.json`. It starts unassessed. In future upgrades preserve it alongside your core log. It is not a browser export and is not silently synchronized with browser storage. Recorded scores and independence declarations are yours; hashes verify evidence-file continuity, not correctness.

```bash
python scripts/study_v5.py next
python scripts/learn.py handoff
python scripts/industry.py list
python scripts/industry.py case wine
python scripts/industry.py status
python scripts/industry.py verify-evidence
python scripts/industry.py handoff
```

After making your own evidence file, record an attempt explicitly:

```bash
python scripts/industry.py record wine --kind practice --score 60 --evidence my_work/wine_attempt.md --note "Need to revisit training-only scaling"
```

Use `--kind assessment --independent --critical-clear` only when those statements are true. A score of at least 85 is a course convention, not accreditation. The tool's review dates are calculated on request; it creates no background notifications. `init` refuses to overwrite an existing log.

## Work with a tutor here

Bring your question, the stage/case ID, your prediction, your calculation, actual output and one uncertainty. Ask for a hint before the full solution. After correction, solve a related unfamiliar problem. Paste the handoff when starting another chat; it carries what you actually attempted rather than assuming completion from downloaded files.

## Reading depth and completion

Complete elementary arguments and hand calculations; for major theorems state assumptions and work the structured deeper-proof readings. Finish one independent case and explain its split, metric, failure cases and limits. All demonstrations' test data are exposed: a genuinely new experiment needs a fresh, appropriately separated evaluation. The actual book text has not been audited, and the course does not claim exhaustive coverage of every branch of topology, geometry or scientific machine learning.
