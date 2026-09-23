# Sources, free readings, and claim provenance

Checked through public primary-source pages on September 20, 2026. Links can change; no third-party book PDFs or videos are bundled. Code versions in the execution report may differ from current online documentation.

## How to distinguish the evidence

**Supplied outline:** the user’s attached staged plan, preserved unchanged in `reference/USER_SUPPLIED_OUTLINE.md`. **Course-authored material:** new explanations, examples, exercises, code and experiment design. **Verified external references:** the official/author pages below. **Computed results:** the actual local notebook outputs and tests under `reports/`. None of these is a review of the full forthcoming book.

## R1 — Raphaël Tinarrage — Topological Data Analysis with Persistent Homology

https://raphaeltinarrage.github.io/EMAp.html

Primary teaching sequence, Lessons 0–11. Free lecture materials, videos and practical notebooks are linked from the course page.

## R2 — ETH Zürich — Introduction to Topological Data Analysis, 2026

https://ti.inf.ethz.ch/ew/courses/TDA26/index.html

Formal reference. Mathematical foundations, homology, persistence, point-cloud complexes, distances/stability, Mapper and advanced extensions. The page lists discrete mathematics, algorithms/data structures and linear algebra prerequisites.

## R3 — Sidney A. Morris — Topology Without Tears

https://www.topologywithouttears.net/

Free author-hosted topology book and accompanying proof/topology videos. Use for open sets, continuity, connectedness and compactness.

## R4 — Richard Hammack — Book of Proof

https://richardhammack.github.io/BookOfProof/

Free author-hosted proof textbook. Use sets, logic, quantifiers, proof methods, relations and functions.

## R5 — MIT OpenCourseWare — Gilbert Strang, Linear Algebra

https://ocw.mit.edu/courses/18-06-linear-algebra-spring-2010/

Free lectures, assignments and solutions. Focus on vector spaces, nullspaces, column spaces, rank, bases and linear maps.

## R6 — Thomas W. Judson — Abstract Algebra: Theory and Applications

https://judsonbooks.org/abstract-algebra-theory-and-applications/

Author-hosted open textbook. Select basic groups, homomorphisms, group actions, vector spaces and fields; a full second algebra course is not a prerequisite here.

## R7 — Allen Hatcher — Algebraic Topology

https://pi.math.cornell.edu/~hatcher/AT/ATpage.html

Author-hosted free electronic book subject to its stated terms. Use geometric preliminaries, fundamental-group introduction and homology. Linked only; not redistributed.

## R8 — Frédéric Chazal and Bertrand Michel — An introduction to Topological Data Analysis

https://arxiv.org/html/1710.04019v2

Primary author paper connecting metric spaces, complexes, persistence, Mapper, stability and statistical interpretation. Read critically after the small exact examples.

## R9 — scikit-learn — Common pitfalls and recommended practices

https://scikit-learn.org/stable/common_pitfalls.html

Primary library guidance on fitting transformations on training data and preventing evaluation leakage.

## R10 — Ioannis Diamantis — The Shape of Data: Topology Meets Analytics

https://arxiv.org/abs/2511.13503

Free author paper for the final critique. The paper’s proposed stability index is not a replacement for algebraic stability or a statistical-significance argument.

## D1 — UCI — Iris

https://archive.ics.uci.edu/dataset/53/iris

Dataset provenance and CC BY 4.0 license metadata. The included array is scikit-learn’s documented corrected variant.

## D2 — UCI — Optical Recognition of Handwritten Digits

https://archive.ics.uci.edu/dataset/80/optical+recognition+of+handwritten+digits

Dataset provenance and CC BY 4.0 metadata. Full UCI collection and original writer-separated split are distinct from this course’s subset and new image split.

## D3 — scikit-learn — Bundled small datasets and their variants

https://scikit-learn.org/stable/datasets/toy_dataset.html

Confirms bundled real Iris and digits descriptions, 1,797 digit images, 8×8 values, original-test-set provenance, and the Iris corrections.

## L1 — Ripser.py — ripser API reference

