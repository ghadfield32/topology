# Which situation am I in?

This is a decision guide, not another lesson series. Each situation points to the canonical concept and tells you what evidence to obtain next.

## 1. I cannot understand the symbols
**Locate the gap:** distinguish a set from an array, a function from its output, and an equality from an assignment. Use the [notation primer](../foundations/00_numbers_symbols_and_types.md), then [Stage 01](stages/01.md). Translate one expression into a sentence before computing. Do not memorize an equation whose inputs you cannot identify.

## 2. I have a spreadsheet of features
**Ask:** what does one row represent, what units do its columns use, and which columns are labels or IDs? Start at [00](stages/00.md), then [02](stages/02.md). Fit any learned scaling on training data only. A length measured in metres is not commensurate with age or a category code just because both are numbers. Compare a simple baseline before a persistence representation.

## 3. My distance behaves strangely
Compute a three-point example. Does symmetry hold? Does the triangle inequality hold? Squared Euclidean distance may be useful in an objective, but it is not generally a metric. Check [02](stages/02.md). Distinguish changing numerical scale from preserving topology, and record how thresholds transform with units.

## 4. I see a loop in a plot
A two-dimensional projection can hide or introduce apparent structure. Specify the ambient observation space, metric, complex, filtration and coefficient field before interpreting a diagram. Use [05–08](stages/05.md). Calculate a square or triangle example first. A graph cycle that is filled by a 2-simplex is a boundary and does not contribute a nonzero H1 class.

## 5. My persistence result disagrees with a library
Check coefficient field, filtration convention, maximum simplex dimension, scale truncation, zero-length intervals and essential classes before changing code. Use [09](stages/09.md) and `tests/test_optional_libraries.py`. Library absence is not agreement. A pipeline that computes H1 must include triangles that can kill 1-cycles.

## 6. My dataset is too large
Start with a documented subset and an exact control. A Rips construction can grow combinatorially; our educational implementation is intentionally small. Subsampling changes the analysis, so preserve the selection rule and rerun sensitivity checks. The [performance stage](stages/18.md) distinguishes data movement, preprocessing, inference and latency. Do not assert that a GPU is the bottleneck before measuring it.

## 7. I have camera images and want metres
Work through [14](stages/14.md), [15](stages/15.md) and [17](stages/17.md). Establish coordinate directions, calibration, scale, timing and visibility. Fit registration using one reference set and evaluate on other measurements. A predicted point cloud, a low reprojection residual, and a true held-out distance error answer different questions. A ground homography does not provide metric locations of airborne objects.

## 8. My tracking has missing or estimated observations
Do not relabel interpolated or extrapolated positions as directly observed. Separate physical elapsed time from frame index and a game clock. Use [19](stages/19.md) and [sports S04](../sports_v8/lessons/S04.md). For live decisions, disallow future frames; report stale-result age and visibility along with any event. Test hard negatives such as a hand passing near a ball without contact.

## 9. I want to predict an athlete's next result
Define the prediction cutoff and independent unit. Keep all data for a held-out athlete, trial or game together as required by the question. Whole-sequence features can leak future information into an earlier-time task. Use [sports S05](../sports_v8/lessons/S05.md) and the [leakage laboratory](../methods_v7/leakage/lesson.md). Do not turn 12 frames from one trial into 12 independent target outcomes.

## 10. I want to combine team totals
Determine the table grain before joining or summing. A player's team rows and season-total row are overlapping summaries. Preserve alias mappings. Rates need numerators and denominators, not a naive sum. Use the [ACB readiness lab](../sports_v9/lesson.md), then test deliberately duplicated records and conflicting IDs.

## 11. A physics-constrained model gives implausible results
Check units, initial/boundary conditions, physical regime, identifiability, time-step size and numerical integration. A soft residual penalty is not a theorem, while one invariant does not establish all of physical validity. Use [21](stages/21.md), [23–26](stages/23.md), and [the source-claim map](../docs/v9/CLAIMS_AND_LIMITS.md). Distinguish measured data from a manufactured example with a known analytic answer.

## 12. The total training loss decreases but a condition gets worse
Inspect each loss and its gradient; compute pairwise inner products before choosing gradient surgery. Opposing nonzero gradients cannot share a strict first-order descent direction. With several losses, sequential operations can change earlier alignments. Use [27](stages/27.md). Repair an incorrect interface condition instead of expecting an optimizer to fix the model's mathematical specification.

## 13. My score improves slightly
Save individual paired predictions. Count successes gained and lost, not only the net change. Check the split, preprocessing and tuning history. Use [11–12](stages/11.md) and the [paired-result session](../sessions/12_session.md). An exposed test set is useful teaching data, not a fresh confirmatory holdout. A small improvement may not justify greater complexity.

## 14. I need uncertainty or deployment acceptance
Specify the population, independent unit, data-generating assumptions, and decision cost. Marginal coverage is not a guarantee for a particular person, mixture or future domain. Use the [concrete lesson](../applications_v7/concrete_slump/lesson.md), [10](stages/10.md), and [30](stages/30.md). Validate on relevant independent measurements before operational use. The course's small examples do not certify clinical, safety-critical or professional sports deployment.

## 15. I cannot run the notebook
Use `python scripts/course.py doctor`, then run the stage's entry check. Read the first actual traceback. Missing dependency, changed input, predecessor failure and a mathematical assertion are different problems. `run --stage` rebuilds declared artifact dependencies in a fresh workspace. Use a new output directory rather than overwriting the evidence that explains the failure. A skipped optional library remains untested.

## 16. I have finished a stage but keep forgetting it
Do a changed problem with notes closed; explain a nonexample and an assumption. Record the exact misconception. Re-read only the relevant subsection, then repeat a different problem later. The progress log stores your declaration and evidence hash, not an independent certification of mastery.
