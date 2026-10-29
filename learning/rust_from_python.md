# Rust from Python: one continuous walkthrough

**Status: worked reference. Not assessed.** This page teaches *tooling and workflow*, not a
second curriculum. The 31-stage route in [curriculum/catalog.json](../curriculum/catalog.json)
remains the single mandatory order, and [native/guides/LEARNING_PATHS.md](../native/guides/LEARNING_PATHS.md)
(sections R0–R6) remains the course's Rust path. Nothing here owns a stage number or a lab key.

Everything below was executed on this Windows host. Where a command was *not* run, it says so.

---

## 0. Six corrections to earlier advice

An earlier version of this walkthrough contained errors. Each was tested here before being
written down. The first one matters most.

| # | Wrong advice | Verified correct rule | How it was checked |
|---|---|---|---|
| 1 | "`cargo test --locked` regenerates a missing lockfile" | **It refuses.** `--locked` rejects a missing *or* stale lockfile. | Deleted `Cargo.lock`; `cargo test --offline --locked` exited **101** and did not create it |
| 2 | "Never copy `Cargo.lock` when recreating a project" | **Keep it** when reproducing the same project. It records resolved versions. | `cargo generate-lockfile --offline` then `--locked` passed |
| 3 | "A bare `rustc` ignores the toolchain file" | The **rustup proxy honours it**. Only the real binary under `.rustup/toolchains/...` bypasses it. | `rustc -V` in a pinned dir → 1.90.0; real binary → 1.97.1 |
| 4 | "`cargo fmt -- --check` changes source" | `--check` **reports only**. Plain `cargo fmt` applies. | SHA-256 of `stats.rs` identical before/after `--check` |
| 5 | "`Result` forces you to use `match`" | It forces *acknowledgement*: ignoring one is a **warning**, not an error. | `cargo check` exited **0** with `warning: unused Result that must be used` |
| 6 | "`values[0]` copies nothing" | It copies **one `f64`** (it is `Copy`), not the vector. | Test asserting the vector still has 3 elements passed |

### The consequence of #1 and #5 together

`cargo check` is not a correctness gate.

```
cargo check --offline            → exit 0, warning: unused `Result` that must be used
cargo clippy ... -- -D warnings  → exit 101, error: unused `Result` that must be used
```

If you only run `cargo check`, a silently discarded error will pass. That is why the daily
routine below ends with a `-D warnings` gate rather than `check`.

---

## 1. The tool map

| Purpose | Python with `uv` | Rust |
|---|---|---|
| Manage language installs | `uv python …` | `rustup …` |
| Create a project | `uv init …` | `cargo new …` |
| Describe the package | `pyproject.toml` | `Cargo.toml` |
| Record resolved versions | `uv.lock` | `Cargo.lock` |
| Select the version | `.python-version` (read by uv/pyenv) | `rust-toolchain.toml` (read by rustup) |
| Run the program | interpreter executes source | compiled binary executes |
| Reusable logic | module / package | library crate (`src/lib.rs`) |
| CLI entry point | `__main__.py` | `src/main.rs` |
| Build outputs | `__pycache__/`, `dist/` | `target/` |
| Isolated environment | `.venv` | *no direct equivalent* |

**The workflow difference:**

```
Python:  source → selected interpreter + packages → computation
Rust:    source + dependencies → compiler/linker → executable → computation
```

Python also runs compiled extensions, and most scientific work already executes native code.
**Do not read that diagram as "rewriting in Rust is faster."** That is a measurement, not a
consequence of the language.

**A distinction that trips people up:** importing a Python module *executes code*. `cargo check`
does **not** execute your program — it type-checks it. They are not the same kind of check.

---

## 2. Inspect the installation, do not reinstall it

```powershell
Set-Location "C:\Users\ghadf\vscode_projects\docker_projects\topology"
Get-Command rustup,cargo,rustc | Select-Object Name,Source
rustup toolchain list
```

**Observed here:** `rustup` 1.29.0; toolchains `stable` (default → rustc **1.97.1**) and
`1.90.0`. Both now have `rustfmt` and `clippy`.

Inspect an existing project:

```powershell
Push-Location my_work/rust201
try {
    rustup show active-toolchain   # which toolchain, and why
    rustc -Vv                      # compiler + host triple
    cargo -V                       # cargo version
    cargo locate-project           # which manifest was found
    Get-Content rust-toolchain.toml
}
finally { Pop-Location }
```

