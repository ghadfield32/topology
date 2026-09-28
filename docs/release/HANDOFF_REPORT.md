# Handoff completion report

Branch: `review/native16-notebooks`. Base revision: `52aa1b6`, which is also
`origin/main`.

The integration is committed on this branch as **`fe2542b`**. It has not been
pushed or merged. A fresh export of that revision reproduces the generated
inventory exactly (see *Fresh checkout* below).

## Second handoff: premises checked against the actual repo

The follow-up plan was written from an **earlier** state (774 tests, "only the
Stage 01 triad was executed"). Checked against the current checkout:

| Plan premise | Actual state |
|---|---|
| 171 workbooks generated | true |
| Only the Stage 01 triad executed | **outdated** — the full sweep now runs: **171/171 passed** |
| Suite 774 passed / 3 skipped | **outdated** — now **817 passed / 3 skipped** |
| Python workbook only inspects an existing run | **was true** — now fixed, see below |
| Python workbook relation to the scientific experiment unclear | **was true** — the notebook now runs the canonical reference |
| `native/` is the current route, `polyglot/` historical | true, preserved |
| 31 stages, 57 native labs | true, verified |
| Local work untracked on `main` | true — **all** of it is untracked |
| `uv lock --check` | **passed**, 130 packages, exit 0 |

Four genuine gaps remained and were addressed. Several plan requests were already
satisfied by the first handoff's work (`tools/verify_language_notebooks.py`,
`tools/evidence_pointer.py`, the full sweep, explicit evidence modes).

### What this round changed

1. **`--check` was a silent no-op.** The plan's Phase B command
   `tools/build_language_notebooks.py --check` previously ignored the unknown
   flag, **rewrote all 171 workbooks, and exited 0**. There is now a real
   checker: it renders the expected tree in memory (a single `render()` source of
   truth), compares it, and exits 1 naming every missing, stale or unexpected
   artifact. Proven able to fail: editing `README.md` by hand returns 1;
   restoring it returns 0. Unknown flags are now a hard error.
2. **Fresh vs review execution modes.** The Python notebook's evidence cell now
   has `MODE = "fresh"` (default) or `MODE = "review"`, with `PINNED_RUN`
   required in review mode. Fresh mode **creates** the evidence by compiling and
   running the native labs into the notebook's own directory — verified by
   executing Stage 01, which produced a new run whose identity was recorded.
   Review mode opens a specific run and labels it as previous execution. Neither
   scans for "the newest plausible folder".
3. **Learner mutation is now a full cycle.** The test proves the private copy is
   what gets evaluated (via `go list -f {{.Dir}}`), then fail → repair → pass:
   the XOR→OR edit fails `TestRankField`, and restoring the source makes it pass
   again. Both languages verified.
4. **An inaccurate aliasing claim was corrected.** My earlier note called the Go
   `append` a "row-aliasing" case. It is not one: `clone` deep-copies each row
   (`b[i] = append([]float64(nil), a[i]...)`), so `x` cannot be reached. The
   walkthrough now says so explicitly and turns the correct fact into the
   exercise (delete `clone` and observe the difference).

## Scope note first

The handoff expected `Topology_Repository_Implementation_Plan.md` in the
checkout. **It is not present**, and no copy was found under the user profile
either. It is reported here rather than invented. The work below follows the
handoff's own phase list, its stated constraints and `AGENTS.md`.

## 1. Audit and checkpoint

| Item | Value |
|---|---|
| Branch | `review/native16-notebooks` (created from `main`) |
| HEAD | `52aa1b6f0194db041904c820a8f4052cebf112ba` |
| `origin/main` | identical to HEAD |
| Dirty entries at start | 38 |
| Committed by this work | **none** |

HEAD equals `origin/main`, so **all native16, notebook and tooling work was
local-only and uncommitted.** That is why no commit was made automatically:
committing would have decided for the user how to group a large body of work.

