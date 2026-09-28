# Native16: one curriculum, two native execution paths

Start at [START_NATIVE.html](../START_NATIVE.html) or [the setup guide](guides/SETUP.md). Then read [the language learning paths](guides/LEARNING_PATHS.md), choose your current unit with `python native_course.py show stage01`, and compare it.

Prefer notebooks? Every one of the 57 units has a Python, Go and Rust notebook in [workbooks/polyglot](../workbooks/polyglot/index.html). The Python one runs the canonical course reference; the Go and Rust ones compile and run the real native programs. Worked session: [the Stage 01 walkthrough](../docs/release/STAGE01_WALKTHROUGH.md). What each check does and does not establish: [separate checks](../docs/release/CHECKS.md).

The original Python course, source audits and Poux extension remain unchanged. The new Go/Rust implementations parse their own source inputs and execute their own mathematics and training. The Python launcher only coordinates processes and compares evidence; the independent Python checks are expressly separate.

Read [coverage](COVERAGE.md) before saying “full parity.” A unit may reproduce an exact mathematical core while using a different experimental architecture from the original notebook.

## Code map

| File pair under `go/engine` and `rust/src` | Responsibility |
|---|---|
| `data.go` / `data.rs` | Bounded CSV/JSON/NPY/NPZ/PNG/PFM decoding, value types, path checks |
| `math.go` / `math.rs` | Matrices, rank, solves, covariance, Jacobi eigenvalues, deterministic RNG |
| `topology.go` / `topology.rs` | Complex validation, F2 persistence, pixel topology, bottleneck, Mapper |
| `learning.go` / `learning.rs` | Native AD, second-order jets, actual small-model training, preprocessing |
| `datasets.go` / `datasets.rs` | Cross-sector data protocols and honest model evaluation |
| `geometry.go` / `geometry.rs` | Cameras, stereo, registration, motion, integration, constraints |
| `operators.go` / `operators.rs` | Trained branch/trunk and spectral controls, differentiable fitting |
| `trace.go` / `trace.rs` | Consumed-file hashes and explicit boundary matrices |
| `labs.go` / `labs.rs` | The 57 explicit native-unit dispatch arms |

These are pedagogical f64 kernels, not optimized BLAS replacements or hardened arbitrary-upload services. Their command interfaces contain failures; several internal invariant checks use Go panic / Rust assert and are caught at the boundary. Practice converting such a boundary to typed `Result`/error without hiding the failure.
