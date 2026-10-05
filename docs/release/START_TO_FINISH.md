# Start to finish: how to work through this repository and show it works on real data

Version 14 • 4 October 2026 • the single ordered route through both layers

This page is the ordered journey. It tells you what to open first, what a
complete pass looks like for one lesson and for the whole system, and how to
produce and inspect evidence that the code ran on real (selected observed) data.
It does not grade you, and it never claims mastery on your behalf.

Two rules from the course hold everywhere:

1. **Notebook → understand it. Project → prove you can engineer it.**
2. Every lesson is **Explain → Predict → Implement → Break → Apply**.

## 0. One-time setup

You need Python via uv. The engineering layer additionally wants a C/C++
compiler + CMake, Go, Rust/Cargo, Node + `tsc`, and optionally CUDA/PyO3/OpenCV.

On Windows, set UTF-8 mode first — the lessons contain non-ASCII text
(superscripts and arrows) and several tools read it with the default code page:

```powershell
$env:PYTHONUTF8 = '1'
```

Install and check the environment:

```powershell
uv python install 3.13.5
uv run --no-project --python 3.13.5 python tools/bootstrap.py --profile physics
uv run --no-sync python course.py doctor --profile physics   # declared versions, not a full audit
uv run --no-sync python learn.py doctor                      # which compilers/toolchains exist
```

`learn.py doctor` printing a path is **availability, not acceptance**. A missing
tool is reported honestly and blocks only the units that need it.

TypeScript (only needed for the integrated demo and sys06) — the version the
course was tested with:

```powershell
npm install --global typescript@5.8.3
```

## 1. See the whole map (read, no execution)

Open **[LEARN_TOPOLOGY.html](../LEARN_TOPOLOGY.html)**. That is the new front
door: it links the mathematical layer (31 stages, 5 representation units, 25
cases, 133 references) and the engineering layer (sys00–sys09). The offline
reader **[START_HERE.html](../START_HERE.html)** renders every lesson with its
saved outputs and needs no installation.

Confirm the two layers resolve:

```powershell
uv run --no-sync python learn.py list
```

You should see the existing application/native keys, then
`SOURCE-MAPPED ENGINEERING PROJECTS` with `sys00`–`sys09`.

## 2. One complete core lesson (the mathematical layer)

This is the smallest full loop, using Stage 01. Pick a **fresh output
directory** for every attempt.

```powershell
uv run --no-sync python course.py study 1 --output my_work/study01_attempt01
```

Open `my_work/study01_attempt01/START.md`. It links the *same* canonical lesson
and lists the exact run and report commands.

1. **Explain/Predict.** Write in `prediction.md` (and `reflection.json` later):
   one observation, one feature, the units, the smallest hand calculation you can
   do without the notebook, the expected result, and the assumption it rests on.
2. **Implement/run the reference.**

   ```powershell
   uv run --no-sync python course.py run --stage 1 --output my_work/study01_attempt01/run01
   ```

   The runner uses a fresh copied workspace and fresh kernels; `execution.json`
   records notebook identity, teaching-cell count, interpreter, input continuity
   and SHA-256 hashes.
3. **Apply.** Solve `practice/learner.ipynb` and write `answer.md`. A
   `NotImplementedError` here is an assignment, not a failure.
4. **Break.** Change exactly one condition in your private copy and predict the
   effect before running. Keep the result.
5. **Complete the reflection** — six nonempty fields (`question`,
   `observation_unit`, `method`, `result_interpretation`, `limitation`,
   `next_experiment`) in `reflection.json`.
6. **Export your local evidence packet.**

   ```powershell
   uv run --no-sync python course.py report --run my_work/study01_attempt01/run01 `
     --reflection my_work/study01_attempt01/reflection.json `
     --output my_work/study01_attempt01/report01
   ```

   Open `report01/index.html`. `packet.json` has `published: false`. The exporter
   refuses changed/missing/added run files, unexecuted cells, saved error
   outputs, unsafe paths, or a missing output seal. Full detail:
   [RESULTS_WORKFLOW.md](RESULTS_WORKFLOW.md).

**A core lesson is "complete" when:** the reference run passed with inputs
unchanged, you wrote a prediction *before* running, you finished the private
notebook, you produced the report packet, and you stated a limitation. It is
still **not** an assessment of mastery — hashes show byte continuity, not
understanding.

The engineering counterpart of the same loop (native Go/Rust practice copies) is:

```powershell
uv run --no-sync python learn.py session --lab stage01 --output my_work/learning_stage01_99
```

## 3. One complete engineering project (the project layer)

```powershell
uv run --no-sync python learn.py project --unit sys01 --output my_work/c_reader01
uv run --no-sync python learn.py check-project --workspace my_work/c_reader01 --output my_work/c_reader01/attempt01
```

