> Historical v14 companion documentation. Use [the native16 route](../START_NATIVE.html) and `native_course.py` for current substantive native implementations. The older code is retained for comparison, not assigned again.

# Python + Go + Rust learning track

This directory adds two **parallel implementation languages** to the existing course without creating a second curriculum.

- **Python remains the canonical full reference** because the course notebooks contain the complete data science / scientific ML workflows, figures, PyTorch models and external-library comparisons.
- **Go and Rust reproduce the algorithmic core** of every core stage and every named application/method case using the same bundled files where practical.
- Every lab has one language-neutral page in `polyglot/specs/<lab>/README.md` linking back to its Python lesson/reference/practice and stating the parity boundary.

The current manifest contains **57 companion labs**: 31 core stages, 25 named cases, and the Poux Stage-01 bridge.

## Why use three languages?

Python teaches the mathematics and scientific ecosystem. Go forces explicit data movement, errors, slices and concurrency-friendly systems habits. Rust adds ownership, borrowing, explicit numeric types and memory-safe systems programming. The goal is not to prove one language is "better"; it is to understand the same algorithm well enough to reimplement it.

The source map motivating the spatial-AI extension recommends Python for the broad toolchain and explicitly notes that Rust can be useful when performance or real-time requirements justify a lower-level implementation. The course therefore keeps Python first and uses Rust/Go as second implementations, not replacements.

## Daily workflow for a stage or case

1. Read the normal course lesson and make the hand prediction.
2. Run the Python reference and save its evidence.
3. Read `polyglot/specs/<lab>/README.md`.
4. Run the Go companion.
5. Reimplement one helper or lab calculation yourself in `my_work/polyglot/...`.
6. Run the Rust companion after installing Rust.
7. Compare output *meaning*, units, shapes and invariants. Do not expect identical plot files or floating-point formatting.
8. Write what each language made explicit that another hid.

Example for Stage 01:

```powershell
# Python reference
uv run --no-sync python course.py run --stage 1 --output my_work/stage01_python01

# Go
Push-Location polyglot/go
go test ./...
go run ./cmd/shape-go --repo ../.. --lab stage01
Pop-Location

# Rust
Push-Location polyglot/rust
cargo test
cargo run --bin shape-rust -- --repo ../.. --lab stage01
Pop-Location
```

## Toolchain versions

- Python: use the course's declared Python/uv setup.
- Go: `go.mod` declares Go 1.23. The build environment executed with Go 1.23.2.
- Rust: `Cargo.toml` declares Rust 1.83. Rust was **not installed in the archive build environment**, so the Rust source received static structure checks only here. CI and the Rust Dockerfile compile/test it on a machine with the toolchain.

## What "all labs" means

`polyglot/specs/labs.json` is the source of truth. It includes every 31-stage entry and every 25 case entry from the existing course catalogs, plus `poux_bridge`. Each entry has:

- canonical lesson
- canonical Python reference notebook/script
- independent Python learner notebook or extension plan
- Go companion
- Rust companion
- completion gate / scope

## Important parity boundary

A language companion is not a fake translation of a library call. For example:

- Python may use scikit-learn for a full classifier; Go/Rust may implement the schema check, baseline statistic or hand-checkable distance calculation that validates the foundation.
- Python may train an HNN/PINN; Go/Rust implement the exact mechanics/PDE control that the learned model must respect.
- Python may use plotting and notebook display; Go/Rust return numerical summaries.

Use the Python reference when the learning goal is specifically a third-party scientific library. Use the Go/Rust implementation when the learning goal is the underlying algorithm and systems behavior.
