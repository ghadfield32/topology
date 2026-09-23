# Listening to Shape — Learning Lab 2.0

A beginner-first, original companion to your supplied 12-stage learning outline. Start at Stage 00 even with no topology background. This is not the book text, not an official course from its author, and not a verified substitute for every section of the forthcoming book.


## Version 2: your complete working route

Start with **Stage 00's hub**, then use **lesson → beginner workbook → worked lab → your coding notebook → independent questions → delayed recall**. No topology, proof, or Python background is assumed; four primers explain numbers/notation, Python, proofs, and linear algebra. The package includes 13 original core lessons, 13 expanded workbooks, 102 conceptual exercises with solutions, 65 coding exercises, and 39 new delayed-retrieval questions.

There are **26 executed reference notebooks**: 13 worked labs and 13 coding-answer notebooks. The **13 learner notebooks are intentionally unfinished assignments**, with clear starter errors, hints and checks. They are not counted as successful executions. Changing them is encouraged and does not break the package test suite.

- `docs/START_YOUR_FIRST_SESSION.md`: a concrete first session from zero.
- `stages/00/README.md` through `stages/12/README.md`: the stage-by-stage resource hubs.
- `foundations/` and `workbooks/`: prerequisite explanations and deeper worked reasoning.
- `practice/learner/`: write your own code here; `practice/answers/` contains executed reference answers.
- `docs/PROOF_ATLAS.md`: complete elementary proofs and explicit advanced proof obligations.
- `docs/LEARNING_SYSTEM_V2.md`: assessment rubric, review rules, evidence log and upgrade safety.
- `docs/BRING_YOUR_OWN_DATA.md`: a small exploratory CSV pipeline, not a production model.
- `COMPLETE_COURSE_V2.md`: combined reading volume; answers remain separate.

### Run only the reference answer checks

```bash
python scripts/run_practice_answers.py --stages 0 1
python scripts/run_practice_answers.py
```

### Keep learning with evidence

```bash
python scripts/learn.py status
python scripts/learn.py due
python scripts/learn.py handoff
```

Create your own answer files under `my_work/` and follow `docs/LEARNING_SYSTEM_V2.md` to record practice, assessment and recall. The untouched new record is `progress/learning_log_v2.json`. Scores are self-reported, not automatically graded proof claims. The old browser progress page remains a separate legacy scratchpad and does not sync with the new log.

## Start without installing anything

Extract the ZIP completely. Open **START_HERE.html** in your browser. It links all thirteen lesson sections, executed labs, worked solutions, flashcards, sources, and verification notes. Everything needed for the included reading and saved outputs is local; external free readings require internet. No account is needed. The reader uses system fonts, not downloaded font files.

Do not browse the ZIP as if it were an extracted folder: relative links and Python paths need the extracted directory structure.

## Run it on a Mac or Linux computer

The commands below create an isolated environment inside the course folder. They do not change your production projects. Python 3.13 is recommended because Python 3.13.5 on Linux was used for the recorded execution. Other Python/platform combinations have not been executed here.

```bash
cd /path/to/listening_to_shape_lab
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -e ".[notebooks,test,reader]"
python -m pytest -q -ra
python -m jupyterlab
```

Open `notebooks/00_lab.ipynb` and run from the top. To execute the first two stages without opening Jupyter:

```bash
python scripts/run_notebooks.py --stages 0 1
```

To rerun the full worked course:

```bash
python scripts/run_notebooks.py
```

The stage runner uses a fresh kernel for each notebook. It writes working outputs under `reports/` and updates notebook outputs. It does not modify raw data. Stage 12 expects Stage 11's validation selection. Rerunning the already viewed capstone is reproduction, not a newly independent test.

## Run it on Windows without changing PowerShell execution policy

```powershell
cd C:\path\to\listening_to_shape_lab
py -3.13 -m venv .venv
.\.venv\Scripts\python.exe -m pip install --upgrade pip
.\.venv\Scripts\python.exe -m pip install -e ".[notebooks,test,reader]"
.\.venv\Scripts\python.exe -m pytest -q -ra
.\.venv\Scripts\python.exe -m jupyterlab
```

