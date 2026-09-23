# Stage 08 workbook — Remember which classes survive, not just how many

## A sequence of counts loses information

Consider two barcodes. A has intervals [0,3) and [1,2). B has intervals [0,2) and [1,3). Both have one active class before 1, two between 1 and 2, and one between 2 and 3. Their Betti curves are identical.

Yet the class already present at time 0 survives past 2 in A but not in B. The rank of the map from time 0 to time 2.5 is one for A and zero for B. Persistent homology records those maps through the filtration, not only dimensions at individual times.

This example is an abstract barcode comparison. It demonstrates missing information in snapshot counts without claiming that either barcode came from the same particular image.

## Follow the maps

An inclusion K_s⊆K_t sends chains, cycles, and boundaries in the earlier complex into the later one. It therefore induces a linear map Hₖ(K_s)→Hₖ(K_t). For s≤t≤u, composing the maps from s to t and t to u agrees with the map from s to u. The spaces and compatible maps form a persistence module.

For finite-index, finite-dimensional persistence modules over a field, interval decomposition describes the module using intervals. The existence and uniqueness theorem is deeper than observing a few barcodes. The core explains the statement and implements its boundary-reduction realization for finite filtered complexes; the full proof is an explicit advanced reading assignment.

## Hand-derive the square before running it

The four corners are (0,0), (1,0), (1,1), and (0,1). Vertices enter at zero. At edge threshold one the four sides enter, creating a connected loop. Before √2 the diagonals are absent, so no clique triangles fill it. At √2 both diagonals enter and the clique triangles fill the cycle. Hence the positive H₁ interval is [1,√2).

The same construction gives three positive finite H₀ merge intervals with birth zero and death one, plus one surviving H₀ class. Simultaneous events can have different valid creator representatives under different tie choices; the positive barcode is the invariant quantity. The creator simplex is not automatically a uniquely identifiable physical feature.

## Interpret a diagram point precisely

An interval [b,d) becomes a point (b,d) above the diagonal. Vertical separation from the diagonal corresponds to lifetime d−b in these coordinates, while L-infinity distance to the diagonal is half that lifetime. Multiplicity matters: two intervals with identical endpoints are still two classes in the diagram.

A zero-length interval has no parameter range on which it is present under the half-open convention. The core omits those by default. That is a reporting convention, not a tunable denoising threshold that discards every short but positive interval.

An infinite death is not a large finite numerical value. It describes an unpaired class in the supplied filtration. Its interpretation depends on whether the filtration was complete, truncated in scale, or truncated in dimension.

## From a real image to its diagram

For a training image, form f=1−intensity/16. At parameter t, include all closed pixels with f≤t. Build the filtration-preserving triangulation and compute H₁ persistence. By threshold 1 every pixel of the rectangular image is present, so its completed H₁ is zero. That is why the finite H₁ diagram is appropriate for this particular experiment.

Read the birth and death values of each reported interval. Translate them back to intensity thresholds using intensity≥16(1−t). A death is caused by the relevant cycle becoming a boundary, not by the code deleting a previously included pixel. The filtration only adds cells.

## What persistence does not decide for you

Longer persistence means survival over a larger range of the declared parameter. It does not automatically mean statistical significance, biological importance, or useful predictive information. A poor metric, an outlier, or an inappropriate filtration can produce long intervals too.

Before interpreting a feature, state its dimension, parameter units, data representation, coefficient field, and cutoff. Then ask what alternative modeling choices could produce or remove it. Stage 10 turns that question into controlled perturbation checks.

**Before advancing:** reconstruct a barcode from a small filtration, read exact endpoints, and explain why two equal Betti curves can hide different persistence modules. Sources R1, R2, R8, and L1 provide the theoretical and computational reference.

## Work through this stage in three passes

**Pass A — Understand:** read this workbook and the core lesson. Define the new terms in your own words and work one small example by hand.

**Pass B — Implement:** inspect the original real-data lab, predict its outputs, then complete the five new coding activities without opening the answer notebook. Use the visible tests and add one new test.

**Pass C — Defend and retain:** solve the original exercises, explain one failed alternative, and answer the three new retrieval prompts after a delay. Record assistance honestly. A passed program does not prove an essay or theorem.

**Next files:** [Core lesson](../lessons/08_lesson.md) · [Worked lab](../notebooks/08_lab.ipynb) · [Your coding notebook](../practice/learner/08_practice.ipynb) · [Reference coding solutions](../practice/08_solutions.md) · [Retrieval prompts](../practice/retrieval.md).
