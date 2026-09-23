# Stage 00 guided session — Read a measurement before calculating with it

**Role:** Original v4 teaching supplement. It deepens the preserved lesson; it does not replace the book or its unavailable full text.

**Read first:** [Stage lesson](../lessons/00_lesson.md), then use this explanation before the [consolidation notebook](../consolidation/00_lab.ipynb). The [original workbook](../workbooks/00_workbook.md) and [worked lab](../notebooks/00_lab.ipynb) remain available. Repair earlier concepts only where needed; do not restart the whole course.

**Data and evidence:** Real Iris measurements; the three-number mean is an explicitly constructed arithmetic example.

## What you will be able to demonstrate

1. Identify one observation, one measured feature, one label, and a source identifier.
2. Explain the two axes of a table and the three axes of an image collection.
3. Produce a small descriptive result with explicit units and a reproducible row selection.
4. Distinguish executing a reference solution from demonstrating your own understanding.

## Begin with a single row
Imagine a notebook containing measurements of flowers. One row represents one recorded specimen. A column such as sepal length is a measurement, expressed in centimetres. A species name is a label. A row identifier tells us which record we used; it is not another measurement of the flower. Before making a graph, say what each of these means.

The notation `X[i, j]` means: take row `i` and column `j` from an array named `X`. Python starts counting at zero, so `X[0, 1]` is in the first row and second column. A table with 150 observations and four measurements has shape `(150, 4)`. Its shape describes how numbers are arranged, not the physical shape of the flowers.

Selecting measurement columns explicitly avoids a subtle error. If we put an arbitrary specimen number into a Euclidean distance calculation, renumbering the specimens changes the distances. If we put the species label into that calculation, observations may appear close partly because we supplied the answer. Neither is a neutral analysis of the measured features.

## Calculate one statistic by hand
For three lengths 2, 3, and 7 centimetres, the mean is `(2+3+7)/3 = 4` centimetres. The mean has the same unit as its inputs. The deviations are -2, -1, and 3 centimetres and sum to zero. This does not establish a distribution, a causal explanation, or representativeness of a population. It is a descriptive calculation on three records.

Now consider two observations `[2, 1]` and `[5, 5]`, with both coordinates in centimetres. Their displacement is `[3, 4]` centimetres and Euclidean distance is `sqrt(3²+4²)=5` centimetres. We have made a choice: differences in these two measurements are being combined using the Euclidean rule. Later stages investigate that choice rather than treating it as the only definition of similarity.

## Read a program as a small argument
An import brings a named tool into the notebook. An assignment stores a value under a name. A function applies a rule to inputs and returns an output. An assertion states something that must hold for this particular run. `assert X.shape[1] == 4` checks that there are four selected measurement columns; it does not prove that every measurement was collected correctly.

A result is easier to trust when you can identify its input records and the operation that produced it. Keep the specimen IDs next to your outputs even though they are excluded from the metric. When you change a selection, state the change before running the calculation. Avoid replacing real data with generated values just to obtain a prettier graph.

## The first learning record
Write a short answer containing your prediction, the observed output, and one correction to your prediction. A mismatch is useful information. The shipped course has no completed learner assessments, even though its reference notebooks have executed successfully. Your evidence starts with work you actually do, not with inheriting the author's outputs.

## Predict, execute, and explain

### Step 1

Load the bundled table. Select only columns whose names declare centimetres. The ID and labels stay available but do not enter X.

```python
from shape_lab.data import load_iris_data
frame = load_iris_data()
columns = [c for c in frame.columns if c.endswith('_cm')]
X = frame[columns].to_numpy()
print('table:', frame.shape, 'measurements:', X.shape)
display(frame.head(3))
assert X.shape == (150, 4)
```

### Step 2

Verify a familiar mean manually, then calculate the corresponding descriptive summaries of the actual records.

```python
example_cm = np.array([2., 3., 7.])
assert example_cm.mean() == 4
summary = frame[columns].agg(['min', 'mean', 'max'])
display(summary)
result = {'rows': len(frame), 'measurement_columns': columns,
          'units': 'centimetres', 'labels_used_as_features': False}
```

### Step 3

A simple plot lets you inspect individual measurements. It is not evidence that row order is time.

```python
import matplotlib.pyplot as plt
plt.figure(figsize=(7, 3.5))
plt.plot(frame['sample_id'], frame['sepal_length_cm'], '.', markersize=4)
plt.xlabel('Record ID (not time)'); plt.ylabel('Sepal length (cm)')
plt.title('One measured feature in the bundled Iris table'); plt.tight_layout(); plt.show()
```

## Transfer problems — attempt without the solution

### 00.T1

Why is a 150 by 4 array not a statement that the underlying objects live on a four-dimensional manifold?

<details><summary>Reveal reasoning after your attempt</summary>

Array width counts selected features. Manifold dimension is a local structural property; neither dimension nor manifold assumptions follow from the table shape.

</details>

### 00.T2

Would adding 1000 to every sample ID change your feature distances? Explain both the correct and incorrect implementations.

<details><summary>Reveal reasoning after your attempt</summary>

Correct: IDs are excluded, so distances do not change. Adding a common constant to an incorrectly included ID column also preserves its pairwise differences; that test alone does not expose the mistake. Arbitrarily permuting or rescaling IDs can expose it. IDs remain invalid measurement coordinates even if one translation test passes.

</details>

## Record what you actually demonstrated

Copy [the response template](../curriculum/response_templates/00_response.md) to a new dated file in `my_work/`. Explain each output, attempt the two transfer questions, and complete the original independent coding tasks. A passed reference notebook is not a mastery score. The four outcomes above are assessed by explanation, calculation, implementation and critique; delayed recall remains a separate check.

**References:** The original stage's reading assignments remain authoritative for that stage. See [the core source ledger](../docs/SOURCES.md), [the geometry source ledger](../docs/SOURCES_V3.md), and [the v4 source and scope ledger](../docs/SOURCES_V4.md). The worked calculations and these questions are original course additions; theorem proof obligations remain explicit in the proof atlases.
