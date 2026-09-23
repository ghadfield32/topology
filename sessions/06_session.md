# Stage 06 guided session — Learn what coefficient fields reveal and forget

**Role:** Original v4 teaching supplement. It deepens the preserved lesson; it does not replace the book or its unavailable full text.

**Read first:** [Stage lesson](../lessons/06_lesson.md), then use this explanation before the [consolidation notebook](../consolidation/06_lab.ipynb). The [original workbook](../workbooks/06_workbook.md) and [worked lab](../notebooks/06_lab.ipynb) remain available. Repair earlier concepts only where needed; do not restart the whole course.

**Data and evidence:** Real training digit threshold sweep; exact oriented simplicial and specified cellular-chain controls.

## What you will be able to demonstrate

1. Construct an oriented integer boundary and check boundary-of-boundary.
2. Calculate how a coefficient change affects a cellular boundary map.
3. Independently verify image homology across multiple thresholds.
4. Distinguish Betti numbers from full integer homology, including torsion.

## Revisit the triangle with signs
With increasing vertex order, the oriented boundary of `[0,1,2]` is `[1,2]−[0,2]+[0,1]`. Taking another boundary gives `(2−1)−(2−0)+(1−0)=0`. Every vertex cancels. The sign comes from the position of the removed vertex. Over F₂, minus one equals plus one, so the signed formula reduces to the binary rule you already used.

This demonstrates why adding a prime-field rank routine alone is not enough to generalize binary homology. The boundary matrices must also use the correct orientation signs. A zero–one triangle matrix copied unchanged into F₃ generally loses the cancellation property.

## Work a coefficient-sensitive example
The standard cellular description of the real projective plane has one cell in each of dimensions zero, one, and two. Its cellular boundary maps are `d₁=0` and `d₂=[2]`. This is a compact *cellular* description, not the simplicial triangle matrix from the earlier lab.

Over F₂, the entry two becomes zero. Both boundary ranks vanish, so the Betti numbers are `(1,1,1)`. Over F₃, multiplication by two is invertible. The rank of d₂ is one, giving `(1,0,0)`. A coefficient change genuinely changes the answer because the question has changed.

Over the integers, the one-dimensional cycles form Z and the boundaries form 2Z. Their quotient is Z/2Z: a nonzero class whose double is zero. This is torsion. It has no free integer rank, so a list of integer Betti numbers alone does not describe the full homology group. The two-dimensional integer kernel of multiplication by two is zero. We derive these facts directly from this specified cellular chain complex; we do not claim to have implemented a general integer homology solver.

## Check a real image two ways
For the declared closed-square image object, compute β₀ by walking the square-connectivity graph. Count distinct square vertices and edges to compute Euler characteristic. Because this is a finite planar square complex with no two-dimensional homology, infer `β₁=β₀−χ`. That route does not use persistence reduction or the simplicial rank function.

Independently, triangulate the same thresholded square union and use the boundary matrices. Agreement over many thresholds is more informative than comparing two calls to the same routine under different names. It is still software evidence, not proof that the sensor captured every physical feature.

## Make the quotient concrete
When a cycle is itself a boundary, it represents zero in homology. The chain has not vanished; the equivalence relation identifies its homology class with zero. Saying “the loop disappeared” is a shorthand for that algebraic statement. Keep the chain, cycle, boundary, and equivalence class separate in your own explanation.

The proof atlas and external algebraic-topology reading provide the path to deeper theory. Complete the finite hand calculations first, then use the field-sensitive example to understand why more general coefficient systems require more than changing one library flag.

## Predict, execute, and explain

### Step 1

Compute the cellular projective-plane example directly in two prime fields. These are cellular matrices, not a new triangulation.

```python
from shape_lab.audits import rank_prime, oriented_boundary, pixel_betti_oracle
cellular = {}
for p in [2, 3]:
    r2 = rank_prime([[2]], p)
    cellular[p] = [1, 1-r2, 1-r2]
print(cellular)
assert cellular == {2: [1, 1, 1], 3: [1, 0, 0]}
```

### Step 2

Check the oriented triangle identity over the integers before reducing to any field.

```python
from shape_lab.algebra import closure
K = closure([(0, 1, 2)])
d1 = oriented_boundary(K, 1); d2 = oriented_boundary(K, 2)
print('d1:', d1); print('d2:', d2)
assert np.all(d1 @ d2 == 0)
```

### Step 3

Compare two distinct computational routes on a real digit at every integer intensity threshold.

```python
from shape_lab.data import digit_example
from shape_lab.persistence import pixel_filtration
from shape_lab.algebra import betti_numbers
image, sample_id = digit_example(8)
filtration = pixel_filtration(1-image/16.)
rows = []
for threshold in range(17):
    chosen = [s for s, t in filtration if t <= 1-threshold/16.]
    by_chains = betti_numbers(chosen, 1)
    by_cells = list(pixel_betti_oracle(image >= threshold))
    assert by_chains == by_cells
    rows.append([threshold, *by_cells])
import pandas as pd
display(pd.DataFrame(rows, columns=['intensity threshold', 'beta0', 'beta1']))
result = {'sample_id': sample_id, 'independent_threshold_comparisons': len(rows),
          'all_agree': True, 'cellular_field_example': cellular}
```

## Transfer problems — attempt without the solution

### 06.T1

Why must signed boundaries accompany an F3 rank routine?

<details><summary>Reveal reasoning after your attempt</summary>

The integer boundary uses alternating orientation signs. Those signs remain distinct modulo three. Omitting them can make boundary-of-boundary nonzero, so the purported homology quotient need not be defined.

</details>

### 06.T2

For the integer map Z→Z, n↦2n, what are its kernel and cokernel?

<details><summary>Reveal reasoning after your attempt</summary>

The kernel is zero because 2n=0 implies n=0. The image is 2Z, and the cokernel is Z/2Z. The finite torsion quotient cannot be summarized by a positive free rank.

</details>

## Record what you actually demonstrated

Copy [the response template](../curriculum/response_templates/06_response.md) to a new dated file in `my_work/`. Explain each output, attempt the two transfer questions, and complete the original independent coding tasks. A passed reference notebook is not a mastery score. The four outcomes above are assessed by explanation, calculation, implementation and critique; delayed recall remains a separate check.

**References:** The original stage's reading assignments remain authoritative for that stage. See [the core source ledger](../docs/SOURCES.md), [the geometry source ledger](../docs/SOURCES_V3.md), and [the v4 source and scope ledger](../docs/SOURCES_V4.md). The worked calculations and these questions are original course additions; theorem proof obligations remain explicit in the proof atlases.