`rustup show active-toolchain` reporting `overridden by '...\rust-toolchain.toml'` is the
sentence you want to see. If it says `(default)`, the pin is not active.

Only install when missing — these can download:

```powershell
rustup toolchain install 1.90.0 --profile minimal
rustup component add --toolchain 1.90.0 rustfmt clippy
```

On a genuinely new Windows machine, `rustup` and the **MSVC linker** are separate concerns. A
missing linker is a build-tools problem, not a Rust problem.

---

## 3. Create one new project safely

Never run `cargo new` over an existing project.

```powershell
$Repo = "C:\Users\ghadf\vscode_projects\docker_projects\topology"
$Project = Join-Path $Repo ("my_work\rust_from_python_" + (Get-Date -Format 'yyyyMMdd-HHmmssfff'))
if (Test-Path $Project) { throw "Choose a new project directory." }

cargo +1.90.0 new --bin --edition 2021 --name rust_from_python --vcs none $Project
if ($LASTEXITCODE -ne 0) { throw "Project creation failed." }
Set-Location $Project
```

Reading the flags: `+1.90.0` selects the toolchain for this one command, `--bin` makes an
executable template, `--edition 2021` fixes the language edition, `--name` sets the package
name, `--vcs none` avoids a nested repository.

**Verified:** this exact command produced a working project and `cargo run --offline --locked`
printed `Hello, world!`.

`--vcs none` also means **no `.gitignore` is written**. Add one containing `/target`.

### Pin the compiler

`rust-toolchain.toml`:

```toml
[toolchain]
channel = "1.90.0"
profile = "minimal"
components = ["rustfmt", "clippy"]
```

Measured effect: active toolchain changed from `stable (default)` to
`1.90.0 (overridden by '...\rust-toolchain.toml')`, and `cargo -V` went from 1.97.1 to 1.90.0.
The `components` key **auto-installs** what it names.

### Manifest with three different version concepts

```toml
[package]
name = "rust_from_python"
version = "0.1.0"        # your package's version
edition = "2021"         # language compatibility edition
rust-version = "1.83"    # minimum supported compiler
publish = false

[dependencies]
```

`rust-version` is **enforced**. Setting it to `1.99` produced:

```
error: rustc 1.90.0 is not supported by the following package:
  rust_from_python@0.1.0 requires rustc 1.99
```

Edition 2024 is **supported by 1.90** (it stabilised in 1.85). 2021 is used here for continuity
with the course, not because 2024 fails.

**TOML trap, hit live:** appending a second `[dependencies]` heading gives
`error: duplicate key --> Cargo.toml:10:2`. Add entries *under* the existing table.

### Create the lockfile deliberately

```powershell
if (-not (Test-Path Cargo.lock)) { cargo generate-lockfile --offline }
cargo check --offline --locked
cargo run --offline --locked
```

`cargo generate-lockfile --offline` succeeded and created the file; only then did the `--locked`
commands pass. This is correction #1 in practice.

**Checkpoint:** before continuing, explain what `fn main`, the braces, the semicolon and
`println!` do.

---

## 4. Syntax, translated from Python

### Variables and mutability

```python
count = 2
count += 1
```
```rust
let mut count: usize = 2;
count += 1;
```

`let` binds, `mut` permits reassignment. Without `mut`, `count = 3;` is a compile error. Most
local types are inferred, but a binding's type does not change; a second `let` creates a new
binding through **shadowing**:

```rust
let count = "3";
let count: usize = count.parse().expect("fixed valid example");
```

Do not copy that `expect` policy into user-input handling — see §6.

### Functions and the semicolon rule

```rust
fn square(x: f64) -> f64 {
    x * x        // final expression: this is the returned value
}
```

`return x * x;` also works. But this does **not** return a float:

```rust
fn square(x: f64) -> f64 {
    x * x;       // semicolon discards the value -> returns ()
}
```

Rust distinguishes *statements* from value-producing *expressions*.

### Arrays, vectors, slices

```rust
let fixed: [f64; 3] = [1.0, 2.0, 3.0];
let mut owned: Vec<f64> = vec![1.0, 2.0, 3.0];
owned.push(4.0);
let borrowed: &[f64] = &owned;
```

| Form | Meaning |
|---|---|
| `[f64; 3]` | fixed-size array of three floats |
| `Vec<f64>` | owned, growable |
| `&[f64]` | borrowed view, read-only |
| `&mut [f64]` | borrowed view, elements mutable |

A Rust slice is a **view**, not a copy. Python's `values[0:2]` creates a new list; Rust's
`&values[0..2]` does not.