`project` copies the **real** source into `my_work/c_reader01/project/` plus the
binary contract data. `check-project` builds and tests **your private copy** —
not the reference — so your edits are what is tested.

First engineering calculation: explain why the 12-record portable trajectory
file is **588 bytes** (12-byte header + 12 × 48), name every field, then
truncate a private copy and predict how Python, C and Rust respond before you
run them. Exit codes: `0` passed, `3` blocked (a required optional dependency is
absent), `1` failed (a real build/assertion error — not a missing-dependency
excuse).

Repeat `--unit sys00`…`sys09`. Read [docs/v17/FIRST_RUN.md](../v17/FIRST_RUN.md)
and [docs/v17/SOURCE_MAP.md](../v17/SOURCE_MAP.md) for what each unit teaches and
where work remains.

## 4. The connected real-data demonstration

Once C, C++ and TypeScript toolchains are present:

```powershell
uv run --no-sync python learn.py demo --output my_work/integrated_demo01
```

Open `my_work/integrated_demo01/index.html` and read `results.json`. The demo
walks one selected SPL basketball excerpt through the portable binary contract,
a C reader and Rust validator, a Python initial-state fit, a C++ trajectory
prediction, an SQL error audit, and a TypeScript-validated viewer.

Expected measured values (this repository, reproduced 4 October 2026 — see
[V17_INTEGRATION.md](V17_INTEGRATION.md)):

| Result | Value |
|---|---|
| Records / portable binary | 12 / 588 bytes |
| C++ vs Python max difference | 8.881784197001252e-16 m |
| Height fitting RMSE | 0.017536917337837687 m |
| Two-point later height MAE | 0.04881247418842305 m |
| Last-height baseline MAE (**better**) | 0.0446230812746351 m |
| Fitting-mean baseline MAE | 0.25015376535622336 m |

The honest result is that the **simple last-height baseline beats the fitted
model on those two later points**. Confidence was not supplied and stays unknown.
This is a selected excerpt, not independent physical ground truth.

## 5. Show the whole system is complete and honest

This is the acceptance pass. Run each in a fresh directory and inspect the exit
code and the JSON it writes.

```powershell
$env:PYTHONUTF8 = '1'
uv lock --check                                                    # lock matches the manifest
uv run --no-sync python -m pytest -q -ra                           # full Python suite
uv run --no-sync python -m unittest discover -s systems/tests -p 'test_*.py'
uv run --no-sync python learn.py workbooks --check                 # 181 generated interfaces, no drift
uv run --no-sync python learn.py verify-projects --output my_work/projects_acceptance01
uv run --no-sync python tools/verify_v17_archive.py                # only against a freshly extracted archive
```

On this Windows host the reference pass produced **876 passed, 6 skipped**
(Python suite) and **24 passed** (systems suite), and the ten-project matrix
produced **8 passed / 0 failed / 2 blocked** (sys04 OpenCV headers, sys08 PyO3).
`verify-projects` intentionally exits `3` when any requested unit is blocked —
that is a truthful partial, not an all-pass.

**"Complete" means, precisely:**

- every command above ran and its exit code and JSON were inspected;
- blocked items are labelled blocked, not relabelled passed;
- failures and interrupted attempts are retained, not deleted;
- the real-data numbers match, **including the baseline that beats the model**.

**"Complete" does not mean:** learner mastery, clean-install proof, deployment
success, GPU/CUDA execution, PyO3 packaging, C++ OpenCV execution, original
notebook parity for all 133 references, or publisher-book coverage. Those remain
explicitly open and are listed in [V17_INTEGRATION.md](V17_INTEGRATION.md) and
[VERIFICATION.md](VERIFICATION.md).

## 6. Optional: the language notebooks and the full native track

```powershell
uv run --no-sync python learn.py workbooks --check
uv run --no-sync jupyter lab        # open learning/workbooks/index.html or workbooks/polyglot/index.html
uv run --no-sync python native_course.py compare --lab stage01 --output my_work/native_stage01_99
uv run --no-sync python native_course.py verify --science --output my_work/native_acceptance99
```

Python interfaces run the actual original scientific notebook; Go and Rust
interfaces compile and run the real native programs. Never hand-edit generated
notebooks — edit `systems/tools/generate_workbooks.py` (or
`tools/build_language_notebooks.py`) and regenerate.

## 7. Your daily loop from here

Continue at **topology Stage 01** and never restart the whole course:

```powershell
uv run --no-sync python course.py next
```

Explain the idea. Predict one result. Implement it in a real project. Break one
assumption deliberately in an isolated copy. Apply it to registered real data.
Then record what surprised you, what failed, why, the Python comparison, and an
unsupported conclusion. Use a **new `my_work/` directory** for each attempt and
preserve every one.
