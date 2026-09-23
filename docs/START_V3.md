# Start the complete learning system, version 3

## No installation route
Extract the ZIP fully into a new folder and open `START_HERE.html`. Open **Stage 00** unless you have independently completed it. Read the lesson, use the relevant primer and inspect the saved lab outputs. Reading the page is not an assessment.

For the first session, explain the difference between an observation and a feature, inspect the provided table dimensions, and attempt Stage 00 exercise 00.C1. Do not begin by installing VGGT. Geometry predictions make more sense after metric spaces, coordinate frames, projection and uncertainty are understood.

## Python route on Mac or Linux
Use Python 3.13 when practical; the build was executed on Linux with Python 3.13.5. Mac and Windows were not executed here.

```bash
cd /path/to/listening_to_shape_lab
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -e ".[notebooks,test,reader]"
python -m pytest -q -ra
python -m jupyterlab
```

Open `notebooks/00_lab.ipynb`, run top to bottom, then open `practice/learner/00_practice.ipynb`. First-time installation requires internet or cached packages. All three required real datasets are already included. Do not install optional model packages into the course environment merely to read the material.

## Python route on Windows PowerShell

```powershell
cd C:\path\to\listening_to_shape_lab
py -3.13 -m venv .venv
.\.venv\Scripts\python.exe -m pip install --upgrade pip
.\.venv\Scripts\python.exe -m pip install -e ".[notebooks,test,reader]"
.\.venv\Scripts\python.exe -m pytest -q -ra
.\.venv\Scripts\python.exe -m jupyterlab
```

Using the environment's Python executable directly avoids requiring a PowerShell activation-policy change.

## Running later stages
Run a specific lab or coding reference with:

```bash
python scripts/run_notebooks.py --stages 13
python scripts/run_practice_answers.py --stages 13
```

Omitting `--stages` runs all 21 in order. Stage 20 assembles prior geometry reports, so execute 13–19 first. Reference notebooks overwrite their own saved outputs and reports; keep your changed work under `my_work/`.

## Continuing from version 2
Keep your v2 folder. Follow [the migration instructions](LEARNING_SYSTEM_V3.md) to preserve attempt history and evidence. You do not need to repeat demonstrated foundations or discard your previous answers.

## What the supplied VGGT post adds
It motivates an applied continuation, not a replacement for topology. The sequence is: charts and rotations → cameras and stereo → attention and model outputs → registration and holdouts → pipeline timing → causal event hypotheses → independent project. The official model's predictions remain candidates until the relevant evidence is checked.
