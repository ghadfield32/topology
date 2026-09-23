# Verification — Listening to Shape Learning System 2.0

Verified in the local Linux Python 3.13.5 environment on September 20, 2026. These checks describe this release, not universal correctness or learner mastery. Original version-1 records are preserved under `reports/archive_v1/`.

## Freshly executed evidence

| Check | Result |
|---|---|
| Full test suite | **171 passed; 2 optional skips; 0 failures** |
| Original worked notebooks | **13/13 successfully rerun**, fresh kernel per notebook |
| New reference-answer notebooks | **13/13 executed**, fresh kernel per notebook |
| Executed reference code cells | **189**, no saved error outputs |
| Learner notebook templates | **13**, with 65 explicit unfinished coding assignments; not counted as passed |
| Reference coding activity checks | **65/65**, also exercised in the test suite |
| Fixed-grid finite H1 perturbation checks | **20/20** satisfied their stated numerical bound |
| Saved analytical figures | **22**: 21 core lab figures and one seeded real-CSV diagram |
| Separate extracted candidate suite | **171 passed; 2 optional skips** |
| Stage/content/schema checks | Passed for all 13 stages |
| Learner stages pre-assessed | **0** |
| Actual book sections audited | **0**; 24 supplied section titles have a pending audit inventory |

Test logs: `reports/pytest.txt`, `reports/pytest.xml`, `reports/extracted_copy_tests.txt`. Notebook records: `reports/notebook_execution.json`, `reports/practice_execution.json`. Current content inventory: `reports/v2_content_checks.json`. Combined machine-readable report: `reports/v2_release.json`.

The first large notebook batch exceeded a host tool time limit while beginning Stage 11. That kernel was interrupted; Stage 11 and Stage 12 were then rerun successfully in a separate batch. The final records reflect successful executions, not an ignored failure. The educational starter functions intentionally raise NotImplementedError until completed; the ordinary test suite permits learners to edit them.

## Reader and package checks

The static checker inspected **138 HTML pages and 4,861 local link targets**, with no broken file targets. It verifies target files, not every in-document anchor or external website. No font files are distributed.

Eight representative documents were rendered in Chromium using their actual HTML and bundled stylesheet loaded in memory. The home, stage hub, homology workbook, coding answers, notation table, recall page, learning guide and capstone rendered successfully. Details expansion and a mobile-width home layout were checked; no document-level horizontal overflow was observed on that mobile home view.

**Browser limit:** this environment blocked local HTTP navigation with `ERR_BLOCKED_BY_ADMINISTRATOR`. The in-memory check does not establish file-origin navigation, downloadable-link behavior, or persistent browser storage. Static file links were checked independently. The legacy browser scratchpad is not the durable v2 log; it does not synchronize with the CLI. See `reports/browser_checks.json`.

The ZIP is distributed with `MANIFEST.sha256` for its included files. Final archive integrity and checksum verification are performed after packaging; those checks establish byte consistency, not authorship or mathematical truth.

## Optional comparisons that are NOT passed

Ripser and GUDHI were not installed. An installation attempt did not obtain available distributions in this environment. Both comparison tests are skipped and the optional alpha-complex demonstration remains unexecuted. Run the README's optional commands locally to complete this independent-validation gate. The core calculations have hand-derived fixtures, invariants and other checks, but those are not a substitute claim of agreement with these libraries.

## Reproduced real-data result

The already-declared 360-image demonstration test split gives:

| Representation | Correct | Accuracy |
|---|---:|---:|
| Pixels | 347/360 | 96.39% |
| Topology descriptors | 168/360 | 46.67% |
| Pixels + topology | 351/360 | 97.50% |
| Majority label | 36/360 | 10.00% |

The four-image difference between combined and pixel features is not asserted statistically significant. Writer identifiers are absent, so this is not an unseen-writer evaluation. Test labels and results are now exposed; rerunning is reproduction, not a new independent test. Predictions, chosen regularization settings and experiment contract are saved under `reports/stage_12/`.

The own-CSV example uses 20 seed-selected Iris rows with explicit measurement columns and Euclidean units. Its report records source hash, sample positions, field, simplex dimension and diagrams. It is exploratory only; no population-topology recovery or predictive improvement is claimed.

## Scope and reproducibility limits

The archive contains original instruction aligned to the supplied topic outline. It is not the actual book, not endorsed by the author, and not exhaustive coverage of all topology. The proof atlas distinguishes complete elementary arguments from substantial theorems whose full proofs remain deeper-reading obligations. No proof assistant or independent human reviewer certified these explanations.

The numerical environment and 99 installed dependency records are saved in `reports/environment.json` and `reports/tested_dependency_snapshot.txt`. Direct dependencies are pinned. This is not a cross-platform lockfile or a clean internet-install test. Windows and macOS instructions are supplied, but only Linux execution was tested. The included small examples do not require GPU code.

The learning log stores self-reported grades, dates and evidence hashes. Its rules separate practice, independent demonstration and delayed recall. It does not automatically judge mathematical correctness, schedule notifications, or certify permanent retention. All distributed learner histories remain empty.

## Reproduce the checks

From the extracted course root, after installing the documented environment:

```bash
python -m pytest -q -ra
python scripts/run_notebooks.py
python scripts/run_practice_answers.py
python scripts/build_reader_v2.py
python scripts/check_package.py
```

`python scripts/check_release_v2.py` is a **shipping-state check**, not an everyday learner command: it expects untouched templates and an empty distributed log. Once you begin your own work, that release-only check should no longer claim pristine learner state. Ordinary pytest and package checks remain the normal software checks.
