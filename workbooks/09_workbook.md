# Stage 09 workbook — Understand every moving part of the persistence algorithm

## The algorithm starts before matrix reduction

First validate the filtration. Every simplex must have its faces present, and no face may enter later than its coface. Sort by entrance time, then dimension, then a deterministic tuple order. This places faces before cofaces when their entrance times tie.

Create one row and one column for each simplex in that order. A boundary column contains ones at the rows of its codimension-one faces. Vertex columns are zero in ordinary homology. Because faces precede cofaces, nonzero boundary rows precede the corresponding column.

These are boundary coordinates over F₂, not distances or intensities. The entrance values remain attached to the row and column identities for interpreting pairings afterward.

## Trace a single triangular graph

Take vertex columns first, then the edges 01,12,02. The first edge boundary is {0,1}; the second is {1,2}; the third is {0,2}. Here the sets store vertex-row indices.

The third column has largest row 2, which already belongs to the second reduced column. XOR them: {0,2} XOR {1,2}={0,1}. The largest row is now 1, which belongs to the first edge column. XOR again, giving the empty set. Thus the closing edge gives a zero reduced column and a one-dimensional birth.

If a triangular face is later added, its boundary can pair with that birth and kill it. The edge loop has not vanished from the complex; it is now in the image of the next boundary map.

## The reduction invariant

Maintain at most one previous reduced column for each largest nonzero row, often called low. When a new column shares that row, adding the previous owner cancels it. The largest row strictly decreases, so this loop terminates. A nonzero reduced column establishes a birth/death pairing between its pivot row and the current column.

A zero reduced column represents a birth. If its index is never used as a later pivot, it survives the supplied filtration. Interpret finite pair dimensions from the birth simplex; a killing coface has one higher dimension.

The practice implementation uses sparse sets and XOR, which makes the logic visible. It is intentionally not an optimized production engine. A dense or sparse representation change can alter performance without changing the mathematical reduction rules.

## Verify different aspects with different checks

A hand-derived square interval checks an exact nontrivial answer. Boundary-of-boundary checks chain-complex consistency. Comparing Betti numbers at a threshold checks a snapshot. The rank-invariant test at pairs of thresholds checks whether classes were paired consistently through the filtration.

Union-find provides a different route to H₀ merge distances: process pairwise edges from short to long and merge currently separate components. Every successful merge kills one component. This agrees with the finite H₀ death values after matching the zero-length convention.

The course also supplies optional Ripser and GUDHI comparisons. They remain recorded as skipped when the libraries are absent, not silently treated as passes. Agreement with a library is complementary evidence, not a formal proof that every possible input is correct.

## Boundary cases are mathematical cases

Empty matrices occur naturally at the bottom of a chain complex. Equal entrance times require consistent tie handling. Duplicate coordinates give zero-distance events between distinct IDs. A graph-only complex intentionally differs from a clique complex. A filtration ending before a class dies needs a censored interpretation.

Do not remove a test because one of these cases seems inconvenient. First decide what the declared mathematical model requires, then determine whether the implementation matches it.

## Real-data check

On a small declared Iris subset, compare the union-find H₀ merge list with persistent reduction. Print the selected IDs and distances. Positive agreement establishes that these two routes agree on this measured subset and convention; it does not verify a species interpretation or every higher-homology calculation.

For the independent coding attempt, implement the reduction rather than calling the supplied reducer inside your function. Use the supplied reducer as an oracle afterward. Save one manually traced example in your evidence file; that explanation is needed in addition to the passing code.

**Before advancing:** explain filtration ordering, sparse column support, XOR cancellation, pivot ownership, birth/death extraction, and the meaning of an unpaired index. Sources R1, R2, and L1–L3 provide the reference conventions.

## Work through this stage in three passes

**Pass A — Understand:** read this workbook and the core lesson. Define the new terms in your own words and work one small example by hand.

**Pass B — Implement:** inspect the original real-data lab, predict its outputs, then complete the five new coding activities without opening the answer notebook. Use the visible tests and add one new test.

**Pass C — Defend and retain:** solve the original exercises, explain one failed alternative, and answer the three new retrieval prompts after a delay. Record assistance honestly. A passed program does not prove an essay or theorem.

**Next files:** [Core lesson](../lessons/09_lesson.md) · [Worked lab](../notebooks/09_lab.ipynb) · [Your coding notebook](../practice/learner/09_practice.ipynb) · [Reference coding solutions](../practice/09_solutions.md) · [Retrieval prompts](../practice/retrieval.md).
