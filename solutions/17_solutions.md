# Stage 17 conceptual solutions

Attempt the lesson questions first. These are answer criteria, not scores assigned to your work.

## 1. What information is needed before fitting a similarity transform?

Known paired coordinates, consistent units/status, enough non-collinear anchors, a declared proper-rotation model, and a split separating fit and evaluation evidence.

## 2. Why do collinear anchors fail to constrain all orientation freedom?

Rotating around the anchor line can leave every anchor unchanged. Additional off-line information is needed.

## 3. Distinguish registration residual from held-out measurement error.

The residual is evaluated on data used to choose the transform. A held-out error uses references that did not influence that fit or its parameter selection.

## 4. How do translation, rotation and uniform scaling affect a Rips filtration?

Rigid transforms preserve all pairwise distances, hence the distance-based filtration. Uniform positive scaling multiplies thresholds and finite barcode coordinates by the same factor.

## 5. Why can a reconstructed hole be an observation failure rather than a physical hole?

Visibility gaps, invalid depth, sampling and masks can remove observations. A hole in a sampled representation need not be an opening in the true object.

## 6. What does this stage prove, and what does it not prove about VGGT?

It checks an imposed similarity, held-out synthetic perturbations and distance-based invariance on real-shaped data. No VGGT predictions were produced by this stage, so it proves no VGGT benchmark performance.
