# Stage 01 — Mathematical language, proofs, and linear algebra

**Starting point:** Complete the Stage 00 mastery gate first, or use its worked solutions to close a specific gap.

**Learning cycle:** understand → define → work by hand → predict → run → critique → retrieve later.

## 1. Sets and functions give us a precise vocabulary
A **set** is a collection in which membership matters, not order or repetition. `{1, 2, 2}` describes the same mathematical set as `{1, 2}`. A list can retain order and duplicates, so it is not the same object. We write `x ∈ A` when x belongs to A and `A ⊆ B` when every member of A belongs to B. The empty set has no members. An intersection keeps common members; a union keeps members appearing in either set.

A **function** `f: X → Y` assigns exactly one output in Y to every input in X. X is the domain and Y is the codomain. The **image** `f(A)` is the set of outputs obtained from A. The **inverse image** `f⁻¹(B)` is the set of inputs whose outputs lie in B. Inverse image notation does not assert that an inverse function exists.

For `f(x)=x²` on the real line, the inverse image of `(1,4)` is `(-2,-1) ∪ (1,2)`. We solve `1 < x² < 4`, which is equivalent to `1 < |x| < 2`. The intervals are open because their endpoints produce outputs 1 or 4, which were excluded.

An injective function never maps two different inputs to the same output. A surjective function reaches the entire declared codomain. A bijection does both. Whether a function is surjective depends on its codomain: x² maps the real line onto the nonnegative real numbers but not onto the whole real line.

## 2. Quantifiers and proofs
“For every” is a universal quantifier. “There exists” is an existential quantifier. The negation of “every sample has property P” is “there is at least one sample without P.” It is not “no samples have P.” One counterexample can refute a universal statement, but a thousand confirming examples do not by themselves prove it for an infinite domain.

A direct proof starts from assumptions and reaches the claim using justified steps. A contrapositive proof of “P implies Q” proves “not Q implies not P.” A contradiction proof assumes the claim is false and derives an impossibility. Induction proves an initial case and that each case implies the next; it needs both pieces.

Worked proof: if `A ⊆ B`, then `f⁻¹(A) ⊆ f⁻¹(B)`. Take any x in `f⁻¹(A)`. By definition, f(x) belongs to A. Since A is contained in B, f(x) belongs to B. Therefore x belongs to `f⁻¹(B)`. Because x was arbitrary, the inclusion follows. Notice how each line has a reason; the picture was not the proof.

## 3. Equivalence relations and quotients
A relation is an equivalence relation when it is reflexive, symmetric, and transitive. Having the same remainder modulo three satisfies these rules. The integers split into three equivalence classes, and the quotient keeps these classes as the new objects.

This idea will return in homology. There, cycles differing by a boundary are treated as equivalent. A quotient does not mean dividing numerical lengths. It means forgetting differences declared irrelevant by an equivalence relation or a compatible algebraic construction.

## 4. Vectors and matrices from zero
A vector is an element of a vector space. In our initial examples it is a list of numbers. We can add vectors and multiply them by scalars. A linear combination adds scalar multiples of vectors. A span contains all such combinations. A basis is a spanning collection with no redundant member; its size is the dimension.

A matrix can describe a **linear map**. Multiplication by A sends an input vector x to Ax. The **kernel** contains inputs sent to zero. The **image** contains all outputs Ax. Rank is the dimension of the image; nullity is the dimension of the kernel. For a finite-dimensional input space, rank plus nullity equals its dimension.

Take `A = [[1, 1], [0, 0]]` over the real numbers. It sends `(x,y)` to `(x+y,0)`. Its image is the horizontal line, with dimension one. Its kernel is the line `(t,-t)`, also dimension one. Two input dimensions split into rank one and nullity one. The matrix is not invertible because distinct inputs can share an output.

The scalar field matters. Over the two-element field F₂, `1+1=0`, and subtraction is the same as addition. The three rows of `[[1,1,0],[1,0,1],[0,1,1]]` have real rank three but F₂ rank two: the first two add modulo two to the third. This is why we cannot use a real-valued rank function blindly for homology.

## 5. What the code can show
The notebook translates set operations into Python, calculates a small real kernel by hand, compares real rank with F₂ rank, and examines the shape and rank of the Iris measurement matrix. Numeric matrix rank uses a tolerance: it is evidence about that numerical array, not a universal theorem about all flowers.

Graph connectivity is another reusable foundation. A graph consists of vertices and edges. A graph path is a sequence of adjacent vertices; a component contains vertices reachable from one another. This combinatorial notion will connect to the topological path components of a graph's geometric realization.

## 6. Efficient practice
Do the worked inverse-image calculation, one inclusion proof, and the two matrix calculations before opening the notebook. When a term is unclear, translate it into an input/output question. Read Hammack for logic and proof technique and MIT for linear algebra only where needed; the assigned topic matters more than a page number in a changing edition.

## Independent exercises

Do these before reading the worked solutions. A copied solution is not an independent pass.

**01.1.** Find f⁻¹([1,9]) for f(x)=x² on R. Explain the endpoints.

**01.2.** Negate: “For every radius r>0 there exists a sample with property P(r).”

**01.3.** Prove f⁻¹(A ∩ B)=f⁻¹(A) ∩ f⁻¹(B).

**01.4.** Prove that congruence modulo three is an equivalence relation.

**01.5.** Find the kernel and image of [[1,2],[2,4]] over R.

**01.6.** Explain why the binary three-by-three matrix in the lesson has different ranks over R and F₂.

**01.7.** Why does having four measured columns not prove that a biological population is a four-dimensional manifold?

**01.8.** Explain the difference between a list of observations with duplicates and the set of distinct measurement vectors.

## Mastery gate

Solve inverse images, write a correct elementary proof, and explain kernel/image and real versus F₂ rank.

Explain one limitation and solve a new variant after a delay. Suggested progression threshold: 85% on the local knowledge check, with every critical error corrected. This is a course rubric, not accreditation.

## Free readings and attribution

Source IDs: R4, R5, D1, D3. See `docs/SOURCES.md` for direct official links and assigned topics. The exposition, examples, code, and solutions here are original course material, not copied textbook chapters.

## Run and continue

Open `notebooks/01_lab.ipynb`. Its saved outputs are also readable from the browser reader. After the lab, compare with `solutions/01_solutions.md`, record what was independent, and continue only when the gate is met.
