# Stage 17 — Register, validate, and ask topology the right question

Frame agreement is necessary; it is not independent physical truth.

**Track:** applied geometry continuation, not a claimed chapter of the book. **Prerequisites:** Stage 06, Stage 07, Stage 08, Stage 10, Stage 15, Stage 16.

## 1. Registration aligns descriptions
Two reconstructions may differ by a global rotation, translation and scale. A similarity transform writes `y=sRx+t`, with s positive and R a proper rotation. Finding these parameters from paired landmarks is registration. It does not repair every local shape error and does not discover correct point correspondences on its own.

Our fit first subtracts the point-set means. It uses a singular-value decomposition of a cross-covariance matrix to determine the proper rotation, then solves for scale and translation. Reflection is explicitly excluded. Non-collinear paired anchors are required in this educational implementation. Collinear anchors leave rotation around the line unconstrained.

## 2. Fit and evaluate on different evidence
Choose registration anchors before assessing the held-out error. Fit only to those anchors. Apply the same fitted transform to the remaining correspondences. If you fit to every point and report its fit residual as “held-out accuracy,” the label is wrong even when the residual is small.

The real-data lab creates a known transformed version of the benchmark-derived cloud, fits on one subset, and checks the remaining subset. It verifies recovery of an imposed coordinate change on real-shaped data. Because we imposed the transformation, it is not a measurement of VGGT quality. A second controlled experiment perturbs only unregistered points to demonstrate why a perfect anchor fit can hide local errors.

## 3. There are several kinds of error
A paired-point error compares corresponding 3D coordinates. A distance error compares lengths between specified landmarks. A camera rotation error compares orientations. Reprojection error compares predicted pixels against observed pixels. Completeness asks what valid support remains. Scale consistency asks whether metric scale stays appropriate across views or independent subsets.

These metrics answer different questions. A nearest-neighbour cloud distance can be low even with incorrect identities, missing regions, or surfaces shifted onto a nearby structure. Rigid alignment can remove an arbitrary pose difference but must not be used to conceal a calibration requirement that the experiment intended to test.

Our lesson does not set a universal “good enough” threshold. Acceptance thresholds must come from the application's measurement needs and be specified before the final evaluation.

## 4. What topology contributes
Persistent homology describes the shape of a chosen complex or filtration. It does not determine which point is a hand, which loop is a basketball rim, or whether coordinates are physically accurate. A Rips diagram uses metric distances; rigid transforms preserve them, positive scaling rescales its filtration coordinates, and local warping can change them.

The notebook checks this on a small, fixed sample of the real cloud. It uses the existing course implementation and a deliberately small sample rather than constructing an enormous Rips complex. That is a controlled mathematical diagnostic, not a complete reconstruction-quality score.

A cloud can have convincing topology while being badly stretched. Conversely, removing unseen or invalid points can change a diagram without proving a physical structure appeared or disappeared. Before interpretation, state the sampling, mask, metric, coefficients, maximum simplex dimension and scale interval.

## 5. A reconstruction hole is not automatically a physical hole
Imagine a camera misses a patch of a wall. A hole in the observed sample may reflect occlusion rather than an opening in the wall. Additional views may fill it. If a method inpaints the area, a visually closed surface is a model-generated hypothesis. Label observed, inferred and unavailable regions differently.

Do not let a descriptor retroactively promote inferred pixels into observed evidence. The reconstruction should retain source IDs and confidence/visibility metadata so you can inspect where a claimed structure came from.

## 6. A useful paired acceptance protocol
For a future captured scene, choose independent measured landmarks, reserve some for evaluation, and keep the original image evidence. Compare a classical calibrated baseline, a registered learned proposal, and any refinement initialized by the proposal. Save all variants. Match sampling and masks for a fair comparison, and report coverage changes explicitly.

A result can be useful without replacing the authoritative calibration. It can initialize optimization, suggest correspondences, expose missing views or prioritize review. The output should enter the existing state only under its allowed evidence status.

## 7. What remains outside this lab
There is no new human-subject capture, independently measured basketball scene, or executed VGGT checkpoint in the reference notebook. The code establishes registration and invariance behaviour. The capstone protocol makes the missing external measurement work concrete rather than pretending it happened.

## Independent conceptual exercises

1. What information is needed before fitting a similarity transform?
2. Why do collinear anchors fail to constrain all orientation freedom?
3. Distinguish registration residual from held-out measurement error.
4. How do translation, rotation and uniform scaling affect a Rips filtration?
5. Why can a reconstructed hole be an observation failure rather than a physical hole?
6. What does this stage prove, and what does it not prove about VGGT?

## Mastery gate

Defend the fit/evaluation split and distinguish metric evidence from topology diagnostics.

Readings: G06, D04, T01. See the [source ledger](../docs/SOURCES_V3.md) for checked links, evidence status and source differences.