Checkpoint evidence: `my_work/checkpoint01/checkpoint.json`, produced by
`tools/checkpoint_current_state.py`. It records branch, HEAD, dirty count, tool
paths and versions, and the inventory (31 stages, 57 labs, 55 registered data
files, 171 notebooks).

Deletions at the root (`COMPLETE_COURSE_V2..V7.md`) are the 536-byte retired
**stubs**; their content also exists as `archive/COMPLETE_COURSE_V2..V7.md`.
This was verified by comparing against `HEAD`, not assumed.

## 2. One source of truth; generator fixed, not notebooks

Verified: `curriculum/catalog.json` is the only curriculum owner (31 stages),
`native/protocols/labs.json` is the only native registry (57 keys, declared
count matches actual), and `workbooks/polyglot` contains **no** JSON catalogue.
`data/industries/catalog.json` is a data index, and `polyglot/specs/labs.json`
is the historical v14 companion spec — neither claims the curriculum.

Generator changes in `tools/build_language_notebooks.py`:

- The Python route now **runs the canonical reference** via
  `shape_lab.course.run_references(..., jobs=1, timeout=300)` — fresh kernel,
  isolated copied workspace, provenance probe, `allow_errors=False`.
- Sections are labelled by intent: "Run the canonical Python experiment",
  "input audit", "output audit". The audit sections no longer read as a
  re-implementation.
- Script references are handled separately. The Poux lab's reference is
  `curriculum/extensions/poux_spatial_ai/bridge.py`, so it is classified
  `script`, its companion `test_bridge.py` is run instead, and a test asserts it
  is never handed to `run_references`.
- The misleading `[lesson](reference)` link was corrected.

## 3. Evidence dependencies are explicit

New `tools/evidence_pointer.py`. Resolution order: explicit `run_dir`, then
`my_work/native_evidence.json`, then **nothing** in strict mode. A clean QA
worktree returns nothing rather than picking someone's newest `my_work` run.
Older evidence is usable only in labelled review mode, and the notebook prints
that warning itself.

`native_course.py` now writes an `identity` block into `execution.json`:
per-language `source_sha256` and `binary_sha256`, an
`input_fingerprints_sha256`, and the protocol. The Python notebook compares the
recorded source hash against the live source and prints `MATCH` or `DIFFERS`.
Verified on a real run (`my_work/identity_check01`).

## 4. Independent practice routes through real `prepare` copies

`tests/test_learner_mutation.py` proves the loop:

- Baseline: untouched `native/go` passes `go test -count=1 ./...` (exit 0).
- A private copy with F2 elimination changed from XOR to OR **fails**, exit 1,
  specifically in `TestRankField`.
- The canonical `native/go/engine/math.go` hash is unchanged afterwards.

The Rust equivalent runs when `SHAPE_TEST_RUST_MUTATION=1`; it was executed and
passes. `native_course.py prepare` already produces those private copies.

## 5. `tools/verify_language_notebooks.py`

Derives the expected 171 entries from the registry; audits for missing,
duplicate and unexpected notebooks; fresh kernel per entry via the repo's own
kernel-spec and provenance validator; explicit output directory; compiles each
native binary once per source identity; **serial**; `allow_errors=False`; no
error-tolerance flag exists; hashes the whole tree before and after so a mid-run
regeneration cannot produce a green mixed-source result; exits non-zero unless
coverage is complete.

Two real bugs were found and fixed during its development: an executed-cell
count that summed `execution_count` integers, and a relative output path that
broke `relative_to`.

## 6. Separate checks

`tools/check_matrix.py` runs six independently labelled checks — `contracts`,
`python`, `readers`, `native`, `science`, `notebooks` — and states in its own
output what none of them establish. Observed here:

| Check | Result |
|---|---|
| `contracts` | passed, 3.2 s |
| `python` | passed, 816 passed / 4 skipped (817 / 3 with the opt-in Rust mutation) |
| `readers` | passed (110 decoder comparisons) |
| `native` | passed (Go 34, Rust 28, 0 failed) |
| `science` | passed (57+57 labs, 110 data, 64 fixture, 220 scientific) |
| `notebooks` | **passed: 171/171**, coverage complete, 0 failed, tree unchanged |

