# Delayed retrieval: 39 new transfer questions

Try these with the lesson and reference code closed. The suggested review gaps (1, 3, 7, 14, 30 days) are a course-design convention, not a proven optimal schedule for every learner. A score must reflect your own work; seeing an answer is not recall. Three per stage provide a checkpoint, not exhaustive assessment.

## Stage 00

### 00.R1

An image has 8 rows and 8 columns. Explain how it can be one observation with 64 features, or 64 observations with spatial information.

<details><summary>Answer criteria — reveal after attempting</summary>

The observation unit depends on the question. In classification one image is a row with 64 intensities. In a pixel analysis pixels may be observations with coordinates/intensity. State which relationships the representation preserves.

</details>

### 00.R2

A notebook ran yesterday, but a fresh kernel gives NameError. What is your first reproducibility check?

<details><summary>Answer criteria — reveal after attempting</summary>

Restart the kernel and run cells from the top. Look for a missing import/definition or reliance on out-of-order state. Do not claim that the saved outputs establish reproducibility.

</details>

### 00.R3

What three things does a real-data picture fail to establish by itself?

<details><summary>Answer criteria — reveal after attempting</summary>

Examples include correct computation, ground-truth topology, stability, statistical significance, and generalization. Give three and say what additional evidence each requires.

</details>

## Stage 01

### 01.R1

Compute the inverse image of [4,9] for x↦x² on R, then change the declared domain to nonnegative reals.

<details><summary>Answer criteria — reveal after attempting</summary>

On R it is [−3,−2]∪[2,3]; on the nonnegative domain only [2,3]. Inverse image does not require an inverse function.

</details>

### 01.R2

Why does rank plus nullity equal the number of input coordinates rather than output coordinates?

<details><summary>Answer criteria — reveal after attempting</summary>

A basis of the kernel extends to a basis of the domain; the added basis images form a basis of the image. Thus dimension of the domain splits into nullity plus rank.

</details>

### 01.R3

State which parts of proving a relation is an equivalence relation must be checked. Apply this to equal parity.

<details><summary>Answer criteria — reveal after attempting</summary>

Reflexive, symmetric, transitive. Each integer has its own parity; equality of parity reverses; two equalities compose. The quotient has two classes, not a division of numbers.

</details>

## Stage 02

### 02.R1

Is d(x,y)=|x−y|² a metric? Use three explicit points.

<details><summary>Answer criteria — reveal after attempting</summary>

No. At 0,1,2 the distance from 0 to 2 is 4 while the sum through 1 is 2, violating the triangle inequality.

</details>

### 02.R2

Why does the finite set of 100 samples from a circle have a discrete induced metric topology?

<details><summary>Answer criteria — reveal after attempting</summary>

For each sample choose an open radius smaller than its minimum distance to another distinct sample. Every singleton and hence every subset is open. The inferred loop belongs to a constructed model, not the raw finite topology.

</details>

### 02.R3

Distinguish an open set in X from an open set in a subspace A⊆X using A=[0,1].

<details><summary>Answer criteria — reveal after attempting</summary>

A subset of A is relatively open when it is A∩U for ambient-open U. For example [0,1/2) is relatively open in A but not open in R.

</details>

## Stage 03

### 03.R1

Give the missing condition in: a continuous bijection is a homeomorphism.

<details><summary>Answer criteria — reveal after attempting</summary>

Its inverse must be continuous. A sufficient theorem is compact domain and Hausdorff codomain, but these are not part of the bare assertion.

</details>

### 03.R2

Prove continuity of g∘f using open sets, without drawing a graph.

<details><summary>Answer criteria — reveal after attempting</summary>

For open O, (g∘f)⁻¹(O)=f⁻¹(g⁻¹(O)); successive continuity makes it open. Name the intermediate spaces.

</details>

### 03.R3

Can projection be continuous while losing information? Explain the consequences for interpreting a 2D scatterplot.

<details><summary>Answer criteria — reveal after attempting</summary>

Yes; projection is continuous but usually not injective. Distinct high-dimensional observations may coincide. Apparent 2D shape is not automatically the original topology or distance structure.

</details>

## Stage 04

### 04.R1

Explain why a deformation retraction is not generally a homeomorphism.

