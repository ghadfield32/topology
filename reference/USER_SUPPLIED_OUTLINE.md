Geoff, let’s turn this into a **complete, mastery-based course that we work through here**, rather than a collection of books and videos.

The structure will be:

**Understand the idea → state it precisely → work an example by hand → implement it → test it → explain its limitations.**

Your attached outline already gives us the right broad progression—topology, algebraic topology, and topological data analysis—and identifies understanding, proofs, computation, interpretation, and application as the completion criteria. We will preserve that structure while making the assignments and assessment much more explicit.

One scope clarification: **this is a curriculum for the topics in the supplied table of contents, not a claim that I have examined the complete book.** The listing you provided says March 2027; I could not independently recheck the publisher’s page today. When you have the actual text, the final step will be a chapter-by-chapter coverage audit.

# 1. What we are working toward

By the end, you should be able to take an unfamiliar dataset and explain:

> “Here is what an observation represents, why this distance makes sense, how I constructed a mathematical representation of shape, what its persistent features mean, which conclusions are supported, and whether the approach adds anything beyond simpler methods.”

You should also be able to calculate the underlying mathematics on small examples without relying on a library.

I recommend a **24-week core plan at approximately 8–10 hours per week**, giving a planning budget of 192–240 hours. That is my proposed workload, not a guarantee about learning speed. Strong prerequisite performance can shorten the beginning; difficult proofs or implementation problems can extend a unit.

**Progress is determined by demonstrated understanding, not the calendar.**

## How the course maps to the book

This mapping is based on the chapter titles you supplied.

| Book materialWhere we cover it                                    |                                        |
| ----------------------------------------------------------------- | -------------------------------------- |
| Appendix A: mathematical toolbox                                  | Unit 1, with targeted refreshers later |
| Closeness, good maps, combination, paths, loops, deformation      | Units 2–4                              |
| Surfaces, simplices, homology, Betti numbers                      | Units 5–6                              |
| Changing spaces, filtrations, persistence, barcodes, diagrams     | Units 7–9                              |
| Shape from data and reliability of inferred structure             | Units 7 and 10                         |
| Seeing structure, real-world applications, continuing the journey | Units 11–12                            |

Mapper, machine-learning evaluation, and the software-testing requirements below are **applied extensions I am adding**. They are useful for your goals, but I am not claiming that the book develops each of them in the same detail.

---

# 2. The resource system: one main course, one rigorous reference

We should not attempt to read every resource in the attachment cover to cover.

Use this small core:

