# Updating an existing course repository to v14

Do not overwrite `my_work/`, progress logs, a genuine `uv.lock`, or locally edited learner notebooks.

Recommended approach:

1. Commit or back up the existing repository.
2. Extract v14 into a separate folder.
3. Compare the v14 tree against your current course repository.
4. Copy the additive `polyglot/`, `curriculum/extensions/poux_spatial_ai/`, `deploy/polyglot/`, `.github/workflows/polyglot.yml`, `polyglot.py`, and v14 docs first.
5. Reconcile the release-version files only if you want the whole repository to identify as v14.
6. Keep the genuine `uv.lock` already generated on your computer when it is still consistent with `pyproject.toml`; run `uv lock --check` / `uv sync --locked` after reconciling the project version.
7. Run Python acceptance, Go verification, then Rust verification.

Do not delete the already verified Kubernetes PVC or learner evidence as part of a course update.