### Strings

```rust
let label: &str = "basketball";        // borrowed UTF-8
let mut d = String::from(label);       // owned, growable
d.push_str(" observations");
```

Rust strings are not integer-indexable like Python's. Bytes, Unicode scalar values and
displayed characters are three different things.

### Loops and if-expressions

```rust
for (index, value) in values.iter().enumerate() {
    println!("{index}: {value}");
}

let status = if values.is_empty() { "empty" } else { "nonempty" };
```

---

## 5. Ownership: the part Python cannot teach you

```python
a = [1.0, 2.0]
b = a
b.append(3.0)     # both names refer to the same list
```

```rust
let a = vec![1.0, 2.0];
let b = a;              // ownership MOVED into b
println!("{b:?}");
// println!("{a:?}");   // use-after-move: would not compile
```

For a `Vec`, assignment transfers ownership. `a.clone()` asks for an independent copy. Scalars
like `f64` are `Copy`, so copying one number is not cloning a vector — correction #6.

### Borrow to inspect, `&mut` to change

```rust
fn count(values: &[f64]) -> usize { values.len() }        // borrows, cannot mutate

fn increment(values: &mut [f64]) {                         // explicit mutation
    for value in values { *value += 1.0; }                 // * dereferences
}
```

At the call site the intent is visible: `increment(&mut values);`

**Predict this failure:**

```rust
let mut values = vec![1.0, 2.0];
let first = &values[0];
values.push(3.0);
println!("{first}");
```

Observed diagnostic (`error[E0502]`): the shared borrow at `&values[0]` is still needed by
`println!`, while `push` needs exclusive access.

Two repairs, different meanings:

```rust
let first = values[0];       // copies ONE f64; vector untouched
```
```rust
let first = values[0];
values.push(3.0);
println!("{first}");          // equivalent here, no borrow held
```

Choose the repair that matches your intent, not the one that silences the message.

Python's equivalent hazard is real and silent — a function that calls `values.sort()` reorders
the caller's list with no warning at all. Rust's version requires `&mut` in the signature *and*
`&mut` at the call site.

---

## 6. Build a useful library function

```
src/
├── lib.rs     pub mod stats;      reusable logic
├── stats.rs   the functions
└── main.rs    command line only
```

Compare signatures:

```python
def mean(values: list[float]) -> float: ...
```
```rust
pub fn mean(values: &[f64]) -> Result<f64, StatsError>
```

| Part | Meaning |
|---|---|
| `pub` | part of the public API |
| `values: &[f64]` | borrows a slice of floats |
| `Result<f64, StatsError>` | either a float or a named error — failure is in the type |

Worked implementation:

```rust
#[derive(Debug, PartialEq)]
pub enum StatsError {
    Empty,
    NonFinite { index: usize },
    Overflow,
}

pub fn mean(values: &[f64]) -> Result<f64, StatsError> {
    if values.is_empty() {
        return Err(StatsError::Empty);
    }
    let mut total = 0.0;
    for (index, &value) in values.iter().enumerate() {
        if !value.is_finite() {
            return Err(StatsError::NonFinite { index });
        }
        total += value;
        if !total.is_finite() {
            return Err(StatsError::Overflow);
        }
    }
    Ok(total / values.len() as f64)
}
```

Unfamiliar parts: `enum` names alternatives; `#[derive(Debug, PartialEq)]` generates
formatting and equality used by tests; `(index, &value)` is a pattern that copies the referenced
`f64`; `as f64` converts the count for floating-point division.

**Documented limitation, not a compiler concern:** sequential summation can lose precision, and
this rejects a nonfinite *intermediate* sum even when a better algorithm would find a finite
mean. That is a numerical choice you must state.

---

## 7. `match`, `Option`, and `?`

```rust
match mean(&values) {
    Ok(average) => println!("mean: {average:.6}"),
    Err(error) => eprintln!("invalid data: {error:?}"),
}
```

`Option` is absent vs present — not the same as failed:

```rust
match values.first() {
    Some(value) => println!("first: {value}"),
    None => println!("there is no first observation"),
}
```

`?` propagates, and only inside a function returning a compatible `Result`:

```rust
let values = parse_numbers(&text)?;
// conceptually:
// let values = match parse_numbers(&text) {
//     Ok(values) => values,
//     Err(error) => return Err(error),
// };
```

`?` is not "ignore errors", and it does not catch panics or undo earlier mutation.

**Correction #5:** the type encourages handling but does not force `match`. Discarding is
possible — it merely warns. That is why the `-D warnings` gate exists.