| RoleFree resourceHow we will use it |                                                                         |                                                                                                                                                                                                                                                                                                                                                                  |
| ----------------------------------- | ----------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Primary teaching sequence**       | Raphaël Tinarrage, *Topological Data Analysis with Persistent Homology* | Lessons 0–11, selected exercises, and the accompanying notebooks. The course provides videos and corrections for its programming tutorials. ([Raphaël Tinarrage](https://raphaeltinarrage.github.io/EMAp.html "EMAp Summer Course"))                                                                                                                             |
| **Formal reference and assessment** | ETH Zürich, *Introduction to Topological Data Analysis*, 2026           | Mathematical definitions, proofs, algorithms, and chapter-end oral-exam questions. Its notes cover topology through persistence, point-cloud complexes, stability, Mapper, and applications. ([Theoretical Computer Science Institute](https://ti.inf.ethz.ch/ew/courses/TDA26/index.html "TDA 2026 (Theory of Combinatorial Algorithms, ETH Zürich)"))          |
| **Topology clarification**          | Sidney Morris, *Topology Without Tears*                                 | Extra explanations and exercises when open sets, continuity, or proof-writing need more practice. The author also provides accompanying videos. ([Topology Without Tears](https://www.topologywithouttears.net/ "Topology Without Tears by Sidney A. Morris. Topology book and Videos on Pure Mathematics, Topology and Writing Proofs supplementing the book")) |
| **First computational tool**        | Ripser.py                                                               | Small point-cloud persistence experiments and comparison against your own implementation. Its documentation includes interactive examples. ([Ripser](https://ripser.scikit-tda.org/en/latest/ "Setup — Ripser.py 0.6.15 documentation"))                                                                                                                         |
| **Broader computational tool**      | GUDHI                                                                   | Explicit complexes, alternative filtrations, cubical data, diagram distances, and machine-learning representations. ([GUDHI library](https://gudhi.inria.fr/python/latest/index.html "GUDHI Python modules documentation — gudhi v3.13.0 documentation"))                                                                                                        |

Use **Hammack, MIT linear algebra, Judson, and Hatcher only where assigned below**.

An important correction to the earlier outline: ETH lists **discrete mathematics, algorithms and data structures, and linear algebra** as prerequisites—not just linear algebra. We will check those foundations explicitly rather than discovering gaps during persistent-homology algorithms. ([Theoretical Computer Science Institute](https://ti.inf.ethz.ch/ew/courses/TDA26/index.html "TDA 2026 (Theory of Combinatorial Algorithms, ETH Zürich)"))

---

# 3. How every unit will work in this chat

Each unit will have the same learning cycle.

| StepWhat happens hereYour evidence of understanding |                                                                      |                                                        |
| --------------------------------------------------- | -------------------------------------------------------------------- | ------------------------------------------------------ |
| **Intuition**                                       | We introduce the problem and compare examples and counterexamples.   | Explain the concept in your own words.                 |
| **Formalization**                                   | We introduce definitions, notation, and assumptions.                 | State the definition and identify a nonexample.        |
| **Reasoning**                                       | We work through a proof or hand calculation.                         | Complete a related problem independently.              |
| **Computation**                                     | We translate the concept into a small Python experiment.             | Produce the expected output and explain it.            |
| **Critique**                                        | We deliberately change assumptions, data, or parameters.             | Explain what changes, what should not change, and why. |
| **Assessment**                                      | You solve unfamiliar questions without following the worked example. | Pass the unit’s mastery check.                         |

For a typical week, budget roughly two hours for reading or video, three for exercises and proofs, two for computation, and one for retrieval practice and corrections.

**We will not treat generated code as verified merely because it looks plausible.** Execution results, test outputs, mathematical arguments, and interpretations will be recorded separately.

A proof with an unresolved step stays unresolved. A notebook that runs but gives an unexplained answer is not yet a passed assignment.

---

# 4. The full learning path

## Unit 1 — Mathematical language and computational foundations

**Weeks 1–2**

### What to learn

Start with sets, functions, images and inverse images, relations, equivalence classes, quantifiers, and proof techniques. Then review vector spaces, bases, linear maps, kernels, images, rank, and nullity.

For algorithms, review graphs, connected components, sorting, and basic time and memory complexity.

Use selected sections of Hammack’s *Book of Proof*: sets and logic; direct proof, contradiction, and counterexamples; relations; and functions. The official site provides the free text and its chapter contents. Use MIT’s linear algebra course for any gaps in matrix reasoning. ([Richard Hammack](https://richardhammack.github.io/BookOfProof/ "Book of Proof"))

### What you will do

Write short proofs about sets and functions. Calculate kernels and images of small matrices by hand, then verify them numerically. Explain the difference between showing several examples and proving a universal statement.

Create a small learning workspace with separate places for notes, exercises, notebooks, tests, and results. Use one isolated Python environment; record and lock working dependency versions after the first successful smoke test.

### Completion gate

You can explain what a quotient does—grouping objects considered equivalent—and why the distinction between a kernel and an image will matter later.

You can also recognize an invalid argument even when its conclusion happens to be true.

**Do not spend weeks relearning Python. This unit is about mathematical reasoning.**

---

## Unit 2 — Distance, neighborhoods, and topological spaces

**Weeks 3–4**

### What to learn

Study metrics, open balls, neighborhoods, open and closed sets, topology axioms, bases, and subspace topology.

The central question is:

> “Which information comes from numerical distances, and which information only depends on the resulting notion of neighborhood?”

Read Tinarrage Lesson 1, working its assigned Exercises 4 and 5. Use Morris for reinforcement.

### What you will do

Compare Euclidean, Manhattan, and maximum-distance neighborhoods. Construct several different topologies on a small finite set.

Prove that squared Euclidean distance is not generally a metric. Prove that a finite set of distinct points, with its usual induced metric topology, is discrete.

That second exercise addresses an important TDA distinction: a sampled circle is a finite set of observations; the continuous-looking shape is something we construct or infer from those observations. The point-cloud-to-complex step is therefore substantive, not cosmetic. ([arXiv](https://arxiv.org/html/1710.04019v2 "An introduction to Topological Data Analysis: fundamental and practical aspects for data scientists"))

### Completion gate

You can distinguish a dataset, its metric, its topology, and an inferred underlying shape.

You can explain why a set can be open and closed simultaneously, and why “open” depends on the ambient space.

---

## Unit 3 — Continuity, good maps, connectedness, and compactness

**Weeks 5–6**

### What to learn

Study continuity through inverse images of open sets, continuous bijections, homeomorphisms, connectedness, path-connectedness, compactness, and the Hausdorff property.

A **homeomorphism** requires a continuous bijection with a continuous inverse. Merely being continuous and bijective is not enough in general. These distinctions belong to the mathematical foundations developed in the ETH notes.

Read Tinarrage Lesson 2 and complete its assigned Exercises 8 and 11. Use Morris for the additional point-set topology topics.

### What you will do

Prove that compositions of continuous maps are continuous. Construct a homeomorphism between two suitable intervals. Explore why identifying endpoints changes an interval into a different space.

Work through the theorem that a continuous bijection from a compact space to a Hausdorff space is a homeomorphism, identifying where each assumption is used.

### Completion gate

Given two spaces and a proposed map, you can say exactly what must be checked.

You can distinguish:

**distance-preserving equivalence, topological equivalence, and the weaker deformation-based equivalence introduced next.**

---

## Unit 4 — Groups, actions, paths, loops, and homotopy

**Weeks 7–8**

### What to learn

Study group operations, identity, inverses, subgroups, homomorphisms, and simple group actions. Then connect these ideas to paths, loops, homotopies, deformation retracts, homotopy equivalence, and the fundamental group.

Use selected group-theory material from Judson, Tinarrage Lesson 3, and the introductory portions of Hatcher’s Chapters 0 and 1. Judson’s text is openly available, and Hatcher provides free individual chapters. ([Judson Books](https://judsonbooks.org/abstract-algebra-theory-and-applications/ "Abstract Algebra: Theory and Applications – Judson Books"))

### What you will do

Model rotations and reflections of a square as operations. Determine which operations commute.

Construct a deformation of an annulus onto a circle. Explain why a disk can contract to a point but a circle cannot.

Study how loop concatenation becomes a group operation after passing to the appropriate homotopy classes. Work through winding-number examples rather than treating “loops form a group” as a slogan.

### Completion gate

You can distinguish **homeomorphism from homotopy equivalence** using examples.

You can explain why counting visible holes is not enough to prove that two arbitrary spaces are homeomorphic.

**Depth boundary:** covering-space theory and a full treatment of van Kampen’s theorem are extensions, not prerequisites for finishing the core TDA course.

---

## Unit 5 — Surfaces and the combinatorial language of shape

**Weeks 9–10**

### What to learn

Study surfaces, boundary, orientability, genus, polygon identifications, triangulations, simplices, and simplicial complexes.

Distinguish a geometric realization from an abstract complex: coordinates describe one realization, while the abstract complex records which collections of vertices form simplices. The face and intersection requirements are essential to the definition.

Read Tinarrage Lesson 4 and work its assigned Exercises 20 and 25.

### What you will do

Represent an interval, triangle boundary, filled triangle, tetrahedron boundary, and filled tetrahedron as collections of simplices.

Write a small validator that checks whether all required faces are present.

For surfaces, compare a sphere, torus, cylinder, and Möbius strip. Learn how boundary and orientability distinguish examples that informal “hole counting” can confuse.

### Completion gate

You can explain the difference between:

- A triangular loop and a filled triangle.
- A tetrahedron’s surface and its filled interior.
- A graph and its clique complex.

These distinctions must appear correctly in both your drawings and your data structures.

---

## Unit 6 — Chains, boundaries, homology, and Betti numbers

**Weeks 11–12**

### What to learn

This is the algebraic center of the course.

Learn chain groups, boundary maps, cycles, boundaries, quotient spaces, homology, and Betti numbers. Begin with coefficients in `\mathbb F_2`, the field with two elements.

The essential relationships are

```math
Z_k=\ker \partial_k,\qquad B_k=\operatorname{im}\partial_{k+1},
```

```math
H_k=Z_k/B_k,\qquad \beta_k=\dim_{\mathbb F}H_k.
```

For finite complexes over a field,

```math
\beta_k = \dim C_k-\operatorname{rank}(\partial_k) -\operatorname{rank}(\partial_{k+1}).
```

The quotient is valid because a boundary is always a cycle: `\partial_k\partial_{k+1}=0`.

### What you will do

Use Tinarrage Lessons 5–6 and their assigned exercises. Build boundary matrices and implement elimination over `\mathbb F_2`.

Work through this small example completely:

**Triangle boundary:** three edges, with boundary-map rank two, produce one independent one-dimensional homology class.

**Filled triangle:** adding the triangular face makes that cycle a boundary, so its `H_1` class disappears.

### Completion gate

You can prove that boundary-of-boundary is zero and compute small homology examples without a library.

You must also explain why ordinary real-valued matrix rank cannot automatically replace rank over `\mathbb F_2`.

A correction to the earlier intuitive description: Betti numbers measure dimensions of homology groups. “Enclosed voids” is a useful picture in some settings, not the general definition of `\beta_2`.

---

## Unit 7 — Building shape from data and constructing filtrations

**Weeks 13–14**

### What to learn

Study proximity graphs, Vietoris–Rips complexes, Čech complexes, Delaunay/alpha constructions, covers and nerves, and filtrations.

We will use the explicit Rips convention

```math
\sigma\in\mathrm{VR}_{\epsilon}(X) \quad\Longleftrightarrow\quad d(x_i,x_j)\leq\epsilon \text{ for every pair of vertices in }\sigma.
```

For Čech complexes, membership depends on a common intersection of the relevant balls—not merely pairwise overlap. These constructions and their relationships are developed in ETH Chapter 5.

### What you will do

Generate small synthetic datasets: separated clusters, a circle, a disk, and a figure-eight. Construct complexes at several thresholds and predict their homology before computing it.

Use Tinarrage Lessons 7–8 and the associated tutorial. Compare a Rips construction with an alpha construction on a small Euclidean dataset.

Keep scale conventions explicit: GUDHI’s default alpha filtration uses squared-radius values, so its raw filtration coordinates should not be compared blindly with edge-distance thresholds. ([GUDHI library](https://gudhi.inria.fr/python/latest/delaunay_complex_user.html "Delaunay complex user manual — gudhi v3.13.0 documentation"))

### Completion gate

You can defend why a particular complex is appropriate and state the assumptions behind an inference from the complex to an underlying shape.

You can distinguish **distance scale, function threshold, and chronological time** as different possible filtration parameters.

---

## Unit 8 — Persistent homology, barcodes, and diagrams

**Weeks 15–16**

### What to learn

Study inclusion-induced maps, persistence modules, birth and death, persistence intervals, barcodes, diagrams, multiplicities, and essential classes.

The central object is not just a sequence of hole counts. It includes maps:

```math
H_k(K_0)\longrightarrow H_k(K_1) \longrightarrow H_k(K_2)\longrightarrow\cdots.
```

Those maps tell us which classes survive between stages. Persistent homology records more than separate Betti numbers at each threshold.

Use Tinarrage Lesson 9 and its assigned Exercise 52.

### What you will do

Construct a filtration by hand. Draw its barcode and convert that barcode into a diagram. Work backward from a diagram to statements about which features are present at specified scales.

Use a square as an exact test case. For four vertices of a unit square under our Rips convention, the perimeter loop exists for

```math
1\leq\epsilon<\sqrt 2.
```

At `\sqrt2`, the diagonals and higher simplices enter and the loop is filled. Derive this directly from the pairwise distances and simplex rule.

### Completion gate

You can interpret every interval in a small example.

You can also explain why an interval reaching the end of a truncated computation does **not** prove that the feature would survive all larger scales.

---

## Unit 9 — Implementing persistent homology and checking correctness

**Weeks 17–18**

### What to learn

Study filtration-compatible simplex ordering, boundary-matrix construction, column reduction, pivots, persistence pairing, and union-find for `H_0`.

Use ETH’s algorithm section and Tinarrage’s practical persistence tutorial. ETH explicitly describes ordering equal-time simplices by dimension before performing matrix reduction.

### What you will build

Implement a deliberately small educational pipeline:

**point cloud → distances → Rips simplices → ordered filtration → boundary matrix → reduction → persistence intervals.**

Begin with hand-checkable examples. Then compare against Ripser and GUDHI.

Do not optimize prematurely. The purpose of this implementation is understanding and testability, not competing with established libraries.

### Completion gate

Your implementation agrees with hand-derived results and the libraries after aligning coefficient fields, filtration conventions, dimensions, truncation, and zero-length-interval policies.

Keep the output of a library’s representative **cocycle** distinct from an automatically recovered geometric loop; Ripser documents representative cochains as a separate computational output. ([Ripser](https://ripser.scikit-tda.org/en/latest/ "Setup — Ripser.py 0.6.15 documentation"))

**This unit is not passed merely because one noisy circle produces a plausible diagram.**

---

## Unit 10 — Stability, noise, uncertainty, and justified interpretation

**Weeks 19–20**

### What to learn

Study bottleneck distance, Wasserstein distance, matching to the diagonal, interleavings, sampling effects, outliers, and statistical uncertainty.

A central stability statement compares tame sublevel-set filtrations on the same suitable space:

```math
d_B\bigl(\mathrm{Dgm}_k(f),\mathrm{Dgm}_k(g)\bigr) \leq \|f-g\|_\infty.
```

We will state the hypotheses and explain the result before studying its proof structure. We will not apply it indiscriminately to unrelated metrics or arbitrary preprocessing pipelines.

### What you will do

Use Tinarrage Lesson 10 and Exercise 53. Perturb controlled datasets using coordinate noise, missing samples, outliers, and changes in sampling density.

Separate three questions:

**Did the computation work? Is the descriptor stable? Is the detected structure scientifically meaningful?**

Read the statistical sections of Chazal and Michel’s introduction. Their treatment separates deterministic stability from statistical questions such as significance, uncertainty, and robustness. ([arXiv](https://arxiv.org/html/1710.04019v2 "An introduction to Topological Data Analysis: fundamental and practical aspects for data scientists"))

### Completion gate

You can explain why a long-lived feature is a candidate for investigation—not automatic proof of a meaningful mechanism.

You can design a suitable comparison or null experiment and identify what uncertainty remains.

---

## Unit 11 — Turning topology into useful analysis

**Weeks 21–22**

This is where we connect the mathematics to your Python and machine-learning background.

### What to learn

Study diagram summaries, Betti curves, persistence landscapes, persistence images, and model-ready representations. GUDHI provides several such representations and interfaces for combining them with machine-learning workflows. ([GUDHI library](https://gudhi.inria.fr/python/latest/representations.html "Representations manual — gudhi v3.13.0 documentation"))

Also learn the basic Reeb-graph and Mapper constructions: a chosen function or “lens,” a cover of its range, clustering within preimages, and connections induced by overlap. These are covered in ETH Chapter 7.

### What you will do

Choose one primary lab and one short comparison.

For the primary lab, compare a conventional feature baseline, topological features alone, and their combination.

For the comparison, use either a Mapper parameter-sensitivity experiment, a cubical-complex image example, or a delay-coordinate time-series example. GUDHI supports cubical complexes and time-series embedding utilities. ([GUDHI library](https://gudhi.inria.fr/python/latest/index.html "GUDHI Python modules documentation — gudhi v3.13.0 documentation"))

### Completion gate

You can explain exactly what the topological features add—or report that they add nothing useful.

For our evaluation protocol, preprocessing and parameter selection stay inside the appropriate training procedure. Split by the real independent unit: person, session, recording, or time period as appropriate.

**A visually interesting graph is not, by itself, a successful analysis.**

---

## Unit 12 — Independent capstone and book reconciliation

**Weeks 23–24**

### What you will do

Choose a new dataset or a substantially new problem formulation. State the research question before exploring persistence diagrams.

Prepare a short report that covers the observation unit, metric, preprocessing, complex, filtration, coefficients, homology dimensions, software versions, validation, sensitivity analysis, and conclusion.

Then defend the analysis in an oral-style discussion here. Questions should include:

> Why this metric? What could produce the same pattern? Which assumptions matter? What would falsify your interpretation? Would you still recommend the method after accounting for its cost?

### Author-specific reading

At this stage, read Diamantis’s freely available *The Shape of Data: Topology Meets Analytics*. It presents applied examples and introduces a proposed Topological Stability Index derived from persistence lifetimes. Treat it as a paper to examine critically, not as a substitute for the formal stability theory or statistical validation. ([arXiv](https://arxiv.org/abs/2511.13503 "\[2511.13503] The Shape of Data: Topology Meets Analytics. A Practical Introduction to Topological Analytics and the Stability Index (TSI) in Business"))

### Completion gate

You can reproduce the analysis, defend its choices, and clearly distinguish results from speculation.

Once the actual book is available, compare each chapter against your completed work. Any unfamiliar definition, example, argument, or application becomes a specific remaining assignment rather than an assumed pass.

---

# 5. The practical test suite we should build

The attachment correctly recommends implementing the mathematics before relying entirely on libraries. We will retain that project but make its correctness requirements more demanding.

## Mathematical checks

Every constructed complex must contain its required faces. Every boundary-matrix pair must satisfy

```math
\partial_k\partial_{k+1}=0.
```

Calculated Betti numbers must be nonnegative and agree with hand-derived examples. For finite complexes, the alternating simplex count must agree with the alternating Betti-number sum. These follow from the finite chain-complex framework developed in the homology material.

## Implementation checks

Our proposed test suite should include disconnected points, a tree, an unfilled triangle, a filled triangle, the square filtration, a tetrahedron boundary, and a filled tetrahedron.

It should also include deliberate failure cases: missing faces, invalid ordering, duplicate observations, inconsistent distance inputs, and insufficient maximum simplex dimension.

For an `H_k` computation, we must account for `(k+1)`-simplices that can kill `k`-dimensional classes. A graph-only calculation is not automatically a correct Rips `H_1` calculation because a Rips complex includes cliques as higher-dimensional simplices. ([GUDHI library](https://gudhi.inria.fr/python/latest/rips_complex_user.html "Rips complex user manual — gudhi v3.13.0 documentation"))

## Invariance and sensitivity checks

Reordering observations should not change the mathematical result. Translating or rotating a Euclidean point cloud preserves pairwise distances, so it should preserve its distance-based filtration. Uniform rescaling should rescale filtration coordinates under our distance convention.

By contrast, an arbitrary shape deformation can preserve topology while changing distances and therefore changing persistence coordinates. Deriving that distinction will be one of your test explanations.

**Library agreement is one source of evidence. Hand calculations and mathematical identities are independent sources. We want all three.**

---

# 6. How we will connect this to your work

I recommend **one controlled synthetic project before one sports or computer-vision project**. That prevents application complexity from hiding gaps in the mathematics.

For a later sports project, a suitable research question could be:

> “Do topological descriptors of movement windows add reproducible information beyond ordinary kinematic features?”

We would first define each observation—such as a vector of joint angles or a motion window—and specify which transformations should count as irrelevant. Then we would test whether the chosen representation behaves accordingly.

For a computer-vision project, we could investigate how controlled occlusion or reconstruction defects change descriptors of a surface or point cloud.

These are **proposed experiments, not established benefits for your system**. The capstone must be allowed to conclude that TDA is unhelpful for the selected task.

Keep this learning work separate from production initially. There is no need to modify the WMS pipeline to understand boundary matrices or persistence reduction.

---

# 7. How we will decide that you have completed the course

We will use the following proposed assessment standard. It is a learning rubric, not a claim of formal accreditation.

| AreaRequired evidence         |                                                                                                   |
| ----------------------------- | ------------------------------------------------------------------------------------------------- |
| **Definitions and intuition** | Explain the central terms accurately and supply examples and counterexamples.                     |
| **Mathematical reasoning**    | Complete foundational proofs and hand calculations, with assumptions stated.                      |
| **Algorithms**                | Perform a small persistence reduction manually and explain your implementation.                   |
| **Software correctness**      | Pass the agreed tests and reproduce results in established libraries.                             |
| **Interpretation**            | Distinguish topology, metric structure, stability, statistical evidence, and application meaning. |
| **Independent work**          | Complete and defend the capstone without copying a tutorial’s choices.                            |
| **Retention**                 | Solve new cumulative problems after a delay, not only immediately after instruction.              |
| **Book coverage**             | Audit the actual text and close any remaining topic-specific gaps.                                |

For ordinary unit quizzes, I propose **85% as an initial progression threshold**, with every critical conceptual error corrected before proceeding. A high average does not compensate for believing that every cycle is a nontrivial homology class or that every persistent feature is meaningful.

We should also include a delayed reassessment about a week after each major unit.

## Proof depth will be explicit

Not every theorem needs the same treatment.

For elementary results—continuity composition, metric examples, boundary-of-boundary—you should produce the proof.

For major results—interval decomposition, stability, and the nerve theorem—you should state a correct version, explain its assumptions and proof strategy, and recognize valid and invalid applications. Full proofs can become additional assignments as your mathematical comfort develops.

Advanced topics such as cohomology rings, spectral sequences, comprehensive manifold classification, and multiparameter-persistence theory are **a subsequent course**, not hidden requirements for completing this one.

---

# 8. Keeping the learning organized here

At the end of each unit, we should produce a short progress record containing:

**Current unit; completed readings; solved problems; verified notebooks; assessment result; unresolved misconceptions; next assignment.**

“Read,” “attempted,” “corrected with help,” and “solved independently” should remain different statuses.

This record will also provide a reliable handoff to a new chat. We should preserve the actual evidence rather than depend on a vague statement such as “we already covered homology.”

For the book audit, use four statuses:

| StatusMeaning                  |                                              |
| ------------------------------ | -------------------------------------------- |
| **Introduced**                 | You have encountered the concept.            |
| **Practiced**                  | You have completed guided work.              |
| **Independently demonstrated** | You can solve unfamiliar problems using it.  |
| **Retained**                   | You can still do so on a delayed assessment. |

**“Complete” will mean that every agreed core outcome has evidence behind it and no unresolved critical gaps remain.**

---

# 9. Your starting point: a diagnostic, not more setup

Before assigning the first readings, we should identify what you already know. These questions are placement questions; not knowing the topology ones yet is expected.

| QuestionWhat it checks                                                                                        |                                  |
| ------------------------------------------------------------------------------------------------------------- | -------------------------------- |
| For `f(x)=x^2`, what is `f^{-1}((1,4))`?                                                                      | Inverse images and set reasoning |
| What is the negation of “every element has property `P`”?                                                     | Quantifiers                      |
| Explain kernel, image, rank, and nullity without using software.                                              | Linear-algebra foundations       |
| Show that “having the same remainder modulo 3” is an equivalence relation.                                    | Proof and equivalence classes    |
| Does `d(x,y)=(x-y)^2` define a metric on `\mathbb R`? Justify your answer.                                    | Definitions and counterexamples  |
| Why might a triangular outline and a filled triangle have different mathematical structure?                   | Initial shape intuition          |
| What should happen to a Euclidean distance matrix when all observations are translated by the same vector?    | Invariance reasoning             |
| A program produces a long persistence bar. What else would you need before calling it a meaningful discovery? | Scientific interpretation        |

**Start by answering these in your own words, marking anything unfamiliar as “not yet.” We will use the results to begin Unit 1 at the right level, then work through the course one assessed lesson at a time.**