# Optional Rust practice (worked reference)

A small, dependency-free crate for **ownership, API contracts and typed errors**, kept beside
the course. It is **not a second curriculum**: it owns no stage order, no lab key and no
learner assessment. The 31-stage course in `curriculum/catalog.json` remains the single route,
and the Go/Rust reference implementations in `native/` remain the scientific reference.

This is a **worked reference**, not the assignment. The independent change is described in
[EXERCISES.md](EXERCISES.md) and stays `not_assessed` until you demonstrate it.

## Why this crate exists

The course asks you to explain *what each language made explicit about memory, types, errors
and algorithm choice*. This crate isolates four of those decisions so each one is visible in
a signature rather than buried in a numerical pipeline:

| Module | The decision it exposes |
|---|---|
| [src/error.rs](src/error.rs) | A rejected record is a value the caller must handle, not a panic. |
| [src/table.rs](src/table.rs) | Borrow to inspect, own to produce. Validation completes before output exists. |
| [src/translate.rs](src/translate.rs) | A mutating function documents what happens to the caller's data on error. |
| [src/rank.rs](src/rank.rs) | A numerical rank is meaningless without the tolerance that produced it. |

Two consequences are tested, not asserted:

- A failed call that would have partially changed data leaves **every** element untouched.
- Appending a column that is a linear combination of existing columns **cannot** increase
  rank. `dependent_feature_kernel` gives the kernel vector that makes this checkable.

## Setup

The crate pins its own toolchain and has no dependencies, so it needs no `vendor/` directory
and no network access:

```
cd optional/rust_practice
rustup toolchain install 1.90.0
```

`rust-toolchain.toml` requests `1.90.0` and the same `rust-version = "1.83"` floor as the
course. **A bare `rustc` on `PATH` may be a different release** — `rust-toolchain.toml` is
honoured by `cargo` and by `rustup run`, not by invoking `rustc` directly. The compiler-case
checker resolves the pin for exactly this reason and fails if the selected compiler does not
match the declaration.

## Run it

Every run goes in a new `my_work/` directory. Nothing here rewrites a previous record.

```
cargo check --offline --locked
cargo test --offline --locked
cargo run --offline --release --example iris_rank -- ../../data/raw/iris.csv
python check_compiler_cases.py --output ../../my_work/compiler01
```

`check_compiler_cases.py` refuses an existing output directory, and treats a missing
compiler as `blocked` (exit 2) and a wrong diagnostic as `failed` (exit 1). Only matching
predictions exit 0.

## Observed on this Windows host

Recorded from real runs on 28 October 2026 with `rustc 1.90.0 (1159e78c4 2025-09-14)`
selected through the pin. See [VERIFICATION.md](VERIFICATION.md) for the exact commands and
what each record does **not** establish.

| Check | Observed |
|---|---|
| `cargo test --offline --locked` | 13 integration tests passed, 3 doc-tests passed |
| `check_compiler_cases.py` | 6/6 matched: 2 compiled, 4 rejected as E0499, E0382, E0106, E0502 |
| `iris_rank` on `data/raw/iris.csv` | 150 rows; rank 4 before and after; `max abs(row . kernel) = 0` |

## Boundaries

- The Iris rows are one **measured** table. A rank result says nothing about the biology,
  the sampling design or the predictive value of the four measurements.
- Passing tests show one program satisfied its assertions under one tolerance. They do not
  show the algorithm is the right one for your question.
- Agreeing with the course's Go/Rust reference implementations would be software evidence, not
  independent data collection.
- Nothing here assesses learner mastery. Delayed recall and independent reasoning stay open.

## Course links

- [Rust learning path](../../native/guides/LEARNING_PATHS.md) (sections R0–R6)
- [Stage 01 guide](../../native/guides/labs/stage01.md) — the current learning position
- [Repository layout](../../docs/release/REPOSITORY_LAYOUT.md)
