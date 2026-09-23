# Measurement, uncertainty, and evidence — a second beginner primer

## Start by identifying the object of a claim
“Depth is accurate” is incomplete. Which pixels, which scene, which reference, which units, which error statistic, and which selection rule? A measurement claim becomes testable only after those choices are stated.

An observation might be a pixel, an image, a person, or a recording session. Thousands of pixels from one image do not provide thousands of independent scenes. Correlation is not a defect to hide; it is a feature of the data-generating process that changes the evaluation design.

## Numbers, errors, and averages
Given paired scalar predictions pᵢ and references rᵢ, residuals are `eᵢ=pᵢ-rᵢ`. Mean absolute error averages `|eᵢ|`; root mean squared error takes the square root of the mean of `eᵢ²`. Large errors influence the second statistic more. A median describes the middle ordered error, while a high percentile describes the upper tail. Always label units.

```python
import numpy as np
prediction = np.array([2.0, 2.2, 3.5])
reference = np.array([2.1, 2.1, 2.1])
e = prediction-reference
print('MAE:', np.abs(e).mean())
print('RMSE:', np.sqrt(np.mean(e**2)))
print('Median absolute error:', np.median(np.abs(e)))
```

Accuracy on only the easiest valid predictions is incomplete. Report coverage: the number evaluated divided by the number eligible for the stated evaluation. Missing predictions are not zero-error measurements. If a denominator is zero, return “undefined,” not a reassuring zero.

## Random error, systematic error, and reference error
Small unbiased noise varies around a reference. A wrong focal length or a unit mismatch can create systematic error. A provided benchmark reference also has an acquisition procedure and limitations. Agreement with it is evidence relative to that reference, not proof of an inaccessible exact physical truth.

Do not call every mismatch “model error” before checking coordinate systems, image resizing, time alignment, and invalid values. Conversely, do not alter the reference or select samples after seeing the predictions to make an error disappear.

## Standard deviation is not a universal error bar
Variance measures average squared deviation from a mean. Covariance describes how pairs of errors vary together. A quoted standard deviation only answers a well-defined question under its data and model assumptions. It is not automatically a confidence interval, prediction interval, worst-case bound, or calibrated model confidence.

An arbitrary network confidence score of 0.9 does not mean a 90% probability of correctness. That interpretation requires a defined correctness event and calibration evidence on appropriate data. Even an actual probability can be calibrated for one population and fail on another.

## Why splitting matters
Fit registration on one set of correspondences and measure error on different correspondences. Choose hyperparameters on training/validation information, not the held-out test answer. With images from the same session, keep the whole session on one side of the relevant split when the scientific question concerns new sessions.

In time-series prediction, use only evidence available by the decision time. An offline smoothed path may use later frames; a live detector cannot. A fair comparison makes this difference explicit instead of counting both outputs as live predictions.

The bundled stereo data are one static demonstration scene. Its reference disparities are intentionally visible for teaching. Repeated experimentation on this scene does not produce an unseen-scene benchmark. The course's synthetic corruption experiments answer mathematical sensitivity questions, not model generalization questions.

## Claims ladder
A shape and dtype check establishes format. An inverse-transform test establishes an algebraic identity on tested inputs. A real-data round trip establishes consistency of operations on those observations. A held-out physical measurement tests an external claim. A model comparison over independent scenes tests generalization. Each rung needs evidence that the earlier rung does not supply.

Keep a ledger with a claim, source, experiment, result, and remaining uncertainty. “No evidence yet” is a useful state. It prevents an unfinished experiment from becoming a remembered success.

## Minimum mastery check
Calculate MAE and RMSE on the example. Explain how masking changes a denominator. Give one correlated observation unit in sports video. Distinguish reference agreement from independent truth. Explain why tuning after reading a test result uses up that test. State the difference between onset time and decision time for a delayed live event detector.
