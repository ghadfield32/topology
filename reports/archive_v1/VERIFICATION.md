# Verification evidence and remaining limits

This page separates what was actually executed from what remains a learning task or an unexecuted optional check. Build environment: CPython 3.13.5 on Linux. See `reports/environment.json` for the complete platform record and selected dependency closure.

## Executed results

| Check | Recorded result | What it establishes |
|---|---|---|
| Full Python test suite | **79 passed, 2 skipped, 0 failed** | The declared checks pass in the recorded environment. |
| Core notebooks | **13 of 13 executed successfully** | Stages 00–12 run in fresh kernels, with no code-cell errors. |
| Executed code cells | **46** | Every included code cell has an execution count and saved output where applicable. |
| Saved figures | **21 PNG files** | Inspectable plots created by the executed labs. |
| Original stage exercises | **102, with 102 worked solutions** | Teaching material exists; this does not imply learner completion. |
| Fixed-grid stability experiment | **20 of 20 bounded perturbation checks passed** | The specified finite H₁ diagram distances obey the applicable measured uniform-change bound on the selected examples. |
| Data integrity | Hash, schema, split coverage and disjointness tests passed | Included observations and partitions match the declared manifest. |
| External Ripser / GUDHI checks | **NOT RUN: both optional imports unavailable** | No external-library agreement is claimed. |
| Actual book text coverage | **Not audited** | Alignment is to the supplied table of contents and staged outline, not the complete text. |

The final test command was `python -m pytest -q -ra --junitxml=reports/pytest.xml`. The text and machine-readable results are saved in `reports/pytest.txt` and `reports/pytest.xml`. `reports/notebook_execution.json` records each notebook's execution. `reports/REFERENCE_RESULTS.json` preserves a summary of the build's actual results.

## The checks test different things

The suite includes exact homology examples, face closure, boundary-of-boundary, rank arithmetic over F₂, the Euler–Poincaré identity, valid filtration ordering, known persistence intervals, coordinate/permutation invariance, truncated-filtration behavior, diagonal matching, and finite-topology examples.

It also checks persistence pairings through an induced-map rank computation at pairs of filtration thresholds, rather than comparing only a sequence of Betti numbers. Small bottleneck cases are compared against exhaustive assignments. The independent-check guide states where code is shared; these checks are complementary evidence, not complete independent certification.

A special check distinguishes the graph of a square from its filled clique complex. Another distinguishes a boundary triangle from a filled triangle. A pixel ring tests an image hole without relying on subjective interpretation of handwriting.

## The real-data capstone result

The completed teaching experiment selected regularization using 1,077 training and 360 validation images, refitted using those 1,437 development images, and evaluated the declared 360-image test partition.

| Representation | Correct test images | Image-level test accuracy |
|---|---:|---:|
| Pixels | 347 / 360 | 96.39% |
| Topological descriptors | 168 / 360 | 46.67% |
| Pixels + topological descriptors | 351 / 360 | 97.50% |
| Majority-class baseline | 36 / 360 | 10.00% |

These are the actual saved results, not target values chosen in advance. The combined representation classified four more images correctly than the pixel-only representation on this one partition. That is not a demonstrated general improvement, a statistical-significance result, or an unseen-writer evaluation. Writer identifiers are absent from the bundled snapshot.

The test results are now exposed. Rerunning this lesson reproduces the worked experiment; it does not provide a fresh independent holdout. For an independent project, freeze a new protocol and use genuinely unexamined data or a justified evaluation design.

Per-image predictions, classification reports and the confusion matrix are under `reports/stage_12/`. The model-selection record is under `reports/stage_11/`.

## What was not executed or independently certified

The build container could not download optional dependencies. The provided Ripser and GUDHI comparison tests therefore remain visibly skipped. The GUDHI alpha demonstration is supplied as an optional script and is not part of the executed notebook count. Run these locally to finish that external comparison gate; investigate mismatches rather than deleting the checks.

The code was not executed on macOS or Windows. Platform-specific setup instructions are supplied, but those are not a claim of validated installation on every OS. The direct package pins and installed Linux dependency snapshot are not a universal cross-platform lockfile.

There was no separate independent reviewer and no formal proof-assistant verification. Definitions, hand derivations, counterexamples, tests and primary reading references provide reviewable evidence; none is presented as a guarantee of correctness on all possible inputs.

No real sports/biomechanics dataset is included or claimed to have been evaluated. The sports and computer-vision project guides are transfer proposals. No production WMS system was changed.

## Historical failing-test logs

`reports/tdd_initial_red.txt`, `reports/tdd_persistence_red.txt` and `reports/tdd_features_red.txt` record intentionally failing tests before the corresponding implementation existed. They document development history; they are not unresolved failures in the final suite. The latest complete suite result is `reports/pytest.txt`.

## Learning completion is a separate decision

`progress/learner_progress.json` deliberately starts with all stages unassessed. Run the notebooks, solve the exercises independently, explain the results, pass the cumulative assessment, and revisit unfamiliar problems after a delay. Inspect the proof-depth guide for major theorems requiring fuller external reading. When the actual book text becomes available, perform the chapter-specific gap audit instead of assuming equivalence.

## Reader and packaging checks

The reader was rendered in Chromium at desktop and mobile widths. Stage navigation elements, decoded saved figures, exercise filtering/reveal, and in-memory manual progress updates were checked. No JavaScript page errors were observed. The container's browser policy blocked direct file and localhost navigation, so visual/interaction checks used the same authored HTML and CSS in memory. Local-file storage persistence and download-export behavior remain unverified on a normal browser origin; the interface handles unavailable storage and provides export instructions.

The release checker verifies local HTML targets, notebook validity, absence of saved cell errors, untouched learner status, and required per-stage artifacts. Archive integrity and an extracted-copy test run are recorded separately. Initial package installation was checked as an editable install against the existing tested runtime with dependency downloads disabled; that is not a clean installation on a new machine.
