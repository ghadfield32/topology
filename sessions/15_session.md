# Stage 15 guided session — Turn disparity error into a physical uncertainty calculation

**Role:** Original v4 teaching supplement. It deepens the preserved lesson; it does not replace the book or its unavailable full text.

**Read first:** [Stage lesson](../lessons/15_lesson.md), then use this explanation before the [consolidation notebook](../consolidation/15_lab.ipynb). The [original workbook](../workbooks/15_workbook.md) and [worked lab](../notebooks/15_lab.ipynb) remain available. Repair earlier concepts only where needed; do not restart the whole course.

**Data and evidence:** Real stereo-reference disparities with generated local noise; no independent calibration-noise measurement.

## What you will be able to demonstrate

1. Derive the principal-point offset in rectified stereo.
2. Carry pixels and metres through the depth formula.
3. Compare a first-order uncertainty calculation with controlled numerical perturbations.
4. State which uncertainties a supplied-reference experiment cannot measure.

## Derive the denominator instead of memorizing it
For rectified cameras, let the right camera center be B to the right of the left center. A point has horizontal coordinates X and X−B in the two camera frames. Its pixels are `u_L=fX/Z+cx_L` and `u_R=f(X−B)/Z+cx_R`. Subtracting gives disparity `d=u_L−u_R=fB/Z+cx_L−cx_R`.

Define `doffs=cx_R−cx_L`. Then `d+doffs=fB/Z`, so `Z=fB/(d+doffs)`. The offset's sign follows from the chosen disparity definition. Reversing one without the other is not a cosmetic convention change.

With f in pixels, disparity and offset in pixels, and B in metres, depth is in metres. The original Middlebury calibration reports baseline in millimetres; the package's calibration explicitly converts it. A plausible point cloud does not reveal a factor-of-1000 unit error by itself.

## Work a sensitivity example
For f=1000 pixels, B=0.1 metres, corrected disparity 50 pixels, depth is two metres. Holding calibration fixed, `dZ/dd=−fB/(d+doffs)²`, which here is -0.04 metres per pixel. A small disparity standard deviation of 0.5 pixels gives a first-order depth standard deviation of about 0.02 metres.

This linear approximation is local. It worsens near a small denominator, and it does not turn a confidence score into a calibrated probability. A complete uncertainty calculation may include calibration, correspondence errors, distortion, and correlations. Gross matching failures are not adequately represented by tiny Gaussian noise around the correct match.

## Use the actual reference carefully
Select valid disparities from the real stereo reference. Add small generated Gaussian perturbations with a fixed seed, compute resulting depths, and compare empirical spread with the derivative approximation. This tests the propagation calculation under the imposed noise model.

It is not an empirical measurement of the actual stereo matcher's noise distribution. The original Stage 15 lab separately compares a simple image-based matcher with the supplied reference and reports its large failures. Keep those two experiments distinct: reference perturbation studies sensitivity; matcher evaluation measures a particular algorithm against available reference data.

A practical reconstruction report should show error distributions, eligible coverage, failures, units, and independent holdouts. A low reprojection error alone can coexist with wrong scale or weakly constrained depth. State what is observed, what is supplied, what is estimated, and what is imposed by an experimental control.

## Predict, execute, and explain

### Step 1

Select finite reference disparities and compute the local derivative with explicit units.

```python
from shape_lab.stereo import reference_sample, depth_from_disparity
_, _, reference, calibration = reference_sample()
samples = reference[::80, ::80].ravel()
samples = samples[np.isfinite(samples)][:25]
f = calibration['focal_px']; B = calibration['baseline_m']; offset = calibration['doffs_px']
sigma_px = .2
expected_sigma_m = f*B/(samples+offset)**2 * sigma_px
assert len(samples)>5
print('first reference depths:', depth_from_disparity(samples, f, B, offset)[:5])
```

### Step 2

Generate only the declared perturbation, not replacement reference truth.

```python
rng = np.random.default_rng(1504)
perturbed = samples[None,:] + rng.normal(0, sigma_px, size=(5000,len(samples)))
depths = depth_from_disparity(perturbed, f, B, offset)
measured_sigma_m = np.std(depths, axis=0, ddof=1)
ratio = measured_sigma_m/expected_sigma_m
print('empirical / first-order standard deviation:', ratio)
assert np.all(np.abs(ratio-1)<.06)
```

### Step 3

Store what is fixed and what is random so the numerical agreement cannot be mistaken for complete sensor uncertainty.

```python
result = {'points': len(samples), 'perturbation_trials': len(perturbed),
          'disparity_sigma_px': sigma_px, 'median_empirical_to_linear_sigma_ratio': float(np.median(ratio)),
          'calibration_fixed': True, 'noise_model': 'synthetic independent Gaussian disparity noise',
          'actual_matcher_uncertainty_established': False}
```

## Transfer problems — attempt without the solution

### 15.T1

If the baseline is multiplied by 1000 but disparity and focal length are unchanged, what happens to reconstructed depth?

<details><summary>Reveal reasoning after your attempt</summary>

Depth is multiplied by 1000. The unit of depth follows the baseline; this error can preserve relative shape while ruining metric scale.

</details>

### 15.T2

Why does a local Gaussian perturbation experiment not characterize gross correspondence failures?

<details><summary>Reveal reasoning after your attempt</summary>

It perturbs values near a reference match under an imposed distribution. Incorrect matches can have large, structured, non-Gaussian errors and require direct algorithm evaluation.

</details>

## Record what you actually demonstrated

Copy [the response template](../curriculum/response_templates/15_response.md) to a new dated file in `my_work/`. Explain each output, attempt the two transfer questions, and complete the original independent coding tasks. A passed reference notebook is not a mastery score. The four outcomes above are assessed by explanation, calculation, implementation and critique; delayed recall remains a separate check.

**References:** The original stage's reading assignments remain authoritative for that stage. See [the core source ledger](../docs/SOURCES.md), [the geometry source ledger](../docs/SOURCES_V3.md), and [the v4 source and scope ledger](../docs/SOURCES_V4.md). The worked calculations and these questions are original course additions; theorem proof obligations remain explicit in the proof atlases.
