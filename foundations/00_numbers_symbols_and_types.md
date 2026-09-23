# Foundation A — Read the mathematics before trying to remember it

No previous topology is assumed. This page introduces the language used in the first stages. Return to it whenever notation interrupts your understanding. A mathematical expression becomes easier when you ask three questions: **What kind of object is this? What operation is being applied? What kind of object comes out?**

## Numbers, coordinates, and units

A scalar is one number. A vector in our introductory examples is an ordered collection of numbers: `(3, 4)` can record a location on a plane. The order matters. `(4, 3)` is usually a different location. A matrix is a rectangular array of numbers; it can represent a table of observations or a linear map, depending on its role.

Real numbers, written ℝ, include integers and fractions and quantities such as √2. The symbol ℝ² means ordered pairs of real numbers; ℝ⁴ means ordered four-tuples. It does not mean raising a particular number to the fourth power. Four flower measurements produce one point in ℝ⁴, even though a computer stores the entire dataset in a two-dimensional array.

A coordinate should have a meaning and a unit. A length of 5 centimetres and a length of 50 millimetres describe the same physical length but give different raw numerical entries. A distance calculation cannot discover missing unit conversions on its own. Changing just one column's unit can change nearest neighbors unless the calculation is adjusted consistently.

The square root of a nonnegative number is its nonnegative root. For a displacement `(3,4)`, the Euclidean length is √(3²+4²)=√25=5. Squaring distances and taking their square root are different operations. In particular, squared Euclidean distance is not generally a metric; Stage 02 shows the failed axiom.

## Read these symbols aloud

| Symbol | Read it as | Example and meaning |
|---|---|---|
| `x ∈ A` | x is an element of A | `2 ∈ {1,2,3}` is true. |
| `A ⊆ B` | A is a subset of B | Every element of A is in B; equality is allowed. |
| `∅` | the empty set | A set containing no elements; it is not the set `{0}`. |
| `A ∪ B` | A union B | Elements in at least one of the sets. |
| `A ∩ B` | A intersection B | Elements in both sets. |
| `A \ B` | A minus B | Elements of A not in B. |
| `\|A\|` | cardinality of A | The number of elements when A is finite. |
| `f: X → Y` | f maps X to Y | Each input from X has exactly one output in Y. |
| `f⁻¹(V)` | inverse image of V | Inputs whose outputs belong to V; no inverse function is required. |
| `∀` | for every | A claim covers all objects of the stated kind. |
| `∃` | there exists | At least one object has the stated property. |
| `⇒` | implies | Whenever the left statement holds, the right one holds. |
| `⇔` | if and only if | Both directions of implication hold. |
| `Σ` | sum | Add all specified contributions. |
| `\|\|x\|\|` | norm of x | A notion of vector length; specify which norm. |
| `max` | maximum | The largest value, when it exists. |
| `sup` | supremum | The least upper bound; need not be attained. |
| `ker A` | kernel of A | Inputs sent to zero by a linear map. |
| `im A` | image of A | Outputs that the map can produce. |
| `dim V` | dimension of V | Size of a basis of a vector space. |
| `∂ₖ` | boundary map in dimension k | A map from k-chains to (k−1)-chains. |
| `Hₖ` | homology in dimension k | Cycles modulo boundaries, not a physical coordinate. |
| `βₖ` | kth Betti number | Dimension of Hₖ over the specified field. |

A subscript usually labels something: `x_i` is the ith object. A superscript can mean a power, a dimension, an index, or an inverse depending on context. Do not guess from its position alone.

## Finite sets are not ordered lists

The set `{1,2,2,3}` is the same set as `{1,2,3}`. Repetition does not create another element. A list `[1,2,2,3]` does contain four entries. The point-cloud code often needs lists of observations with persistent row identities. Two rows can have the same measured coordinates without being the same observation.

A set of sets is useful for a topology. In Python, `set` is mutable and cannot be a member of another set; `frozenset` supplies an immutable set representation. The implementation detail does not change the mathematical concept.

A Cartesian product `A × B` consists of ordered pairs `(a,b)` with `a ∈ A` and `b ∈ B`. For `A={0,1}` and `B={a,b,c}`, it contains six pairs. This is the source of the rectangle intuition, not an assertion that every product space has only two numerical dimensions.

## Open and closed interval notation

`(a,b)` means all real numbers strictly between a and b. `[a,b]` includes both endpoints. `[a,b)` includes a but excludes b. Parentheses also denote ordered pairs, so the surrounding sentence matters.

The persistence intervals in this course are `[birth, death)`. A class with interval `[1,2)` is present at 1 and absent at 2. Infinity is not an ordinary finite death value. In the saved JSON, an unpaired death is encoded by `null` together with a stated interpretation.

## Follow types through the whole course

A raw image is an 8-by-8 numerical array. A filtered pixel model is a collection of simplices with entrance values. A boundary matrix is an array over F₂. A homology class is an equivalence class of cycles. A persistence diagram is a multiset of birth/death pairs. A persistence image is a numerical feature array built from a diagram.

These objects can all be drawn, but they are not interchangeable. In particular, a persistence image is not a cleaned-up version of the original handwriting image. Naming every object's type is one of the fastest ways to catch a conceptual error.

## First independent checks

Without opening another page, explain why `{0}` differs from `∅`; why a 150-by-4 measurement table contains points in four-dimensional feature space; and why `f⁻¹(V)` does not require f to be one-to-one. Then explain the endpoints of `[1,√2)` in words.

**Primary follow-up:** R4 in [Sources](../docs/SOURCES.md), especially sets, functions, and logic. The examples on this page are original course examples, not excerpts from that book.
