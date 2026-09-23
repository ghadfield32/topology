# Stage 07 guided session — Understand why the same points give different complexes

**Role:** Original v4 teaching supplement. It deepens the preserved lesson; it does not replace the book or its unavailable full text.

**Read first:** [Stage lesson](../lessons/07_lesson.md), then use this explanation before the [consolidation notebook](../consolidation/07_lab.ipynb). The [original workbook](../workbooks/07_workbook.md) and [worked lab](../notebooks/07_lab.ipynb) remain available. Repair earlier concepts only where needed; do not restart the whole course.

**Data and evidence:** Real Iris point sample; exact equilateral-triangle scale derivation.

## What you will be able to demonstrate

1. Derive edge and face entry times from a declared filtration convention.
2. Explain pairwise overlap versus a common intersection.
3. Build a small Rips filtration and verify that faces appear no later than cofaces.
4. Use a real point cloud without treating its label columns as geometry.

## Connect first, then decide what is filled
At a fixed Rips threshold ε, join every pair of observations separated by at most ε. A collection of vertices forms a simplex when every pair in the collection satisfies that rule. Three connected vertices therefore bring a filled triangle, not merely its three-edge outline. Four mutually connected vertices bring a tetrahedron when that dimension is included.

The filtration value of a simplex is its largest pairwise distance. A face cannot have a larger diameter than the simplex containing it, so the face necessarily appears no later. This monotonicity is the property that lets homology map consistently from one stage to the next.

## Compare an equilateral triangle
Use three points forming an equilateral triangle of side one. In the edge-length Rips convention, all three edges and the filled triangle appear at ε=1. There is no positive-length one-dimensional persistence interval from the outline: the filling arrives at the same time.

For a Čech complex constructed from radius-r balls, pairwise intersections begin at r=1/2. A common intersection of all three balls begins at the circumradius r=1/√3. Thus a Čech loop exists between those values, under the corresponding closed-ball convention. Pairwise intersection is not the same as a common intersection. Comparing the raw numbers one and one-half without explaining edge-length versus ball-radius conventions confuses two scales.

This example is about an explicit finite construction. A nerve theorem can connect a suitable cover to its union, but its hypotheses matter. A graph drawn on arbitrary data does not inherit such a theorem merely because it resembles overlapping circles.

## Read the real-data filtration
Choose a small number of Iris observations with their four measurements. For each threshold, count vertices, edges, and triangles and compute the requested homology. Use the same points at every threshold. If the point sample itself changes, you no longer have the simple nested filtration that this calculation assumes.

A larger threshold never removes simplices, but it can both create and destroy homology classes. An edge might join components or create a cycle. A triangle can fill a cycle. Counting more edges therefore does not imply more persistent loops.

The educational enumerator is intentionally small. Combinations grow quickly even when the coordinate dimension is modest. Computing H1 requires triangles; computing H2 requires tetrahedra that can kill two-dimensional cycles. Later production libraries improve efficiency, but they do not eliminate these mathematical requirements.

## Predict, execute, and explain

### Step 1

Calculate the two geometric scales before asking any library for a persistence diagram.

```python
edge_rips = 1.
cech_pair_radius = .5
cech_triple_radius = 1/np.sqrt(3)
print('Rips edge scale:', edge_rips)
print('Cech radii:', cech_pair_radius, cech_triple_radius)
assert cech_triple_radius > cech_pair_radius
```

### Step 2

Build a filtration from actual measurements. The stored tuple records each simplex and its entry value.

```python
from shape_lab.data import load_iris_data
from shape_lab.persistence import rips_filtration
from shape_lab.algebra import betti_numbers
frame = load_iris_data().iloc[::15]
X = frame[[c for c in frame if c.endswith('_cm')]].to_numpy()
filtration = rips_filtration(X, max_homology=1)
values = dict(filtration)
from itertools import combinations
for simplex, value in filtration:
    if len(simplex)>1:
        assert all(values[face] <= value for face in combinations(simplex, len(simplex)-1))
print('records:', len(X), 'stored simplices:', len(filtration))
```

### Step 3

Compare several nested complexes. Their simplex counts are monotone; their Betti numbers need not be.

```python
scales = [0., .5, 1., 2., 5., 10.]
rows = []
for scale in scales:
    K = [s for s,t in filtration if t <= scale]
    rows.append([scale, len(K), *betti_numbers(K, 1)])
import pandas as pd
display(pd.DataFrame(rows, columns=['edge threshold (cm)', 'simplices', 'beta0', 'beta1']))
assert np.all(np.diff([row[1] for row in rows]) >= 0)
result = {'sample_ids': frame.sample_id.astype(int).tolist(), 'filtration_rows': rows,
          'scale_convention': 'maximum pairwise Euclidean edge length in selected cm features'}
```

## Transfer problems — attempt without the solution

### 07.T1

Can a Rips filtration on an equilateral three-point cloud have a positive-length H1 bar?

<details><summary>Reveal reasoning after your attempt</summary>

Not in the full clique construction under the stated edge-length convention: the triangle enters with its edges. A graph-only construction can retain the loop, but it is a different complex.

</details>

### 07.T2

Why do we need (k+1)-simplices when computing Hk?

<details><summary>Reveal reasoning after your attempt</summary>

They contribute the image of the next boundary map and can make k-cycles into boundaries. Omitting them may report classes that would be filled in the intended complex.

</details>

## Record what you actually demonstrated

Copy [the response template](../curriculum/response_templates/07_response.md) to a new dated file in `my_work/`. Explain each output, attempt the two transfer questions, and complete the original independent coding tasks. A passed reference notebook is not a mastery score. The four outcomes above are assessed by explanation, calculation, implementation and critique; delayed recall remains a separate check.

**References:** The original stage's reading assignments remain authoritative for that stage. See [the core source ledger](../docs/SOURCES.md), [the geometry source ledger](../docs/SOURCES_V3.md), and [the v4 source and scope ledger](../docs/SOURCES_V4.md). The worked calculations and these questions are original course additions; theorem proof obligations remain explicit in the proof atlases.
