# Independent spatial capstone

## Choose one question, not an entire application
A suitable first question is whether a candidate reconstruction improves held-out static-scene measurement error at a declared coverage threshold compared with a calibrated baseline. A different question is whether TDA detects intentionally introduced reconstruction defects beyond ordinary geometric residuals. Do not combine pose estimation, release detection, forecasting and deployment into one undiagnosable acceptance test.

## Define the observation and target
Specify one observation (pixel, correspondence, point, view, scene or event), its source ID, coordinate frame, unit, timestamp, uncertainty meaning and reference source. Define the target population: your captured static rooms, one camera configuration, or a specified set of sports sessions. A single motorcycle scene is a demonstration, not that population.

## Freeze the split and the measurement contract
Assign scene/session IDs to development and final evaluation before selecting parameters. Within a scene, reserve measurement references from registration and refinement. Do not fit scale on the same distances used to claim accuracy. Nearby points within one scene are not independent scenes. Record any calibration uncertainty of the reference itself.

Write down in advance the baseline, candidate, units, eligible observations, rejection rules, coverage denominator and error convention. Use separate camera orientation, position, reprojection, held-out length, completeness and timing metrics where they answer different questions. Set thresholds based on the intended measurement need, not after seeing the answer.

## Preserve a minimum reproducible run
The run record needs: input hashes/order; dataset permission; raw and processed image sizes; pixel mapping; exact code commit; dependency versions; checkpoint filename/hash/license; camera convention; inference precision; point-selection rules; fit-anchor IDs; holdout IDs; random seeds; actual timing boundaries; and all rejected/missing observations. Store generated controls in a different namespace from real annotations.

## Analyze one intervention at a time
Compare calibrated baseline, candidate, and optionally candidate-initialized refinement. Change one factor—image count, resolution, synchronization, mask, confidence selection or sampling—while preserving others. Refit only on the allowed development evidence. Report failure cases and coverage with every error summary. Do not silently drop challenging frames after seeing their residuals.

## Add TDA only with a specific question
A finite point cloud has a topology induced by its chosen metric; an inferred shape needs an explicit complex and filtration. Declare coefficients, maximal simplex dimension, filtration scale units and truncation. On a small fixed-ID sample, test invariance to rigid frame changes and expected scaling. Then compare a topological descriptor with ordinary geometry baselines. Similar topology alone cannot establish metric calibration correctness.

## Live events require a different dataset
A static reconstruction dataset has no basketball-event ground truth. Obtain appropriate permissions and independently annotate onset, offset, identity, visibility and uncertainty in sports clips. Include no-contact proximity, crossing identities, brief occlusion, repeated interactions and truncated clips. Evaluate past-only detection separately from offline smoothing. Match events one-to-one under a predeclared tolerance and report decision delay separately from onset error.

## Your report must support a negative result
Write a one-page question/protocol before the experiment, then a reproducible results report with baselines, all eligibility counts, sensitivity results and limitations. A result that the method adds no value is a valid completion. Do not automatically deploy a method because a notebook ran or a plot looks plausible.

## Oral defense questions
Why is the chosen metric appropriate? What changes under rescaling? Which observations were used to fit the world frame? What did the confidence score actually mean? What can the reference fail to measure? How was missing evidence handled? What result would reject your interpretation? Which other scenes remain untested?

## Completion record
Keep a completed protocol, source manifest, untouched evaluation-ID list, run log, predictions, reference-aligned evaluation, tests and your explanation in `my_work/capstone_spatial/`. Record an assessment only after this evidence is reviewed. The included worked notebooks are practice evidence, not an independent final capstone.
