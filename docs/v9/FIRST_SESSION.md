# First session and migration — v9

## Read first, with no installation
Extract the full archive to a new folder. Open `START_HERE.html` in a browser. Choose Stage 00 unless your saved evidence establishes a later starting point. Each stage has one primary lesson, one primary worked lab, one independent task and separate answers. Repair resources are optional, so you do not reread the same concept in four mandatory documents.

`reader/` contains the canonical offline renderings. The browser can display saved code results, but it does not execute Python. Equations remain available as text and source notation; no online account is needed. External books, papers, videos and optional data still need internet access.

## Run Python
Python 3.13 is the tested minor-version family. The exact validation build uses Python 3.13.5 on Linux. The commands below do not prove that dependency installation was tested on every operating system.

Mac/Linux:
```bash
cd /path/to/listening_to_shape_lab
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -e ".[notebooks,test,reader,physics]"
python scripts/course.py doctor
python scripts/course.py check 0
python scripts/course.py run --stage 0 --output my_work/stage00_run01
python -m jupyterlab
```

Windows PowerShell:
```powershell
cd C:\path\to\listening_to_shape_lab
py -3.13 -m venv .venv
.\.venv\Scripts\python.exe -m pip install --upgrade pip
.\.venv\Scripts\python.exe -m pip install -e ".[notebooks,test,reader,physics]"
.\.venv\Scripts\python.exe scripts/course.py doctor
.\.venv\Scripts\python.exe scripts/course.py run --stage 0 --output my_work/stage00_run01
.\.venv\Scripts\python.exe -m jupyterlab
```
Using the environment executable directly avoids changing PowerShell execution policy. Initial dependency installation requires internet or a suitable local cache. Nothing in this ZIP is a bundled Python runtime or wheelhouse. For the topology/industry/sports-only route, omit `physics`; stages using PyTorch require it.

## What a run produces
`execution.json` records every actually executed dependency and requested notebook, environment, source hashes, pass/fail status and timings. `executed/` contains the saved notebooks, and `artifacts/` contains their produced reports. Required earlier reports are rebuilt instead of copied from old output. Each notebook uses a fresh kernel in a temporary copy of the course inputs.

Use a new output folder each time. The runner refuses to overwrite an existing destination and does not change your original notebooks, datasets or progress record. A capstone may execute several predecessors; inspect the manifest rather than assuming only one file ran.

To run all cataloged references:
```bash
python scripts/course.py run --all --jobs 2 --output my_work/all_reference_run01
```
This is a larger verification task, not a prerequisite for reading Stage 00. To rerun the new ACB metadata lesson, use `--acb` instead of `--all`.

## Record learning, not just a green check
Create a text file in `my_work/` with your prediction, hand calculation, observed output, explanation and one unsupported conclusion. Record it using the retained `scripts/learn.py` command after doing the work. Do not mark a proof correct solely because code ran.

## Continue without losing v8 work
Keep your old folder. Copy your own `my_work/`, edited learner notebooks and referenced evidence files into the corresponding locations of the new folder. Preserve `progress/learning_log_v5.json`, `progress/industry_log_v6.json` and `progress/sports_log_v8.json` when present; their older names are deliberate. The 31 stage IDs and seven sports IDs have not changed.

Do not overwrite a new folder's evidence with unrelated files sharing a name. Compare conflicting versions manually. Use the existing evidence-verification commands before relying on migrated assessment declarations. No migration deletes your prior archive, performs a silent merge or auto-passes new work.

## One navigation command
```bash
python scripts/course.py list
python scripts/course.py stage 6
python scripts/course.py next
python scripts/course.py cases
python scripts/course.py handoff
```

`next` relies on your declared learning log; it is not an independent examiner. Delayed-review records remain under `scripts/learn.py due`. There are no background reminders.
