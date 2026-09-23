# Listening to Shape v6 — verification and limits

## Executed evidence

The parent v5 ZIP was integrity-checked before extraction. All 83 inherited reference notebooks and 16 new reference notebooks were then executed again in fresh kernels. Every code cell had outputs cleared before execution. The 39 learner notebooks remain intentionally unexecuted assignments.

| Check | Recorded result |
|---|---:|
| Full Python suite | **432 passed, 2 skipped; zero failures** |
| Reference notebooks | **99 / 99 passed** |
| Executed reference code cells | **571** |
| Embedded PNG outputs | **70** |
| Core stage sections | **31** |
| Parallel industry case sections | **8** |
| Industry normalized snapshots | **8; 4,273 source-format rows** |
| Included observed sources, combined course | **13** |
| Current reader HTML pages checked | **846** |
| Local file-link targets checked | **39,213; zero broken targets at this check** |
| Font files included | **0** |
| Preassessed core stages / industry cases | **0 / 0** |

The exact current file-link count is recalculated in `reports/v6/release_check.json` after the final documentation render; adding local report links can increase it without changing the notebooks. The final archive is separately extracted and tested; delivery details and ZIP hash are supplied in the external final-archive report.

## Evidence files in the ZIP

- `reports/v6/tests_full.txt`: full-suite output, including both named skips.
- `reports/v6/all_notebook_execution.json` and `.log`: all 99 fresh notebook runs, cell counts and timings.
- `reports/v6/release_check.json`: executed-cell checks, normalized/raw hashes, original data integrity, deliberate learner assignments, empty logs and local links.
- `reports/v6/environment.json`: Python and package versions.
- `reports/v6/browser.json`: actual browser rendering/interactions and the navigation limitation.
- `reports/v6/industries/<case>/`: input/protocol identifiers, split tables, preprocessing, predictions, measurements and figures.

The data-loader, exercises and progress features were checked first in failing states and then with implementations; those red/green logs are preserved. A release-version mismatch detected by the full suite was corrected in both package metadata and its matching version assertion; the final suite is green. No independent human or separate-agent review is claimed.

## Concrete outcomes to inspect

**Wine:** On the declared 36-row test partition, ordinary features classify 32 correctly, topology-only summaries 23, and combined features 34; the majority baseline classifies 14. The models share the same supervised fitting rows; a separate fixed training reference set supplies local topology. This is one fixed, now-exposed experiment, not statistical confirmation of a general advantage. See `reports/v6/industries/wine/results.json` and `test_predictions.csv`.

**CO₂:** 2,284 time slots include 2,225 observed values and 59 missing values. The window builder produces 2,022 complete candidate windows; strict raw-block support assigns 1,124 training, 432 validation and 445 test windows, leaving 21 boundary-crossing candidates unused. It never invents observations across gaps. See `window_audit.json` and `split.csv` in that case's report folder.

**Transportation:** 840 alternative rows are grouped into 210 complete four-mode choice sets before evaluation. A person's alternatives cannot appear in different partitions. The model evaluates 42 travelers in each validation/test block. These choice-based sampled proportions are not population market shares.

**Healthcare:** The fixed test split happens to be perfectly classified by the small baseline. That does not establish diagnostic safety, new-site performance or population accuracy; original patient/site identifiers are absent from this teaching export. The lesson explicitly retains these limitations rather than turning a high score into a deployment recommendation.

## What was not verified

**Optional library comparisons:** Ripser and GUDHI are not installed. Their two comparison tests are skipped, not passed; this package does not claim external-library agreement. Their optional dependency group remains available for your environment.

**Platforms:** This execution used Python 3.13.5 on Linux with CPU PyTorch 2.10.0+cpu. Mac, Windows and GPU behavior were not executed here. The setup instructions are included but not described as platform certification.

**Reader navigation:** Chromium successfully rendered the home, data primer, stage page, wide data card and notebook; search filtering, 56-question answer reveal, embedded images and 390-pixel layouts passed. Navigating to a local file URL returned `ERR_BLOCKED_BY_ADMINISTRATOR` in this environment. Static file-target validation is separate from full navigation, which remains unverified. No browser storage synchronization is implemented for the new industry log.

**Acquisition:** The eight required datasets are real offline exports from installed package distributions, not new network downloads. Their official descriptions/licenses were checked on the web. Python download access failed. None of the ten optional larger/restricted datasets was acquired or executed. The exact acquisition/version boundaries appear in the cards and optional catalogue.

**Scientific reach:** Full-paper reproductions, clinical decisions, causal economic or environmental findings, learned metric calibration, trained VGGT inference, unseen athlete validation and physically correct operator rollouts are not established by these experiments. Earlier manufactured examples remain clearly labeled. Unknown units and missing metadata are not filled in by assumption.

**Learning:** Every supplied log starts unassessed. A test passing is evidence about the specified code behavior, not your proof or retention. Scores and independence declarations are self-reported. The actual book has not been completely audited and advanced theorem proofs retain their deeper-reading obligations.

## Reproduce

Follow [Start](START.md), [Reproduce](REPRODUCE.md), and the [source audit](SOURCE_AUDIT.md). The eight new cases require no dataset download and run on CPU. Preserve your own evidence files and progress records before overwriting reference outputs or replacing a course directory.
