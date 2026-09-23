# Verification and scope — version 9

## Fresh execution completed
All **123 cataloged reference notebooks** were executed successfully in this build using fresh kernels in a temporary copy of the source inputs. Earlier `reports/`, `physics/reports/`, `industry/reports/`, processed caches, rendered pages and learner work were not copied in. Dependency-producing notebooks were run before capstones that read their outputs.

The execution contains **724 code cells and 80 embedded PNG outputs**. Details, per-notebook timing and source hashes are in `reports/v9/notebook_execution.json`. Code outputs do not automatically establish mathematical correctness, calibration accuracy, domain generalization or learner mastery.

## Test and runner checks
The full build test suite reports **631 passed, 2 skipped, zero failures**. The two skips are the unavailable Ripser and GUDHI comparisons. `reports/v9/pytest_final.txt` contains the actual run; earlier `tdd_red` logs are deliberate failing regression checks captured before implementation, not the final suite.

All **31 stage-entry checks** passed in a fresh copy. `reports/v9/lesson_execution_matrix.json` maps each stage to its primary reference notebook, entry-check result and still-unassessed learner gate.

A separate run of the documented Stage 00 CLI command passed. SHA-256 comparisons showed **237 source notebook, dataset and progress files unchanged**. Repeating the same destination was refused with exit code 2 and did not alter the existing execution manifest. The temporary-copy operation excludes `.venv`, `venv`, caches and learner work, so it does not duplicate installed environments.

The reader uses one canonical render per source and lightweight aliases for old paths. Static checking verifies local file destinations and HTML fragment targets. Search, answer reveal, code displays, an embedded figure and a 390-pixel mobile layout passed browser rendering checks. Actual file and localhost navigation were blocked by an administrative policy in this execution environment. The successful rendering tests use exact generated HTML through `page.set_content` with local CSS inlined; they do not establish full navigation behavior. External links were not exhaustively crawled.

## Environment and remaining limits
Execution uses Python 3.13.5 on Linux; the package records NumPy, SciPy, pandas, scikit-learn, notebook and PyTorch versions. The small physics examples execute on CPU. Mac, Windows, GPU execution and a clean internet-based dependency install were not tested here. Initial installation needs internet or an existing package cache.

Ripser and GUDHI remain unavailable, so comparisons against them are not claimed. Existing tests retain visible skips. All other final test, reader and archive checks are recorded separately in `reports/v9/` and the final archive-check JSON delivered alongside the ZIP.

## Source integrity and sports scope
The ten-game ACB metadata snapshot reproduces the Git blob SHA returned by the GitHub source connector. SHA-256 and source details are stored with the data. This checks the file identity, not the independent correctness of every sporting result.

The ACB tracking, dynamic events and season aggregates are not bundled or evaluated. Earlier small SPL and soccer excerpts retain their acquisition caveats. Other optional sports sources are acquisition plans, not executed benchmarks. Learned VGGT inference and new physical measurements are not claimed.

## Meaning of the learner checks
Reference execution checks supplied code. Stage-entry checks exercise selected calculations. Conceptual proofs, independent exercises, delayed recall and capstone interpretation still require assessment of the learner's own work. Progress logs start unassessed and are not modified by this verification run.

The actual full book text has not been audited. The course covers the agreed introductory scope and explicit extensions; it does not certify exhaustive mastery of topology, all scientific machine learning or every industry application.
