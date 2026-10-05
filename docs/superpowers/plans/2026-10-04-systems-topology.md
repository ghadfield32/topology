# Systems-topology integration implementation plan

> Implement inline with isolated build workspace; evidence before completion.

**Goal:** An executable, source-mapped topology/engineering course rather than another pile of notebooks.
**Architecture:** Preserve v16 and add systems/ plus a single study front door. Share real data by path and hashes. Projects use explicit artifacts rather than hidden state.
**Tech Stack:** Existing Python/uv + Go + Rust, C11, C++20/CMake, TypeScript/Node; gated pybind11, OpenCV, PyO3, PyTorch/Triton/CUDA.
**Spec:** docs/v17/DESIGN.md.

## Global constraints
- Preserve all 31 primary lessons and 57 native units, datasets and private progress.
- Native calculations remain native; generated workbooks do not claim new independent science.
- New output directories; source hashes recorded; unknown confidence is not zero certainty.
- No default external services, remote writes, production contexts or destructive import.
- Existing v16 tests/evidence stay distinct from new v17 tests/evidence.

## Review focus
- Truncated, malformed, nonfinite and oversized binary inputs rejected before allocation.
- Native prediction evaluated on distinct selected later observations; no athlete generality claim.
- Private source edits drive private builds; no silently compiling reference while editing a copy.
- Notebook fresh-run paths never search for a convenient old run.
- GPU/optional bindings/cluster steps explicitly blocked without prerequisites.

## Tasks
- [ ] Write contract tests and observe failures before new implementations.
- [ ] Implement shared artifact contract, C/C++ cores and negative-input tests.
- [ ] Implement Rust validator, TypeScript viewer and bounded Go service tests.
- [ ] Add gated integration bindings, OpenCV and GPU projects.
- [ ] Run measured sports pipeline and independent numerical controls.
- [ ] Map complete supplied path to ten systems units and existing stages.
- [ ] Generate 171 honest workbook interfaces, plus systems experiments; test generator.
- [ ] Execute stage triad, core/native suite, added suites and available system experiments.
- [ ] Package preserved originals + additions; check extraction, paths, hashes and links.


## Execution checkpoint

The core was preserved. C/C++/Rust/Go/TS projects andpybind11 were executed; the eightavailable project checks passed, with OpenCV C++andPyO3 explicitlyblocked. All171referenceinterfaces passed a full fresh sweep after correcting caller-owned kernel cleanup. Native57×2acceptance,data/fixtures/scientificchecks passed. Final packaging/extracted-copy results are attached separately. GPU, live Docker/Kubernetes andremoteCIare not claimed as completed.
