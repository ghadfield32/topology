# stage25 — Constraints, projections, retractions and rank failure

**Kind:** stage  
**Canonical Python lesson:** `physics/lessons/25.md`  
**Canonical Python reference:** `physics/notebooks/25_lab.ipynb`  
**Independent Python practice:** `physics/practice/learner/25_practice.ipynb`

## Use the three languages in this order
1. Predict and do the smallest calculation by hand.
2. Run the Python reference. It remains the full course reference implementation.
3. Run the Go companion: `go run ./cmd/shape-go --repo ../.. --lab stage25` from `polyglot/go`.
4. Run the Rust companion: `cargo run --bin shape-rust -- --repo ../.. --lab stage25` from `polyglot/rust`.
5. Compare units, shapes, invariants, and limitations—not only printed numbers.

## Completion gate
Identify which constraint was enforced and residual remaining.

## Language-learning exercise
Reimplement one helper used by this lab without consulting the sibling language, add a test, then explain any difference in ownership, error handling, iteration, numeric types, or data parsing.

## Parity boundary
The Go and Rust companions intentionally reproduce the **algorithmic core and data checks** in a dependency-light way. They are not automatic source-to-source translations of every Python plotting, PyTorch, scikit-learn, Open3D, or notebook cell. When the Python lab uses a specialized library, the companion focuses on the hand-checkable computation that the library is supposed to implement or validate.
