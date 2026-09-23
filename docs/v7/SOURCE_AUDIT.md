# Source audit — preserve claims, label extensions

## Basis of the course

The original learning source proposes: understand the idea, state it precisely, calculate by hand, implement, test and explain limitations. The 31 retained stages and 31 new entry guides continue that organization. The book’s table of contents, not its complete text, supplied the initial scope. No chapter is marked as independently audited against unavailable full text.

The supplied social-media posts and prior WMS integration note are retained as conceptual prompts through the existing source ledgers. We do not redistribute unrelated profile and messaging text. The additional calculations below are original educational extensions requested by the user, not text silently substituted for the source authors' arguments.

| Supplied source | What it asserts or proposes | This course's separate treatment |
|---|---|---|
| PINN/PIKAN gradient-conflict post (supplied lines 65–81) | Composite residual, boundary and interface objectives can conflict; Norm-PCGrad improves the authors' benchmarks. | Preserve benchmark scope; retain Stage 27; add the exact opposite-gradient example, which is not a benchmark reproduction. |
| Invariant-manifold/symplectic post (lines 67–84) | Symplectic structure is presented as ensuring exact energy over arbitrary steps; one algebraic correction is presented as constraining updates to the manifold; major throughput claims are made. | Attribute those claims; separately calculate the oscillator's energy change and a nonzero sphere residual. No GPU/HPC benchmark or climate validation is claimed. |
| HNN/LNN comparison (lines 65–90) | Learn mechanics through Hamiltonian or Lagrangian structure and a Legendre connection. | Retain definitions and add explicit momentum/velocity arithmetic and regularity requirements. The trained LNN remains a restricted teaching model. |
| Smooth-manifold/chart post (lines 67–100) | Local coordinates, smooth transitions and vector-field-generated local diffeomorphisms. | Retain its local framing; teach explicit chart round trips and finite-time flow domains. Numerical steps are not assumed to inherit exact-flow invertibility. |
| WMS geometry/engineering/events note | Geometry proposals need metric registration and holdouts; profiling and temporal evidence matter. | Keep the existing modules and boundaries. Current v7 work changes the learning package, not WMS production code or automations. |

## External research checked for the new addition

UCI Seeds and Concrete Slump metadata and their complete numeric endpoints were inspected. Both source cards specify the units provided, missing metadata, observation counts, licenses and DOI. Source transfer into the container used declared numeric transcription, not a claimed byte-identical download. See the data catalogue for the outstanding remote numeric comparison.

The primary conformal reference is [Angelopoulos and Bates, A Gentle Introduction to Conformal Prediction](https://arxiv.org/abs/2107.07511). The new lab uses a direct finite-sample order statistic and an explicit infinite-radius case. Its guarantee requires a predictor fixed independently of exchangeable calibration/test scores. Marginal coverage is not guaranteed conditional coverage for every recipe. The article's empirical studies are not reproduced here.

The gradient-conflict paper [Tackling Failure Modes of PINNs and PIKANs Using Conflict-Free Gradients](https://arxiv.org/abs/2609.14841) remains a primary reading supporting attribution of the supplied post's research claims. The new opposite-gradient calculation does not establish that Norm-PCGrad wins or loses on its experimental benchmarks.

For formal topology, the retained course uses the [ETH 2026 TDA course](https://ti.inf.ethz.ch/ew/courses/TDA26/index.html), Tinarrage, Morris and the linked deeper references. The entry guides are short original worked examples; they do not replace the formal proofs or claim author endorsement.

## How to state a result honestly

“Source-reported” means an author made the claim in the identified source. “Analytically derived” means the shown argument establishes it under its explicit assumptions. “Executed” means the recorded implementation ran in this environment and produced the retained outputs. “Independently validated” would require appropriate separate evidence; ordinary regression tests and source hashes do not alone establish it.

The v7 data experiments use observed kernel/mixture records; duplicate rows, rectangles, oscillator trajectories, attention arithmetic and sphere corrections are manufactured or analytic controls. They remain labeled that way. A plausible plot is not a proof of causality, calibrated scale, structural safety or domain transfer.