Original 133-notebook parity remains **`not_certified`**; the
`--require-original-parity` guard was left in place.

## 7. Efficient CI

New `.github/workflows/language-notebooks.yml`:

- `push` / `pull_request`: **fast contracts only** — no native build, no sweep.
- `workflow_dispatch`: full sweep and native/science sweep, with a `scope`
  input choosing `fast` or `full`.

`tests/test_ci_workflows.py` asserts the heavy jobs stay gated behind manual
dispatch, that no run step passes an error-tolerance flag, and that evidence is
uploaded with `if: always()` and `if-no-files-found: error`.

## 8. Native deploy — actually executed

`tools/native_deploy_verify.py`. Results on this machine:

| Gate | Result |
|---|---|
| static policy parse | passed (`static_only`, explicitly not runtime) |
| docker runtime | passed, server 29.7.2 |
| image build (Go, Rust) | **passed**, both Dockerfiles including their in-build tests |
| hardened `docker run` | **passed**, exit 0 both; Go reported `real_rank 3`, `f2_rank 2` |
| Jobs in `kind-shape-learning` | **passed**: both `condition met`; a verify Pod read the PVC; both `result.json` parsed with `lab stage01`, `status completed` |

The verifier found a real defect: `kubectl apply` rejects Jobs using
`generateName`. Fixed to `create`, matching `native/guides/DEPLOYMENT.md`.

Safety: the cluster gate refuses a non-disposable context (`docker-desktop` was
blocked and the run exited 2). Manifests are rewritten into the run's own fresh
namespace. Cleanup targets only that namespace and never deletes PVCs. The
learner namespace `shape-study01` and its `learner-work` PVC were left intact —
verified by listing PVCs before and after.

## 9. Stage 01 walkthrough

`docs/release/STAGE01_WALKTHROUGH.md`. It gives the sequence, where to edit,
how to test, where metrics live, what a result cannot establish, and the daily
workflow. It does **not** derive the null vector. It uses the changed redundant
column `5*x0 + 2*x1` and requires the learner to derive the null vector first.
Its canonical command was executed to confirm it works.

## Committed revision and fresh-checkout reproducibility

Commit **`fe2542b`** on `review/native16-notebooks`, 2491 files. Not pushed.

Staged by an explicit path list (`tools/stage_native16_commit.ps1`), never
`git add -A` / `git add .`. Deliberately **excluded**:

- `my_work/` (git-ignored private evidence),
- `notebooks/00..02_lab.ipynb` — learner edits,
- `reports/stage_00`, `reports/stage_02` — reference outputs,
- the root `COMPLETE_COURSE_V2..V7.md` deletions.

Those four groups deserve separate, reasoned commits, so they were left out.
Verified absent from the staged set: secrets, learner work, root deletions.

`tools/verify_fresh_checkout.ps1` exports `HEAD` with `git archive` and checks
the result:

| Check | Result |
|---|---|
| notebooks in the fresh export | 171 |
| `native/protocols/labs.json`, `curriculum/catalog.json`, `native_course.py`, generator, verifier, evidence pointer, `uv.lock` | all present |
| `generator --check` against the fresh export | **exit 0** — committed workbooks match the generator |

Note: piping a binary tar through PowerShell's text pipeline corrupts it; the
script writes the archive to a file first.

### Test identities, not a frozen total

The two suite totals above differ by exactly one test, and the reason is
identified rather than left as noise: `tests/test_learner_mutation.py` collects
three tests, one of which is gated behind `SHAPE_TEST_RUST_MUTATION=1` because it
builds the Rust workspace. Disabled → 816 passed / 4 skipped. Enabled → 3 passed
in that file and no skip → 817 passed / 3 skipped. It was run enabled and passed.

Do not carry a historical total (774, 821, …) across platforms. Compare the
collected tests and justify each skip.

## Current tested / not tested

