# Repository layout: who owns what

The repository holds six kinds of thing. They look similar on disk and have
completely different owners, which is the main source of confusion. This file
defines every path once.

## The paths, defined

| Path | What it is | Owner | Edit it? |
|---|---|---|---|
| `curriculum/catalog.json` | the **single** owner of the 31-stage lesson order | course | no |
| `curriculum/experiments.json` | the 25 named cases | course | no |
| `lessons/` | canonical written explanations | course | no |
| `notebooks/` | original worked Python labs. **No Go or Rust here.** | course | your learner notebook |
| `practice/` | original learner assignments and answers | course | **yes, your copy** |
| `workbooks/` | optional written workbooks (`workbooks/00_workbook.md` …) | course | no |
| `course.py` | the canonical Python course workflow | tooling | no |
| `native/protocols/labs.json` | the **single** owner of the 57 native experiment definitions | course | no |
| `native/go/` | reference Go implementation | read-only | no |
| `native/rust/` | reference Rust implementation (vendored deps) | read-only | no |
| `native/python/` | independent data and scientific checks | read-only | no |
| `native/guides/` | language, setup and deployment guidance | read-only | no |
| `native/evidence/` | committed execution records | evidence | no |
| `native/deploy/` | Dockerfiles, Compose and the Kubernetes Job manifest | deployment | no |
| `native_course.py` | builds, runs and compares the native labs | tooling | no |
| `tools/build_language_notebooks.py` | the **single** owner of `workbooks/polyglot/` | tooling | no |
| `workbooks/polyglot/python/` | 57 notebooks that run the canonical Python reference | generated | no |
| `workbooks/polyglot/go/` | 57 notebooks that run the real Go program | generated | no |
| `workbooks/polyglot/rust/` | 57 notebooks that run the real Rust program | generated | no |
| `tools/verify_language_notebooks.py` | the 171-entry runtime sweep | tooling | no |
| `tools/evidence_pointer.py` | explicit evidence resolution | tooling | no |
| `tools/check_matrix.py` | the separated check runner | tooling | no |
| `tools/native_deploy_verify.py` | real image/Job verification | tooling | no |
| `docs/release/` | verification, checks, layout and import records | documentation | no |
| `deploy/`, `compose.yaml`, `Dockerfile` | the Python course container and cluster assets | deployment | no |
| `systems/catalog.json` | the **single** owner of the sys00–sys09 engineering-unit order | course | no |
| `systems/` | real engineering projects: `c/`, `cpp/`, `rust_validator/`, `go_service/`, `typescript/`, `gpu/`, `pyo3/`, `python/`, `tools/`, `tests/`, `lessons/`, `evidence/` | course | your private copy under `my_work/` |
| `learning/workbooks/` | generated reference interfaces (57 units × Python/Go/Rust plus project interfaces) | generated | no — regenerate with `systems/tools/generate_workbooks.py` |
| `learning/rust_from_python.md` | hand-maintained worked guide: project setup, daily commands, Python comparison. Owns no stage order | optional | **yes if you keep your own notes** |
| `learn.py` | the engineering front door (sessions, projects, demo, project matrix) | tooling | no |
| `LEARN_TOPOLOGY.html` | the combined navigation page for both layers | generated | no |
| `docs/v17/` | the archive's first-run, source-map, migration and verification records | documentation | no |
| `docs/release/START_TO_FINISH.md` | the ordered start-to-finish journey | documentation | no |
| `optional/rust_practice/` | optional, additive Rust practice crate (ownership, typed errors, compiler cases). Owns no lesson order and no lab key | optional | **yes, your private `my_work/` copy** |
| `optional/world_model/` | optional, additive worked reference: a CartPole *world model* in Python (PyTorch, optional) and dependency-free Rust, plus an independent Rust persistence reduction. Owns no lesson order and no lab key | optional | **yes, your private `my_work/` copy** |
| `optional/world_model/rust_ladder/` | optional, additive beginner crate: one runnable example per rung (WM01–WM09), with a Python mirror in `optional/world_model/python/ladder/`. Owns no lesson order and no lab key | optional | **yes, your private `my_work/` copy** |
| `my_work/` | **your** private attempts, runs and evidence (git-ignored) | **you** | **yes** |

## The four ownership rules

1. **Lesson order** lives in `curriculum/catalog.json` and nowhere else.
2. **Native experiment definitions** live in `native/protocols/labs.json` and
   nowhere else. `workbooks/polyglot` contains no catalogue of its own.
3. **Generated notebooks are never hand-edited.** Change
   `tools/build_language_notebooks.py`, regenerate, then run
   `--check`. It refuses unregistered files on purpose, so a hand-added README
   would fail it.
4. **Your work goes in `my_work/`.** Never edit a reference answer or the shared
   `native/go/` / `native/rust/` source to complete an assignment.
5. **Engineering-unit order** lives in `systems/catalog.json` and nowhere else.
   A project check compiles **your private `my_work/` copy**, not the reference
   source, so editing and breaking it is the exercise.

## The distinction people get wrong

| Path | Role |
|---|---|
| `native/go/`, `native/rust/` | the **reference**. Committed, shared, read-only. Every lab uses it. |
| `my_work/<session>/native/go/`, `.../rust/` | **your copy**, created by `native_course.py prepare`. Edit here, then `go test` / `cargo test` in that copy. |

`notebooks/` is the original course and has **no** `go` or `rust` folder. The
171 language notebooks are under `workbooks/polyglot/`.

## Which file do I change?

| I want to… | Change this | Then |
|---|---|---|
| add or reorder a stage | `curriculum/catalog.json` | run `course.py verify` |
| change what a native lab computes | `native/protocols/labs.json` and the dispatch in `native/go/engine/labs.go` / `native/rust/src/labs.rs` | run `native_course.py verify --science` |
| fix wording in a generated notebook | `tools/build_language_notebooks.py` | regenerate, then `--check` |
| do an assignment | `my_work/` | run the lab yourself |
| practise Rust ownership without touching the reference | a copy of `optional/rust_practice/` | `cargo test --offline --locked` in the copy |
| learn how a world model works, in both languages | a copy of `optional/world_model/` | `cargo test --offline --locked`, then the Python run in `my_work/` |
| build one from `Hello, world!` upwards | a copy of `optional/world_model/rust_ladder/` | `cargo run --example 01_state`, then WM02 … WM09 |
| add a check | `tools/check_matrix.py` | add a test for it |
| record what actually ran | `docs/release/` | keep failures in the record |

## Commands that match the layout

```powershell
$env:PYTHONUTF8 = '1'

# course
uv run --no-sync python course.py next
uv run --no-sync python course.py run --stage 1 --output my_work/stage01_ref01

# native labs
uv run --no-sync python native_course.py list
uv run --no-sync python native_course.py compare --lab stage01 --output my_work/stage01_native01

# generated notebooks
uv run --no-sync python tools/build_language_notebooks.py
uv run --no-sync python tools/build_language_notebooks.py --check
uv run --no-sync python tools/verify_language_notebooks.py --output my_work/nb_verify01

# separated checks
uv run --no-sync python tools/check_matrix.py --list
uv run --no-sync python tools/check_matrix.py --fast
```

## What a link in a notebook means

The notebooks sit three levels deep, so their links are root-anchored. Each
notebook opens with a **"Where every path points"** legend that defines the
vocabulary. A bare `` `lessons/01_lesson.md` `` in prose is a *label*; the legend
says where it actually is. Every clickable link resolves from the notebook's own
folder — a test enforces that.
