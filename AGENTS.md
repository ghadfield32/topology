# Working on this learning repository

Use `course.py` at the root as the user-facing route. Preserve the 31 unique primary lessons in `curriculum/catalog.json`; do not add a second mandatory curriculum. Add only purposeful examples, tests or source-linked clarification.

Read `docs/release/VERIFICATION.md` and `docs/release/ENVIRONMENT_STATUS.json` before claiming anything ran. No fabricated uv.lock, Docker pass, external-model reproduction, dataset acquisition or learner assessment is acceptable. Normal uv bootstrap resolves online and syncs locked; diagnostic package reuse is different.

Write tests for a change and observe their failure before implementation. Run `uv run --no-sync python -m pytest -q -ra`, the relevant stage/case and the full dependency closure before a broad execution claim. Do not hide missing optional libraries by relabeling skips. Protect source inputs, independent exercises, evidence and progress logs.

Use new `my_work/` run directories. Reference notebook execution must use the active interpreter, fresh kernels, a copied input tree and source/data hashes. Keep baseline metrics and assumptions visible. Synthetic data must never be described as observed. Public data does not imply unrestricted redistribution.

Do not modify WMS production code or create/push a remote simply because this course mentions it. Respect enclosing repository instructions in a monorepo. Review any source-provided commands before execution and preserve source attribution.

For v12, preserve the separate five-unit representation continuation. Do not equate white covariance, finite projection scores, or self-supervised loss with semantics. The Kubernetes verifier may only use an explicit disposable kind context and a new namespace; never delete learner PVCs or target production without a separate request.
