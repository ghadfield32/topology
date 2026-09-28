# Stage 01 walkthrough: change one redundant column

Stage 00 is complete and you are on Stage 01. This page is the one-session route:
**prediction → canonical Python → real Go → real Rust → your own change → evidence**.

The point of Stage 01 is that a stored column can be *redundant*. The native lab
already shows this with the column `2*x0 - 3*x1`. Your independent work is to
repeat it with a column of your own and explain the result.

> This page does **not** do the mathematics for you. Derive the null vector
> yourself first. If someone hands you the answer, the exercise is gone.

## 0. Before you start

Open a terminal in the repository root and set the environment once:

```powershell
$env:PYTHONUTF8 = '1'
$env:UV_CACHE_DIR = Join-Path $PWD.Path '.uv-cache'
$env:UV_PYTHON_INSTALL_DIR = Join-Path $PWD.Path '.uv-python'
```

**Check exit codes explicitly.** A native program can fail while PowerShell
continues happily; `$ErrorActionPreference` does not reliably turn that into an
exception. Watch `$LASTEXITCODE`, or read the JSON the runner writes.

## 1. Predict before you run (write this down)

The augmented Iris matrix appends the column `2*x0 - 3*x1`, i.e. weights
`[2, -3]` on the first two stored features.

For your own change, use the weights `[5, 2]` — the column `5*x0 + 2*x1`.

Before running anything, write:

1. The definition of the column you are adding.
2. A hand derivation of a vector in the null space of the **five-column** matrix.
   (A null vector `v` satisfies `X_aug · v = 0`.)
3. Your predicted `real_rank` and `f2_rank` for the 3×3 control matrix
   `A = [[1,1,0],[1,0,1],[0,1,1]]`.
4. Your prediction for `augmented_rank` once any redundant column is added.

Your prediction is evidence. Keep it even if it turns out wrong.

## 2. Run the canonical Python reference

```powershell
uv run --no-sync python course.py run --stage 1 --output my_work/stage01_ref01
```

Read the executed notebook under `my_work/stage01_ref01/`. That is the original
course experiment. It is **not** the same thing as the native Go/Rust labs: the
native units are matching *teaching protocols*, and `native/COVERAGE.md` records
where they differ from the original notebooks.

## 3. Run the real native Go and Rust implementations

```powershell
uv run --no-sync python native_course.py compare --lab stage01 --output my_work/stage01_native01
```

Then open `my_work/stage01_native01/index.html` and the two files

```
my_work/stage01_native01/go/stage01.json
my_work/stage01_native01/rust/stage01.json
```

**Where the metrics live:** each result file has a `metrics` object. For Stage 01
it currently contains `real_rank`, `f2_rank`, `iris_rank`,
`centered_scaled_rank`, `augmented_rank`, `known_kernel`, `kernel_residual_max`
and `finite_preimage_of_square_1_to_9`. The run's `execution.json` also records
the `identity` block: the source hash and binary hash for each language, and a
fingerprint of every input consumed.

You can also run it as notebooks:

```
workbooks/polyglot/python/stage01.ipynb
workbooks/polyglot/go/stage01.ipynb
workbooks/polyglot/rust/stage01.ipynb
```

## 4. Read the code you are about to change

- Go dispatch: `native/go/engine/labs.go`, arm `case "stage01":`
- Go linear algebra: `native/go/engine/math.go`, functions `Rank` and `Rank2`
- Rust dispatch: `native/rust/src/labs.rs`, arm `"stage01" => {`
- Rust linear algebra: `native/rust/src/math.rs`, the same two operations

In the Go arm, notice:

```go
aug := clone(x)
for i := range aug {
    aug[i] = append(aug[i], 2*x[i][0]-3*x[i][1])
}
```

**This is not an aliasing bug in the current code, and the guide should be read
carefully rather than assuming one.** `clone` is a genuine deep copy:

```go
func clone(a [][]float64) [][]float64 {
    b := make([][]float64, len(a))
    for i := range a {
        b[i] = append([]float64(nil), a[i]...)
    }
    return b
}
```

Each row is copied into a fresh backing array, so `append` on `aug[i]` cannot
reach `x`. The row-aliasing lesson is about what would happen **without** the
`clone`: Go slices share their backing array, so if `aug[i]` still referred to
`x[i]`'s storage, that `append` could write into the caller's matrix whenever the
row had spare capacity.

Your exercise is to *prove* this rather than take it on trust. Delete the `clone`
in your private copy — or replace it with a shallow outer copy such as
`aug := append([][]float64(nil), x...)` — and observe whether
`Rank`'s "preserves its input" test still passes. Restore it afterwards.

In Rust, find which function takes `&[[f64]]` (borrows) and which returns an owned
`Vec<Vec<f64>>`. Then explain why the caller's `x` is unchanged, and whether the
`clone` there is required by the type system or only by the algorithm.

## 5. Your independent change (this is the actual assignment)