---

## 8. Connect the library to a command line

The parser accepts **numeric tokens separated by commas or newlines**. It is not a general CSV
reader: no quoted fields, no headers, no comment syntax.

```rust
fn run(path: &Path) -> Result<(), String> {
    let text = fs::read_to_string(path)
        .map_err(|error| format!("cannot read {}: {error}", path.display()))?;
    let values = parse_numbers(&text)?;
    let average = mean(&values).map_err(|error| format!("invalid data: {error:?}"))?;
    println!("observations {}", values.len());
    println!("mean {average:.6}");
    Ok(())
}
```

Data flow:

```
Path → String → Vec<f64> → Result<f64, StatsError> → printed output + exit status
```

`map_err` transforms the error, keeping the success path. `Result<(), String>` means success
carries no value — unit `()`.

Exit conventions chosen by this program: `0` success, `1` file/data/computation failure,
`2` wrong usage.

`data/sample.txt` — **synthetic, hand-checkable, not measured observations:**

```
2,4,4,4
5,5,7,9
```

```
cargo run --offline --locked -- data/sample.txt
# observations 8
# mean 5.000000
```

The `--` separates Cargo's own options from your program's arguments. Mean:
(2+4+4+4+5+5+7+9)/8 = **5**.

Malformed input is *correct behaviour*, not a defect: a program that rejects bad data is
working to specification.

---

## 9. Test before declaring it correct

```rust
use rust_from_python::stats::{mean, StatsError};

#[test]
fn mean_matches_a_hand_calculation() {
    assert_eq!(mean(&[2.0, 4.0, 6.0]), Ok(4.0));
}

#[test]
fn empty_input_is_not_zero() {
    assert_eq!(mean(&[]), Err(StatsError::Empty));
}

#[test]
fn caller_order_is_preserved() {
    let values = vec![3.0, 1.0, 2.0];
    let before = values.clone();
    assert_eq!(mean(&values), Ok(2.0));
    assert_eq!(values, before);
}
```

Files under `tests/` use only the public API. Module-local tests can reach private helpers.
Documentation comments are executed as tests too.

**The lesson worth keeping:** an unfinished function written as `todo!()` compiles, and a suite
passes until some test actually calls it. A green suite establishes exactly what its tests
cover — nothing more.

---

## 10. Run the same calculation in Python

```powershell
& "$Repo\.venv\Scripts\python.exe" python_reference.py data/sample.txt
& "$Repo\.venv\Scripts\python.exe" -m unittest -v test_python_reference
```

Both print `observations 8` / `mean 5.000000`. That is an agreement check **for this fixture**,
not proof that both parsers accept the same strings in general.

### Real data

The Rust token parser above is deliberately simple. Use Python's CSV parser to export a column,
recording source and output hashes, then let Rust read the plain numbers:

```powershell
& "$Repo\.venv\Scripts\python.exe" export_column.py `
  --source "$Repo\data\raw\iris.csv" `
  --column sepal_length_cm `
  --output data/iris_sepal_length_cm.txt

