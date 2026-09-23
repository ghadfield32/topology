# Stage 11 workbook — Turn topology into an analysis without leaking the answer

## A diagram is not an ordinary fixed-length feature vector

Different observations can yield diagrams containing different numbers of points. Many conventional models expect the same number of numeric features for each observation. A representation summarizes diagrams in a declared way: counts, lifetime summaries, Betti curves, landscapes, persistence images, or other constructions.

Every summary can lose information. A Betti curve counts intervals alive at each grid value but can forget pairings. A first landscape level keeps the largest tent at each point and discards lower overlapping tents. A finite persistence-image grid can omit Gaussian mass outside its box. State those losses instead of pretending the representation is a perfect copy of the diagram.

## Build one landscape by hand

For [0,2), its tent is max(0,min(t,2−t)). At t=0,0.5,1,1.5,2 the values are 0,0.5,1,0.5,0. Multiple intervals produce multiple tents. The first landscape takes the largest at each t; the second takes the second-largest, using zero where not enough tents exist.

The sampled numerical vector depends on the grid. A plot of it is not the original object's contour. The coding practice implements the first level directly and compares known values.

A persistence image instead places weighted smooth mass in a birth/lifetime coordinate plane and integrates it into bins. The course weights by lifetime and uses a stated Gaussian bandwidth. That array is a feature representation, not an 8-by-8 handwriting reconstruction.

## Fit transformations on the right partition

Suppose training values are 0 and 2. Their mean is 1 and population standard deviation is 1, so the standardized training values are −1 and 1. A later value 100 transforms to 99 using that training scaler. Recomputing a mean using 100 would alter the fitted preprocessing and import later information into development.

The worked capstone uses fixed per-image topology extraction, then fits learned scaling and classifiers within the declared training/validation sequence. The topology extraction itself uses the known intensity range and fixed thresholds, not test-set learned normalization.

For each representation, choose the regularization parameter using validation accuracy and the predetermined smaller-C tie-break. Only after that selection fit on the combined development partition and evaluate the held-out image partition. Once the test results are visible, they cannot be used repeatedly for tuning while remaining an independent holdout.

## Mapper is a different kind of construction

Choose a lens function on observations, cover its range by overlapping sets, cluster observations inside each preimage, and connect clusters sharing observations. The core plots the nerve's graph or one-skeleton, not a complete universal reconstruction of the data space.

The graph changes with the lens, cover resolution, overlap, and local clustering rule. In the real Iris example, compare declared overlap choices and inspect membership counts. A visually attractive branch does not establish a biological taxonomy or a significant cluster.

A Reeb graph identifies connected components of level sets of a function on a space. Mapper is related in motivation but should not be described as identical to the exact Reeb graph of an unknown underlying object for an arbitrary finite dataset.

## Delay coordinates and availability

For samples 0,1,2,3,4,5,6, dimension three and lag two give windows (0,2,4), (1,3,5), and (2,4,6). They become available at indices 4,5,6, not 0,1,2. This matters when making predictions at a time cutoff.

Constructing delayed vectors does not by itself prove a dynamical-system embedding theorem applies. In the original lab, a sinusoid is a labeled synthetic temporal control and a digit column profile is spatial, not real chronological motion data.

## Real evaluation should be allowed to disappoint

Compare a conventional baseline, topological features alone, and their combination. Report exact counts, not just rounded percentages. The original digit experiment finds topology alone much weaker than pixel features, with a small combined improvement on one partition. That is a useful teaching result, not a reason to force every problem into TDA.

**Before advancing:** explain each representation's information loss, show a training-only transformation, state the independent sampling unit, and defend your model-selection rule without consulting a test score. Sources R8, R9, R2, and the library manuals provide deeper references.

## Work through this stage in three passes

**Pass A — Understand:** read this workbook and the core lesson. Define the new terms in your own words and work one small example by hand.

**Pass B — Implement:** inspect the original real-data lab, predict its outputs, then complete the five new coding activities without opening the answer notebook. Use the visible tests and add one new test.

**Pass C — Defend and retain:** solve the original exercises, explain one failed alternative, and answer the three new retrieval prompts after a delay. Record assistance honestly. A passed program does not prove an essay or theorem.

**Next files:** [Core lesson](../lessons/11_lesson.md) · [Worked lab](../notebooks/11_lab.ipynb) · [Your coding notebook](../practice/learner/11_practice.ipynb) · [Reference coding solutions](../practice/11_solutions.md) · [Retrieval prompts](../practice/retrieval.md).
