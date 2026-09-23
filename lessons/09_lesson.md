# Stage 09 — Implement persistence, trace the algorithm, and test it independently

**Starting point:** Complete the Stage 08 mastery gate first, or use its worked solutions to close a specific gap.

**Learning cycle:** understand → define → work by hand → predict → run → critique → retrieve later.

## 1. Make a valid order before reducing anything
List all simplices in increasing filtration value. Break ties by increasing dimension, then by a deterministic vertex order. Every face then precedes its coface. Determinism makes examples reproducible, but it does not make a chosen representative mathematically canonical.

Form the boundary matrix with both rows and columns indexed by that ordered list. A column for a vertex is zero. A column for an edge has its two vertex rows. A column for a triangle has its three edge rows. Over F₂ the entries are zero or one, so adding columns is symmetric difference of their nonzero-row sets.

The **low** of a nonzero column is the largest row index with value one. Reduction aims to make every nonzero reduced column have a different low. Do not confuse this “largest row index” convention with a numeric maximum entry; all nonzero entries are one.

## 2. Trace a complete small reduction
Use a triangle boundary with vertices 0,1,2 appearing first, then edges 01,02,12. Number rows 0 through 5 in that order. The first two edge columns contain {0,1} and {0,2}; their lows are 1 and 2. The last edge column contains {1,2}, also with low 2.

Add the reduced column {0,2} to {1,2}; XOR gives {0,1}, now with low 1. Add the column {0,1}; the result is empty. That zero reduced edge column creates an H₁ class. If a filled triangle enters later, its boundary column pairs with this birth and supplies its death. If no face ever enters, the class survives the supplied filtration.

This sequence is logged by `reduce_boundary`: each operation records which previous column was added to the current one. Read the actual function after tracing this case manually. It contains no machine-learning model; it is exact finite algebra over F₂, apart from the floating-point filtration values supplied by geometric calculations.

## 3. Extract intervals carefully
A zero reduced column marks a birth. If its index later appears as the low of a nonzero column, the latter column kills that class. The dimensions differ by one. A birth index that is never paired has infinite death relative to the supplied filtration.

Births and deaths can share the same numerical value because different simplices enter together. Our default discards only exactly zero-length pairs, rather than treating all short bars as zero. When comparing implementations, agree on coefficient field, scale convention, finite cutoffs, maximum homology dimension, and zero-persistence policy. Floating-point agreement uses a declared tolerance for validation; it does not silently change the mathematical filtration.

The reference implementation validates simplex uniqueness, finite entry values, complete faces, and nondecreasing face values. It deliberately refuses excessive candidate counts. These checks are not mathematical sophistication for its own sake: they prevent incorrect input from yielding confidently wrong diagrams.

## 4. Independent checks that catch different errors
Our strongest exact example is the square, whose interval endpoints are known from its side and diagonal lengths. Boundary-rank Betti numbers at each event provide another check on barcode counts. For H₀, an independently implemented union-find or a minimum spanning tree can recover merge scales for finite distance data. This tests connectivity behavior without using persistence column reduction.

The tests also check triangle and tetrahedron examples, empty complexes, duplicate coordinates, tied entries, input rejection, vertex permutation, translations, rotations and uniform rescaling. These are examples of **metamorphic tests**: we know how an answer should change under a controlled input transformation even without an oracle for every random dataset.

Optional scripts compare the same examples with Ripser and GUDHI. The build environment could not install these packages. Their result is explicitly “not run,” and the executable check remains available in the archive. You should run it in your own environment before treating the independent cross-library validation gate as complete.

## 5. The real-data check
Use the declared small Iris subset and compute its H₀ merge distances in two ways: persistence reduction and an independently coded complete-graph union-find procedure. Compare the sorted finite deaths. Retain zero-length handling explicitly when duplicate feature vectors are present.

Then sample several thresholds and compare H₀/H₁ barcode counts to direct homology of the corresponding subcomplexes. Agreement is strong evidence for the tested data and operations, but because some paths share low-level code, it is not total independence. The report names the methods rather than claiming independent certification.

## 6. Know when to stop implementing
This code is intended for inspecting how persistence works. Specialized packages use more efficient algorithms and data structures. A dense worst-case reduction can be cubic in the number of matrix columns, and simplex enumeration can dominate even earlier. Do not run this enumerator on millions of observations or full-resolution 3D reconstructions.

Once you can trace the algorithm, explain its input assumptions, pass the tests, and compare a specialized implementation, use the specialized implementation for scale. Keeping an exact small reference is useful for regression tests, not an instruction to rebuild an entire research library.

## Independent exercises

Do these before reading the worked solutions. A copied solution is not an independent pass.

**09.1.** Trace the last edge column in the triangle-boundary example until it reduces to zero.

**09.2.** Why must faces precede cofaces at tied filtration values?

**09.3.** What does a zero reduced column mean, and how is its death found?

**09.4.** Why is adding columns by ordinary integer addition wrong over F₂?

**09.5.** Which parameters must match before comparing two library diagrams?

**09.6.** Explain why a graph-only calculation can create a false infinite H₁ bar.

**09.7.** What evidence do the independent H₀ merge calculation and direct Betti checks add?

**09.8.** Open the optional library-check report and explain the difference between SKIPPED and PASSED.

## Mastery gate

Trace reduction manually, explain all tested invariances, and run or explicitly retain the pending external-library validation gate.

Explain one limitation and solve a new variant after a delay. Suggested progression threshold: 85% on the local knowledge check, with every critical error corrected. This is a course rubric, not accreditation.

## Free readings and attribution

Source IDs: R1, R2, L1, L2. See `docs/SOURCES.md` for direct official links and assigned topics. The exposition, examples, code, and solutions here are original course material, not copied textbook chapters.

## Run and continue

Open `notebooks/09_lab.ipynb`. Its saved outputs are also readable from the browser reader. After the lab, compare with `solutions/09_solutions.md`, record what was independent, and continue only when the gate is met.
