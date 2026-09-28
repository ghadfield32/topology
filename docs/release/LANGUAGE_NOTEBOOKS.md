# Notebooks: one lab, three languages

Every one of the 57 native16 learning units now has an interactive notebook in
**Python, Go and Rust** — 171 notebooks in total. This answers the question
"can I learn this in any language?" with a concrete, runnable route.

Index: [`workbooks/polyglot/index.html`](../../workbooks/polyglot/index.html)
(plain text: [`README.md`](../../workbooks/polyglot/README.md)).

## The three notebooks do different jobs

| Route | Notebook | What it actually does |
|---|---|---|
| Python | `workbooks/polyglot/python/<lab>.ipynb` | **Runs the canonical Python reference** in a fresh kernel inside an isolated copied workspace, then audits the registered inputs and resolves a *specific* native run's outputs. |
| Go | `workbooks/polyglot/go/<lab>.ipynb` | Checks the toolchain, shows the **actual dispatch arm** in `native/go/engine/labs.go`, compiles the Go program, runs only this lab, prints its metrics, and verifies input hashes. |
| Rust | `workbooks/polyglot/rust/<lab>.ipynb` | Same, for `native/rust/src/labs.rs`, plus the pinned-toolchain and ownership notes. |

The Go and Rust notebooks end by comparing against the other language using the
runner's own tolerance rules (`1e-8` absolute, `1e-7` relative) and checking that
both languages recorded identical input hashes.

### The Python route runs the real original experiment

The Python notebook calls `shape_lab.course.run_references(ROOT, [reference], out,
jobs=1, timeout=300)` — the same execution path the course itself uses. It gets a
fresh kernel, an isolated copy of the source, a runtime provenance probe, and
`allow_errors=False`. It is **not** a lookalike calculation and it is not a
Python re-implementation of the native unit.

The reference is not always a notebook. The Poux lab's canonical reference is a
script (`curriculum/extensions/poux_spatial_ai/bridge.py`), so it is labelled
`script` and its companion test is run instead of pretending it is a notebook.
A test asserts that a script lab is never handed to `run_references`.

### Sections are labelled by intent

The Python notebook separates three things, and says which is which:

1. **Run the canonical Python experiment** — the original course material.
2. **Input audit** — which registered files this lab consumes, and their hashes.
3. **Output audit** — reads an existing native run; it does not recompute the lab.

The native experiment itself runs in the Go and Rust notebooks.

## Evidence is resolved explicitly, never by "newest file wins"

`tools/evidence_pointer.py` resolves which run a reader should look at:

1. an explicit `run_dir`,
2. `my_work/native_evidence.json` (written by `evidence.write_manifest`),
3. otherwise **nothing** in strict mode.

The Python notebook exposes this as two explicit modes, set at the top of its
evidence cell:

| Mode | Behaviour |
|---|---|
| `MODE = "fresh"` (default) | **creates** the evidence now by compiling and running the native Go and Rust labs into the notebook's own run directory, then verifies its identity. Nothing older is used. |
| `MODE = "review"` | opens a **specific** previous result from `PINNED_RUN` and labels it as previous execution. `PINNED_RUN` is required; there is no scanning fallback. |

Neither mode silently chooses the most recent plausible folder. Runs now record
an `identity` block in `execution.json`, so stale evidence cannot masquerade as
current.

## What these notebooks deliberately do not do

- **They do not compute the science in Python.** A test asserts the Go/Rust
  notebooks never import NumPy/Torch/SciPy/sklearn and always call
  `runner.build(...)` and `runner.execute_lab(...)`. Python is the driver only.
- **They are not a second curriculum.** `curriculum/catalog.json` still owns the
  31 stages; the notebooks carry no catalogue of their own.
- **They do not grade you.** Every notebook is `not_assessed`, and each one keeps
  its lab's stated boundary ("what this lab does not establish").
- **They do not claim original-notebook parity.** That remains
  `not_certified`; see `native/COVERAGE.md`.

