# Stage 09 guided session — Verify persistence without trusting the same algorithm twice

**Role:** Original v4 teaching supplement. It deepens the preserved lesson; it does not replace the book or its unavailable full text.

**Read first:** [Stage lesson](../lessons/09_lesson.md), then use this explanation before the [consolidation notebook](../consolidation/09_lab.ipynb). The [original workbook](../workbooks/09_workbook.md) and [worked lab](../notebooks/09_lab.ipynb) remain available. Repair earlier concepts only where needed; do not restart the whole course.

**Data and evidence:** Real Iris cloud with a deliberately duplicated observation and a deterministic permutation control.

## What you will be able to demonstrate

1. Explain what a boundary-column pivot represents.
2. Relate finite H0 death times to spanning-tree edge weights.
3. Handle duplicate observations and zero-length intervals explicitly.
4. State the dimension and scope actually checked by an independent oracle.

## Reduction is cancellation of a shared boundary term
In the binary boundary matrix, each column contains the indices of faces occurring in a simplex's boundary. The pivot of a nonzero reduced column is its largest remaining row. When two columns share that pivot, add one to the other modulo two. The shared row cancels. Continue until the column is zero or has a pivot not owned by an earlier column.

The algorithm requires a filtration-compatible ordering: faces precede cofaces, including at equal entry values. A zero reduced column indicates a birth; a pivot pairing identifies which earlier class the column kills. To understand this, trace a triangle by hand before inspecting a large matrix.

## H0 admits another route
Begin with every point in its own component. Add edges in increasing distance order. An edge joining different components merges them; an edge within a component does not. The selected merge edges form a minimum spanning tree for a connected complete weighted graph. Consequently their weights are the finite H0 death times when vertices are born at zero.

Our independent check uses dense Prim construction. It builds the tree by repeatedly connecting the cheapest point outside the current tree. It does not form simplices or reduce a homology boundary matrix. Agreement therefore tests a distinct path through the mathematics.

A spanning tree on n labeled points uses n−1 edges. Duplicate coordinates can give zero-length edges. The default persistent-homology report omits bars with exactly zero persistence, while the tree still contains those zero-weight merges. Filter only the zero weights when matching that reporting policy; do not silently remove the duplicated record from the source table.

## Use the real data and an adversarial control
On a small Iris point sample, compare the sorted positive tree weights with finite H0 death values. Then insert a duplicate point and repeat. Finally permute the point order. The merge-edge identities may change under ties, but the multiset of death times must match for the same metric filtration.

This check covers H0, not H1. It also does not verify the accuracy of the measured input coordinates. The image-oracle tests, exact square tests, oriented boundary identities, and optional external libraries cover complementary pieces. Good verification combines checks with different failure modes instead of presenting one successful comparison as proof of an entire system.

SciPy's sparse-graph convention treats zero as no edge in an ordinary dense adjacency matrix. That can erase genuine zero-distance relationships. Our small direct implementation avoids relying on that convention for duplicate coordinates. The source ledger links SciPy's documentation so you can inspect that boundary when choosing a different implementation.

## Predict, execute, and explain

### Step 1

Compare the spanning-tree calculation and boundary reduction on a small real cloud.

```python
from shape_lab.data import load_iris_data
from shape_lab.audits import h0_merge_times
from shape_lab.persistence import rips_filtration, persistent_homology, diagram
frame = load_iris_data().iloc[::10]
X = frame[[c for c in frame if c.endswith('_cm')]].to_numpy()
tree = h0_merge_times(X)
bars = diagram(persistent_homology(rips_filtration(X, max_homology=0)), 0, finite_only=True)
assert np.allclose(tree[tree>0], np.sort(bars[:,1]))
print('finite positive H0 deaths:', np.sort(bars[:,1]))
```

### Step 2

Insert a duplicate observation. Its zero-weight merge is retained by the tree but excluded by the positive-bar policy.

```python
duplicated = np.vstack([X, X[0]])
weights = h0_merge_times(duplicated)
assert len(weights)==len(duplicated)-1 and np.any(weights==0)
other = diagram(persistent_homology(rips_filtration(duplicated, max_homology=0)), 0, finite_only=True)
assert np.allclose(weights[weights>0], np.sort(other[:,1]))
```

### Step 3

Permutation should preserve the multiset of merge weights, including ties and zero merges.

```python
permutation = np.random.default_rng(19).permutation(len(duplicated))
assert np.allclose(h0_merge_times(duplicated[permutation]), weights)
result = {'original_records': len(X), 'with_duplicate': len(duplicated),
          'h0_tree_reduction_agreement': True, 'zero_weight_merges': int(np.sum(weights==0)),
          'h1_independently_verified_by_this_test': False}
```

## Transfer problems — attempt without the solution

### 09.T1

Does matching all H0 bars establish correctness of H1 persistence?

<details><summary>Reveal reasoning after your attempt</summary>

No. H0 concerns connected-component merges. H1 involves cycles and filling by triangles; it needs its own controls and comparisons.

</details>

### 09.T2

Why may tree edges differ while the persistence comparison still passes?

<details><summary>Reveal reasoning after your attempt</summary>

Tied edge lengths can permit multiple valid spanning trees. The finite death-time multiset, not the selected edge identities, is the invariant being compared.

</details>

## Record what you actually demonstrated

Copy [the response template](../curriculum/response_templates/09_response.md) to a new dated file in `my_work/`. Explain each output, attempt the two transfer questions, and complete the original independent coding tasks. A passed reference notebook is not a mastery score. The four outcomes above are assessed by explanation, calculation, implementation and critique; delayed recall remains a separate check.

**References:** The original stage's reading assignments remain authoritative for that stage. See [the core source ledger](../docs/SOURCES.md), [the geometry source ledger](../docs/SOURCES_V3.md), and [the v4 source and scope ledger](../docs/SOURCES_V4.md). The worked calculations and these questions are original course additions; theorem proof obligations remain explicit in the proof atlases.
