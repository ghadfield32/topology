# Stage 15 — Measured stereo, calibration, and uncertainty

Use two images to estimate depth, then test what the estimate really supports.

**Track:** applied geometry continuation, not a claimed chapter of the book. **Prerequisites:** Stage 14.

## 1. What rectification buys you
Two cameras see a static point from different places. With known calibration, corresponding image locations constrain viewing rays. Stereo rectification warps the images so corresponding points are sought on the same scanline in the ideal rectified model. That simplifies matching from a two-dimensional search to a horizontal one. It does not make every pixel matchable: occlusion, repetitive texture, reflections and missing reference data remain.

Our real example is the Middlebury 2014 motorcycle pair distributed with scikit-image. It is a downsampled, already rectified pair. The course preserves its stated calibration and observes the arrays directly: two 500×741 RGB images and a 500×741 disparity array. The documentation's displayed disparity shape contains a trailing-channel inconsistency; the loader and manifest record the actual 2D array instead. This is an explicit source/data reconciliation, not a silent substitution. [D04]

## 2. Derive the depth formula, including the offset
Let baseline B separate the cameras horizontally; use the left camera as the reference. For a point (X,Y,Z),

```text
u_left  = f X/Z + cx_left
u_right = f (X-B)/Z + cx_right.
```

Subtract to get disparity `d=u_left-u_right=fB/Z+cx_left-cx_right`. Define `doffs=cx_right-cx_left`. Solving gives

```text
Z = f B / (d + doffs).
```

The `fB/d` simplification is valid only when this principal-point difference is zero. For the bundled downsampled pair, f=994.978 pixels, B=0.193001 metres and doffs=31.086 pixels. [D04, D05]

The source expresses baseline as 193.001 millimetres. We convert once to metres and label the result. Nonfinite disparity and nonpositive denominator values are missing, not zero-depth observations. Never fill them merely to make a point cloud look complete.

## 3. A simple matching algorithm you can inspect
For a selected pixel, take a square patch from the left image. Compare it with patches on the same row in the right image for integer disparities from 0 to a declared maximum. Sum or average the absolute intensity differences; choose the lowest cost. This is a sum-absolute-difference baseline, abbreviated SAD.

The prediction function receives images and selected pixel coordinates. It never receives the reference disparities. Its parameters are fixed for the demonstration before error measurement. Ties choose the smaller disparity; the margin between the two lowest costs is an ambiguity indicator, not a probability.

This deliberately simple model lacks subpixel refinement, a full occlusion treatment, and a learned feature representation. It is valuable precisely because you can understand why it fails. A comparison to a sophisticated model should include this baseline but should not pretend the baseline is state of the art.

## 4. Measure errors without hiding missing predictions
Evaluate predicted disparities at pixels where a reference is available. Report the number eligible, number evaluated, coverage, mean and median absolute pixel error, and the fraction exceeding a declared threshold. A lower error on a sharply reduced mask can be less useful than a slightly higher error with broad coverage. Show both.

Converting prediction and reference to depth gives an additional metre-error view. This is still agreement with the supplied disparity/calibration reference. It is not an independent measurement of the motorcycle, and it is not an unseen-scene evaluation.

## 5. Triangulation beyond the simplified formula
With general projection matrices P₁ and P₂ and corresponding undistorted pixels, a homogeneous point X satisfies cross-product equations. For each view, use rows like `u P[2]-P[0]` and `v P[2]-P[1]`. Stack them in A and solve `AX≈0` using the last right singular vector; then divide by its homogeneous coordinate.

This linear DLT algorithm minimizes an algebraic quantity. Nonlinear reprojection-error refinement is a different step. Check positive depth in both cameras, geometric conditioning, and correspondence validity. Parallel or coincident rays may not determine a stable finite point. Our tests compare a clean case with OpenCV when available. [G06]

## 6. What calibration itself requires
Intrinsic calibration estimates how camera-frame directions map to pixels, including an appropriate distortion model. Extrinsic calibration determines frame relationships. A known target supplies geometric constraints; varied target poses help constrain the parameters. Independent distances or target observations should evaluate the result instead of reusing every fitted observation as a validation claim. [G07]

The notebook includes a controlled synthetic fit for a simple known-pinhole model. Its world points and answers are generated for a mathematical exercise. The real stereo calibration is supplied by the dataset, not estimated afresh by this lesson. A real phone calibration remains a separate capture-and-evaluation exercise.

## 7. Sensitivity grows at small effective disparity
Differentiate the derived formula: `dZ/dd = -fB/(d+doffs)²`. Small pixel changes can make large depth changes when effective disparity is small. For a small assumed disparity standard deviation σ_d, first-order propagation gives approximately `σ_Z=|dZ/dd|σ_d`, assuming f, B, and doffs are fixed. Their actual uncertainty would need additional terms and correlations.

The lab compares this local approximation with a controlled Monte Carlo experiment. The random perturbations are generated noise, not observed sensor-error statistics.

## 8. Timing is part of geometry
A moving point captured at two different instants is not the same static point. Triangulating those observations under a simultaneous-static assumption can produce a plausible false position. An image timestamp, clock synchronization, exposure timing and rolling-shutter model can all matter. The synthetic timing experiment demonstrates the assumption; it does not measure synchronization on your cameras.

## Independent conceptual exercises

1. Derive Z=fB/(d+doffs) from the two pixel equations.
2. Calculate why the principal-point offset cannot be omitted here.
3. Which inputs does the SAD predictor receive, and which are reserved for evaluation?
4. What is the difference between DLT and nonlinear reprojection refinement?
5. Derive the local depth uncertainty for a fixed calibrated stereo model.
6. Why does a low reprojection residual not establish correct synchronization or scale?

## Mastery gate

Run the baseline, explain its denominators and missing values, and derive the uncertainty approximation.

Readings: D04, D05, G06, G07. See the [source ledger](../docs/SOURCES_V3.md) for checked links, evidence status and source differences.
