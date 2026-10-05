# v17 execution scope — evidence before completion claims

This release preserves the supplied v16 course and adds the source-mapped systems layer. It does not relabel old results as new, equate notebook execution with learner mastery, or certify every source recommendation as implemented.

## Fresh execution in this build

| Check | Result |
|---|---|
| Existing Python test suite | 821 passed, 2 skipped (Ripser/GUDHI absent), no failures. |
| New isolated Python contract/navigation/project tests | 21 passed. |
| Native16 Go/Rust acceptance | All57labs in each language executed; all comparisons passed. Go34tests/subtests; Rust28tests. |
| Native source decoding | 110comparisons for55registeredfiles, plus64reader fixtures and220selected independent scientific checks. |
| New language workbook sweep | 171/171 passed in fresh kernels;513interfacecodecells. |
| Actual original Python calculations behind those interfaces | 56unique original notebooks,74executions including prerequisite repeats. NOT all133original notebook files freshly rerun. |
| Source-mapped project matrix | Eight passed; C++OpenCV and PyO3 blocked. Status is not an all-ten pass. |
| New Go service tests | Seven tests passed under the race detector. Actual loopback HTTP→nativeGoStage01→JSON request passed; graceful termination returned0. |
| New Rust validator | Ten tests passed; actual source-byte decoding executed. |
| New C and C++ projects | CMake/CTest passed: two C tests, three C++ tests. Actual SPL reader and trajectory outputs independently checked. |
| C/Rust portable format boundary checks | 28checks passed across valid and malformed files. |
| pybind11 | Actual C++extension built/imported; trajectory and MST controls passed. |
| TypeScript | Strict compilation and ten Node runtime-contract tests passed. |
| Private edited-source test | Correct copy passed, deliberately wrong count failed, repaired copy passed; reference source unchanged. |
| GPU profiling | CPU profiler executed on repeated real-data buffers. CUDA/Triton/CUDA-C++ not run; explicit CUDA probe returned blocked. |
| Controlled failure teaching | Rust conflicting-borrow/moved-value compile failures and an ASan heap-use-after-free failure were observed. Correct C sanitizer build/tests also passed. |

The current portal check covered24HTMLpages and382localtargets, with none missing. Three public HTTP paths returned200 and three private/traversal/directory paths returned403. Browser rendering, filtering, realJSONloading, viewport sizing and clearing stale plots after an error passed. Actual file navigation was blocked by administrator policy.

The final archive-extraction and browser checks are in `systems/evidence/release_checks.json` and the separately delivered archive-check record. Do not infer them from this table alone.

## Important failures retained

The first workbook sweep leaked caller-owned KernelManager instances. This reached the process memory limit. The interrupted record is preserved. Explicit finally-block shutdown/cleanup fixed the resource ownership; the complete171-workbook sweep then passed. Partial pre-fix progress is not counted as a successful sweep.

A unit test caught compiler errors being mislabeled as missing dependencies. The project checker now distinguishes an explicit dependency block from an actual build/assertion failure. Contract tests also found missing confidence/limitation validation and prediction-overflow checks; the fail-before-fix records remain included.

## Actual measured-data demonstration

The source is the existing selected SPL tracking excerpt:12frames, one participant, one trial. Coordinates are converted from feet to metres; time is an ideal frame/sample-rate clock. Confidence is not supplied and stays unknown. This is not new sensor acquisition or independently certified ground truth.

Five selected points fit an initial state under fixed g=9.81m/s²; two later same-shot points evaluate it. C and Rust agree with Python's count and coordinate means. C++andPython trajectory predictions differ by at most8.8818e-16m in this run.

- Height fitting RMSE:0.0175369173m.
- Two-point later height MAE:0.0488124742m.
- Last observed fitting-height baseline MAE:0.0446230813m.
- Fitting-mean height baseline MAE:0.2501537654m.

The last-height baseline outperforms this fitted model on these two selected points. The exercise must not present the weaker mean baseline as the only comparison. No statistical significance, release detection or out-of-athlete accuracy is established.

## Tested environment

Linux x86_64; Python3.13.5; Go1.23.2; Rust/Cargo1.90.0; GCC/G++14.2; CMake3.31.6; Node22.16.0; TypeScript5.8.3; PyTorch2.10.0+cpu; NumPy2.3.5. These are observed tool versions, not claims to be the latest or production recommendations.

The pybind11 build used explicit genuine headers present in the installed PyTorch include directory. A new online pybind11 installation was not tested. Rust's validator has a genuine Cargo.lock and reuses the base's vendored source dependencies. The optional PyO3 package has no invented lock or vendored dependency claim.

## Still blocked, planned, or outside scope

- New Docker image build/run, new Kubernetes Deployment/Job execution, remote execution of the new manual CI workflow, Windows/WSL/macOS setup, fresh dependency resolution and GPU execution were not performed here.
- New C++OpenCV requires a development package not present here. PythonOpenCV's existing-image/memory/projection probe passed; that is not C++equivalence.
- PyO3/maturin are not installed. The actual extension source is present, but compilation, import and clean packaging await that dependency gate.
- CUDA/Triton kernels are supplied and labeled unexecuted; CPU performance is not GPU performance. Nsight, mixed-precision and torch.compile comparisons are further exercises.
- C++does not implement spin/drag/contact or a general surveyed scene pipeline. The TypeScript display is an offline orthographic projection of3Dcoordinates, not a full WebGLworld. The Go service is bounded/in-memory, not durable or authenticated for public deployment.
- The source's advanced capstone ideas, original-book audit, all original-model protocol equivalence, general alpha/Delaunay construction, trained VGGT/PointNet/semantic-scene pipelines, independent research validation and learner mastery remain explicit obligations.

## Where to inspect evidence

`systems/evidence/` contains development red/green logs, the final original pytestXML, nativeacceptance/data/scientificcomparisons, all171executed interface notebooks,56fresh original references, project-check logs, portable-reader cases, actual HTTPservice result, private-edit mutation evidence, and the integrated-demo data/results/viewer. Binary compiler outputs and toolchain executables are intentionally not distributed.
