# Verification record: optional Rust practice crate

Prepared 28 October 2026 on the Windows development host (`x86_64-pc-windows-msvc`).

This records what actually ran for [optional/rust_practice](.). It is not a course release
record and it is not an assessment of learner mastery. The authoritative course release
status remains [docs/release/VERIFICATION.md](../../docs/release/VERIFICATION.md).

## Toolchain actually used

| Item | Observed on this host |
|---|---|
| `rust-toolchain.toml` pin | `channel = "1.90.0"`, `profile = "minimal"` |
| Compiler honoured by `cargo` in the crate | `rustc 1.90.0 (1159e78c4 2025-09-14)` |
| Compiler selected by the case checker | `rustc 1.90.0 (1159e78c4 2025-09-14)` |
| Bare `rustc`/`cargo` on `PATH` | `rustc 1.97.1 (8bab26f4f 2026-07-14)` — **different release** |
| Installed components for 1.90.0 | `cargo`, `rust-std`, `rustc` only |

The distinction matters. `rust-toolchain.toml` is honoured by `cargo` and by `rustup run`; an
invocation of `rustc` directly ignores it. The first run of `check_compiler_cases.py` silently
used the 1.97.1 default and was **discarded**, not reported. The script now resolves the pin
through `rustup run` and fails if the selected compiler does not match the declaration.

`rustfmt` and `clippy` are **not installed for 1.90.0**. The formatting and lint checks below
were therefore run with the machine's `stable` toolchain (1.97.1) and are labelled that way.
They are not evidence about 1.90.0's lint set.

## Commands and observed results

All commands run from `optional/rust_practice` with `CARGO_NET_OFFLINE=true`, in new output
directories under `my_work/`.

| Command | Observed result |
|---|---|
| `cargo test --offline --locked` | 13 integration tests passed, 0 failed; 3 doc-tests passed |
| `cargo test --offline --locked --release` | same 13 + 3 passed in the release profile |
| `cargo doc --offline --locked --no-deps` | built; 0 warnings after fixing one ambiguous intra-doc link |
| `cargo run --offline --release --example iris_rank -- ../../data/raw/iris.csv` | completed, exit 0 |
| `python check_compiler_cases.py --output my_work/rp_compiler_…` | 6/6 matched predictions, exit 0 |
| `uv run --no-sync python -m pytest tests/test_rust_practice_optional.py -q` | 9 passed |
| `cargo fmt --all -- --check` (**1.97.1**) | clean after formatting the new crate only |
| `cargo clippy --offline --all-targets` (**1.97.1**) | 0 warnings after replacing a range-index loop |
| `check_compiler_cases.py` with `rustc` removed from `PATH` | `status: blocked`, exit 2 — not a pass |
| fresh copy of the crate outside the repository | 13 integration + 3 doc-tests passed |

### Compiler cases

| Case | Prediction | Observed |
|---|---|---|
| `accept/borrows_end_at_last_use.rs` | compiles | exit 0 |
| `accept/returned_reference_lives_as_long_as_input.rs` | compiles | exit 0 |
| `reject/overlapping_mutable_borrows.rs` | `E0499` | `error[E0499]` |
| `reject/use_after_move.rs` | `E0382` | `error[E0382]` |
| `reject/return_reference_to_local.rs` | `E0106` | `error[E0106]` |
| `reject/mutate_while_borrowed.rs` | `E0502` | `error[E0502]` |

Every diagnostic code above was **captured from the compiler before** `cases.json` was
written. The four rejections are the ones the practice material specifies.

### Real-data route

`examples/iris_rank.rs` run on the course's own `data/raw/iris.csv`:

```
rows                  150
columns before/after  4/5
appended column       2*x0 + -3*x1
tolerance             1e-9
rank before           4
rank after            4
max |row . kernel|    0e0
dependent column      did not increase rank, as the algebra requires
```

The exact zero is expected: the kernel vector `[-2, 3, 0, 0, 1]` makes every row product
vanish identically, not approximately. It is a property of the construction, not a lucky
tolerance.

## What was not run, and is not claimed

| Not run | Consequence |
|---|---|
| `rustfmt` / `clippy` on **1.90.0** | those components are not installed for the pin; lint claims belong to 1.97.1 |
| Clippy with `-D warnings` | the crate is warning-free today, but no strict gate is configured |
| Linux, macOS or WSL | only `x86_64-pc-windows-msvc` was exercised |
| Docker, Kubernetes, kind | untouched by this crate and unrelated to it |
| `uv.lock` re-resolution | the crate has no Python dependencies and adds none |
| Any learner assessment | nothing here measures mastery or retention |

## Repository-suite result for this change

`uv run --no-sync python -m pytest -q -ra` on this host:

```
888 passed, 3 skipped in 127.32s
```

The three skips are pre-existing and unrelated: two POSIX filesystem contracts on a Windows
host, and one opt-in Rust mutation test. Running that opt-in test separately
(`SHAPE_TEST_RUST_MUTATION=1 pytest tests/test_learner_mutation.py`) gave **3 passed**, which
confirms the existing `native/rust` reference still builds and still fails on a deliberately
wrong edit.

The baseline before this change was 876 passed / 6 skipped in the release record; the count
here is higher and the skip count lower because this host has Go and Cargo available. The
comparison of interest is that **no existing test regressed** and 9 new tests were added.

The layout document was updated, and `tests/test_repository_layout.py` still passes.

## Honest limitations

- Controlled fixtures and one measured flower table are not a broad benchmarking set.
- Passing assertions show one program matched its own expectations. They do not show the
  algorithm is appropriate for a different question.
- The practice crate agrees with nothing in `native/rust` by construction; it deliberately
  uses a different, smaller contract. Do not describe it as a third reference implementation.
- The independent exercise in [EXERCISES.md](EXERCISES.md) remains `not_assessed`.
