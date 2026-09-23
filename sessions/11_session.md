# Stage 11 guided session — Build a feature pipeline without seeing the answer

**Role:** Original v4 teaching supplement. It deepens the preserved lesson; it does not replace the book or its unavailable full text.

**Read first:** [Stage lesson](../lessons/11_lesson.md), then use this explanation before the [consolidation notebook](../consolidation/11_lab.ipynb). The [original workbook](../workbooks/11_workbook.md) and [worked lab](../notebooks/11_lab.ipynb) remain available. Repair earlier concepts only where needed; do not restart the whole course.

**Data and evidence:** Real train/validation digit pixels and the bundled historical annual sunspot series; no new forecast claim.

## What you will be able to demonstrate

1. Distinguish fixed per-observation transformations from dataset-fitted preprocessing.
2. Apply training-only scaling and identify where validation data may be used.
3. Construct lagged features with their correct availability dates.
4. Separate topological representation design from proof of predictive value.

## A representation is part of the model
A persistence diagram is not immediately a fixed-width feature vector. We can summarize counts, lifetimes, Betti curves, landscapes, or persistence images. Each choice retains some information and discards some. A count of intervals, for example, does not retain their positions. A discretized representation adds grid and bandwidth choices.

Some transformations are fixed before looking at the dataset. Dividing an image's intensities by its documented maximum is a declared per-image conversion. Other transformations estimate parameters from data: a StandardScaler estimates feature means and variances. For predictive evaluation, fit those parameters on the training partition and apply the resulting rule unchanged to validation or test observations.

A scikit-learn Pipeline can keep fitted transformations inside a cross-validation procedure. It cannot protect against leakage that occurred before the pipeline, a wrongly defined split, or features containing future information. Tools enforce only the boundaries their inputs actually preserve.

## Work a time-availability example
For observations x₀,x₁,x₂,…, a backward-looking three-value feature available at time t is `(x[t−2],x[t−1],x[t])`. A forward window `(x[t],x[t+1],x[t+2])` is not available at time t. It can be used at t+2, provided its timestamp is assigned accordingly. The array values can be identical while their interpretation is causally wrong.

The new bundled historical sunspot series supplies real, dated annual observations. We use it to practice delay-coordinate construction and availability—not to assert a perfect low-dimensional dynamical system or forecast solar activity. The vintage ends in 2008 and is not a current operational feed. No new parameter choices are selected on future test labels.

## Inspect a real fitted transformation
Use the existing training and validation digit splits. Fit pixel scaling on training rows only. Check that the fitted means equal training means. Transform validation rows without refitting. The transformed validation mean is not required to be zero: demanding that would tempt you to normalize the validation set separately and change the coordinate system.

Then form the historical lag windows and attach the last included year. Avoid calling a row an independent sample just because it occupies a separate line: adjacent windows overlap. A downstream statistical evaluation must respect that dependence.

The original Stage 11 lab compares actual predictive baselines. This supplement repairs two common prerequisites—fitted preprocessing and information availability—so that a promising score is not accepted before its construction is understood.

## Predict, execute, and explain

### Step 1

Fit a transformation only on the training digit pixels.

```python
from shape_lab.data import load_digit_data
from sklearn.preprocessing import StandardScaler
train, _, _ = load_digit_data('train')
valid, _, _ = load_digit_data('validation')
X_train = train.reshape(len(train), -1)
X_valid = valid.reshape(len(valid), -1)
scaler = StandardScaler().fit(X_train)
assert np.allclose(scaler.mean_, X_train.mean(axis=0))
Z_valid = scaler.transform(X_valid)
print('training rows:', len(train), 'validation rows:', len(valid))
print('mean absolute validation-feature mean:', np.abs(Z_valid.mean(0)).mean())
```

### Step 2

Build windows from a real historical time series and attach the last included year.

```python
import pandas as pd
from shape_lab.features import delay_embedding
series = pd.read_csv(ROOT/'data/time_series/sunspots_yearly.csv')
values = series.SUNACTIVITY.to_numpy()
windows = delay_embedding(values, dimension=3, lag=1)
available_year = series.YEAR.to_numpy()[2:]
assert len(windows)==len(available_year)
assert np.array_equal(windows[0], values[:3])
display(pd.DataFrame({'available_year': available_year[:5],
                      'older': windows[:5,0], 'previous': windows[:5,1], 'current': windows[:5,2]}))
```

### Step 3

Record that this is feature construction, not an independently evaluated forecasting model.

```python
result = {'scaler_fit_rows': len(train), 'validation_transform_rows': len(valid),
          'time_series_window_count': len(windows), 'first_available_year': int(available_year[0]),
          'forecast_validation_performed': False, 'adjacent_windows_independent': False}
```

## Transfer problems — attempt without the solution

### 11.T1

Must a validation partition transformed by a training-fitted StandardScaler have zero mean?

<details><summary>Reveal reasoning after your attempt</summary>

No. Only the fitted training distribution is centered according to its estimated means. Re-centering validation independently changes the fitted transformation and can hide distribution shift.

</details>

### 11.T2

A forward window begins in 1900 and ends in 1902. When can it first be used by a past-only prediction system?

<details><summary>Reveal reasoning after your attempt</summary>

At the availability time of the last included observation, not 1900. The example attaches year 1902, while real systems would also need publication or sensor arrival times.

</details>

## Record what you actually demonstrated

Copy [the response template](../curriculum/response_templates/11_response.md) to a new dated file in `my_work/`. Explain each output, attempt the two transfer questions, and complete the original independent coding tasks. A passed reference notebook is not a mastery score. The four outcomes above are assessed by explanation, calculation, implementation and critique; delayed recall remains a separate check.

**References:** The original stage's reading assignments remain authoritative for that stage. See [the core source ledger](../docs/SOURCES.md), [the geometry source ledger](../docs/SOURCES_V3.md), and [the v4 source and scope ledger](../docs/SOURCES_V4.md). The worked calculations and these questions are original course additions; theorem proof obligations remain explicit in the proof atlases.
