# Listening to Shape — repository edition v14

A beginner-first course from topology to geometry, dynamics and representation learning. **One primary route:** 31 core stages, 5 representation units, 25 named cases, 133 worked references and 56 independent learner notebooks. Industry and sports sources retain their own provenance and terms. Version 14 adds a connected **engineering layer** (real C/C++/Rust/Go/TypeScript/GPU projects) on top of the existing research layer; it does not replace the 31-stage curriculum.

**New front door:** open [LEARN_TOPOLOGY.html](LEARN_TOPOLOGY.html) for the navigation page that joins the two layers. **Ordered journey:** [docs/release/START_TO_FINISH.md](docs/release/START_TO_FINISH.md). **Read:** open [START_HERE.html](START_HERE.html) for the offline reader. **Start:** [first-run guide](docs/release/FIRST_RUN.md) · [v17 first run](docs/v17/FIRST_RUN.md). **Evidence:** [verification](docs/release/VERIFICATION.md) · [v17 integration record](docs/release/V17_INTEGRATION.md). **Import:** [Git guide](docs/release/GIT_IMPORT.md). **Repository assistant:** [copy/paste handoff](docs/release/AGENT_HANDOFF.md).

## Two connected layers, one curriculum

**Notebook → understand it. Project → prove you can engineer it.** Each lesson follows **Explain → Predict → Implement → Break → Apply**.

| Layer | Purpose | Where you work |
|---|---|---|
| Mathematical and research | Learn definitions, derive results, inspect data, run experiments, explain limitations | the 31 topology lessons, Python references and language workbooks |
| Engineering | Build, debug, test, profile and integrate real programs | `systems/` CMake/Cargo/Go/TypeScript projects |

The engineering units run **sys00–sys09** (source-mapped from the supplied Stage 0–9 headings); they never renumber topology Stage 00–30.

## Repository map

Six kinds of thing live here, and they have different owners. Full definitions:
[docs/release/REPOSITORY_LAYOUT.md](docs/release/REPOSITORY_LAYOUT.md).

| Path | What it is | You edit it? |
|---|---|---|
| `curriculum/catalog.json` | **the** owner of the 31-stage lesson order | no |
| `lessons/`, `notebooks/`, `practice/` | canonical explanations, worked Python labs, learner assignments | your learner notebook |
| `course.py` | the canonical Python course workflow | no |
| `native/protocols/labs.json` | **the** owner of the 57 native experiment definitions | no |
| `native/go/`, `native/rust/` | reference Go and Rust implementations | no — read-only reference |
| `native/python/` | independent data and scientific checks | no |
| `native/guides/` | language and implementation guidance | no |
| `native_course.py` | builds and compares the native labs | no |
| `tools/build_language_notebooks.py` | **the** owner of `workbooks/polyglot/` | no |
| `workbooks/polyglot/{python,go,rust}/` | 171 generated teaching notebooks | no — regenerate instead |
| `systems/` | real engineering projects, source-mapped lessons and evidence | your private copy under `my_work/` |
| `learning/` | generated reference interfaces and the navigation view | no — regenerate instead |
| `learn.py` | the engineering front door (sessions, projects, demo) | no |
| `docs/release/` | verification, checks, layout and import records | no |
| `my_work/` | your private attempts and evidence (git-ignored) | **yes** |

Four rules keep this from drifting:

1. **Lesson order** is changed in `curriculum/catalog.json` only.
2. **Native experiment definitions** are changed in `native/protocols/labs.json` only.
3. **Generated notebooks** are never hand-edited: fix `tools/build_language_notebooks.py`, then
   run it and `--check`.
4. **Your answers and experiments** go in `my_work/`, never into a reference file.

## Where do I start?

| I want to… | Go to |
|---|---|
| see the whole journey | [LEARN_TOPOLOGY.html](LEARN_TOPOLOGY.html) |
| begin the course | [START_HERE.html](START_HERE.html) or `course.py next` |
| start a guided session (predict → run → reflect → report) | [docs/release/RESULTS_WORKFLOW.md](docs/release/RESULTS_WORKFLOW.md) |
| learn a lab in Python, Go and Rust | [workbooks/polyglot/index.html](workbooks/polyglot/index.html) |
| understand the Go/Rust track | [START_NATIVE.html](START_NATIVE.html) |
| build a real engineering project | [docs/v17/FIRST_RUN.md](docs/v17/FIRST_RUN.md) · `learn.py project --unit sys01` |
| do Stage 01 now | [docs/release/STAGE01_WALKTHROUGH.md](docs/release/STAGE01_WALKTHROUGH.md) |
| know what actually ran | [docs/release/CHECKS.md](docs/release/CHECKS.md) |
| deploy natively | [native/guides/DEPLOYMENT.md](native/guides/DEPLOYMENT.md) |

## The engineering front door (`learn.py`)

```powershell
uv run --no-sync python learn.py doctor        # which toolchains exist (no installs)
uv run --no-sync python learn.py list          # existing applications + sys00–sys09
uv run --no-sync python learn.py project --unit sys01 --output my_work/c_reader01
uv run --no-sync python learn.py check-project --workspace my_work/c_reader01 --output my_work/c_reader01/attempt01
uv run --no-sync python learn.py demo --output my_work/integrated_demo01
```

`check-project` compiles **your private copy**, not the reference source, so editing and breaking it is the point. A missing optional dependency returns status `blocked` (exit 3); a compiler or assertion error is `failed` (exit 1). See [docs/v17/FIRST_RUN.md](docs/v17/FIRST_RUN.md) for the full journey and [docs/release/RESULTS_WORKFLOW.md](docs/release/RESULTS_WORKFLOW.md) for the study/report loop.

