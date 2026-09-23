# Stage 15 beginner workbook

## Work a corrected depth by hand
For disparity d=40 pixels, use the stated f, B and doffs. Calculate `Z_correct=fB/(40+31.086)` and `Z_wrong=fB/40`. Both are positive and visually plausible; only one uses this calibration convention. Express the relative difference.

## Predict the error pattern
Before inspecting a real error plot, identify likely difficult regions: repeated textures, weak texture, occlusion boundaries and view-dependent appearance. These are hypotheses. Compare a few selected wrong matches to the images and record what the data actually show rather than asserting every failure has the same cause.

## Separate three experiments
The synthetic integer-shift test checks whether your SAD implementation can recover a known correspondence. The real stereo experiment checks reference agreement on one scene. The synthetic calibration/uncertainty calculation checks a mathematical model under chosen assumptions. None can substitute for the others.

## Deep route
Derive DLT rows from projective equality and derive the depth sensitivity. Add focal-length and baseline uncertainty to the Jacobian. Design a held-out physical scale check for a new captured scene, including which references are fitted and which are reserved.

## Three passes

**Understand:** work the hand example and identify an assumption. **Build:** run the worked lab, predict a change, and implement the coding exercises. **Demonstrate:** answer unfamiliar questions without the solutions and return for delayed recall. Passing reference code does not assess your understanding.
