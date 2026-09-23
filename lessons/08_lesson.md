# Stage 08 — Persistent homology, persistence modules, and reading diagrams

**Starting point:** Complete the Stage 07 mastery gate first, or use its worked solutions to close a specific gap.

**Learning cycle:** understand → define → work by hand → predict → run → critique → retrieve later.

## 1. Why separate hole counts are insufficient
At each scale we can compute homology. But knowing the number of classes at each scale does not tell us which class at one scale continues to which class at the next. The inclusions between complexes induce linear maps between homology spaces. A **persistence module** records the spaces and compatible maps together.

For a finite filtration over a field, the associated finite-dimensional one-parameter module decomposes into interval modules. Each interval module has one copy of the field at indices in its interval, zero elsewhere, and identity maps where it persists. The multiset of intervals is the barcode. The existence and uniqueness theorem is deeper than a drawing; here we understand its statement, its field and finiteness hypotheses, and how the reduction algorithm realizes the decomposition computationally.

To see why maps matter, imagine one-dimensional vector spaces at two successive indices. An identity map continues one feature; a zero map kills the old one and leaves a new independent feature at the second index. The dimensions at both indices are one in either case, but the interval decompositions differ.

## 2. Birth, death, and a convention at endpoints
We record a class with interval `[birth, death)`. It is present at birth and absent at death. Classes that survive the whole supplied filtration receive an infinite death. Whether that means a genuinely essential feature of the intended final space or merely survival past a chosen cutoff depends on what was actually computed.

A **barcode** draws these intervals as horizontal segments. A **persistence diagram** places one point at (birth,death) per interval, with multiplicity. An interval's lifetime is death minus birth, not its distance along a curved trajectory in the original data. Zero-length intervals lie on the diagonal and are omitted by our default report.

The barcode row number is arbitrary. It is not a persistent object ID from tracking software. Likewise, there is generally no unique geometric representative loop attached canonically to each diagram point. Representative cycles and cocycles are additional mathematical/computational objects that require interpretation.

## 3. The unit-square example from beginning to end
Put four points at the corners of a unit square. At ε=0 they are four isolated vertices, giving four H₀ classes. At ε=1 the four side edges enter. Three independent merges reduce the number of components to one. The fourth edge closes the perimeter loop.

Until ε=√2, the diagonals are absent, so no triangular faces occur. There is exactly one H₁ class during `[1,√2)`. At ε=√2 all pairwise distances qualify, so the triangular faces fill the perimeter cycle. If higher dimensions are included, the full tetrahedral simplex is present as well. For the H₁ calculation, triangles suffice to kill the loop.

Thus ordinary H₀ has three finite intervals [0,1) and one interval [0,∞). H₁ has one positive interval [1,√2). If we stop at ε=1.1, the H₁ interval in the supplied truncated filtration has infinite death. Reporting that as a permanent hole of the full Rips filtration would be false.

## 4. Relate diagrams back to Betti numbers
At a threshold t, βₖ equals the number of k-dimensional intervals satisfying `birth≤t<death`, using the same conventions and filtration. We will verify this by comparing barcode counts with independently calculated boundary-matrix ranks at every distinct event value in a small example.

This relation does not reverse uniquely: a sequence of Betti numbers alone does not recover the maps and hence may not recover the barcode. Keep both directions of the logical claim straight.

An infinite H₀ bar is expected for a nonempty connected final complex in ordinary homology. It should not be called a failed computation or silently dropped from every statistic. Some representations exclude essential intervals from lifetime sums because their length is infinite; the exclusion must be documented, and separate component information can still be retained.

## 5. The real-data barcode
Compute a Rips barcode for a declared small sample of Iris observations and a pixel-intensity barcode for a training digit. The first filtration axis is Euclidean edge distance in specified feature units. The second uses `f=1−intensity/16`: high-intensity strokes enter early, and darker background pixels later. These axes are not interchangeable.

For the pixel model all squares eventually fill the rectangle at value one, so H₁ has no essential intervals in the complete image filtration. A long H₁ interval says a loop in that pixel model survives over a broad intensity-threshold range. It does not alone establish a biological grouping, meaningful stroke feature, or useful classifier.

Before running the code, sketch the square's diagram by hand and label the diagonal and essential class. Then compare it with the actual saved plot. Changing a plotting style should not change numerical interval endpoints. Changing the filtration definition can.

## Independent exercises

Do these before reading the worked solutions. A copied solution is not an independent pass.

**08.1.** Explain what the maps in a persistence module add beyond the vector-space dimensions.

**08.2.** Write all positive or essential bars for the unit square in H₀ and H₁.

**08.3.** At t=1, t=1.2 and t=√2, what is β₁ under our endpoint convention?

**08.4.** Why can an infinite death mean truncation rather than a permanent feature?

**08.5.** What does multiplicity mean in a persistence diagram?

**08.6.** Does a long interval identify one unique physical loop in the original data?

**08.7.** Explain why the pixel filtration has no essential H₁ after all pixels enter.

**08.8.** Why must the two real-data examples label their horizontal axes differently?

## Mastery gate

Read and derive barcodes and diagrams, interpret endpoint/truncation conventions, and explain the need for induced maps.

Explain one limitation and solve a new variant after a delay. Suggested progression threshold: 85% on the local knowledge check, with every critical error corrected. This is a course rubric, not accreditation.

## Free readings and attribution

Source IDs: R1, R2, R8, L1, L3. See `docs/SOURCES.md` for direct official links and assigned topics. The exposition, examples, code, and solutions here are original course material, not copied textbook chapters.

## Run and continue

Open `notebooks/08_lab.ipynb`. Its saved outputs are also readable from the browser reader. After the lab, compare with `solutions/08_solutions.md`, record what was independent, and continue only when the gate is met.
