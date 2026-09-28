# Native16 import record (Go/Rust native track)

Prepared 26 September 2026. This records what was imported from
`Listening_to_Shape_Learning_System_v16.zip` into this repository, what was
deliberately not imported, and what actually executed on this machine.

This repository continues to identify as **v12** for its Python package. The
native material is an **additive extension**, not a package upgrade. The
archive's own `docs/v16/MIGRATION.md` scoped the additive import to the native
paths and required preserving the genuine `uv.lock`, `pyproject.toml`, local
Windows fixes and learner work — that scope was followed.

## Imported (additive; nothing pre-existing was overwritten)

| Path | Files | What it is |
|---|---|---|
| `native/` | 2008 | Go + Rust implementations, 57 lab guides, bounded data readers, tests and fixtures |
| `polyglot/` | 191 | Historical v14 Go/Rust companion source and specs (superseded by `native/`; kept for comparison) |
| `curriculum/extensions/poux_spatial_ai/` | 7 | Poux six-hub spatial-AI extension and its bridge test |
| `deploy/polyglot/` | 2 | Companion Job example and README |
| `docs/v16/` | 10 | Native16 migration, first session, data index, verification, status, example results |
| `docs/v14/` | 4 | Polyglot-edition migration and readme |
| `reports/v14/` | 62 | Archived v14 evidence records (historical inputs, so the polyglot tests can read them) |
| `native_course.py`, `polyglot.py`, `START_NATIVE.html` | 3 | Launchers; **stdlib-only**, no new Python dependencies |
| `tests/test_native_v16.py`, `tests/test_polyglot_v14.py` | 2 | Native-runner and polyglot-spec contracts |
| `tools/polyglot_verify.py` | 1 | Polyglot smoke verifier |
| `.github/workflows/native-course-v16.yml`, `.github/workflows/polyglot.yml` | 2 | Supplied workflows (not executed here) |

`.gitignore` gained `Listening_to_Shape_Learning_System_v14.zip`,
`Listening_to_Shape_Learning_System_v16.zip`, `**/target/` and
`.native-cache/`. The vendored Rust source under `native/rust/vendor` (36
crates with licenses) and `polyglot/rust` are **source and remain tracked**;
only compiler output directories are ignored.

## Deliberately not imported (deferred, not rejected)

The archive is a v13/v14 base wrapped around native16. The following were held
back because they are a coordinated version change, not additive learning
material, and the repository's `uv.lock` is a genuine, resolved lock tied to the
current package version:

- `src/shape_lab/result_packet.py`, `study_session.py` and the v13 edits to
  `acceptance.py`, `cli.py`, `course.py`, `deployment.py` (`course.py study` /
  `report` commands), with `tests/test_results_v13.py`,
  `tests/test_deployment_receipts_v13.py` and
  `docs/release/RESULTS_WORKFLOW.md`.
- Package version bump `12.0.0` → `14.0.0` in `pyproject.toml` and
  `src/shape_lab/__init__.py`.
- v12 → v13/v14 relabels in `curriculum/catalog.json`, `curriculum/START.md`,
  `RELEASE_MANIFEST.json`, `README.md`, `AGENTS.md`, root docs, the CI workflow
  (`image:12` → `13`) and `deploy/kubernetes/resources.json` (namespace
  `shape-learning-v12` → `v13`).

Relabelling without bumping `pyproject.toml`/`__init__.py` and regenerating
`uv.lock` together would have made `tests/test_release_version_v3.py` fail; the
archive's own migration doc lists that reconciliation as optional step 5/6. A
coordinated v14 reconciliation is a separate, reviewable change.

`notebooks/00_lab.ipynb`, `01_lab.ipynb` and `02_lab.ipynb` have genuine source
edits in the working tree. Those are local learner work and were **preserved**,
not reverted to the archive copies.

The 130 other notebook differences in the archive are saved-output refreshes
only; comparing stripped notebook source confirmed the teaching cells are
identical, so nothing was overwritten.

## What executed on this machine

Environment: Windows x86-64, Python 3.13.5, Go 1.27.1, Rust/Cargo 1.97.1
(stable) with the archive-pinned **1.90.0** toolchain provisioned by `rustup`
and selected by `native/rust/rust-toolchain.toml`. The archive's tested
reference versions were Linux x86-64, Go 1.23.2, Rust 1.90.0.