## Native16 addition (Go and Rust)

Open [START_NATIVE.html](START_NATIVE.html) for the additive native track: 57 learning units implemented in both Go and Rust, each with a guide, three independent challenges and inspectable evidence. The [import record](docs/release/NATIVE16_IMPORT.md) states exactly what was imported, what was deferred, and what executed on this machine.

```powershell
$env:PYTHONUTF8 = '1'
uv run --no-sync python native_course.py doctor
uv run --no-sync python native_course.py build --lang all --output my_work/native_build01
uv run --no-sync python native_course.py compare --lab stage01 --output my_work/native_stage01_01
uv run --no-sync python native_course.py verify --science --output my_work/native_acceptance01
```

Go and Rust do their own decoding, mathematics and training; the Python launcher only coordinates and compares. This is **not** certified as operation-for-operation parity with all 133 original Python notebooks, and `verify --require-original-parity` deliberately refuses that claim.

### Notebooks: learn any lab in any of the three languages

Prefer notebooks to the command line? Every one of the 57 labs has a matched set:

| Route | What it does |
|---|---|
| `workbooks/polyglot/python/<lab>.ipynb` | inspects the real registered inputs and an existing native run |
| `workbooks/polyglot/go/<lab>.ipynb` | compiles and runs the **real Go program**, then compares |
| `workbooks/polyglot/rust/<lab>.ipynb` | compiles and runs the **real Rust program**, then compares |

Start at [the index](workbooks/polyglot/index.html) (or the [plain text](workbooks/polyglot/README.md)). Regenerate with `python tools/build_language_notebooks.py`. These are unassessed and are not a second curriculum — the Python lesson stays canonical.

Verify them, all 171 of them, with `python tools/verify_language_notebooks.py --output my_work/nb_verify01`. It exits non-zero unless coverage is complete.

**Guides:** [notebook guide](docs/release/LANGUAGE_NOTEBOOKS.md) · [Stage 01 walkthrough](docs/release/STAGE01_WALKTHROUGH.md) · [separate checks](docs/release/CHECKS.md)

## Native setup

Install uv through its official instructions, then run from this folder:

```bash
uv python install 3.13.5
uv run --no-project --python 3.13.5 python tools/bootstrap.py --profile physics
uv run --no-sync python course.py acceptance --profile physics --references first --output my_work/acceptance01
uv run --no-sync python course.py stage 0
uv run --no-sync python course.py practice 0 --output my_work/practice00_attempt01
uv run --no-sync jupyter lab
```

Normal setup must resolve/check a genuine `uv.lock` and synchronize it. A clean install was blocked in the build environment, so no fabricated lock is supplied. Review and commit your successful resolver output. Core omits PyTorch; physics supports all references; full additionally requires Ripser/GUDHI with no skipped checks.

## Run a lesson or application

```bash
uv run --no-sync python course.py run --stage 0 --output my_work/stage00_attempt01
uv run --no-sync python course.py cases
uv run --no-sync python course.py run --case wine --output my_work/wine01
uv run --no-sync python course.py practice s00 --output my_work/sports_practice01
uv run --no-sync python course.py acceptance --profile physics --references all --jobs 1 --output my_work/course01
```

A run directory must be new. Experiments copy clean source inputs, not old report caches; notebooks use fresh kernels with interpreter/source checks. Reference source can be read-only. Private answers and progress are not automatically graded or published.

## Container and cluster practice

Follow [Docker](docs/release/DOCKER.md) then [Kubernetes](docs/release/KUBERNETES.md). Static configuration/policy tests are not image builds or live cluster execution. This host lacked those runtimes. Live application requires an explicitly selected disposable context and new namespace; no automatic cluster/namespace/PVC deletion occurs.

## What changed in v14

Version 14 reconciles the repository with the v17 archive and completes the previously-deferred version upgrade. It imports the **systems learning layer** (`systems/`, `learning/`, `learn.py`, `LEARN_TOPOLOGY.html`, `docs/v17/`), the **study-and-report workflow** (`course.py study` / `course.py report`, output sealing, `docs/release/RESULTS_WORKFLOW.md`), the ten deferred v13 tests, and the `reports/v13` evidence the reader uses. It also fixes a real Windows portability bug the archive had: a package-manager command shim (`tsc.cmd`) is now resolved to a shell-free argv instead of failing with `WinError 2`.

It preserves, rather than overwrites, the genuine re-resolved `uv.lock`, the `workbooks/polyglot/` notebooks and generator, the local `NATIVE16_IMPORT.md` record, `native_course.py`'s `run_identity` evidence binding, and existing learner notebook edits. The import record states exactly what ran and what did not: [docs/release/NATIVE16_IMPORT.md](docs/release/NATIVE16_IMPORT.md).

All 25 case practice routes are registered. Direct dependency version mismatches block readiness. Acceptance checks child JUnit totals and exact reference identities, not just exit codes, and now also validates sealed run outputs and container child evidence. Read-only source copying is made writable only in the disposable workspace. Kubernetes denies unsafe/mixed objects; its reader no longer mounts private result storage. Serial execution is the default after a recorded parallel kernel startup failure. Read the exact current evidence and remaining limits before presenting results.

Use each lesson once, repair only the missing prerequisite, attempt your own solution, then return for delayed recall. A test pass is not a proof of mastery, clinical or sports validity, complete-book coverage, or universal physical fidelity. See [source coverage](docs/release/SOURCE_COVERAGE.md) and [license/attribution](LICENSE.md).