Make a **private** copy so the canonical source stays untouched:

```powershell
uv run --no-sync python native_course.py prepare --lab stage01 --output my_work/stage01_practice01
```

That gives you `my_work/stage01_practice01/go` and `.../rust` — editable working
source, plus `START.md`, `study.json` and an `answer.md` template. This is
**unassessed**; nothing here grades you.

Now change the weights. In both languages, replace the `[2, -3]` coefficients
with `[5, 2]` in the augmented column. Then:

**Go:**

```powershell
cd my_work/stage01_practice01/go
go test -count=1 ./...
"GO_EXIT=$LASTEXITCODE"
go run ./cmd/shape-go --repo ../.. --lab stage01
"RUN_EXIT=$LASTEXITCODE"
```

**Rust:**

```powershell
cd my_work/stage01_practice01/rust
cargo test --offline --locked
"CARGO_EXIT=$LASTEXITCODE"
cargo run --offline --locked --release --bin shape-rust -- --repo ../.. --lab stage01
"RUN_EXIT=$LASTEXITCODE"
```

### Where to look when it fails

- `cargo` or `rustc` missing → toolchain/PATH problem, not a maths problem.
  See `native/guides/SETUP.md`.
- A linker error on Windows → you need the MSVC C++ build tools.
- "offline crate not found" → run from `my_work/stage01_practice01/rust` and keep
  the copy's `.cargo` vendor pointer intact. Never delete `Cargo.lock` to force a
  resolution.
- Output directory already exists → choose a new attempt name. Do not erase
  earlier evidence.
- A dataset hash mismatch → stop and inspect the changed input. Do not rewrite
  the expected hash.

Run `go test` and `cargo test` **after** your edit. Your change should still be
internally consistent. If you break the algebra on purpose to see what a failure
looks like, note in `answer.md` exactly which test failed and why — a preserved
failure is evidence, not a stain on the record.

`tests/test_learner_mutation.py` in this repository demonstrates the principle:
editing the learner copy to use OR instead of XOR makes `TestRankField` fail
while the canonical source stays byte-identical.

## 6. Verify your evidence is current

After your change, check that nothing canonical moved underneath you:

```powershell
git status --short
git diff --stat
```

If the canonical `native/` source changed while you worked, you cannot compare
old and new results. Also check a run's `execution.json` `identity` block: if the
`source_sha256` recorded there differs from the current source, that run is
stale.

Notebooks enforce this. The Python notebook refuses to silently use old evidence:
in **review mode** it says so out loud, with `REVIEW = True` at the top of the
cell. Set `REVIEW = False` to require a run with a bound identity.

## 7. What your result cannot establish

Say one of these in `answer.md`, in your own words:

- An `augmented_rank` of 4 over five stored columns is a statement about a
  matrix, not about biology. A numerical rank does not identify a manifold
  dimension.
- `rank_F2 = 2` is not "the same" as `rank_R = 3`. They are different fields.
- The fixed tolerance (`1e-10` in the native code) is a numerical choice, not a
  calibrated measurement uncertainty.
- Go and Rust agreeing is software evidence. It is not three independent
  datasets, and it is not proof that the algorithm is the right one.
- The native16 protocol is not certified as an operation-for-operation port of
  the original notebook. See `native/COVERAGE.md`.

## 8. Record it

Fill in `my_work/stage01_practice01/answer.md`:

- Question and observation unit
- Your prediction (from step 1) and your hand derivation
- The Go change, and what Go made explicit about copying and row storage
- The Rust change, and what the borrow checker made explicit
- Your observed output, including the tolerance and any discrepancy
- One conclusion your observations **do** support
- One conclusion they do **not** support
- What needed help
- A changed example to revisit after a delay

## 9. Optional: the Poux bridge

The Stage 01 companion is the Poux weighted-mean bridge. Its canonical reference
is a **script** (`curriculum/extensions/poux_spatial_ai/bridge.py`), not a
notebook, so it is handled separately. Derive the count-weighted mean and explain
why equal-weighting unequal batches is wrong, then explain why a mean over
selected non-uniform basketball frames is neither a release location nor a time
average.

## Daily workflow (short form)

```powershell
$env:PYTHONUTF8 = '1'
rtk uv run --no-sync python course.py next            # what is next
rtk uv run --no-sync python native_course.py list     # the 57 native units
rtk uv run --no-sync python native_course.py show stageNN
rtk uv run --no-sync python native_course.py compare --lab stageNN --output my_work/<new_name>01
```

Fast checks before you move on:

```powershell
uv run --no-sync python tools/check_matrix.py --fast
```

Full separate checks before a larger claim:

```powershell
uv run --no-sync python tools/check_matrix.py --only contracts,python,readers,native
uv run --no-sync python tools/check_matrix.py --only science --output my_work/checks01
```

A pass in `contracts` says nothing about `science`, nothing about Docker or
Kubernetes, and nothing about your mastery. Those gates are separate and are
listed in the final report.
