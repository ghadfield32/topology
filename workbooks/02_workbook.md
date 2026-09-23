# Stage 02 workbook — What closeness means, and what topology forgets

## A metric has four jobs

A metric d on a set X returns a nonnegative real number for each pair of points. It is zero exactly when the points are identical, is symmetric, and satisfies the triangle inequality d(x,z)≤d(x,y)+d(y,z). These are requirements, not properties supplied by calling an arbitrary similarity score a distance.

For absolute distance on the real line, nonnegativity and symmetry follow from absolute value. Zero distance means x=y. The triangle inequality follows by writing x−z=(x−y)+(y−z) and using |a+b|≤|a|+|b|. In contrast, squared distance fails at 0,1,2: the long direct squared distance is 4 while the two shorter squared distances sum to 2.

The Euclidean, Manhattan, and maximum-coordinate metrics produce different numerical balls in ℝᵈ. In finite-dimensional real coordinate space they induce the same usual topology, but their numerical neighborhoods at a fixed radius and their persistence scales need not be the same. A homeomorphism-level statement does not guarantee identical barcode coordinates.

## Neighborhoods lead to open sets

An open ball B(x,r) consists of y with d(x,y)<r. A set U is open when each point x∈U has some positive-radius ball around it contained in U. The radius can depend on x. In (0,1), points near an endpoint need a smaller radius than points near the middle.

The empty set is open because there is no point at which the condition could fail. The whole space is open. Arbitrary unions of open sets are open: a point in the union belongs to one member, whose small ball also lies in the union. Finite intersections are open: choose the minimum of the finitely many radii. Infinite intersections can fail; intersecting (−1/n,1/n) for n=1,2,… gives {0}, not an open subset of the usual real line.

These properties motivate a topology: an explicitly selected family of subsets satisfying those axioms. A topology need not arise from a metric. In a finite example, list all open sets and check the axioms directly.

## Relative openness answers a common puzzle

The set [0,1) is not open in the usual real line. It is open in the subspace [0,2], because it equals (−1,1)∩[0,2]. A statement that a set is open needs the ambient space and topology. Closed means the complement in that ambient space is open; it does not mean the set visually includes a boundary in every possible drawing.

Some sets are both open and closed. In a discrete space every subset has that property. This is not a contradiction because open and closed are not logical negations of each other.

## Why a sampled circle has no intrinsic continuous ring yet

Take any finite set of distinct metric points. Around one point x, the finitely many positive distances to all other points have a positive minimum m. The ball of radius m/2 contains only x. Thus every singleton is open and every subset, being a union of singletons, is open. The induced topology is discrete.

Therefore a finite point cloud that resembles a circle does not automatically contain a continuous circle in its own subspace topology. The neighborhood complex we construct in Stage 07 connects observations across chosen scales. Inferring an underlying circle then requires assumptions and evidence about sampling and geometry.

If two observation IDs have identical coordinates, their coordinate distance is zero although the IDs differ. That is a pseudometric on IDs. Retaining IDs preserves provenance; taking the quotient by zero distance is a separate modeling choice. The course records the convention rather than silently deleting duplicated measurements.

## Real-data practice

Compute a Euclidean distance matrix using only the four Iris measurements. Confirm its shape, symmetry, and diagonal zeroes. Inspect which other row is nearest to sample zero. Compare your answer after changing just one feature's numerical scale. The changed neighbor is evidence about the chosen distance calculation, not about which biological specimen is inherently most similar by every criterion.

The open-ball exercise uses `<r`. Rips edges later use `≤ε`. Keep those rules explicit, especially at ties. An inequality typo can change an exact birth threshold even when a plot looks unchanged.

**Deeper check:** prove the finite-discrete result and the finite-intersection open-set result without code. The finite-topology validator is a finite illustration, not a replacement for the axioms in infinite spaces. Sources R1–R3 and R8 support the conceptual framework.

## Work through this stage in three passes

**Pass A — Understand:** read this workbook and the core lesson. Define the new terms in your own words and work one small example by hand.

**Pass B — Implement:** inspect the original real-data lab, predict its outputs, then complete the five new coding activities without opening the answer notebook. Use the visible tests and add one new test.

**Pass C — Defend and retain:** solve the original exercises, explain one failed alternative, and answer the three new retrieval prompts after a delay. Record assistance honestly. A passed program does not prove an essay or theorem.

**Next files:** [Core lesson](../lessons/02_lesson.md) · [Worked lab](../notebooks/02_lab.ipynb) · [Your coding notebook](../practice/learner/02_practice.ipynb) · [Reference coding solutions](../practice/02_solutions.md) · [Retrieval prompts](../practice/retrieval.md).
