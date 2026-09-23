# Source statements, mathematical tests and remaining limits

The supplied posts remain attributed source material. This edition does not silently turn promotional statements into proven facts. The author-written lessons are explanatory additions; the numerical reports document actual course experiments, not full-paper reproductions.

| Supplied concept | Source framing | Canonical treatment | What this does not establish |
|---|---|---|---|
| PINN/PIKAN failures | Conflicting residual, boundary and interface gradients; Norm-PCGrad benchmark claims | [Stage 27](../../physics/lessons/27.md), gradient examples and interface controls | Full 2D/3D benchmark reproduction, universal conflict-free descent or measured negligible overhead. |
| Symplectic structure | Post claims exact arbitrary-step energy conservation and eliminated drift | [Stage 24](../../physics/lessons/24.md), separate symplectic, energy and state errors | That preserving one geometric property preserves every physical quantity. |
| Manifold projection | Post describes one algebraic correction as returning to the physical manifold | [Stage 25](../../physics/lessons/25.md), nonlinear residual and iteration checks | One Newton-like correction being exact for a general nonlinear constraint. |
| HNNs and LNNs | Different mechanics formulations related through the Legendre transform | [Stage 23](../../physics/lessons/23.md), regularity assumptions and restricted teaching networks | A general LNN benchmark or physical validity outside the modeled regime. |
| Charts and flows | Local coordinates, smooth transitions and local diffeomorphisms | [13](../../lessons/13_lesson.md) and [22](../../physics/lessons/22.md), explicit map/inverse tests | A camera image being an invertible chart of an entire 3D scene. |
| VGGT and successors | Learned geometry proposed from RGB input | [16](../../lessons/16_lesson.md), architecture and output contracts | Trained VGGT inference, metrically calibrated output, or independently validated fast sports motion. |
| ROS2/point-cloud speed | Source reports throughput and conversion improvements | [18](../../lessons/18_lesson.md), CPU profiling and timing boundaries | Reproduction of the post's GPU hardware or latency benchmark. |
| Human–object interactions | Prototype combines pose, tracks and temporal reasoning | [19](../../lessons/19_lesson.md), timing and negative controls | Proximity proving contact, or independent basketball event precision/recall. |

## A concrete distinction
For a unit-mass oscillator with H=(q²+p²)/2, a kick-then-drift symplectic Euler step from (1,0) with h=0.2 gives p=-0.2 and q=0.96. Its energy is (0.96²+0.2²)/2=0.4808, not 0.5. This is our worked counterexample to a general arbitrary-step exact-energy assertion, not a quotation from the supplied post.

The existing mathematical treatment and source audit are preserved in [the v5 audit](../v5/SOURCE_AUDIT.md), [geometry source references](../SOURCES_V3.md), and [v8 sports audit](../v8/SOURCE_AUDIT.md). Source links are dated; mutable websites can change after review.

## Verification boundaries
A hash verifies identity of bytes relative to the stated expected value. It does not verify the scientific truth of measurements. A notebook run verifies that those code cells executed under the recorded environment. A mathematical theorem requires its hypotheses and proof, not merely many passing numeric checks. An optional acquisition plan is not a downloaded payload.

The original book's complete text has not been inspected. [The book audit](../BOOK_TOC_AUDIT_V2.md) remains open. Major theorems and advanced directions are explicitly identified in [proof deepening](../DEEPENING_PROOFS.md). Do not mark them complete from file counts.
