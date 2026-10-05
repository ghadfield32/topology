# v17 integration record — what was merged, preserved, and executed here

Prepared 4 October 2026. This records how
`Listening_to_Shape_Learning_System_v17.zip` (41.8 MiB, 6,665 files, edition 17,
base v16) was merged into this repository, what was deliberately preserved, and
what was actually executed on this Windows machine. It complements
[NATIVE16_IMPORT.md](NATIVE16_IMPORT.md), which records the earlier native16
import and the version reconciliation this change completed.

The archive's own records remain the source of its own claims:
[docs/v17/](../../docs/v17/), [PACKAGE_V17.json](../../PACKAGE_V17.json) and
[LISTENING_TO_SHAPE_V17 in the archive]. Nothing here relabels an archive result
as a local one, and nothing here presents a blocked dependency as a pass.

## What the archive adds

| Path | What it is |
|---|---|
| `systems/` | Source-mapped engineering projects sys00–sys09: real C, C++20, pybind11, OpenCV, GPU/Triton, TypeScript, Rust, PyO3 and Go code with lessons, contracts, tools, tests and executed evidence |
| `learning/` | Generated language interfaces (57 units × Python/Go/Rust + ten project interfaces) and their index — regenerated, never hand-edited |
| `learn.py` | The engineering front door: `doctor`, `list`, `show`, `session`, `project`, `check-project`, `demo`, `verify-projects`, `workbooks` |
| `LEARN_TOPOLOGY.html` | The single navigation page for both layers |
| `docs/v17/` | The archive's FIRST_RUN, SOURCE_MAP, MIGRATION, DESIGN, VERIFICATION and AGENT_HANDOFF records |
| `src/shape_lab/result_packet.py`, `study_session.py` | Output sealing and the study/report route |
| v13 edits to `acceptance.py`, `cli.py`, `course.py`, `deployment.py` | On-disk child-evidence validation and the `study`/`report` CLI commands |
| `docs/release/RESULTS_WORKFLOW.md`, `IMPLEMENTATION_V13.md` | The learning-to-results workflow |
| `reports/v13/` | The archive's v13 evidence records used by the results workflow and the reader |
| `tools/verify_v17_archive.py`, `MANIFEST_V17.sha256` | Verification of the separately extracted archive |
| `.github/workflows/systems-learning.yml`, `.vscode/tasks.v17.example.json`, `.devcontainer/README.v17.md` | Optional systems CI and editor/container examples (not executed here) |

The archive's `systems/`, `learning/`, `learn.py` and `LEARN_TOPOLOGY.html` did
not previously exist in this repository: the earlier import had deliberately
deferred them because they were part of a coordinated version change. That
change is now completed.

## What was merged (files the archive ships a newer version of)

- `src/shape_lab/{cli,acceptance,course,deployment}.py` — the v13 additions.
- `tools/{docker_verify.py,k8s_verify.py,build_reader.py}` and
  `tests/test_repository_v10.py` — container child-evidence validation and the
  version relabels.
- `docs/release/{FIRST_RUN,VERIFICATION,DOCKER,KUBERNETES,DATA_AND_SPORTS,SPORTS_REFRESH,AGENT_HANDOFF}.md`
  and `docs/release/ENVIRONMENT_STATUS.json` — the archive's current release
  text.
- `deploy/kubernetes/resources.json`, `compose.yaml`, `.github/workflows/course-ci.yml`,
  `curriculum/{catalog,experiments}.json`, `curriculum/START.md` —
  version/image/namespace relabels.
- `reports/v14/summary.json` (new) — the reader's evidence source, derived from
  the archive's `reports/v13/summary.json` and explicitly marked as an archive
  execution record, not this checkout's totals. `reports/v12/*` historical
  records are untouched.

The 130 archive notebook files that differ from this repository carry refreshed
saved outputs only; their teaching source cells were verified identical to this
repository's, so they were **not** overwritten. The three notebooks with genuine
local source edits were likewise preserved.

## What was deliberately preserved (not overwritten)

- `uv.lock` — the genuine, working local lock. It was re-resolved with normal
  `uv lock` so its root package agrees with the 14.0.0 manifest; the resolution
  succeeded against the configured package index.
- `workbooks/polyglot/` and `tools/build_language_notebooks.py` — the local,
  fuller three-language notebook set and its generator.
- `native_course.py`'s `run_identity(...)` evidence binding, which the archive
  lacked. This was kept rather than regressed.
- `docs/release/NATIVE16_IMPORT.md` — extended with a reconciliation section
  instead of being replaced by the archive's shorter root README.
- Root `AGENTS.md`/`README.md` — the repository's own, richer guidance was kept
  and updated, not replaced by the archive's thinner generic versions.
- The repository's fuller `docs/release/FIRST_RUN.md` and `COMPLETE_COURSE.md`.
- All of `my_work/`, existing progress logs, learner notebooks and datasets.
- `.gitignore`/`.dockerignore` — the local entries for ignored delivery ZIPs,
  `.uv-python/` and `.local-bin/` were kept.

## Version reconciliation (now 14.0.0)

