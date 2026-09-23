# Stage 10 guided session — A stability bound is not a discovery certificate

**Role:** Original v4 teaching supplement. It deepens the preserved lesson; it does not replace the book or its unavailable full text.

**Read first:** [Stage lesson](../lessons/10_lesson.md), then use this explanation before the [consolidation notebook](../consolidation/10_lab.ipynb). The [original workbook](../workbooks/10_workbook.md) and [worked lab](../notebooks/10_lab.ipynb) remain available. Repair earlier concepts only where needed; do not restart the whole course.

**Data and evidence:** Real training image plus explicitly generated bounded perturbations; not repeated sensor observations.

## What you will be able to demonstrate

1. State the fixed-domain filtration assumptions behind the tested bound.
2. Explain why a diagram point can match to the diagonal.
3. Compute a bounded image perturbation and its diagram distance.
4. Distinguish deterministic stability, statistical uncertainty, and scientific meaning.

## Three questions, three kinds of evidence
A deterministic stability bound asks how much a mathematical output can change under a bounded change in its input. A statistical statement asks how uncertain an estimate is under a sampling or noise model. A scientific interpretation asks whether the measured structure answers a substantive question. One does not automatically establish the others.

For our finite fixed pixel complex, let f and g be two scalar-valued filtrations constructed on the same grid. If their scalar values differ by at most δ, each f sublevel set lies in the corresponding g sublevel set shifted by δ, and conversely. Under the finite persistence setup this leads to a bottleneck bound of at most δ. The primary stability reading supplies the general theorem; the notebook tests this declared finite application.

## Why diagonal matching matters
A finite diagram point `(b,d)` can be matched to a diagonal point `(t,t)`. Under maximum-coordinate distance, the smallest possible cost is `(d−b)/2`, achieved at the midpoint t. This allows short intervals to disappear at a controlled cost. Forcing every off-diagonal point to match another off-diagonal point would fail when one diagram has an extra small feature.

For a bar `[2,6)`, the diagonal cost is two. This is not the full lifetime four. Derive the midpoint by balancing `t−b` and `d−t`; the larger error is smallest when they agree.

## Perturb actual image values
Select a real training digit and construct f using the fixed intensity convention. Add generated bounded noise with a recorded random seed. The noise is a synthetic intervention on real observations, not a second physical measurement of the same handwriting. Compute the actual maximum absolute change, not just the requested nominal bound.

Complete the pixel filtration so finite H1 intervals really die within the supplied scalar range. Our finite diagram-distance routine rejects infinite endpoints. Never remove them without reporting what comparison remains. This notebook compares H1, for which the finite full rectangular image complex has no surviving loop.

## Interpret success conservatively
A passing numerical bound checks that this experiment is consistent with the theorem and implementation. It does not identify which loops are meaningful, estimate the camera noise distribution, or prove that a long interval is an important physical structure. A structured artifact can be stable. A meaningful rare feature can be short under a poorly chosen metric.

An outlier or a crop can change the point set or domain rather than merely perturbing a scalar on the same fixed complex. Do not reuse this inequality without checking the relevant construction and hypotheses. State a failure as a failed assumption or failed implementation test, not as an inconvenience to hide.

## Predict, execute, and explain

### Step 1

Calculate the distance of one interval to the diagonal exactly.

```python
from shape_lab.persistence import finite_bottleneck, pixel_filtration, persistent_homology, diagram
cost = finite_bottleneck([[2., 6.]], np.empty((0,2)))
print('diagonal cost:', cost)
assert cost == 2.
```

### Step 2

Perturb a real digit on the same fixed grid, then compare completed H1 diagrams.

```python
from shape_lab.data import digit_example
image, sample_id = digit_example(8)
f = 1-image/16.
rng = np.random.default_rng(1004)
rows = []
for nominal in [.01, .03, .08]:
    g = f + rng.uniform(-nominal, nominal, size=f.shape)
    a = diagram(persistent_homology(pixel_filtration(f)), 1)
    b = diagram(persistent_homology(pixel_filtration(g)), 1)
    delta = float(np.max(np.abs(f-g)))
    observed = finite_bottleneck(a, b)
    assert observed <= delta + 1e-10
    rows.append([nominal, delta, observed])
print('nominal bound, actual scalar change, bottleneck:', rows)
```

### Step 3

Keep the scope of the check attached to its result.

```python
result = {'sample_id': sample_id, 'comparisons': rows,
          'same_fixed_pixel_grid': True, 'homology_dimension': 1,
          'noise_is_synthetic': True, 'scientific_significance_established': False}
```

## Transfer problems — attempt without the solution

### 10.T1

A short diagram bar vanishes after a perturbation. Why can this still satisfy stability?

<details><summary>Reveal reasoning after your attempt</summary>

The bar can be matched to the diagonal at half its lifetime in maximum norm. Stability controls an optimal matching, not preservation of every bar as an individually named object.

</details>

### 10.T2

Does a long-lived stable interval imply a scientifically meaningful mechanism?

<details><summary>Reveal reasoning after your attempt</summary>

No. Stability controls changes under a specified perturbation model. Meaning requires appropriate measurement choices, null or comparison models, and task-specific evidence.

</details>

## Record what you actually demonstrated

Copy [the response template](../curriculum/response_templates/10_response.md) to a new dated file in `my_work/`. Explain each output, attempt the two transfer questions, and complete the original independent coding tasks. A passed reference notebook is not a mastery score. The four outcomes above are assessed by explanation, calculation, implementation and critique; delayed recall remains a separate check.

**References:** The original stage's reading assignments remain authoritative for that stage. See [the core source ledger](../docs/SOURCES.md), [the geometry source ledger](../docs/SOURCES_V3.md), and [the v4 source and scope ledger](../docs/SOURCES_V4.md). The worked calculations and these questions are original course additions; theorem proof obligations remain explicit in the proof atlases.