| Check | Observed result here |
|---|---|
| Full repository Python suite (before notebooks) | **766 passed, 3 skipped, 0 failed** |
| New native/polyglot tests only | **16 passed** |
| Full repository Python suite (after notebooks) | **774 passed, 3 skipped, 0 failed** |
| Full repository Python suite (after verification tooling) | **800 passed, 4 skipped, 0 failed** |
| Full repository Python suite (after CI/deploy tooling) | **810 passed, 4 skipped, 0 failed** |
| Full repository Python suite (final) | **811 passed, 4 skipped, 0 failed** |
| `native_course.py doctor` | exit 0; toolchains found; all 55 registered data files pass |
| `native_course.py build --lang all` | Go exit 0; Rust exit 0 (offline, `--locked`, 36 vendored crates) |
| `native_course.py test --lang all` | Go **34** named tests/subtests pass, 0 fail; Rust **28** pass, 0 fail, 0 ignored |
| `native_course.py compare --lab stage01` | passed; 17 values compared, max absolute difference **0.0**, inputs unchanged |
| `native_course.py verify --science` | **passed**: 57 Go + 57 Rust lab runs, **57/57** comparisons, **110** data checks, **64** fixture checks, **220** independent science checks; largest metric absolute difference **2.3283064365386963e-10** |

Stage 01 reproduced the documented results: `rank_R = 3`, `rank_F2 = 2`,
augmented Iris rank `4`, kernel `(-2, 3, 0, 0, 1)`, residual 0, Go ≡ Rust.

Evidence lives under `my_work/` (private, git-ignored):
`native_build01/`, `native_tests01/`, `native_stage01_01/`,
`native_acceptance01/`. Use a new output directory for every new attempt;
existing results are never overwritten.

## Not run here (do not read as passes)

- The 133 original Python reference notebooks were **not** replayed.
- `original_notebook_parity` is **`not_certified`**; `verify
  --require-original-parity` refuses that claim by design and was left in place.
- Docker images, Kubernetes Jobs, macOS, GPU, and the remote CI workflows did
  not execute.
- No external large dataset or model-weight collection was downloaded for this
  import.

## Added afterwards: three-language learning notebooks

On top of the import above, `tools/build_language_notebooks.py` generates an
interactive route through the same 57 native units:

| Path | Count | What it is |
|---|---|---|
| `workbooks/polyglot/python/*.ipynb` | 57 | reads the real registered inputs and an existing native run, re-verifying input hashes |
| `workbooks/polyglot/go/*.ipynb` | 57 | compiles and runs the **real Go program**, then compares |
| `workbooks/polyglot/rust/*.ipynb` | 57 | compiles and runs the **real Rust program**, then compares |
| `workbooks/polyglot/{index.html,README.md}` | 2 | browsable index |
| `tools/build_language_notebooks.py` | 1 | deterministic generator (stdlib only) |
| `tests/test_language_notebooks.py` | 1 | completeness, freshness, parseability, no-Python-delegation |

Full guide: [LANGUAGE_NOTEBOOKS.md](LANGUAGE_NOTEBOOKS.md). Stage 01 was executed
with fresh kernels in all three languages; the Go and Rust notebooks reproduced
`real_rank 3`, `f2_rank 2`, `augmented_rank 4`, kernel `(-2, 3, 0, 0, 1)`, and
cross-language agreement at max absolute difference `0.0` over 17 compared
values. These notebooks compute nothing scientific in Python, are unassessed,
and are not a second curriculum.

## Test-count reconciliation (why 811, not the archive's 821)

The archive reports **821 passed, 2 skipped** on its v13/v14 tree. This
repository runs the v12 tree plus the additive native/polyglot, notebook,
verification-tooling and CI/deploy tests, which is **811 passed, 4 skipped**.
The 10-test gap is the deferred v13 test files above.
The skip difference is also environmental and unrelated: this host skips one
symlink test and one POSIX mode-bit test that the Linux reference host ran.
Neither number is a measure of mathematical completeness, and the archive's
Ripser/GUDHI skips are not among this run's skips.