`pyproject.toml`, `src/shape_lab/__init__.py`, `tests/test_release_version_v3.py`,
`curriculum/catalog.json`, `RELEASE_MANIFEST.json` and
`docs/release/ENVIRONMENT_STATUS.json` identify **14.0.0**. Container and
Kubernetes references use `listening-to-shape:14` and namespace
`shape-learning-v14`. `deploy/kubernetes/resources.json` keeps the archive's
`core` profile default.

## A real portability fix (our change, not the archive's)The archive's `systems/python/workflow.py:command()` ran `tsc` by bare name.
On Windows a package-manager install is a `.cmd` shim that `CreateProcess`
cannot locate, so the integrated demonstration failed with
`[WinError 2] The system cannot find the file specified`. `command()` now
resolves the executable (including a `.cmd`/`.bat` shim through `%COMSPEC%`) to
an absolute, shell-free argv. Regression tests were added in
`systems/tests/test_workflow.py`. The same latent problem existed for any
npm/global shim; it is fixed centrally rather than per call site.

Two imported v13 tests created symlinks unconditionally and failed on a Windows
host that disallows symlink creation (as the repository's own tests already
handled). Both now skip with an explicit `Host disallows symlinks` reason, so
the check still runs on hosts that permit symlinks.

## What executed on this machine

Environment: Windows x86-64, Python 3.13.5, uv 0.12.5, GCC/G++ 14.2.0 (MSYS2),
CMake, Go 1.27.1, Rust/Cargo 1.97.1, Node 22.23.2, TypeScript 5.8.3
(`npm install --global typescript@5.8.3`), CUDA `nvcc` present. `PYTHONUTF8=1`
is required for the non-ASCII lesson text on this host.

| Check | Observed result here |
|---|---|
| `uv lock --check` | Resolved; lock and manifest agree at 14.0.0 |
| Full repository Python suite | **876 passed, 6 skipped, 0 failed** |
| New systems isolated suite | **24 passed** (21 imported + 3 added regression tests) |
| `learn.py doctor` | Toolchains reported; availability explicitly not acceptance |
| `learn.py list` | 57 application/native keys + sys00–sys09 listed |
| `learn.py workbooks --check` | 182 files, 181 notebooks, no mismatches |
| `learn.py project --unit sys01` + `check-project` | Copied project built and tested: **passed** |
| `courses.py run --stage 1` | 1/1 notebook passed; inputs unchanged |
| `native_course.py compare --lab stage01` | Go ≡ Rust ≡ Python; `run_identity` present; inputs unchanged |
| `learn.py demo` | **passed**; real selected SPL excerpt (12 frames) |
| `learn.py verify-projects` (all ten) | **8 passed, 0 failed, 2 blocked** (sys04 OpenCV, sys08 PyO3) |

### The measured-data demonstration (this run)

Source: the bundled selected SPL tracking excerpt, one participant, one trial,
12 frames. Coordinates are a unit conversion of the selected source tracking;
time is an ideal frame/sample-rate clock; confidence was not supplied and stays
unknown. Five selected points fit the initial state under fixed g = 9.81 m/s²;
two later same-shot points evaluate it.

| Result | Measured value |
|---|---|
| C++ vs Python max prediction difference | 8.881784197001252e-16 m |
| Height fitting RMSE | 0.017536917337837687 m |
| Two-point later height MAE | 0.04881247418842305 m |
| Last-observed-height baseline MAE | 0.0446230812746351 m |
| Fitting-mean height baseline MAE | 0.25015376535622336 m |
| Portable binary size | 588 bytes (12-byte header + 12 × 48) |

**The simple last-height baseline beats this fitted model on those two later
points.** The course keeps that result visible instead of presenting only the
weaker mean baseline. No release detection, significance or out-of-athlete
generalisation is established.

## Not run here (do not read as passes)

- Docker image build/run and live Kubernetes admission/Job were not executed.
  `docker_verify.py` and `k8s_verify.py` report readiness from the local daemon
  only; they never emulate a pass.
- GPU/Triton/CUDA kernels, Nsight and mixed-precision comparisons were not
  executed. The CUDA probe is source with an explicit gate.
- C++ OpenCV (sys04) needs a development package not present here; the Python
  OpenCV probe is not C++ equivalence.
- PyO3/maturin (sys08) are not resolved; no PyO3 lock is fabricated.
- The 133 original Python reference notebooks were not replayed in full, and
  `original_notebook_parity` remains `not_certified`.
- The remote `systems-learning.yml` workflow was not run on GitHub.

## How to reproduce this verification

```powershell
$env:PYTHONUTF8 = '1'
uv lock --check
uv run --no-sync python -m pytest -q -ra
uv run --no-sync python -m unittest discover -s systems/tests -p 'test_*.py'
uv run --no-sync python learn.py doctor
uv run --no-sync python learn.py workbooks --check
uv run --no-sync python learn.py project --unit sys01 --output my_work/c_reader01
uv run --no-sync python learn.py check-project --workspace my_work/c_reader01 --output my_work/c_reader01/attempt01
uv run --no-sync python learn.py demo --output my_work/integrated_demo01
uv run --no-sync python learn.py verify-projects --output my_work/projects_acceptance01
```

Use a new output directory for every attempt; existing results are never
overwritten. This records local execution, not learner mastery.
