# Verification — Listening to Shape Learning System 3.0

Build date: **2026-09-20**. This report separates executed demonstrations, learner state, source review and unexecuted work.

## Executed reference evidence

| Check | Result |
|---|---|
| Python test suite | **231 passed, 2 skipped, 0 failed** |
| Reference lab notebooks | **21 executed successfully** |
| Reference coding-answer notebooks | **21 executed successfully** |
| Total executed reference code cells | **276** |
| Learner starter notebooks | **21 deliberately unexecuted** |
| Stage analytical figures | **38** |
| Conceptual exercises and solutions | **150 pairs** |
| Independent coding activities with reference checks | **89** |
| Delayed-recall questions | **63** |
| Foundation primers | **6** |
| Default learner assessments recorded | **0** |

Test output is in `reports/pytest_v3.txt`. Notebook execution records are in `reports/notebook_execution.json` and `reports/practice_execution.json`; the executed notebooks retain outputs. The 24 new coding activities each run independently in the test suite. The original 65 reference activities remain included and executed.

The two skipped tests require **Ripser and GUDHI**, which were unavailable. No agreement with those libraries is claimed. The geometry tests do compare rotation calculations with local SciPy and triangulation with locally installed OpenCV. On a machine lacking optional OpenCV, its explicitly optional check may also skip; inspect your own test summary.

A shell execution timeout interrupted an early batch; those notebooks were rerun successfully in smaller batches. The report reflects the final completed runs, not the interrupted attempt. An initial notebook argument-order mismatch was corrected before final execution.

## Real data and measured outputs

The required course includes Iris, handwritten digits and a real rectified Middlebury motorcycle stereo pair supplied through local scikit-image data. The stereo reference has shape 500×741 with **343,274 finite disparity entries**. Nonfinite data are retained in the raw archive and explicitly excluded from calculations. Dataset source/shape/calibration discrepancies and licenses are documented in `data/stereo/README.md`, `manifest.json` and the source ledger.

The independent integer-SAD stereo demonstration evaluates **441 eligible reference pixels from 480 fixed requests**. Every eligible pixel receives a prediction: **100% coverage among eligible references**. Mean absolute disparity error is **6.6288 pixels**, median absolute error **0.4946 pixels**, and **31.07%** exceed the declared two-pixel threshold. These errors are not hidden by a favorable median. Reference-depth MAE is **0.2629 m**. The deliberately incorrect no-offset formula produces a **76.03% median relative depth error** on its defined comparison subset. See `reports/stage_15/results.json` and the saved source-aligned prediction archive.

The DLT/stereo-formula agreement is a consistency check using the same supplied reference/calibration, not two independent metric truths. The calibration fit, uncertainty perturbations, synchronization example, imposed registration transforms and temporal event sequences are explicitly generated controls. The actual measured CPU vectorization timing applies only to this environment. FIFO queue ages are simulated, not measured camera-to-display latencies.

The original exposed handwriting capstone reproduces its declared results: 347/360 correct with pixels, 168/360 with topology-only features, 351/360 combined and 36/360 majority baseline. These are demonstration results, not new statistically established improvements or unseen-writer evidence.

## Reader verification

Static checks inspected **363 HTML pages and 14,393 local link targets**, with no broken local targets. The checks verify paths, not the continuing availability of every external resource. No font files are bundled.

Chromium rendered the actual home/recall/notebook markup with the same CSS inlined. It verified 21 home stage cards, a Stage 00 link, filtering 63 recall cards to a single query, answer reveal, all five embedded stereo plots, and no horizontal home-page overflow at a 390-pixel viewport. No JavaScript page errors occurred during those checks.

**Local file navigation was blocked by the build environment's browser policy.** Full click-through navigation in a normal user's browser was not executed. Rendering and interaction tests are therefore reported separately from navigation; static link checking is not a substitute for full browser navigation. No browser-storage synchronization is claimed. `reports/browser_v3.json` retains this limitation.

## Model status

**Neither original VGGT nor VGGT-Omega trained inference was executed.** No checkpoint, model repository or weights are bundled. The optional original-VGGT adapter was source-reviewed, syntax-compiled and help-tested. Its output contract and small point sampler are tested using **synthetic arrays labeled as contract fixtures**, not as neural-network predictions.

The adapter records a local code revision, checkpoint/input hashes, preprocessing, coordinate/scale status, optional 2D tracks, device precision and synchronized GPU timing when the user actually runs it. It never marks the resulting geometry as validated metres. Raw-to-processed pixel mapping and registration/holdout validation remain explicit future checks. The original-model adapter does not silently accept Omega's different API.

## Source and scope status

Primary sources were checked on September 20, 2026. The source audit preserves two discrepancies: Omega's project page dates the training/reproduction update September 18 while its README says September 8; the stereo documentation's disparity shape differs from the actual two-dimensional array. No invented reconciliation is supplied.

Real hand–ball event labels, sports-event precision/recall, independent physical scene holdouts, rolling-shutter/fisheye validation, clinical suitability and WMS production deployment are **not established**. The attached source's reported timing figures and prior watch updates are contextual source claims, not work executed here. No production code or scheduled watch was modified.

The package contains an original curriculum for the agreed introductory scope and an applied continuation. It is not the complete book text. Its full-book audit remains false/unassessed. Elementary proofs are supplied; major theorem proof obligations and deeper topics are stated explicitly rather than certified through examples alone.

## Environment and portability

Executed on **Linux x86-64, Python 3.13.5**. Core packages: NumPy 2.3.5, SciPy 1.17.0, pandas 2.2.3, matplotlib 3.10.8, scikit-learn 1.8.0; pytest 9.0.2. Full values are in `reports/environment_v3.json`. Mac/Windows instructions are provided but those systems were not executed. Required labs are CPU-only and use bundled data; first dependency installation requires internet or a cache.

## Archive verification

The delivered archive is tested for ZIP integrity and verified against its internal SHA-256 file inventory. The final extracted-copy test result is saved separately in `reports/extracted_verification_v3.json`. This is a fresh-path package test; it is not a claim to have repeated all model or notebook work on a second operating system.
