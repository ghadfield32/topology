# Start from zero, or continue your existing work

## Read without installing
Extract the complete ZIP into a new directory. Open `START_HERE.html`. The full
31-stage course and previous industry material are included, not replaced by
sports. Follow core Stage 00 for numbers, arrays and notebooks. Start sports S00
alongside it only after you can explain a row, a column and an identifier.

Use one stage at a time: predict a small result, work it by hand, run the example,
change one condition, then implement the independent exercise. Read answers only
after a real attempt. Record what you can now explain, not just what you opened.

## Python setup: Mac/Linux
From the extracted `listening_to_shape_lab` folder:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -e ".[notebooks,test,reader,physics]"
python scripts/sports_v8.py verify
python -m pytest -q -ra
python -m jupyterlab sports_v8/notebooks/S00.ipynb
```

The sports labs do not require torch: omit `physics` for the base topology,
industry and sports path. The full physics continuation uses that extra. Python
3.13 was used in this build; the package declares >=3.11. Initial dependency
installation requires internet or an existing cache. Data excerpts are bundled.
Read the verification report for platforms and optional libraries not tested.

## Windows PowerShell

```powershell
py -3.13 -m venv .venv
.\.venv\Scripts\python.exe -m pip install --upgrade pip
.\.venv\Scripts\python.exe -m pip install -e ".[notebooks,test,reader,physics]"
.\.venv\Scripts\python.exe scripts\sports_v8.py verify
.\.venv\Scripts\python.exe -m pytest -q -ra
.\.venv\Scripts\python.exe -m jupyterlab sports_v8\notebooks\S00.ipynb
```

Using the environment's Python directly avoids changing PowerShell execution
policy. This Windows command path has not been executed here.

## Your first 3 deliverables
Write `my_work/S00.md` with an observation/feature/label/group explanation, the
feet-to-metres calculation, and one claim the data do not support. Run the S00
worked notebook and compare outputs. Implement the three functions in
`sports_v8/practice/S00.ipynb`; they intentionally begin as assignments. Their
worked alternatives are in `sports_v8/solutions/S00.ipynb`.

The new `progress/sports_log_v8.json` starts unassessed. You may edit this manual
record after actual assessment; no script interprets running a notebook as
mastery. Keep source paths and errors you corrected in the record. Use your
existing core progress tooling unchanged for the existing 31 stages.

## Continue from v7 safely
Keep the old extracted folder until you copy `my_work/`, any edited learner
notebooks, and the existing `progress/learning_log_v5.json`,
`progress/industry_log_v6.json`, and v7 assessment records. Preserve evidence-file
paths or update them explicitly. Do not copy the old source implementation over
the new package. Old filenames intentionally remain because their schemas did
not change. No automatic migration resets your scores.

## Independently verify a full sports source
Source bytes could not be downloaded into the build environment. The new excerpts
are transcribed, selected official numbers. After reviewing the actual licenses:

```bash
python scripts/sports_v8.py fetch spl --destination external_data/spl_T0001.json --accept-data-license
python scripts/sports_v8.py verify-source spl external_data/spl_T0001.json
python scripts/sports_v8.py fetch skillcorner --destination external_data/skillcorner_profiles.csv --accept-data-license
```

Downloads are bounded, explicit, and fail on an unexpected revision or an existing
target. They are not scheduled background work. In the build environment only
fixture-based source-verifier tests were executed, not successful full downloads.

## Troubleshooting
A learner `NotImplementedError` is an assignment: implement that function first.
An import error usually means the wrong environment or working folder: check
`python -c "import sys; print(sys.executable)"` and rerun the editable install.
A hash mismatch means inspect changes, not delete the check. An unavailable value
in a gap is expected evidence withholding. A failed network request does not mean
the dataset is empty. A skipped Ripser/GUDHI test is not a passed comparison.
