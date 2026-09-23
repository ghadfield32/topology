# Stage 08 guided session — Read a barcode as a history, not a collection of scores

**Role:** Original v4 teaching supplement. It deepens the preserved lesson; it does not replace the book or its unavailable full text.

**Read first:** [Stage lesson](../lessons/08_lesson.md), then use this explanation before the [consolidation notebook](../consolidation/08_lab.ipynb). The [original workbook](../workbooks/08_workbook.md) and [worked lab](../notebooks/08_lab.ipynb) remain available. Repair earlier concepts only where needed; do not restart the whole course.

**Data and evidence:** Real digit intensity filtration and an exact complete/truncated square control.

## What you will be able to demonstrate

1. Derive the square filtration and its positive-length interval.
2. Explain half-open interval endpoints and zero-length bars.
3. Cross-check barcode Betti counts against thresholded real images.
4. Distinguish an unpaired class in a truncated filtration from a globally essential class.

## Follow one square through scale
Place points at `(0,0)`, `(1,0)`, `(1,1)`, and `(0,1)`. At scale zero there are four vertices. At scale one, the four side edges enter. Three of those edge additions merge components; the remaining edge closes a loop. No triangle is present yet because every triangle needs one diagonal of length √2.

At √2 the diagonals and their associated higher-dimensional simplices enter. The loop is filled. The positive-length H1 interval is therefore `[1,√2)`. At its birth it is present. At its death it is no longer present. Using a closed interval at both ends would count a class after it has died.

The finite H0 bars record three component merges at one; one component survives. Equal-time simplex choices can change a reduction algorithm's intermediate pairings, but the interval multiset of this filtration should not depend on an arbitrary legal tie ordering.

## A diagram retains birth and death
A diagram point `(b,d)` stores when a class appears and disappears. Its vertical distance above the diagonal is related to lifetime, but a diagram is not just a histogram of lifetimes. Two classes with the same duration can occur at different scales. Essential or truncated classes require a stated convention rather than silently inserting an enormous finite number.

If you stop the square filtration at 1.2, its loop is unpaired at the end. That does not mean the loop would survive every possible future scale. The full square example already tells us it dies at √2. Report the computed maximum scale next to any unpaired interval.

## Connect the barcode to an actual image
For a digit, use `f=1−intensity/16` on closed pixels and include pixels when `f≤t`. A persistence barcode implies a Betti count at each threshold: count intervals satisfying `birth≤t<death`. Calculate the same count directly from the selected square cells. Agreement links the temporal-looking interval representation to the underlying image geometry.

Filtration scale is not time in this experiment. Nothing physically moves while we vary an intensity threshold. Terms such as “birth” and “death” describe changes in the mathematical filtration. This distinction prevents an easy mistake when later applying similar notation to real sequences.

Explain the first threshold at which the measured digit acquires a loop, and then the threshold at which it fills. A result for this specific discretized image is not a claim about every symbol with the same label.

## Predict, execute, and explain

### Step 1

Recover the exact square interval with the course implementation.

```python
from shape_lab.persistence import rips_filtration, persistent_homology, diagram, pixel_filtration
square = np.array([[0.,0.],[1.,0.],[1.,1.],[0.,1.]])
bars = persistent_homology(rips_filtration(square))
h1 = diagram(bars, 1)
print(h1)
assert np.allclose(h1, [[1., np.sqrt(2)]])
```

### Step 2

Read barcode counts at declared thresholds on a real digit and compare with the direct square-cell oracle.

```python
from shape_lab.data import digit_example
from shape_lab.audits import pixel_betti_oracle
image, sample_id = digit_example(0)
f = 1-image/16.
bars = persistent_homology(pixel_filtration(f))
counts = []
for t in [0., .25, .5, .75, 1.]:
    predicted = [sum(b.dim==k and b.birth<=t<b.death for b in bars) for k in [0,1]]
    direct = list(pixel_betti_oracle(f<=t))
    assert predicted == direct
    counts.append([t, *direct])
print(counts)
```

### Step 3

Stop the square early to demonstrate an infinite endpoint caused by truncation.

```python
truncated = diagram(persistent_homology(rips_filtration(square, max_edge=1.2)), 1)
assert len(truncated)==1 and np.isinf(truncated[0,1])
result = {'sample_id': sample_id, 'image_counts': counts,
          'square_complete_h1': h1.tolist(), 'truncated_square_h1_survives_end': True,
          'truncated_max_edge': 1.2, 'global_essential_claim': False}
```

## Transfer problems — attempt without the solution

### 08.T1

At t=√2, should the square H1 bar [1,√2) count toward beta1?

<details><summary>Reveal reasoning after your attempt</summary>

No. The interval is half-open; the death event has occurred. The filled complex at that scale has no H1 class from the square outline.

</details>

### 08.T2

Why can equal lifetimes describe different information?

<details><summary>Reveal reasoning after your attempt</summary>

Intervals [1,2) and [10,11) both last one unit but occupy different scales. A lifetime-only summary discards their positions in the filtration.

</details>

## Record what you actually demonstrated

Copy [the response template](../curriculum/response_templates/08_response.md) to a new dated file in `my_work/`. Explain each output, attempt the two transfer questions, and complete the original independent coding tasks. A passed reference notebook is not a mastery score. The four outcomes above are assessed by explanation, calculation, implementation and critique; delayed recall remains a separate check.

**References:** The original stage's reading assignments remain authoritative for that stage. See [the core source ledger](../docs/SOURCES.md), [the geometry source ledger](../docs/SOURCES_V3.md), and [the v4 source and scope ledger](../docs/SOURCES_V4.md). The worked calculations and these questions are original course additions; theorem proof obligations remain explicit in the proof atlases.
