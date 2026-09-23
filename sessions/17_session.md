# Stage 17 guided session — Fit on anchors, evaluate elsewhere

**Role:** Original v4 teaching supplement. It deepens the preserved lesson; it does not replace the book or its unavailable full text.

**Read first:** [Stage lesson](../lessons/17_lesson.md), then use this explanation before the [consolidation notebook](../consolidation/17_lab.ipynb). The [original workbook](../workbooks/17_workbook.md) and [worked lab](../notebooks/17_lab.ipynb) remain available. Repair earlier concepts only where needed; do not restart the whole course.

**Data and evidence:** Real reference point arrangement; target transforms and held-out deformations are generated controls.

## What you will be able to demonstrate

1. Distinguish rigid alignment from a similarity transform with scale.
2. Separate fitting references from held-out evaluation points.
3. Construct a negative control showing why fitted residual is optimistic.
4. Explain why perfect synthetic-transform recovery does not validate physical scene scale.

## What alignment is allowed to change
A rigid transformation rotates and translates. A similarity transformation additionally multiplies all lengths by one positive scale. In our row-vector convention it is `Y=s X R.T+t`. These models cannot correct arbitrary local warping or depth-dependent distortion. Selecting a more flexible model merely to reduce residuals can hide the very error you intended to measure.

Correspondence is a separate problem. The least-squares fit assumes that each source row is paired with the correct target row. A good fitted transform does not verify the pairing, and this small function does not perform correspondence discovery or robust outlier removal.

## Work an exact example first
If target coordinates were constructed using scale two, a known rotation, and a translation, sufficient noncollinear paired anchors should recover those parameters up to numerical tolerance. Collinear anchors leave some rotations unconstrained; the implementation rejects them. This tests observability and algebra in a controlled case.

The real stereo-reference points below serve as a nontrivial point arrangement. We deliberately transform them to create targets. The target coordinates are generated, not independent physical measurements. Perfect recovery verifies the fitting code on this control; it does not validate VGGT scale or the original camera calibration.

## Show why a holdout is necessary
Choose every other selected point as fitting anchors. Leave the others out. Fit the transform to the anchors and evaluate residuals on held-out points. In the exact control both residuals should be near zero.

Now add a local displacement to only the held-out targets and refit using the unchanged anchors. The training residual stays near zero while held-out residual increases. This deliberately simple negative control makes the logic visible: a fit can look excellent while unseen parts of a scene disagree. The perturbation is not claimed to reproduce a particular model's errors.

## Formulate a physical validation study
For a real comparison, registration anchors and validation measurements must be genuinely separated. Record their identities, collection procedure, units, uncertainty, and visibility. Evaluate distances, orientation, reprojection, completeness, and failure modes appropriate to the task. Avoid describing an alignment to the same reference points as independent validation.

Topology can summarize structure but does not repair metric scale. Two reconstructions can have similar topological descriptors and different lengths. A plausible point cloud is a proposal until the intended measurement claims are supported. This is the practical bridge from the mathematical invariance lessons to responsible learned-geometry evaluation.

## Predict, execute, and explain

### Step 1

Generate a known transformation of actual reference point locations. The targets are explicitly synthetic.

```python
from shape_lab.stereo import reference_sample, point_cloud
from shape_lab.geometry import exp_so3, fit_similarity
_, _, disparity, calibration = reference_sample()
X, _ = point_cloud(disparity, calibration, stride=70)
X = X[:45]
true_scale = 1.7; true_R = exp_so3([.12,-.08,.05]); true_t = np.array([.2,-.1,.3])
Y = true_scale*X@true_R.T + true_t
anchor = np.arange(len(X)) % 2 == 0
assert anchor.sum()>=3 and (~anchor).sum()>=3
```

### Step 2

Fit only on anchors, then evaluate the rest.

```python
scale, rotation, translation = fit_similarity(X[anchor], Y[anchor])
predicted = scale*X@rotation.T + translation
clean_error = np.linalg.norm(predicted[~anchor]-Y[~anchor], axis=1)
assert np.allclose(scale, true_scale)
assert np.max(clean_error)<1e-10
print('clean held-out maximum:', clean_error.max())
```

### Step 3

Change only held-out targets. The anchor fit cannot expose this local deformation.

```python
warped = Y.copy(); warped[~anchor] += [.03, 0., 0.]
s, r, t = fit_similarity(X[anchor], warped[anchor])
fit_prediction = s*X@r.T + t
fit_error = np.linalg.norm(fit_prediction[anchor]-warped[anchor], axis=1)
holdout_error = np.linalg.norm(fit_prediction[~anchor]-warped[~anchor], axis=1)
assert fit_error.max()<1e-10
assert np.allclose(holdout_error, .03)
result = {'anchors': int(anchor.sum()), 'held_out': int((~anchor).sum()),
          'anchor_max_error': float(fit_error.max()), 'warped_holdout_mean_error': float(holdout_error.mean()),
          'targets_are_generated': True, 'independent_physical_validation': False}
```

## Transfer problems — attempt without the solution

### 17.T1

Can a global similarity transform correct arbitrary depth-dependent distortion?

<details><summary>Reveal reasoning after your attempt</summary>

No. It has one scale, one rotation, and one translation. A locally varying deformation is outside that model even if some fitted anchors align well.

</details>

### 17.T2

Why is evaluating the alignment on exactly its fitting anchors insufficient?

<details><summary>Reveal reasoning after your attempt</summary>

Optimization explicitly minimizes their residuals. Their agreement does not measure behavior at independent points or rule out overfitting, deformation elsewhere, or shared measurement errors.

</details>

## Record what you actually demonstrated

Copy [the response template](../curriculum/response_templates/17_response.md) to a new dated file in `my_work/`. Explain each output, attempt the two transfer questions, and complete the original independent coding tasks. A passed reference notebook is not a mastery score. The four outcomes above are assessed by explanation, calculation, implementation and critique; delayed recall remains a separate check.

**References:** The original stage's reading assignments remain authoritative for that stage. See [the core source ledger](../docs/SOURCES.md), [the geometry source ledger](../docs/SOURCES_V3.md), and [the v4 source and scope ledger](../docs/SOURCES_V4.md). The worked calculations and these questions are original course additions; theorem proof obligations remain explicit in the proof atlases.
