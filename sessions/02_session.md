# Stage 02 guided session — Separate units, distance, and topology

**Role:** Original v4 teaching supplement. It deepens the preserved lesson; it does not replace the book or its unavailable full text.

**Read first:** [Stage lesson](../lessons/02_lesson.md), then use this explanation before the [consolidation notebook](../consolidation/02_lab.ipynb). The [original workbook](../workbooks/02_workbook.md) and [worked lab](../notebooks/02_lab.ipynb) remain available. Repair earlier concepts only where needed; do not restart the whole course.

**Data and evidence:** Real Iris measurements, plus the exact counterexample 0,1,2.

## What you will be able to demonstrate

1. Check the metric axioms on an explicit counterexample.
2. Explain why positive coordinate rescaling preserves Euclidean-space topology but changes distance scale.
3. Compare nearest observations before and after a declared feature rescaling.
4. State the difference between distinct locations and distinct observation IDs.

## Distance is a rule, not a picture
A metric takes two points and returns a nonnegative number. It is zero exactly when the points are equal, symmetric in its arguments, and satisfies the triangle inequality. An open ball consists of points strictly closer than a chosen radius. Open sets in a metric space are sets around each of whose points some open ball fits inside the set.

For real numbers 0, 1, and 2, squared distance gives `d(0,2)=4` but `d(0,1)+d(1,2)=2`. That violates the triangle inequality. Squared distances are useful in other algorithms, but usefulness does not make them a metric. In contrast, absolute distance gives equality in this example and satisfies the axiom in general.

## Change a unit deliberately
Take coordinates `(length, width)` in centimetres. Multiplying only the first coordinate by ten gives `T(x,y)=(10x,y)`. This transformation is continuous and has continuous inverse `(u,v)→(u/10,v)`, so it is a homeomorphism of the plane. It preserves the Euclidean topology, but not numerical distances, round balls, or all nearest-neighbor relationships.

The distinction becomes crucial for persistence. Topology studies qualitative properties of a specified space. A Rips filtration uses quantitative distances. A transformation can preserve the topology of the ambient space and still change a dataset's persistence diagram. You should never infer full persistence invariance from homeomorphism alone.

## A finite sample is not the curve it resembles
For a finite set of distinct points, fix one point and find the smallest positive distance to the others. A ball with smaller radius contains only the chosen point. Every singleton is therefore open in the induced topology, and every subset is a union of open singletons. This finite space is discrete.

The claim does not mean a point-cloud analysis is useless. It means that recovering a continuous-looking structure requires an additional model, such as connecting nearby points and filling certain collections of connections. We will explicitly construct that model in Stage 07.

Two separate records can have identical feature coordinates. Euclidean distance then vanishes between distinct record IDs. On the ID set this is a pseudometric, not a metric. Retaining both records may be important for provenance. Treating duplicate locations as one point may be appropriate for another question. State the choice instead of letting an implicit deduplication determine it.

## Make the computation answer your question
In this notebook, select a small group of actual Iris records and rescale one feature. The scale change is intentional and not learned from test labels. Observe changed distances; do not demand that the nearest neighbor must change for every query. An invariant check and a sensitivity check answer different questions. A conclusion that depends on one arbitrary coordinate scale should be reported as such.

## Predict, execute, and explain

### Step 1

Show exactly why squared Euclidean distance fails one metric axiom.

```python
left = (0 - 2)**2
right = (0 - 1)**2 + (1 - 2)**2
print('squared-distance triangle inequality would require', left, '<=', right)
assert left > right
```

### Step 2

Select real measurements and compute pairwise distances with no labels in the feature array.

```python
from shape_lab.data import load_iris_data
from scipy.spatial.distance import cdist
frame = load_iris_data().iloc[::5].copy()
columns = [c for c in frame if c.endswith('_cm')]
X = frame[columns].to_numpy()
D = cdist(X, X)
Y = X.copy(); Y[:, 0] *= 10
D_scaled = cdist(Y, Y)
np.fill_diagonal(D, np.inf); np.fill_diagonal(D_scaled, np.inf)
changed = np.argmin(D, axis=1) != np.argmin(D_scaled, axis=1)
print('changed nearest-neighbor selections:', changed.sum(), 'of', len(X))
```

### Step 3

A translation is an isometry: it must preserve these Euclidean distances. Rescaling one coordinate is not.

```python
assert np.allclose(cdist(X + 100, X + 100), cdist(X, X))
assert not np.allclose(cdist(Y, Y), cdist(X, X))
result = {'records': len(X), 'rescaled_feature': columns[0], 'multiplier': 10,
          'nearest_neighbor_changes': int(changed.sum()),
          'translation_distance_check': 'passed'}
```

## Transfer problems — attempt without the solution

### 02.T1

Does multiplying all distances by three preserve the filtration at the same numeric threshold?

<details><summary>Reveal reasoning after your attempt</summary>

No. The same complex appears after multiplying the threshold by three. Persistence coordinates scale, while the ordering of simplex appearances is preserved.

</details>

### 02.T2

A feature table has two identical rows with different IDs. Which axiom fails when Euclidean distance is declared a metric on IDs?

<details><summary>Reveal reasoning after your attempt</summary>

Identity of indiscernibles: distinct IDs have zero distance. It is a pseudometric on IDs, although Euclidean distance remains a metric on distinct feature locations.

</details>

## Record what you actually demonstrated

Copy [the response template](../curriculum/response_templates/02_response.md) to a new dated file in `my_work/`. Explain each output, attempt the two transfer questions, and complete the original independent coding tasks. A passed reference notebook is not a mastery score. The four outcomes above are assessed by explanation, calculation, implementation and critique; delayed recall remains a separate check.

**References:** The original stage's reading assignments remain authoritative for that stage. See [the core source ledger](../docs/SOURCES.md), [the geometry source ledger](../docs/SOURCES_V3.md), and [the v4 source and scope ledger](../docs/SOURCES_V4.md). The worked calculations and these questions are original course additions; theorem proof obligations remain explicit in the proof atlases.
