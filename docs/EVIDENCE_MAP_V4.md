# Data and evidence map — v4

“Real data in every stage” does not mean that every mathematical claim is an empirical discovery. Some stages use real observations to illustrate a concept and exact or generated controls to test it. The role is recorded in every consolidation report.

| Stage | Input and evidence role |
|---|---|
| 00 | Real Iris measurements; the three-number mean is an explicitly constructed arithmetic example. |
| 01 | Real training digit intensities plus an exact, constructed three-by-three matrix. |
| 02 | Real Iris measurements, plus the exact counterexample 0,1,2. |
| 03 | Exact finite topology plus a noninjective projection demonstrated on actual Iris records. |
| 04 | Real digit under exact array transformations; constructed matrices and annulus radii. |
| 05 | Real training digit foreground; exact ring and diagonal-pair controls. |
| 06 | Real training digit threshold sweep; exact oriented simplicial and specified cellular-chain controls. |
| 07 | Real Iris point sample; exact equilateral-triangle scale derivation. |
| 08 | Real digit intensity filtration and an exact complete/truncated square control. |
| 09 | Real Iris cloud with a deliberately duplicated observation and a deterministic permutation control. |
| 10 | Real training image plus explicitly generated bounded perturbations; not repeated sensor observations. |
| 11 | Real train/validation digit pixels and the bundled historical annual sunspot series; no new forecast claim. |
| 12 | Actual saved handwriting predictions from an already-exposed image-level holdout; exploratory analysis only. |
| 13 | Real stereo-reference directions mapped onto a constructed unit sphere; not a spherical scene claim. |
| 14 | Real calibrated stereo-reference points plus a hand-checkable pinhole control. |
| 15 | Real stereo-reference disparities with generated local noise; no independent calibration-noise measurement. |
| 16 | Real stereo-image patches processed by an explicitly untrained attention operator; no VGGT predictions. |
| 17 | Real reference point arrangement; target transforms and held-out deformations are generated controls. |
| 18 | Real reference point table for measured CPU operations; separate deterministic FIFO simulation. |
| 19 | Real historical annual observations for causal timing; no human-contact or scientific solar-event ground truth. |
| 20 | Actual bundled dataset bytes and executed reference reports; learner and deployment claims remain separate. |

## Four bundled datasets
Iris is a corrected scikit-learn measurement snapshot; labels and identifiers are excluded from selected measurement metrics. Digit images are a scikit-learn snapshot without writer identifiers; the declared image-level test partition is exposed. Stereo images and reference disparity are one Middlebury scene as bundled by scikit-image, not a new multi-scene model benchmark. The sunspot series is a historical annual statsmodels export, not latest solar measurements or a labeled event dataset.

## Limits on cross-stage transfer
A successful round trip verifies consistency of the formulas being used. It does not show that camera calibration was measured correctly. Known transforms applied to real point arrangements generate synthetic targets. Threshold episodes on a real time series are defined by our teaching rule; they are not independent ground-truth annotations. A stable descriptor can be consistently unhelpful. These distinctions travel with the notebook outputs.
