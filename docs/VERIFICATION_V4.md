# Verification report — Listening to Shape Learning System v4

Release: 4.0.0. Build date: September 20, 2026. This report describes the current package; versioned earlier reports are historical.

## Executed checks

| Check | Result |
|---|---|
| Original v3 baseline before changes | 231 passed, 2 optional-library skips |
| Final Python suite | 296 passed, 2 optional-library skips, 0 failed |
| Original worked labs re-executed | 21 of 21 |
| Reference coding-answer notebooks re-executed | 21 of 21 |
| New consolidation notebooks executed | 21 of 21 |
| Total executed reference notebooks | 63 |
| Executed reference code cells | 381 |
| Embedded figures in these reference outputs | 41 |
| Intentionally unexecuted learner notebooks | 21 |
| Explicit stage outcomes | 84 |
| Concept questions / additional transfer questions | 150 / 42 |
| Coding assignments / delayed-recall questions | 89 / 63 |
| Data snapshots with provenance | 4 |
| HTML pages checked | 661 |
| Existing local file-link targets checked | 28400 |
| Broken local file-link targets | 0 |
| Font files distributed | 0 |
| Learner stages assessed by the package | 0 |

The link checker verifies destination files, not every fragment anchor or live external URL. The original 21 learner notebooks contain intentional assignment placeholders. They were not executed as reference notebooks, and are not counted among the 63 successful references. The 41 embedded figures include reference outputs; duplicate rendered copies are not counted as new experiments.

## What is independently checked

The new checks compare planar closed-pixel connectivity/Euler counting with boundary-based homology, compare dense-Prim H0 merge times with the main reduction procedure, and verify signed boundary identities and coefficient-dependent small chain examples. They add different computational routes within this course. They are not a substitute for external-library agreement or a proof of every theorem.

Tests also cover malformed inputs, exact fixtures, prime-field arithmetic, duplicate point handling, paired comparison calculations, evidence integrity, notebook syntax, metadata coverage and read-only navigation. Navigator tests use temporary logs, so ordinary assessment entries do not make those tests fail.

The final code suite output is in `reports/v4_tests_final.txt`; execution records are `reports/notebook_execution.json`, `practice_execution.json`, and `consolidation_execution_v4.json`. Current structural counts are in `reports/v4_content_checks.json`. Release-only checks require a clean shipped learner state and should not be confused with normal unit tests after you start studying.

## Optional libraries and unexecuted model work

Ripser and GUDHI were not available in the execution environment. An installation attempt returned no matching distribution from the available package index. The two optional comparisons remain explicitly skipped. They are not counted as passed and no external-library numerical agreement is claimed. Installation diagnostics were retained rather than replacing real output with a fabricated comparison.

No trained VGGT or VGGT-Omega inference was executed. The inherited optional runner and synthetic contract fixtures remain educational preparation, not a measured model benchmark. No camera deployment, physical holdout collection, real sports-event annotation study, or WMS production modification was performed.

## Runtime and browser scope

The executed environment is Linux with Python 3.13.5. Exact package versions are in `reports/environment_v4.json`; they are pinned for this course rather than claimed as the latest public versions. Statsmodels 0.14.6 was used to export the historical sunspot table and is not required to run the bundled CSV labs. Mac and Windows setup instructions were supplied but not executed on those operating systems.

Chromium rendering checks passed for the 21-card home, the 42-question transfer filter and answer reveal, the 63 delayed-recall cards, an embedded new real-data figure, and 390-pixel layouts for the home, homology session and transfer page. Browser JavaScript errors: none in the final render/interaction check. Actual file navigation was blocked by the environment (`ERR_BLOCKED_BY_ADMINISTRATOR`), so full click-through navigation is not claimed. The fallback renders actual HTML with the same CSS inlined; see `reports/browser_v4.json`.

## Real-data result and its interpretation

On the existing exposed 360-image handwriting partition, pixel features gave 347 correct predictions and the combined representation gave 351. Paired outcomes were 344 both correct, 6 both wrong, 7 newly correct and 3 newly wrong. The gain is 4 images, or 1.111 percentage points.

The new exploratory exact discordance calculation returns p = 0.34375. The 4,000-resample paired percentile interval for the accuracy difference, with seed 2026, is approximately -0.556 to 2.778 percentage points. These quantities assume image-level resampling/independence and condition on fixed fitted predictions. Writer identifiers are unavailable. No model-selection, repeated-testing or unseen-writer guarantee follows. This is not a new confirmatory holdout.

The new time-series dataset contains 309 historical annual observations from 1700–2008, with actual bytes and provenance bundled. Teaching threshold episodes are not independently annotated solar events or basketball events. Controlled camera perturbations and known registration targets remain synthetic even when applied to real scene-point arrangements.

## Problems found and corrected during the build

The initial test-first run failed because new functions and navigation were absent. A generated Stage 06 consolidation print statement had a malformed newline; notebook compilation tests exposed it and the source was corrected before successful execution. The release checker was adjusted to transform legitimate IPython notebook magics before Python compilation. Reader search code was put inside a function scope after repeated-document rendering exposed top-level variable redeclaration. These are recorded fixes, not evidence that every possible defect has been excluded.

The course was self-reviewed against its structure and explicit claims. No independent human or separate-model review is claimed. The tests provide reproducible evidence, not an absolute guarantee of mathematical completeness.

## Release and learning boundaries

The final delivery includes a SHA-256 file inventory and an external ZIP checksum. The archive is checked after extraction into a separate directory; the separately delivered final archive-check JSON records that fresh result and its ZIP hash. The checksum proves byte identity, not correctness of the content.

The full book text was not audited. All earlier supplied section-title mappings remain in the book audit with `verified_full_book=false`. Major theorem proofs and independent capstones have explicit deeper-study obligations. No learner assessments are pre-filled. Preserve your own evidence and compatible v3 log when upgrading; the package version does not reset your learning history.