https://ripser.scikit-tda.org/en/latest/reference/stubs/ripser.ripser.html

Primary reference for points/distance matrices, maxdim, coefficient field, cutoff and returned diagrams. Optional package not installed in the build environment.

## L2 — GUDHI — Rips and Delaunay/alpha manuals

https://gudhi.inria.fr/python/latest/rips_complex_user.html

Primary complex-construction reference. Alpha details: https://gudhi.inria.fr/python/latest/delaunay_complex_user.html . Default alpha values use squared-radius units. Optional library not executed in this build.

## L3 — GUDHI — Cubical complex manual

https://gudhi.inria.fr/python/latest/cubical_complex_user.html

Primary reference for square/cubical input semantics. Our core uses its own explicit filtration-preserving triangle subdivision, not an unexecuted GUDHI call.

## Topic-based reading assignments

| Stage | Primary assignment | Deeper reading when needed |
|---|---|---|
| 00 | This starter; data documentation D3 | Tinarrage Lesson 0 |
| 01 | Hammack sets/functions/logic; MIT kernels and images | Judson vector spaces and fields |
| 02 | Tinarrage Lesson 1 | Morris topology, bases and subspaces |
| 03 | Tinarrage Lesson 2 | Morris continuity, connectedness, compactness; ETH foundations |
| 04 | Tinarrage Lesson 3; Judson basic groups/actions | Hatcher geometric preliminaries and fundamental-group introduction |
| 05 | Tinarrage Lesson 4 | ETH homology introduction; Hatcher surfaces and complexes |
| 06 | Tinarrage Lessons 5–6 | ETH homology; Hatcher Chapter 2 selections |
| 07 | Tinarrage Lessons 7–8 | ETH point-cloud complexes; Chazal–Michel complexes and nerves |
| 08 | Tinarrage Lesson 9 | ETH persistence modules and interval decomposition |
| 09 | Tinarrage practical persistence tutorial | ETH persistence algorithms; Ripser/GUDHI primary API manuals |
| 10 | Tinarrage Lesson 10 | ETH distances/stability; Chazal–Michel statistical interpretation |
| 11 | Chazal–Michel Mapper and representations; sklearn pitfalls | ETH Reeb/Mapper; further vectorization literature through primary sources |
| 12 | Diamantis paper as a critique exercise | Actual book section audit when text is available |

No external exercise solutions are reproduced here. The worked solutions in this archive answer the course’s own questions. External course exercise numbering may change; follow topic headings and verify the edition before using a numbered assignment.

## Book status

The supplied listing names *Listening to Shape: Topology, Persistence and Structure*, Ioannis Diamantis, DOI https://doi.org/10.1142/15081, with a March 2027 date. The DOI redirected to a publisher page that the browsing tool could not retrieve. The date, page count, ISBN and exact chapter contents are therefore not independently reconfirmed in this build. Use the supplied outline for topic alignment, not as proof of chapter-complete equivalence.

## Optional references not used as validation evidence

Ghrist’s *Elementary Applied Topology* remains a useful reference in the supplied plan, but its author page returned 403 in this check. It is not needed to execute the package. No inaccessible page is cited as evidence of a successful test or a book-coverage audit.

## P1 — Python — An Informal Introduction to Python

https://docs.python.org/3/tutorial/introduction.html

Official syntax reference for the new from-zero primer. The page may document a newer Python release than the executed environment.

## Source audit for version 2

The v2 build rechecked the author/official HTML pages for Tinarrage, ETH TDA 2026, Morris, Hammack, Judson, Hatcher, Chazal–Michel, Python, scikit-learn toy datasets and leakage guidance, Ripser API, and GUDHI alpha/cubical manuals. Existing MIT, author-paper and UCI citations are retained from the v1 source record; they were not all fetched again during this update. No live link check establishes that every theorem has been independently formally verified. The book text is still not examined.

The new workbooks, code exercises, retrieval prompts and proofs are course-authored additions. Mathematical claims use the source framework above; specific calculations and results have their own tests and execution evidence. Free external texts and videos are linked, not bundled.
