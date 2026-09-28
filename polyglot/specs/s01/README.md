# s01 — Landmark angles and velocity

**Kind:** case  
**Canonical Python lesson:** `sports_v8/lessons/S01.md`  
**Canonical Python reference:** `sports_v8/notebooks/S01.ipynb`  
**Independent Python practice:** `sports_v8/practice/S01.ipynb`

## Use the three languages in this order
1. Predict and do the smallest calculation by hand.
2. Run the Python reference. It remains the full course reference implementation.
3. Run the Go companion: `go run ./cmd/shape-go --repo ../.. --lab s01` from `polyglot/go`.
4. Run the Rust companion: `cargo run --bin shape-rust -- --repo ../.. --lab s01` from `polyglot/rust`.
5. Compare units, shapes, invariants, and limitations—not only printed numbers.

## Completion gate
One-shot sparse frames or selected profile rows; not a sports benchmark.

## Language-learning exercise
Reimplement one helper used by this lab without consulting the sibling language, add a test, then explain any difference in ownership, error handling, iteration, numeric types, or data parsing.

## Parity boundary
The Go and Rust companions intentionally reproduce the **algorithmic core and data checks** in a dependency-light way. They are not automatic source-to-source translations of every Python plotting, PyTorch, scikit-learn, Open3D, or notebook cell. When the Python lab uses a specialized library, the companion focuses on the hand-checkable computation that the library is supposed to implement or validate.
