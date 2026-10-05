# sys08 — Python ↔ Rust with PyO3
**Source:** Stage 8. **Project:** `systems/pyo3`, wrapping the tested pure Rust validator rather than copying its algorithm.

## Explain the purpose
Python remains the research interface while Rust owns the validation contract. A boundary should specify data types, copying, error mapping and versions. The included PyO3 module accepts Python bytes, borrows their byte slice for the call, runs the shared `capture_validator::validate_bytes`, and returns the count and centroid. Invalid data becomes a Python ValueError with a deliberate error message.

The pure validator is a separate Rust crate and can be tested without a Python runtime. The wrapper crate is a cdylib whose exported module name matches the Python import. Its Cargo dependency on the validator is a path dependency. This separation prevents the binding and CLI from silently implementing different validation rules.

## Current execution boundary
The pure Rust project compiles and runs in this package's evidence. The PyO3 wrapper source and pyproject are supplied, but PyO3/maturin were not installed in this environment and package-index access failed. This module is therefore BLOCKED, not 'tested because Rust works'. No synthetic Cargo.lock or copied wheel is provided. The first project check explains the missing gate and refuses to claim a pass.

## Connected-machine procedure
Use a separately reviewed environment or the prepared project copy, not an uncontrolled install into the working course. Install maturin, resolve the exact PyO3 dependency from Cargo.toml, review/retain Cargo.lock, then build/import with the target Python. The project's local `pyproject.toml` does not replace the course root manifest. Run from the PyO3 workspace; its own dependency requirements are separate from the pre-vendored native16 scientific workspace.

A typical flow after resolution is `maturin develop` in an activated environment followed by an import of `capture_validation_py`. Document the actual compiler, Python executable and module path. Do not confuse a successful build with an installed module in a different interpreter.

## Predict and validate
Use the same 588-byte derived basketball file as the C and Rust CLI. Predict count=12 and a three-coordinate centroid. Compare outputs with independent Python decoding. Try truncated bytes, wrong magic and nonfinite coordinates; check that each fails rather than returning partial output. Rebuild after changing the Rust source and restart Python before testing the new extension.

## Apply and exit
Explain argument borrowing, the pure-core/wrapper split, the returned values, how errors cross into Python, and what measurements the validator cannot certify. Benchmark conversion and validation separately only after successful equivalence checks. A later buffer-based zero-copy API or PyO3 GIL-release design needs its own safety contract. The supplied binding is a focused learning implementation, not a complete production packaging matrix.
