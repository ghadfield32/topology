# Stage 03 guided session — A continuous map can discard the information you need

**Role:** Original v4 teaching supplement. It deepens the preserved lesson; it does not replace the book or its unavailable full text.

**Read first:** [Stage lesson](../lessons/03_lesson.md), then use this explanation before the [consolidation notebook](../consolidation/03_lab.ipynb). The [original workbook](../workbooks/03_workbook.md) and [worked lab](../notebooks/03_lab.ipynb) remain available. Repair earlier concepts only where needed; do not restart the whole course.

**Data and evidence:** Exact finite topology plus a noninjective projection demonstrated on actual Iris records.

## What you will be able to demonstrate

1. Use inverse images, rather than pictures alone, to define continuity.
2. Distinguish a continuous bijection from a homeomorphism.
3. Construct a projection that sends different inputs to the same output.
4. Explain why a finite numerical check cannot prove an infinite-space theorem.

## Maps have a domain and a codomain
A function assigns one output to each input in its domain. A continuous map respects the declared topologies: the inverse image of every open codomain set must be open in the domain. “Inverse image” does not require an inverse function. For `f(x)=x²`, the inverse image of `(1,4)` is `(-2,-1) ∪ (1,2)` even though the function is not one-to-one on the real line.

A homeomorphism is a bijection for which both the map and its inverse are continuous. The word “both” cannot be dropped. Give the same two-element set the discrete topology in the domain and the indiscrete topology in the codomain. The identity is a continuous bijection: the only codomain opens are empty and the whole set. Its inverse is not continuous because a singleton is open on one side but not the other.

## Work a loss-of-information example
Projection `P(x,y)=x` is continuous. Points `(2,1)` and `(2,9)` both map to 2. No function of the projected value alone can recover which original point was used. This is not a small numerical error; the map has discarded information. A linearly projected representation can still be useful, but it is not automatically topologically equivalent to the original object.

The real-data experiment drops three of the four Iris measurements. Records with the same first coordinate can collapse together even when their full measurement vectors differ. We search for such a pair and display it. The example illustrates noninjectivity. It does not establish the entire topology of the distribution from which flowers were sampled.

## Compactness is about every open cover
An open cover is a collection of open sets whose union contains the space. Compactness means that every such cover has a finite subcollection still covering it. This definition includes an “every,” so checking a handful of covers cannot prove it in an infinite space. In finite spaces compactness is automatic: select at most one covering set for each point.

For a compact space X and a Hausdorff space Y, a continuous bijection `f:X→Y` is a homeomorphism. The proof route is: closed subsets of X are compact; their continuous images are compact; compact subsets of a Hausdorff space are closed; consequently f maps closed sets to closed sets, which makes its inverse continuous. The main lesson and proof atlas develop these steps. Do not replace this reasoning with a plot of a smooth-looking curve.

## What the machine can establish here
The finite topology checker exhaustively evaluates the relevant sets for its tiny finite inputs. That is a complete check for those declared finite examples. The projection calculation is an exact counterexample to injectivity. Neither is a numerical proof of all theorems about arbitrary spaces. Learning to match the strength of evidence to the statement is part of learning mathematics.

## Predict, execute, and explain

### Step 1

Check a continuous bijection whose inverse is not continuous on the declared two-point topologies.

```python
from shape_lab.topology import powerset, is_continuous
X = [0, 1]
discrete = powerset(X); indiscrete = [set(), set(X)]
identity = {0: 0, 1: 1}
forward = is_continuous(X, discrete, X, indiscrete, identity)
backward = is_continuous(X, indiscrete, X, discrete, identity)
print('forward continuous:', forward, 'inverse continuous:', backward)
assert forward and not backward
```

### Step 2

Find actual measurement vectors that collide when only sepal length is retained.

```python
from shape_lab.data import load_iris_data
frame = load_iris_data()
columns = [c for c in frame if c.endswith('_cm')]
pair = None
for _, group in frame.groupby('sepal_length_cm'):
    unique = group.drop_duplicates(columns)
    if len(unique) >= 2:
        pair = unique.iloc[:2]; break
assert pair is not None
display(pair[['sample_id'] + columns])
X = pair[columns].to_numpy()
print('full distance:', np.linalg.norm(X[0]-X[1]))
print('projected distance:', abs(X[0,0]-X[1,0]))
```

### Step 3

Store the precise property demonstrated, not an exaggerated conclusion about the whole dataset.

```python
result = {'forward_continuous': bool(forward), 'inverse_continuous': bool(backward),
          'colliding_sample_ids': pair.sample_id.astype(int).tolist(),
          'claim': 'Declared projection is noninjective on this pair; no population-topology claim.'}
```

## Transfer problems — attempt without the solution

### 03.T1

Why does P(x,y)=x have an inverse image operation even though it has no two-sided inverse?

<details><summary>Reveal reasoning after your attempt</summary>

The inverse image of a set collects every input whose output lies in that set; this is defined for any function. A two-sided inverse requires bijectivity.

</details>

### 03.T2

Does a successful exhaustive finite-space check prove the analogous statement for all compact spaces?

<details><summary>Reveal reasoning after your attempt</summary>

No. It verifies the enumerated finite example. An arbitrary-space statement needs its hypotheses and a general argument; infinite quantifiers are not exhausted by the finite test.

</details>

## Record what you actually demonstrated

Copy [the response template](../curriculum/response_templates/03_response.md) to a new dated file in `my_work/`. Explain each output, attempt the two transfer questions, and complete the original independent coding tasks. A passed reference notebook is not a mastery score. The four outcomes above are assessed by explanation, calculation, implementation and critique; delayed recall remains a separate check.

**References:** The original stage's reading assignments remain authoritative for that stage. See [the core source ledger](../docs/SOURCES.md), [the geometry source ledger](../docs/SOURCES_V3.md), and [the v4 source and scope ledger](../docs/SOURCES_V4.md). The worked calculations and these questions are original course additions; theorem proof obligations remain explicit in the proof atlases.