<details><summary>Answer criteria — reveal after attempting</summary>

It gives a homotopy equivalence but may collapse many points onto one, as annulus radial segments collapse onto the circle. A homeomorphism is bijective with continuous inverse.

</details>

### 04.R2

Why are elements of the fundamental group not raw parameterized loops?

<details><summary>Answer criteria — reveal after attempting</summary>

Elements are based loops modulo based homotopy. Concatenation is well-defined on these classes, and reparameterizations/homotopies give associativity and inverse relations on classes.

</details>

### 04.R3

Does a digit classifier have to be invariant under all rotations because rotations form a group?

<details><summary>Answer criteria — reveal after attempting</summary>

No. A mathematical group action does not ensure label preservation. The scientific/task invariances must be justified; a rotation may change the written symbol or create an ambiguous image.

</details>

## Stage 05

### 05.R1

List every simplex in a filled triangle and then remove only the triangular face. What changes?

<details><summary>Answer criteria — reveal after attempting</summary>

Three vertices, three edges, one face; after removing the face the boundary remains. Counts change from (3,3,1) to (3,3,0), Euler characteristic from 1 to 0, and a nonbounding one-cycle appears.

</details>

### 05.R2

Four planar points generate a full abstract Rips simplex at a large scale. Why is that not a contradiction?

<details><summary>Answer criteria — reveal after attempting</summary>

The abstract simplex is determined by vertex subsets and has dimension three. Its geometric realization need not use the original planar coordinates as an affine simplex.

</details>

### 05.R3

Two bright pixels touch only at a corner. Are they connected in this course's closed-square union?

<details><summary>Answer criteria — reveal after attempting</summary>

Yes; they share a vertex. A four-neighbor pixel adjacency rule could answer differently. The image-to-space convention is part of the analysis, not an implementation detail.

</details>

## Stage 06

### 06.R1

Is every cycle a nonzero homology class? Explain with a filled triangle.

<details><summary>Answer criteria — reveal after attempting</summary>

No. The perimeter is a cycle but is also the boundary of the filled face, so its homology class is zero. H is cycles modulo boundaries.

</details>

### 06.R2

Why must boundaries be contained in cycles for homology to be defined this way?

<details><summary>Answer criteria — reveal after attempting</summary>

The quotient needs the boundary space to be a subspace of cycles. ∂²=0 supplies that inclusion. State which chain dimensions the maps connect.

</details>

### 06.R3

Your H1 code builds only vertices and edges. What kinds of classes can be wrong?

<details><summary>Answer criteria — reveal after attempting</summary>

Cycles filled by triangles in the intended complex would be falsely retained. Correct H1 needs the boundary map from C2; in general Hk needs k+1-dimensional simplices that can kill k-cycles.

</details>

## Stage 07

### 07.R1

What is the difference between the Rips and Čech triangle conditions?

<details><summary>Answer criteria — reveal after attempting</summary>

Rips requires all three pairwise distances below the edge threshold. Čech requires a common intersection of three balls at the declared radius. Pairwise overlap alone need not supply a common intersection.

</details>

### 07.R2

An alpha diagram has coordinates in squared-radius units. Can you compare them directly with Rips edge lengths?

<details><summary>Answer criteria — reveal after attempting</summary>

No. Identify and transform parameter conventions before comparing coordinates; even matched units do not make different filtrations equal.

</details>

### 07.R3

Why can sequential independent clusterings fail to be a filtration?

<details><summary>Answer criteria — reveal after attempting</summary>

A filtration requires nested objects with compatible inclusion maps. Recomputing clusters at each scale may split/reassign observations in ways that are not nested.

</details>

## Stage 08

### 08.R1

An interval is [2,5). At which of 1,2,4,5 is it alive? Explain the endpoint convention.

<details><summary>Answer criteria — reveal after attempting</summary>

Alive at 2 and 4, not 1 or 5. Birth is included and death excluded. Counts at tied filtration values depend on the declared convention.

</details>

### 08.R2

Why can two filtrations have identical Betti counts at each time yet different persistence?

<details><summary>Answer criteria — reveal after attempting</summary>

Counts omit the maps tracking which classes continue. For example [0,3)+[1,2) and [0,2)+[1,3) have identical count curves but different interval pairings.

