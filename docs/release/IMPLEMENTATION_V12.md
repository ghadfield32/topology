# v12 — integration and acceptance plan

## Goal and boundaries
Preserve the 31 canonical core lessons, five representation units, 133 reference notebooks and all supplied cases. Complete the path from a named case to a private learner copy; make environment and deployment acceptance reject incomplete evidence. Do not add duplicate mathematical lessons, fabricate a lockfile, silently download restricted data, or claim a live deployment from static validation.

## Tasks
1. Reproduce the v11 baseline and capture its actual tests. Inspect bootstrap, Docker, Kubernetes, reader, data provenance and case registries.
2. Add failing tests for all case practice routes, incompatible installed package versions, and incomplete deployment evidence. Implement only the missing integrations and re-run tests.
3. Strengthen Kubernetes policy checks and remove the reader's unnecessary attachment to the single-writer results PVC. Add regression tests; keep live acceptance opt-in and namespace-safe.
4. Add a single acceptance command that actually runs the selected native tests and reference scope, retains all logs, checks evidence, and probes (not deploys) Docker/Kubernetes separately. No green deployment badge without a live result.
5. Add a beginner launch plan and stage-by-stage evidence map by linking the existing primary material, not copying explanations. Add portable experiment cards for choosing data/splits/baselines and reporting failures. Preserve all prior learner logs and data licenses.
6. Re-run all references, exercise every practice route, test non-root/read-only-source behavior, perform static and HTTP checks, and attempt real uv resolution. Record unavailable checks as blocked.
7. Build the reader and a safe ZIP. Verify from fresh ZIP extraction and a local Git export. Report exact counts and scope, retaining historical evidence with its original release labels.

## Review focus
- A source table's rows are not necessarily independent observations.
- Installed distribution presence is not version compatibility, a clean sync, or a full dependency audit.
- Exit code zero without expected child outputs is insufficient evidence.
- Reader and batch jobs should not require co-scheduling on a shared RWO volume.
- Required course routes must expose the existing learner notebooks for all 25 named cases.
- No command may overwrite a previous answer, run directory, namespace, or remote repository.

## Initial evidence
v11 baseline: 698 tests passed, 2 explicitly skipped (Ripser/GUDHI), no failed tests. Container cannot resolve pypi.org; Docker/kubectl/kind are absent. These are observations on this build host, not predictions about a user's computer.

## Final implementation record

Implemented practice registry, version-aware checks, child evidence validation, explicit native acceptance, stronger Kubernetes policy, separate reader storage, read-only-source execution copies, editable private practice, serial-default reference execution and bounded bootstrap commands. Preserved failed attempts and source-derived curriculum. No remote repository/cluster was changed. No fresh install or live Docker/Kubernetes pass is claimed. Final extraction and Git export are checked separately.