| Claim | Status |
|---|---|
| Python suite (default) | **816 passed, 4 skipped, 0 failed** |
| Python suite with `SHAPE_TEST_RUST_MUTATION=1` | **817 passed, 3 skipped, 0 failed** |
| Native Go/Rust tests | 34 / 28 passed, 0 failed |
| Native data decoders | 110 comparisons passed |
| Independent scientific oracles | 220 passed |
| Language notebooks, full sweep | see `my_work/nb_verify_full02/coverage.json` |
| Native images build + run | passed |
| Language notebooks, full sweep | **171 / 171 passed**, coverage complete, tree unchanged |
| Native Jobs in disposable kind | passed |
| Docker/Compose Python image, full course | not re-run in this session |
| Live cluster of the **Python** course image | not re-run; earlier evidence retained |
| macOS / Windows-Linux parity / GPU | not run |
| Remote CI workflows | not run |
| Original 133-notebook native parity | **not certified** |

### Skips, with reasons

1. `tests/test_deploy_v11.py` — host disallows symlinks.
2. `tests/test_integration_v12.py` — POSIX directory mode-bit contract; not a
   Windows filesystem model.
3. `tests/test_learner_mutation.py` — the slower Rust mutation build; opt in with
   `SHAPE_TEST_RUST_MUTATION=1` (executed separately and passed).
4. `tests/test_repository_v10.py` — POSIX symlink creation control.

These differ from the Linux reference host's skips (Ripser/GUDHI). A pass count
is not frozen across platforms; compare test identities and justify each skip.

## Failures preserved

- First Job attempt failed: `cannot use generate name with apply`. Kept in
  `my_work/native_deploy_jobs01/`.
- Second attempt failed because the success heuristic looked for the string
  `completed` in logs. Kept in `my_work/native_deploy_jobs02/`.
- The first full sweep was invalidated by a mid-run regeneration and stopped;
  the tree-change guard now detects exactly that.
- The second full sweep returned **170 passed, 1 failed** and a `compile_once`
  error. Both were real:
    - `compile_once` called `runner.build` without creating its output
      directory, so `go_version.json` could not be written. Fixed and covered by
      a test.
    - `python/stage27` failed with `FileExistsError`, because an interrupted run
      from the killed sweep had left `my_work/notebook_stage27_reference/`
      holding only an `execution.json`. The notebook now detects that state and
      explains it, rather than letting `run_references` raise a bare error.
      Evidence was **not** erased to make the run green.

## Protocol gaps

| Category | Applies to |
|---|---|
| exact | rank, counts, F2, IDs |
| numerical (1e-8 abs / 1e-7 rel) | native f64 metrics |
| same-protocol optimization | native16 small models |
| related control | several geometry and operator labs |
| not implemented | full FNO, VGGT inference, alpha/Delaunay |

A different Wine split or network architecture is a protocol difference, **not** a
language performance comparison.

## Next commands for Stage 01

```powershell
$env:PYTHONUTF8 = '1'
uv run --no-sync python course.py run --stage 1 --output my_work/stage01_ref01
uv run --no-sync python native_course.py compare --lab stage01 --output my_work/stage01_native01
uv run --no-sync python native_course.py prepare --lab stage01 --output my_work/stage01_practice01
```

## Concise daily workflow

```powershell
$env:PYTHONUTF8 = '1'
rtk uv run --no-sync python course.py next
rtk uv run --no-sync python native_course.py show stageNN
rtk uv run --no-sync python native_course.py compare --lab stageNN --output my_work/<new_name>01
uv run --no-sync python tools/check_matrix.py --fast
```

Before a larger claim:

```powershell
uv run --no-sync python tools/check_matrix.py --only contracts,python,readers,native
uv run --no-sync python tools/check_matrix.py --only science --output my_work/checks01
uv run --no-sync python tools/verify_language_notebooks.py --output my_work/nb_verify01
```

## Not claimed

No complete native original-notebook parity. No full deployment (the Python
course image and its live cluster were not re-run here). No learner mastery:
every generated notebook remains `not_assessed`.