</details>

### 08.R3

A bar reaches the maximum threshold your program computed. What may you conclude?

<details><summary>Answer criteria — reveal after attempting</summary>

It has not died in the computed filtration. It is not necessarily essential in a larger intended filtration. Separate computational truncation from a completed-domain essential class.

</details>

## Stage 09

### 09.R1

Trace the reduction of columns {0,1}, {1,2}, {0,2} over F₂.

<details><summary>Answer criteria — reveal after attempting</summary>

The first pivots at 1 and second at 2. The third XOR second becomes {0,1}, then XOR first becomes empty. Empty is a birth candidate; nonempty reduced columns pair their pivot row with the column.

</details>

### 09.R2

Why must faces precede cofaces even when filtration values tie?

<details><summary>Answer criteria — reveal after attempting</summary>

The boundary must refer to already present generators. Time/dimension/vertex ordering supplies a compatible order. A different valid tie order may alter representatives but not positive-length interval multisets.

</details>

### 09.R3

What three independent forms of evidence should support your implementation?

<details><summary>Answer criteria — reveal after attempting</summary>

Exact hand-derived fixtures, mathematical invariants such as ∂²=0 or Euler–Poincaré, and external-library agreement under aligned conventions. Repeated tests using one buggy routine are not independent evidence.

</details>

## Stage 10

### 10.R1

Derive why a point (b,d) can be matched to the diagonal at cost (d−b)/2 in L∞.

<details><summary>Answer criteria — reveal after attempting</summary>

For any t, d−b≤|d−t|+|t−b|≤2max(...). The midpoint t=(b+d)/2 attains the bound.

</details>

### 10.R2

What must stay fixed before using the image experiment's uniform perturbation bound?

<details><summary>Answer criteria — reveal after attempting</summary>

The underlying domain/cell complex, correspondence, filtration construction, homology dimension, and field. The measured change is in function values. Altering segmentation or resolution requires another analysis.

</details>

### 10.R3

A feature survives perturbation. Does that establish a biological mechanism or a statistically unusual signal?

<details><summary>Answer criteria — reveal after attempting</summary>

No. Stability is sensitivity to specified changes. Mechanistic meaning and significance require additional design, null models, independent observations and appropriate evidence.

</details>

## Stage 11

### 11.R1

Why must a scaler be fitted on training data rather than the concatenation of train and test?

<details><summary>Answer criteria — reveal after attempting</summary>

Test statistics would inform the representation and contaminate the evaluation. Fit on training, transform validation/test unchanged; refit on train+validation only after selection when the protocol permits.

</details>

### 11.R2

What choices affect a Mapper graph before any homology is computed?

<details><summary>Answer criteria — reveal after attempting</summary>

Observation representation/metric, lens, cover intervals and overlap, local clustering and its parameters, and nerve construction. The graph is a parameter-dependent summary, not an automatic recovered truth.

</details>

### 11.R3

A delay vector includes x(t+2τ), but your forecast is issued at t. What is wrong?

<details><summary>Answer criteria — reveal after attempting</summary>

That coordinate is unavailable at prediction time and leaks future information. Use an availability-aligned convention or move the forecast origin accordingly.

</details>

## Stage 12

### 12.R1

The supplied test labels and results are public in this archive. Is a new tuning experiment on this same test set an untouched evaluation?

<details><summary>Answer criteria — reveal after attempting</summary>

No. Reproducing known results is useful but does not create an unseen holdout. A new independent evaluation needs new reserved data or a clearly exploratory designation.

</details>

### 12.R2

Pixels plus topology got four extra correct predictions. What must you inspect before a general improvement claim?

<details><summary>Answer criteria — reveal after attempting</summary>

Paired disagreements, uncertainty, split construction, dependence/grouping, tuning history, replication and operating cost. A four-count difference alone is not universal or statistically significant evidence.

</details>

### 12.R3

What evidence is required before the course log says retained, and what does that status still not certify?

<details><summary>Answer criteria — reveal after attempting</summary>

A qualifying independent assessment and a qualifying delayed recall at least seven days later under the proposed policy. It records self-reported evidence, not externally graded mastery of the entire book or field.

</details>
