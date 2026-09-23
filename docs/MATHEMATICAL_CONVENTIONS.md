# Mathematical and computational conventions

These are binding for comparing the notebook results. Changing one creates a different analysis unless a theorem shows equivalence.

| Item | Convention in the executable core |
|---|---|
| Observation identity | Original dataset row IDs retained; labels are excluded from geometry unless the experiment explicitly models labels. |
| Distances | Euclidean distances on declared features; stage-specific rescaling always stated. Distinct IDs with identical coordinates give a pseudometric on IDs. |
| Complex | Finite abstract simplices stored as sorted nonempty tuples of distinct integer vertex IDs. |
| Face condition | Every nonempty face must be present. Validation rejects missing faces; closure deliberately constructs them. |
| Coefficients | F₂; row and column arithmetic modulo two, implemented with XOR. |
| Homology | Ordinary simplicial homology, not reduced homology. A point has β₀=1. |
| Rips parameter | ε is maximum allowed pairwise edge length, not radius. The complex includes simplices whose diameter is ≤ε. |
| Dimension | To report Hₖ of a Rips model, build through dimension k+1. The returned maximum homology dimension is separately stated. |
| Ties | Sort by filtration value, then simplex dimension, then vertex tuple. Faces precede cofaces at equal values. |
| Intervals | Half-open [birth,death); exactly zero-length intervals omitted by default. No arbitrary denoising cutoff is silently applied. |
| Infinity | An unpaired class survives the supplied filtration. Infinity may mean truncation, not a globally essential class. |
| JSON | Nonfinite endpoints encode as null, with the report noting the convention. Finite results are never serialized as invalid JSON NaN or Infinity. |
| Pixel object | Union of closed squares; corner-touching squares are connected; no periodic boundary or padded exterior. |
| Pixel scalar | f=1−intensity/16 for digits. Both triangles of a square enter at the square value; shared faces receive the minimum incident value. |
| Pixel triangulation | Filtration-preserving subdivision of the declared square-cell union, not a general physical surface reconstruction. |
| Diagram distance | `finite_bottleneck` uses maximum-norm matching with diagonal matches and rejects essential intervals. Stage 10 uses completed finite H₁. |
| Features | Fixed per-image 20-vector; finite lifetime summaries plus Betti counts including essential classes. Dataset-learned scaling occurs only inside model pipelines. |
| Mapper | Scalar-lens cover, DBSCAN with min_samples=1, nodes = local clusters, edges = shared original observations. Only the nerve's 1-skeleton is plotted. |
| Delay windows | Forward windows are available only at the last included sample. A spatial image profile is not described as temporal data. |
| ML split | Frozen per-image training/validation/test split; no writer IDs; no claim of writer independence. |
| Library comparisons | Match field, scale, dimension, cutoffs, zero-length policy and tolerance. Optional checks not executed here remain pending. |

## Important clarifications to earlier intuition

“Same number of holes” is not sufficient to establish a homeomorphism. A torus **surface** has two independent H₁ classes; a solid torus has the homotopy type of a circle. “Enclosed void” is not a general definition of H₂. In arbitrary spaces, H₀ counts path components in the relevant homology framework; the finite simplicial examples make connected and path-connected components coincide.

A topology can be defined without a metric. A finite metric sample of distinct points is discrete even when it resembles a curve. Rips persistence encodes numerical distance scale and is not invariant under every homeomorphism of a generating shape.

These are explicit course clarifications and expansions of the supplied outline. The original attachment is preserved unchanged; no revision is attributed to the book's author.
