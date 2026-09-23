# Stage 04 guided session — Symmetry preserves some things, not everything

**Role:** Original v4 teaching supplement. It deepens the preserved lesson; it does not replace the book or its unavailable full text.

**Read first:** [Stage lesson](../lessons/04_lesson.md), then use this explanation before the [consolidation notebook](../consolidation/04_lab.ipynb). The [original workbook](../workbooks/04_workbook.md) and [worked lab](../notebooks/04_lab.ipynb) remain available. Repair earlier concepts only where needed; do not restart the whole course.

**Data and evidence:** Real digit under exact array transformations; constructed matrices and annulus radii.

## What you will be able to demonstrate

1. Calculate a rotation and reflection and show that their order can matter.
2. Distinguish a group action from a label-preserving data augmentation assumption.
3. Explain homotopy using an annulus and a circle.
4. Identify what prevents a proposed deformation from being well defined.

## Combination needs rules
A group is a set with an associative operation, an identity, and an inverse for every element. Rotations and reflections of a square provide a small example. Applying two symmetries in succession is the operation. Doing nothing is the identity. Undoing a symmetry gives its inverse. The transformation must map the square to itself; an arbitrary stretch is not one of these square symmetries.

Take the quarter-turn `R(x,y)=(-y,x)` and reflection `F(x,y)=(-x,y)`. Applied to `(1,0)`, first F then R gives `(0,-1)`. First R then F gives `(0,1)`. Thus `RF` and `FR` differ. “Group” does not mean “commutative.” When composing camera transformations later, the same attention to order will matter.

## An image operation is not a scientific guarantee
Rotating an 8 by 8 array through 90 degrees permutes its entries. Its intensity sum and histogram remain unchanged. Four such rotations return the original array. These are exact properties of the array operation. The semantic label need not be unchanged. Rotating a digit can make it ambiguous or resemble a different symbol. A mathematical group action is not, by itself, a justification for applying label-preserving augmentation in machine learning.

## Deformation is a continuous family of maps
For an annulus `1 ≤ ||x|| ≤ 2`, define `H(x,t)=((1-t)+t/||x||)x` for `0≤t≤1`. At time zero this is x. At time one it lies on the unit circle. If x already lies on that circle, it stays fixed. Its radius is `(1-t)||x||+t`, which stays between one and two. Hence this is a deformation retraction of the annulus onto its inner circle.

The same formula cannot retract the entire disk onto its boundary: it is undefined at x=0. Simply ignoring that point would change the domain, not fix the argument. This is a useful habit: locate the exact obstruction to a tempting formula rather than saying it “looks wrong.”

A loop is a path whose endpoints agree. Homotopy classes of based loops, with concatenation, form the fundamental group. On the circle, winding number records the integer number of turns. Homology later makes certain questions easier to compute by passing to algebraic summaries, but it does not preserve every distinction present in the fundamental group.

## What to show before advancing
Calculate the two transformation orders by hand. Explain the domain restriction in the annulus formula. Then examine the real digit under array rotations. State separately which numerical properties are unchanged and which semantic conclusions are unsupported. This prepares you to evaluate both mathematical invariance and domain-specific assumptions.

## Predict, execute, and explain

### Step 1

Use two explicit matrices to demonstrate noncommutativity.

```python
R90 = np.array([[0, -1], [1, 0]])
F = np.array([[-1, 0], [0, 1]])
p = np.array([1, 0])
print('R F p:', R90 @ F @ p, 'F R p:', F @ R90 @ p)
assert not np.array_equal(R90 @ F, F @ R90)
```

### Step 2

Apply the array action to a real digit. Preserve numerical invariants without assuming the label remains valid.

```python
from shape_lab.data import digit_example
image, sample_id = digit_example(6)
rotated = np.rot90(image)
assert np.array_equal(np.rot90(image, 4), image)
assert image.sum() == rotated.sum()
assert np.array_equal(np.sort(image.ravel()), np.sort(rotated.ravel()))
import matplotlib.pyplot as plt
plt.figure(figsize=(4, 4)); plt.imshow(rotated)
plt.title('Rotated real digit: label invariance is not assumed'); plt.axis('off'); plt.show()
```

### Step 3

Numerically check the annulus radius formula for selected points; the text supplies the all-points argument.

```python
radii = np.array([1., 1.5, 2.])
for t in [0., .25, .5, 1.]:
    moved = (1-t)*radii + t
    assert np.all((moved >= 1) & (moved <= 2))
result = {'sample_id': sample_id, 'rotation_order_test': 'passed',
          'label_preservation_claimed': False, 'annulus_check': 'selected radii; proof in text'}
```

## Transfer problems — attempt without the solution

### 04.T1

Does norm preservation guarantee that two transformations commute?

<details><summary>Reveal reasoning after your attempt</summary>

No. Rotations and reflections can preserve norms while their composition order changes the result. The displayed R and F supply an explicit counterexample.

</details>

### 04.T2

Why cannot the radial formula retract a full disk onto its circle boundary?

<details><summary>Reveal reasoning after your attempt</summary>

It divides by ||x|| and is undefined at the center. A valid deformation must be continuous and defined at every point of the stated domain for every time.

</details>

## Record what you actually demonstrated

Copy [the response template](../curriculum/response_templates/04_response.md) to a new dated file in `my_work/`. Explain each output, attempt the two transfer questions, and complete the original independent coding tasks. A passed reference notebook is not a mastery score. The four outcomes above are assessed by explanation, calculation, implementation and critique; delayed recall remains a separate check.

**References:** The original stage's reading assignments remain authoritative for that stage. See [the core source ledger](../docs/SOURCES.md), [the geometry source ledger](../docs/SOURCES_V3.md), and [the v4 source and scope ledger](../docs/SOURCES_V4.md). The worked calculations and these questions are original course additions; theorem proof obligations remain explicit in the proof atlases.
