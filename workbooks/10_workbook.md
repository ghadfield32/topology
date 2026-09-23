# Stage 10 workbook — Stable does not mean meaningful

## First define the comparison

Let f and g be scalar functions on the same fixed domain, and suppose their uniform difference is at most δ. If f(x)≤t, then g(x)≤f(x)+δ≤t+δ. Therefore the f-sublevel set at t lies inside the g-sublevel set at t+δ. The same reasoning in reverse gives the companion inclusion.

These are the basic shifted inclusions behind an interleaving. They are direct consequences of the uniform bound. Connecting the induced homology modules to a bottleneck diagram bound requires the appropriate algebraic stability theorem and its hypotheses. The original proof atlas distinguishes the elementary inclusion proof from that deeper theorem.

“Same domain” is not a decorative phrase. Cropping an image, changing its topology, or moving to unrelated point-cloud constructions is not automatically covered by the exact fixed-grid argument used in this lab.

## Understand diagonal matching by hand

For one point (b,d), its L-infinity distance to a diagonal point (t,t) is max(|b−t|,|d−t|). Choosing t=(b+d)/2 makes the two distances equal at (d−b)/2. No smaller maximum is possible because the triangle inequality requires |d−b|≤|d−t|+|t−b|.

For two one-point diagrams, compare matching the points directly against matching each to the diagonal. The latter cost is the larger of their two diagonal costs. Choose the smaller possible bottleneck. A point at (0,2) and one at (5,7) cost only one when both use the diagonal, despite their large direct separation.

For multiple points, assignments interact. Greedily taking the nearest available point can block a better complete matching. The core routine searches thresholded bipartite perfect matchings. It supports finite diagrams and explicitly rejects essential intervals rather than silently discarding them.

## Use the right input norm

A maximum pixel change is not the same as average absolute error. One highly changed pixel can matter even when thousands of unchanged pixels make the average small. The lab computes the maximum absolute difference of the entrance arrays and compares it with the measured finite H₁ bottleneck distance on the fixed completed pixel filtration.

The real-data checks add bounded perturbations to training images, clip entrance values back into [0,1], and report the actual post-clipping uniform change. The bound is measured from the arrays actually used, not from an assumed nominal noise amplitude alone.

## Separate three questions

**Correctness:** did the code compute the declared object? Use exact controls, structural identities, and independent checks.

**Stability:** how much can the descriptor change when a specified input changes by a bounded amount? State the norm, domain, construction, and theorem.

**Scientific or predictive meaning:** does the result support a particular interpretation or improve a chosen task beyond appropriate alternatives? This requires a separate study design.

A constant descriptor is maximally stable but may be useless for distinguishing anything. A sensitive descriptor can sometimes be informative but hard to use robustly. Neither stability nor instability alone answers every application question.

## Noise is not one universal mechanism

Coordinate noise, outliers, missing observations, uneven sampling, and image occlusion are different perturbations. A coordinate perturbation bound is not automatically robust to inserting a far-away outlier. Resampling individual frames from a correlated video as though they were independent people gives a misleading uncertainty calculation.

A null model must preserve what the scientific null assumes irrelevant and randomize what it assumes exchangeable. Shuffling all labels, reshuffling pixels, or independently resampling points tests different hypotheses. The course does not present an arbitrary shuffle as a universal significance test for persistent features.

## What to save

Record the original sample ID, noise seed, perturbation mechanism, input norm, diagram convention, measured distance, applicable bound, and result. Include one deliberately violated numeric bound in the small checking exercise so you know the condition can fail rather than always reporting success.

The real-data stability notebook supplies empirical examples, while the theory explains when the bound should hold. A collection of passed inequalities is not an independent proof of the full theorem.

**Before advancing:** derive the shifted inclusions and diagonal cost, compute a one-point bottleneck by hand, and explain one application conclusion the passed stability test cannot establish. Sources R2 and R8 provide the deeper mathematical and statistical treatment.

## Work through this stage in three passes

**Pass A — Understand:** read this workbook and the core lesson. Define the new terms in your own words and work one small example by hand.

**Pass B — Implement:** inspect the original real-data lab, predict its outputs, then complete the five new coding activities without opening the answer notebook. Use the visible tests and add one new test.

**Pass C — Defend and retain:** solve the original exercises, explain one failed alternative, and answer the three new retrieval prompts after a delay. Record assistance honestly. A passed program does not prove an essay or theorem.

**Next files:** [Core lesson](../lessons/10_lesson.md) · [Worked lab](../notebooks/10_lab.ipynb) · [Your coding notebook](../practice/learner/10_practice.ipynb) · [Reference coding solutions](../practice/10_solutions.md) · [Retrieval prompts](../practice/retrieval.md).
