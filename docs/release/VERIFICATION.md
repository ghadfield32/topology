# Version 12 verification: evidence and its scope

Prepared 22 September 2026. This report is the current release record; older version reports remain historical. The final ZIP extraction check is supplied alongside the archive, because a file cannot embed its own final ZIP hash. A local Git commit/archive export was separately tested: 751 passed, two optional skips. Private work and active logs were not tracked; blank templates were retained. The initial export caught a missing compatibility field in the environment-status report; it was repaired and the export rerun.

## Executed checks

| Check | Observed result |
|---|---|
| Final local suite | 751 passed, 2 skipped, 0 failures/errors |
| Fresh serial reference replay | 133 passed, 0 failed |
| Teaching code cells | 766 |
| Additional interpreter/source-provenance cells | 133 |
| Embedded reference PNG outputs | 80 |
| Reference-run protected input hashes | 504, unchanged |
| Reference teaching source comparison | 133 unchanged teaching sources against the successful replay |
| Non-root/read-only native acceptance | Passed tests and Stage 00 with UID 65534, root-owned mode 0444/0555 source and separate writable output |
| uv-launched first notebook | Passed with explicitly inherited installed dependencies |
| All named practice routes | 25 cases plus 31 stages resolve to existing learner notebooks |
| Independent topology packages | Ripser and GUDHI absent; two comparisons skipped |
| Kubernetes | Static project-policy checks pass; live cluster not exercised |

The reference replay ran before the final bootstrap-timeout and private-practice-copy changes; those do not alter teaching cells and are covered by later tests and smoke runs. Saved notebook outputs are copied from the successful current replay. The ledger's source hashes identify its input notebook bytes, before refreshed outputs were copied back.

## Failures were not erased

The starting v11 suite passed 698 tests with two skips. New regression tests first failed, then passed after implementation. The first parallel replay completed 132 references but one kernel died before answering its startup handshake. It was not silently retried into a green log. A separate full serial replay completed all 133. Serial is now the default; two-to-four workers remain an explicit choice, not a promised safe setting for every host.

The non-root harness first inherited the wrong USER name and collided with a root-owned pytest temporary directory. After correcting that harness, a tampering fixture inherited read-only file modes. After repairing its private-copy fixture, the actual execution workspace was found to preserve read-only directory modes. The runner now grants owner-write only in its disposable copied workspace. The source is unchanged. Finally, private learner copies use an editable destination rather than inheriting a read-only source mode.

These records are preserved under [reports/v12](../../reports/v12/summary.json). A native permissions test is not a container, syscall-sandbox or cluster test.

## What readiness now means

`doctor` checks declared direct-package versions and Python compatibility, not only imports. It does not solve every transitive requirement, audit vulnerabilities, or verify a fresh install. Full profile requires the independent topology packages.

`acceptance` runs tests and either Stage 00 or all references, then checks the exact profile, consistent nonempty JUnit counts, unique expected notebook set, successful teaching cells, and source continuity. Missing child reports, contradictory totals, missing notebooks, changed inputs or full-profile skips are not accepted. This is consistency checking of locally generated evidence, not a signature authenticating arbitrary third-party logs.

Kubernetes performs the same child-evidence check inside the Job and at the host verifier. Its project-policy validator rejects unsafe/mixed resources, but is not the Kubernetes OpenAPI schema. The reader no longer attaches the private single-writer work PVC.

## Explicitly incomplete deployment gates

An actual normal uv resolution attempt failed fetching the pandas package-index page because DNS lookup failed. No genuine lock was produced. The earlier interrupted attempt remains labeled interrupted. Diagnostic reuse then created a venv pointing explicitly to installed packages and successfully ran Stage 00. **That diagnostic is not a clean dependency installation.** No fabricated `uv.lock`, wheelhouse, or dependency audit is supplied.

Docker, kubectl, and kind are absent. Image build/run, live API admission, scheduling, PVC binding, completed cluster Job, and cluster reader access therefore did not execute. The commands emit blocked/not-run statuses. The native system used Linux, Python 3.13.5, CPU PyTorch and uv 0.10.0. Mac, Windows, GPU, remote GitHub Actions, and arbitrary platform/dependency combinations were not tested.

Final reader checks passed: 31 stage cards, search, answer reveal, two embedded figures and a 390-pixel viewport with zero page overflow. Python HTTP tests returned 200 for two public paths and 403 for four private/traversal paths. Chromium navigation returned ERR_BLOCKED_BY_ADMINISTRATOR; visual checks used set_content and are not end-to-end navigation. Static checks found no missing targets among 29,470 file targets and 648 fragments. See reports/v12/browser.json and reports/v12/links.json.

## Experiments and source boundaries

The existing real-data numerical reports were regenerated by the reference replay. Manufactured shapes, dynamics, PDE controls and copied-row leakage examples remain manufactured. Selected sports frames/profiles remain selected excerpts; full modern tracking/video, trained VGGT, original-paper benchmark reproductions and independent physical validation are not claimed. No new observed payload was acquired in this version.

The supplied SIGReg, manifolds, HNN/LNN, physics-gradient and symplectic/projection concepts retain their source audits. Existing claims are not erased or converted into general guarantees. The course is an original curriculum, not the complete publisher book. Independent proofs, delayed recall, unseen capstones and eventual book reconciliation remain learner work.

## Direct evidence

- [Final local JUnit results](../../reports/v12/tests.xml) and [full test output](../../reports/v12/tests.log).
- [Every fresh reference](../../reports/v12/reference_execution.json) and [native full-scope acceptance](../../reports/v12/acceptance_full.json).
- [Initial parallel attempt](../../reports/v12/parallel_attempt.json), including its failure.
- [Non-root native run](../../reports/v12/nonroot_pass.json), [its tests](../../reports/v12/nonroot_tests.json), [its notebook](../../reports/v12/nonroot_stage00.json).
- [Normal uv failure](../../reports/v12/clean_install_attempt.json) and [its log](../../reports/v12/clean_install_attempt.log).
- [Explicit diagnostic uv setup](../../reports/v12/uv_diagnostic_setup.json) and [uv notebook evidence](../../reports/v12/uv_stage00.json).
- [Docker readiness](../../reports/v12/docker_probe.json), [Kubernetes project policy](../../reports/v12/k8s_static.json), [live preflight block](../../reports/v12/k8s_preflight.json).

A successful example is not a guarantee that all future inputs, mathematics or applications are correct. Preserve the distinction between source integrity, reproducible computation, scientific interpretation, installation, deployment and learner mastery.

[Git-export evidence](../../reports/v12/git_export.json) and [its test log](../../reports/v12/git_export_tests.log). The earlier broad glob matched tracked blank progress templates, not private answers; the corrected check distinguishes templates from active records. No remote repository was modified.