cargo run --offline --locked -- data/iris_sepal_length_cm.txt
```

**Verified on this host** by an independent Python read of `data/raw/iris.csv`:

```
observations 150
mean 5.843333
```

The rank exercise in [optional/rust_practice](../optional/rust_practice) is a separate,
larger route: 150 rows, rank 4 before and after adding a dependent feature, zero kernel
residual — recorded in that crate's own [VERIFICATION.md](../optional/rust_practice/VERIFICATION.md).

---

## 11. The daily routine

You do not run all of these after every keystroke.

| When | Command | Purpose |
|---|---|---|
| While editing | `cargo check --offline --locked` | fast compiler feedback |
| After a behaviour change | `cargo test --offline --locked` | run the declared tests |
| To inspect behaviour | `cargo run --offline --locked -- data/sample.txt` | execute |
| Before checkpointing | `cargo fmt --all` | apply formatting |
| Formatting gate | `cargo fmt --all -- --check` | confirm no differences (reports only) |
| **Lint gate** | `cargo clippy --offline --locked --all-targets -- -D warnings` | reject warnings |
| Documentation | `cargo doc --offline --locked --no-deps` | build API docs |
| Optimized artifact | `cargo build --release --offline --locked` | release executable |

Formatting, compilation, linting, testing and optimized builds answer different questions.
`cargo check` can also miss errors exposed only during code generation, so a full build is a
separate check.

Run one command at a time while learning, and read the whole diagnostic instead of piping it
away. (When capturing `$LASTEXITCODE` in PowerShell, do not pipe into a cmdlet — check it on its
own line. A pipeline can report the cmdlet's status, not the tool's.)

Approximate Python equivalents:

```
cargo test          ↔ unittest / pytest
cargo fmt           ↔ a Python formatter
cargo clippy        ↔ lint / static analysis
cargo run           ↔ running the Python entry point
cargo build release ↔ a native artifact, not merely a wheel
```

---

## 12. Running without Cargo

```powershell
cargo build --release --offline --locked
if ($LASTEXITCODE -ne 0) { throw "The release build did not succeed." }
.\target\release\rust_from_python.exe data\sample.txt
```

On Linux/WSL the path is `./target/release/rust_from_python data/sample.txt`.

Build for the intended platform; portability also depends on target and native libraries. When
measuring performance, build first and time the executable separately. Timing an eight-value
file measures startup and I/O, not language performance.

---

## 13. Dependencies, reopening, and copying

### Adding a dependency

```powershell
cargo add csv@1.3.1
cargo check
cargo test --locked
cargo fetch --locked
```

`cargo add` edits the manifest and changes the lock; resolution may need network access. Review
those changes.

**Flag names are not portable between tools.** In Cargo `--frozen` combines locked and offline.
In `uv`, `--locked`, `--frozen` and `--no-sync` each mean something different. Do not assume a
shared name implies shared semantics.

### Reopening a project

Enter the directory, inspect the selected toolchain, run its focused tests. **Do not `cargo new`
again.**

### Repairing

Read the first meaningful error, repair the smallest identified problem. A duplicate TOML table
is not a reason to rebuild the repository.

### Copying the same project reproducibly

Preserve:

```
Cargo.toml
Cargo.lock              <-- keep: it records resolved versions
rust-toolchain.toml
src/
tests/
examples/
required input fixtures
required .cargo configuration and dependency sources
```

Exclude `target/` — it is rebuildable output. Creating a *different* package or deliberately
updating dependencies is a separate operation with its own reviewed resolution.

**Your practice lives under `my_work/`, which is git-ignored.** A successful commit will not back
it up. Save learner source deliberately; do not force-add environments, caches or private data.

---

## 14. What to learn next, and how to prove it

| Next topic | Evidence to produce |
|---|---|
| Structs and `impl` | represent an observation; explain which methods borrow or mutate |
| Enums and typed errors | distinguish missing, malformed, estimated and measured |
| Iterators and closures | rewrite a loop without changing behaviour or allocation assumptions |
| Traits and generics | extract one genuinely useful shared interface |
| Lifetimes | explain the owner and validity of a returned reference |
| Data readers | preserve schema, units, identity, missingness and failure context |
| Performance and concurrency | measure first; add bounded parallelism only for a justified workload |
| Python bindings | package the reviewed core and test the imported artifact |

Do not jump to `async` or `unsafe` because they sound advanced. The immediate goal is to explain
ordinary code completely.

### Your next independent exercise

```rust
pub fn span(values: &[f64]) -> Result<f64, StatsError>
```

Maximum minus minimum, **without changing the caller's data.** Before implementing, specify and
test:

- `[2.0, 4.0, 9.0]`
- a single observation
- empty or nonfinite input
- an extreme finite-input difference that overflows
- preservation of input order

Then explain **why it borrows its input, why it returns `Result`, and why compiling successfully
does not establish that the numeric result is correct.**

That is the point at which this becomes your Rust skill rather than a sequence you followed.

---

## What this page does not establish

- It was not run on Linux, macOS or WSL. Only `x86_64-pc-windows-msvc` was exercised here.
- No learner assessment, retention or mastery claim is made. Every item is `not_assessed`.
- The Python and Rust agreement is for the stated fixtures only, not parser equivalence.
- Docker, Kubernetes and deployment were not touched by this walkthrough.
- `rustfmt` and `clippy` were exercised on **1.90.0** via the pin; lint behaviour differs
  between compiler versions.
- A passing test suite says what its tests cover, not that the analysis is appropriate.

## See also

- [Rust learning path R0–R6](../native/guides/LEARNING_PATHS.md) — the course's own progression
- [Optional Rust practice crate](../optional/rust_practice) — worked reference + compiler cases
- [Stage 01 guide](../native/guides/labs/stage01.md) — current learning position
- [Repository layout](../docs/release/REPOSITORY_LAYOUT.md) — who owns what
- [Learning area index](README.md)