## Run them

In VS Code, open any notebook under `workbooks/polyglot/` and run the cells top
to bottom. Or from the command line, from the repository root:

```powershell
$env:PYTHONUTF8 = '1'
uv run --no-sync jupyter lab
```

Or execute headless (this is how they were verified):

```powershell
uv run --no-sync jupyter nbconvert --to notebook --execute `
  --output-dir my_work/notebook_run `
  workbooks/polyglot/python/stage01.ipynb
```

The Python notebook needs an existing native run to have something to read. The
first time, create one:

```powershell
uv run --no-sync python native_course.py compare --lab stage01 --output my_work/notebook_stage01_first01
```

The Go and Rust notebooks build what they need themselves and write to
`my_work/notebook_<lab>_<language>/`.

## Verified

Stage 01 was executed end-to-end with fresh kernels in all three languages:

| Notebook | Observed result |
|---|---|
| `python/stage01.ipynb` | ran the canonical `notebooks/01_lab.ipynb` (`1/1 passed`); read 150 Iris rows; resolved the native run; Go ≡ Rust, 17 values, max diff 0.0; input hashes OK |
| `go/stage01.ipynb` | showed `case "stage01"` at line 185 of `labs.go`; the `clone` call there deep-copies each row (`b[i] = append([]float64(nil), a[i]...)`) before the `append`, so the source matrix is **not** mutated; built and ran Go; `real_rank 3`, `f2_rank 2`, `augmented_rank 4`, kernel `(-2,3,0,0,1)`; hashes MATCH |
| `rust/stage01.ipynb` | built and ran Rust; same metrics with `0.0`-typed floats; compared against Go: agreement true, 17 values, max diff 0.0 |

The full 171-entry sweep is run by `tools/verify_language_notebooks.py`, which
derives the expected set from the registry, uses fresh kernels and explicit
working directories, compiles each native binary once per source identity, runs
**serially**, preserves failures, rejects missing/duplicate/stale entries, and
**returns non-zero unless coverage is complete**. There is no flag to tolerate
errors, and partial runs report `coverage.complete = false`.
Observed full sweep (`my_work/nb_verify_full03/coverage.json`):

| Measure | Value |
|---|---|
| expected / selected / executed | 171 / 171 / 171 |
| passed / failed | **171 / 0** |
| coverage complete | true |
| notebook tree unchanged during the run | true |
| set problems (missing/duplicate/unexpected) | none |
| executed code cells | 1311 |
| native binaries | compiled once each; source + binary hashes recorded |
A "verify" result is not the same claim as "three smoke notebooks ran". See the
sweep's `coverage.json` for the actual counts and every failure record.

## Regenerate

The notebooks are generated, not hand-edited, so they stay consistent when the
lab catalogue changes:

```powershell
uv run --no-sync python tools/build_language_notebooks.py
```

Verify without writing anything:

```powershell
uv run --no-sync python tools/build_language_notebooks.py --check
```

`--check` exits non-zero and names every missing, stale or unexpected artifact.
It genuinely can fail: deleting an artifact, editing one by hand, or adding an
unregistered notebook all make it return 1. Unknown flags are now a hard error
rather than a silent full rewrite.

Then run the test above; it fails if the committed tree is stale. The generator
is `tools/build_language_notebooks.py` and reads `native/protocols/labs.json`
plus the existing `native_course.py` runner API — no new dependency is added.

**Do not regenerate while a verification sweep is running.** The sweep hashes the
whole notebook tree before and after, and reports `coverage.complete = false` if
it changed, precisely so a mixed-source result cannot look green. Regenerate
first, then sweep.

## Boundaries that remain

The untested gates from the native import still stand: the 133 original
notebooks were not replayed, and Docker, Kubernetes, macOS, GPU and the remote
CI workflows did not execute here. These notebooks are a convenience layer over
the same native16 evidence, not extra certification of it. See
[NATIVE16_IMPORT.md](NATIVE16_IMPORT.md).
