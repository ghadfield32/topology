# Stage 14 beginner workbook

## Hand example
Let R be a 90-degree turn about z and t=(1,0,0). Then p=(1,0,0) becomes (1,1,0). Recover p using `Rᵀ(p_B-t)`. Compare to the incorrect expression `Rᵀp_B-t` and identify the missing frame conversion.

For f=800 pixels, principal point (320,240), and p=(0.2,0.1,2) metres, the pixel is (400,280). The point (0.4,0.2,4) produces the same pixel. Optical depth is 2 in the first case; radial range is sqrt(4.05), not 2.

## Real-data experiment
Load the calibrated stereo sample, create a sparse reference cloud, transform it to a made-up lab frame, and invert the transform. A small residual proves numerical consistency of those operations. It does not independently establish that the benchmark's calibration is physically exact.

## Debugging challenge
Swap u and v in backprojection. The array still has a valid shape, but reprojection no longer matches source pixels. This is a semantic error that a shape-only assertion cannot catch.

## Deep route
Prove that composing two proper rotations gives a proper rotation. Derive the homogeneous inverse. Show that Euclidean pairwise distances are preserved by a rigid transform, and predict what should happen to a Rips persistence diagram. Explain why this invariance says nothing about whether a particular world frame has correct metre scale.

## Three passes

**Understand:** work the hand example and identify an assumption. **Build:** run the worked lab, predict a change, and implement the coding exercises. **Demonstrate:** answer unfamiliar questions without the solutions and return for delayed recall. Passing reference code does not assess your understanding.