If `py -3.13` is not found, install Python 3.13 using the official Python distribution or select an existing compatible Python interpreter. The code itself is platform-neutral, but Windows and macOS execution were not tested in the build environment. CPU execution is sufficient for these small labs; no GPU is required.

## Existing uv users

```bash
uv venv --python 3.13
uv pip install --python .venv/bin/python -e ".[notebooks,test,reader]"
```

On Windows select `.venv\Scripts\python.exe` instead. The project pins direct tested core dependencies; it does not pretend to contain a universally validated cross-platform lockfile. `reports/environment.json` records the actual environment, and `reports/tested_dependency_snapshot.txt` records the relevant installed dependency closure. Initial installation needs internet or an existing local package cache; the lessons do not download datasets.

## Optional independent library checks

```bash
python -m pip install -e ".[crosscheck]"
python scripts/check_optional_libraries.py
python -m pytest tests/test_optional_libraries.py -q -ra
python scripts/optional_alpha_demo.py
```

**These are not required to run the core notebooks.** Ripser and GUDHI could not be installed in the build container, so both external-library checks are recorded as NOT RUN / SKIPPED. Do not count these skips as successful validation. Run them locally to finish the external-library validation gate. The alpha demo is also optional and unexecuted in the bundled environment.

## The learning sequence

Each numbered stage has a detailed lesson, a fully runnable worked notebook, and separate original exercises with worked solutions. Stages 00–10 build foundations and persistence; Stage 11 covers representations, Mapper and validation; Stage 12 runs the capstone and prepares an independent project and actual-book audit.

Follow this cycle: **read → predict → calculate → run → explain → solve independently → revisit after a delay**. Do not mark a stage mastered merely because its code ran. Your progress template starts with no stages marked complete.

## Real data and claims

Iris: 150 measured samples, four features; scikit-learn's corrected snapshot. Digits: 1,797 real 8×8 images with intensities 0–16, distributed by scikit-learn from the UCI original test set. Our new split is 1,077 training / 360 validation / 360 test images, not the original 3,823/1,797 UCI train/test design. Writer IDs are unavailable, so the reported evaluation is image-level, not unseen-writer generalization. Attribution, source links, variants, hashes and license notes are in `data/README.md` and `data/manifest.json`.

Synthetic circles, triangles, grids, and sinusoids are labeled controls. No synthetic data are silently substituted for real measurements.

## What is in the project

- `lessons/`, `notebooks/`, `solutions/`: thirteen staged sections and their practical work.
- `src/shape_lab/`: inspectable original topology, homology, persistence and feature code.
- `tests/`: exact examples, invariance tests, independent checks and optional library comparisons.
- `data/`: attributed real datasets, frozen splits and content-addressed feature caches.
- `reports/`: executed plots, results, predictions, environment and validation evidence.
- `docs/`: sources, conventions, glossary, coverage, assessment, capstone, proof-deepening and tutor guides.
- `progress/`: untouched learner record and book-audit gap log.
- `site/` and `START_HERE.html`: offline reading interface, including saved lab outputs.

## Troubleshooting

“Module not found” usually means Jupyter is using a different interpreter from the installed environment. Start it with the same `python -m jupyterlab` command used above. “Open this notebook inside…” means the working folder is outside the extracted project. Restart a notebook kernel and run all cells to remove stale variables. A failed mathematical assertion should be investigated; do not remove the assertion to obtain a green result.

The educational Rips builder caps candidate counts. Use the small supplied examples or a specialized TDA library for large inputs. If you intentionally change raw data, regenerate the manifest and document a new experiment rather than bypassing hash checks. Do not delete or alter test rows to improve a reported score.

For continued learning here, use `docs/CONTINUE_WITH_TUTOR.md` and share your answers plus stage output. That supplies concrete evidence for targeted instruction rather than repeatedly rebuilding the plan.
