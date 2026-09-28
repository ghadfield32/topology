# Native16 verification and coverage record

Prepared 26 September 2026. This is a new execution record, not a relabeling of previous archives. The baseline was the actual mounted v14 combined archive; no v15 archive was available to verify. The retained Python teaching material remains in the archive. The native addition is a separate workspace and does not require resetting the 31-stage course.

## Executed results

| Check | Observed result |
|---|---|
| Combined root Python tests | 821 passed, 2 optional-library skips, zero failures |
| Go native tests | 34 passing named tests/subtests; zero failing assertions |
| Rust native tests | 28 passed, zero failed or ignored |
| Native lab execution | 57 Go + 57 Rust runs, all completed |
| Go/Rust result comparisons | 57 passed; input hashes also agree |
| Registered data decoding | 55 source files in each language: 110 full-value comparisons passed |
| Numeric values compared by source decoder | 9,896,088; CSV fields/text/IDs also compared exactly |
| Valid/invalid reader fixture checks | 64 passed across both languages |
| Independent scientific comparisons | 220 passed using NumPy, retained Python topology and PyTorch |
| Protected native/data inputs during acceptance | 90, unchanged |
| Editable practice copies | Stage 01 and Wine prepared; Stage 01 Go and Rust private workspaces compiled/tested |
| Full original Python notebook replay in this turn | Not run; saved previous outputs retained |
| New Docker images / Kubernetes Jobs | Configurations provided and policy-checked; not built/deployed here |

The 34 Go count includes named subtests; a command package with no test files is not counted as a passed test. The Rust binary/doc-test groups have zero tests and are not added to the 28 library tests. The 820 Python tests include existing course tests and 11 native-runner contracts; counts from different suites are not a measure of mathematical completeness.

## What agreement means

The Go and Rust programs implement the same **native16 teaching protocols**. They perform their own data reading, mathematics, optimization and serialization. They do not call a Python program to obtain their scientific results. The Python runner builds/invokes the binaries and compares evidence. The independent Python checks are separate calculations, including full classifier coefficients/predictions and HNN/restricted LNN/PINN training under the matching native protocol.

Integer results compare exactly. Floating-point native metrics use absolute tolerance 1e-8 and relative tolerance 1e-7; the maximum observed absolute difference across the current lab comparisons was 2.32830643654e-10. Source decoding compares values with zero numerical tolerance, plus shape/order/dtype, IDs, text, missingness and source hashes. Numeric counts include repeated storage forms and metadata; they are not counts of independent observations.

## Full data access versus every possible dataset

The registry covers every listed bundled input under `data/`, `sports_v8/data/` and `sports_v9/data/` in the supported forms. CSV, JSON, NPY/NPZ, PNG and text metadata/terms are included in the source audit; PFM is independently tested with manufactured endian/scale fixtures. The parsers deliberately reject unsupported encodings, object arrays and unsafe/oversized inputs. They are bounded learning readers, not hardened arbitrary-upload services.

No new external dataset payload was acquired. Original source cards and license/transcription/sample-selection limits remain applicable. Selected SPL frames are not a new independent set of shots; soccer season profiles are not pitch trajectories; ACB metadata is not a full tracking corpus. The recorded observed-image stereo calculation remains separate from manufactured dynamics.

## What is NOT certified

Full operation-for-operation equivalence to all 133 original Python notebooks is **not certified**. `native/COVERAGE.md` states every unit's native work and original-protocol difference. Some classifiers use a new declared split and solver, some geometric labs are smaller controls, the LNN fixes mass and learns a potential, and the spectral learner is a small Fourier-multiplier model rather than a full multilayer FNO. General Delaunay/alpha construction, pretrained VGGT, full PointNet/reconstruction/semantic-scene pipelines, original-paper benchmarks, independent measured validation and the actual book audit are not completed by these checks.

The command `verify --require-original-parity` refuses that larger claim. A successful comparison is software evidence, not a guarantee of scientific meaning or learner mastery. The new study records are unassessed.

## Actual compiler and environment provenance

Executed on Linux x86_64 with Python 3.13.5, Go 1.23.2 and Rust/Cargo 1.90.0. These are the tested versions, not a newest-version recommendation. Rust was previously absent. A scoped workflow on the isolated `learning/native-parity-v16` branch provisioned the official compiler and resolved/vendorized reader dependencies. Its artifact checksum was verified; the actual course compiled and ran locally using those tools. The remote smoke alone did not certify the course. `main` was not changed and new native source was not pushed. The artifact/compiler binaries are not bundled; 36 dependency source crates and their licenses are.

The branch push also ran the earlier repository's core CI on Linux/macOS/Windows, which succeeded; that is separate evidence about the existing remote source, not platform certification of this ZIP. Its full/Docker job skipped. The new full-native workflow is supplied in the ZIP but has not run remotely. Mac, Windows, GPU, clean Python dependency installation, new container runtime and new cluster deployment are not claimed. Preserve the genuine Python lock already resolved on the user's machine; no fabricated uv.lock is added here.

## Failures were corrected, not hidden

The initial regression runs exposed missing behavior and compile errors. Rust's default decimal JSON conversion differed by one ULP for selected source numbers; round-trip float parsing corrected it. PNG conversion through premultiplied channels lost original values; direct channel decoding corrected it. Boolean/Unicode/endian/Fortran arrays and palette/alpha images now have explicit fixtures. Essential diagram-cardinality mismatch now yields infinite bottleneck distance instead of a panic. Public Rips H0/H1 reports no longer misreport H2 classes created by a dimension-truncated complex. Ridge intercept calculation now centers arbitrary input features internally. A packaging check also caught cache-hit logging replacing the original compiler record; the runner now retains first-build and reuse records separately, with a regression test. Failed and passing scoped logs are preserved beside the final records.

## Reader checks and configuration checks

Static checks found no missing or escaping targets among 830 native-reader local links. Actual HTTP checks returned 200 for the home, Stage 01 guide and its Go result, and 403 for private-work and Git paths. Chromium is absent here, so no new visual/browser-navigation result is claimed. Older screenshots are historical.

The deployment YAML parsed; two Jobs passed project-specific security and resource checks. This is not Kubernetes OpenAPI admission or Docker/cluster execution. Target-platform acceptance remains explicit.

## Inspect and rerun

- `native/evidence/acceptance/acceptance.json`: whole native acceptance scope.
- `native/evidence/acceptance/execution.json`: all native runs, comparisons and input hashes.
- `native/evidence/acceptance/go/` and `rust/`: exact parameters, losses, predictions and output fields.
- `native/evidence/acceptance/data_comparison.json`: all registered source comparisons.
- `native/evidence/acceptance/reader_fixtures.json`: malformed and edge-case inputs.
- `native/evidence/acceptance/scientific_checks.json`: independent scientific checks.
- `native/evidence/python_final.xml` and `.log`: combined Python suite.
- `native/evidence/toolchain_provenance.json`: remote provisioning versus local execution.

Fresh extracted-archive checks and the final archive hash are delivered alongside the ZIP, because an archive cannot embed its own final hash. Rerun `python native_course.py verify --science --output my_work/native_acceptance01` on the target machine and retain the actual logs. Use a new output directory; never erase earlier evidence just to obtain a green screen.
