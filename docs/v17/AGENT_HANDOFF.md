# Repository agent: integrate the systems learning layer

Work only in the user's topology learning repository. Read AGENTS.md, local setup notes, current Git status, the real dependency locks, and the new SOURCE_MAP.md before changing files. Preserve completed learning and all private attempts.

The requested outcome is one topology curriculum with research notebooks and real language projects following Explain → Predict → Implement → Break → Apply. Do not create six full duplicate mathematics curricula or replace working root project manifests. Do not reset Stage01 progress.

Import additive v17paths from the separately extracted package after inspecting collisions: systems/, learning/, learn.py, LEARN_TOPOLOGY.html, docs/v17/. Preserve unpublished workbooks/polyglot/ and its generator. Reconcile navigation rather than copying over it. Existing canonical Python and native16 code remain reference implementations, with the original coverage limits visible.

Run in a new output folder:
```
uv run --no-sync python -m unittest discover -s systems/tests -p 'test_*.py'
uv run --no-sync python learn.py workbooks --check
uv run --no-sync python native_course.py verify --science --output my_work/native_review01
uv run --no-sync python learn.py project --unit sys01 --output my_work/c_review01
uv run --no-sync python learn.py check-project --workspace my_work/c_review01 --output my_work/c_review01/attempt01
uv run --no-sync python learn.py demo --output my_work/system_demo01
```
Inspect every exit code. Missing optional GPU/PyO3/C++OpenCV tools remain blocked; compilation or assertion errors remain failures. Never modify a gate just to turn a skipped test green.

Run the complete generated-workbook sweep only as an explicit bounded verification task; it executes originals and native16protocols, not a single identical scientific experiment in all languages. Its fresh kernels must be terminated after each notebook. Preserve failed/interrupted attempts.

Prove edited learner source is actually used: a private deliberate wrong change must fail; reverting it must pass; original source hashes must remain unchanged. Do not push private work or alter WMS production code. Inspect license constraints before sharing derived sports data.

Docker/WSL/Kubernetes instructions are deployment exercises, not pre-certified local runtime state. Use an explicit disposable context and new namespace; do not delete existing PVCs. A completed Job must expose its test and result evidence separately from a ready reader service. Stop before publishing ports beyond loopback or deploying into production.

Before finishing, report: changed paths, exact current test totals and scopes, numerical results with baseline, blocked items, untouched learner data, and the next Stage01 assignment. No automatic learner assessment.
