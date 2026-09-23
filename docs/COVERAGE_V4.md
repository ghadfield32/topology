# Stage coverage and explicit outcomes — v4

All 21 stages are preserved. These are original curriculum targets, not checked learner achievements. See [the learning policy](COMPLETION_SYSTEM_V4.md).

## Stage 00 — Start here: how to learn, run, and question the results
**Focus:** Read a measurement before calculating with it
**Prerequisites:** none; use the beginner primers

1. Identify one observation, one measured feature, one label, and a source identifier.
2. Explain the two axes of a table and the three axes of an image collection.
3. Produce a small descriptive result with explicit units and a reproducible row selection.
4. Distinguish executing a reference solution from demonstrating your own understanding.

[Guided session](../sessions/00_session.md) · [Reference lab](../notebooks/00_lab.ipynb) · [Consolidation](../consolidation/00_lab.ipynb) · [Learner code](../practice/learner/00_practice.ipynb)

## Stage 01 — Mathematical language, proofs, and linear algebra
**Focus:** Why the arithmetic system changes the answer
**Prerequisites:** 00

1. Translate a small matrix into a system of equations.
2. Perform a row operation and explain why it preserves the solution set.
3. Compare rank over the real numbers and over a prime field.
4. Distinguish a numerical calculation on an image from a topological invariant.

[Guided session](../sessions/01_session.md) · [Reference lab](../notebooks/01_lab.ipynb) · [Consolidation](../consolidation/01_lab.ipynb) · [Learner code](../practice/learner/01_practice.ipynb)

## Stage 02 — Closeness, metrics, neighborhoods, and topologies
**Focus:** Separate units, distance, and topology
**Prerequisites:** 01

1. Check the metric axioms on an explicit counterexample.
2. Explain why positive coordinate rescaling preserves Euclidean-space topology but changes distance scale.
3. Compare nearest observations before and after a declared feature rescaling.
4. State the difference between distinct locations and distinct observation IDs.

[Guided session](../sessions/02_session.md) · [Reference lab](../notebooks/02_lab.ipynb) · [Consolidation](../consolidation/02_lab.ipynb) · [Learner code](../practice/learner/02_practice.ipynb)

## Stage 03 — Continuity, homeomorphisms, connectedness, and compactness
**Focus:** A continuous map can discard the information you need
**Prerequisites:** 02

1. Use inverse images, rather than pictures alone, to define continuity.
2. Distinguish a continuous bijection from a homeomorphism.
3. Construct a projection that sends different inputs to the same output.
4. Explain why a finite numerical check cannot prove an infinite-space theorem.

[Guided session](../sessions/03_session.md) · [Reference lab](../notebooks/03_lab.ipynb) · [Consolidation](../consolidation/03_lab.ipynb) · [Learner code](../practice/learner/03_practice.ipynb)

## Stage 04 — Groups, symmetries, paths, loops, and homotopy
**Focus:** Symmetry preserves some things, not everything
**Prerequisites:** 03

1. Calculate a rotation and reflection and show that their order can matter.
2. Distinguish a group action from a label-preserving data augmentation assumption.
3. Explain homotopy using an annulus and a circle.
4. Identify what prevents a proposed deformation from being well defined.

[Guided session](../sessions/04_session.md) · [Reference lab](../notebooks/04_lab.ipynb) · [Consolidation](../consolidation/04_lab.ipynb) · [Learner code](../practice/learner/04_practice.ipynb)

## Stage 05 — Surfaces, simplices, triangulations, and pixel geometry
**Focus:** Choose the object before counting its holes
**Prerequisites:** 04

1. Distinguish closed-square pixel geometry from a graph of pixel centers.
2. Count vertices, edges, and faces of a small cell complex.
3. Explain why diagonal touching connects closed squares.
4. Declare the intensity threshold before interpreting a real image.

[Guided session](../sessions/05_session.md) · [Reference lab](../notebooks/05_lab.ipynb) · [Consolidation](../consolidation/05_lab.ipynb) · [Learner code](../practice/learner/05_practice.ipynb)

## Stage 06 — Chains, boundaries, homology, and Betti numbers
**Focus:** Learn what coefficient fields reveal and forget
**Prerequisites:** 05

1. Construct an oriented integer boundary and check boundary-of-boundary.
2. Calculate how a coefficient change affects a cellular boundary map.
3. Independently verify image homology across multiple thresholds.
4. Distinguish Betti numbers from full integer homology, including torsion.

[Guided session](../sessions/06_session.md) · [Reference lab](../notebooks/06_lab.ipynb) · [Consolidation](../consolidation/06_lab.ipynb) · [Learner code](../practice/learner/06_practice.ipynb)

## Stage 07 — From data to shape: Rips, Čech, alpha, and filtrations
**Focus:** Understand why the same points give different complexes
**Prerequisites:** 06

1. Derive edge and face entry times from a declared filtration convention.
2. Explain pairwise overlap versus a common intersection.
3. Build a small Rips filtration and verify that faces appear no later than cofaces.
4. Use a real point cloud without treating its label columns as geometry.

[Guided session](../sessions/07_session.md) · [Reference lab](../notebooks/07_lab.ipynb) · [Consolidation](../consolidation/07_lab.ipynb) · [Learner code](../practice/learner/07_practice.ipynb)

## Stage 08 — Persistent homology, persistence modules, and reading diagrams
**Focus:** Read a barcode as a history, not a collection of scores
**Prerequisites:** 07

1. Derive the square filtration and its positive-length interval.
2. Explain half-open interval endpoints and zero-length bars.
3. Cross-check barcode Betti counts against thresholded real images.
4. Distinguish an unpaired class in a truncated filtration from a globally essential class.

[Guided session](../sessions/08_session.md) · [Reference lab](../notebooks/08_lab.ipynb) · [Consolidation](../consolidation/08_lab.ipynb) · [Learner code](../practice/learner/08_practice.ipynb)

## Stage 09 — Implement persistence, trace the algorithm, and test it independently
**Focus:** Verify persistence without trusting the same algorithm twice
**Prerequisites:** 08

1. Explain what a boundary-column pivot represents.
2. Relate finite H0 death times to spanning-tree edge weights.
3. Handle duplicate observations and zero-length intervals explicitly.
4. State the dimension and scope actually checked by an independent oracle.

[Guided session](../sessions/09_session.md) · [Reference lab](../notebooks/09_lab.ipynb) · [Consolidation](../consolidation/09_lab.ipynb) · [Learner code](../practice/learner/09_practice.ipynb)

## Stage 10 — Stability, diagram distances, noise, and scientific uncertainty
**Focus:** A stability bound is not a discovery certificate
**Prerequisites:** 09

1. State the fixed-domain filtration assumptions behind the tested bound.
2. Explain why a diagram point can match to the diagonal.
3. Compute a bounded image perturbation and its diagram distance.
4. Distinguish deterministic stability, statistical uncertainty, and scientific meaning.

[Guided session](../sessions/10_session.md) · [Reference lab](../notebooks/10_lab.ipynb) · [Consolidation](../consolidation/10_lab.ipynb) · [Learner code](../practice/learner/10_practice.ipynb)

## Stage 11 — Useful representations, Mapper, time windows, and honest machine learning
**Focus:** Build a feature pipeline without seeing the answer
**Prerequisites:** 10

1. Distinguish fixed per-observation transformations from dataset-fitted preprocessing.
2. Apply training-only scaling and identify where validation data may be used.
3. Construct lagged features with their correct availability dates.
4. Separate topological representation design from proof of predictive value.

[Guided session](../sessions/11_session.md) · [Reference lab](../notebooks/11_lab.ipynb) · [Consolidation](../consolidation/11_lab.ipynb) · [Learner code](../practice/learner/11_practice.ipynb)

## Stage 12 — Capstone: reproduce, defend, transfer, and audit the book
**Focus:** Interpret a small improvement with paired evidence
**Prerequisites:** 11

1. Construct the paired correctness table for two models on the same observations.
2. Distinguish percentage points, counts, and conditional inferential quantities.
3. Calculate an exploratory exact discordance test and paired bootstrap interval.
4. Explain why reanalyzing an exposed holdout cannot create a fresh confirmatory test.

[Guided session](../sessions/12_session.md) · [Reference lab](../notebooks/12_lab.ipynb) · [Consolidation](../consolidation/12_lab.ipynb) · [Learner code](../practice/learner/12_practice.ipynb)

## Stage 13 — From topology to smooth manifolds
**Focus:** A chart changes coordinates, not the underlying point
**Prerequisites:** 12

1. Write the domain restriction of a stereographic chart.
2. Check that chart-to-space-to-chart returns the same point.
3. Construct a tangent vector by removing its radial component.
4. Explain why normalizing scene points does not prove a spherical physical scene.

[Guided session](../sessions/13_session.md) · [Reference lab](../notebooks/13_lab.ipynb) · [Consolidation](../consolidation/13_lab.ipynb) · [Learner code](../practice/learner/13_practice.ipynb)

## Stage 14 — Rotations, rigid transforms, and the camera model
**Focus:** Make camera equations reversible only when the information exists
**Prerequisites:** 13

1. Name the source and destination frame of a rigid transformation.
2. Distinguish optical-axis depth from radial distance.
3. Project and unproject real reference points using the same calibration.
4. Explain why a round-trip check is not independent measurement validation.

[Guided session](../sessions/14_session.md) · [Reference lab](../notebooks/14_lab.ipynb) · [Consolidation](../consolidation/14_lab.ipynb) · [Learner code](../practice/learner/14_practice.ipynb)

## Stage 15 — Measured stereo, calibration, and uncertainty
**Focus:** Turn disparity error into a physical uncertainty calculation
**Prerequisites:** 14

1. Derive the principal-point offset in rectified stereo.
2. Carry pixels and metres through the depth formula.
3. Compare a first-order uncertainty calculation with controlled numerical perturbations.
4. State which uncertainties a supplied-reference experiment cannot measure.

[Guided session](../sessions/15_session.md) · [Reference lab](../notebooks/15_lab.ipynb) · [Consolidation](../consolidation/15_lab.ipynb) · [Learner code](../practice/learner/15_practice.ipynb)

## Stage 16 — Attention and VGGT, from pixels to proposed geometry
**Focus:** Attention moves information; training gives it task meaning
**Prerequisites:** 15

1. Identify query, key, and value shapes in scaled dot-product attention.
2. Explain why each attention row sums to one.
3. Check a controlled attention calculation on patches from a real image.
4. Distinguish an attention example, a model-output contract, and actual trained VGGT inference.

[Guided session](../sessions/16_session.md) · [Reference lab](../notebooks/16_lab.ipynb) · [Consolidation](../consolidation/16_lab.ipynb) · [Learner code](../practice/learner/16_practice.ipynb)

## Stage 17 — Register, validate, and ask topology the right question
**Focus:** Fit on anchors, evaluate elsewhere
**Prerequisites:** 16

1. Distinguish rigid alignment from a similarity transform with scale.
2. Separate fitting references from held-out evaluation points.
3. Construct a negative control showing why fitted residual is optimistic.
4. Explain why perfect synthetic-transform recovery does not validate physical scene scale.

[Guided session](../sessions/17_session.md) · [Reference lab](../notebooks/17_lab.ipynb) · [Consolidation](../consolidation/17_lab.ipynb) · [Learner code](../practice/learner/17_practice.ipynb)

## Stage 18 — Make the pipeline efficient without changing the evidence
**Focus:** Separate throughput from how old the answer is
**Prerequisites:** 17

1. Preserve numerical outputs while changing an implementation.
2. Distinguish measured code duration from simulated queue latency.
3. Derive queue growth when service is slower than arrival.
4. Report warm-up, work units, and timing boundaries.

[Guided session](../sessions/18_session.md) · [Reference lab](../notebooks/18_lab.ipynb) · [Consolidation](../consolidation/18_lab.ipynb) · [Learner code](../practice/learner/18_practice.ipynb)

## Stage 19 — From geometry to cautious interaction hypotheses
**Focus:** Do not let future observations leak into an event decision
**Prerequisites:** 18

1. Distinguish event onset, confirmation time, and observation availability.
2. Construct a past-only confirmation rule on a real dated series.
3. Check that extending the future does not revise already-issued decisions.
4. Separate a threshold-rule output from validated human–object interaction labels.

[Guided session](../sessions/19_session.md) · [Reference lab](../notebooks/19_lab.ipynb) · [Consolidation](../consolidation/19_lab.ipynb) · [Learner code](../practice/learner/19_practice.ipynb)

## Stage 20 — Independent spatial capstone and continuing mastery
**Focus:** Turn a completed course into a reproducible next investigation
**Prerequisites:** 19

1. Assemble the chain from question through measurement, representation, computation and claim.
2. Audit the presence and integrity of execution evidence without equating it with mastery.
3. Identify what a new independent dataset must provide for the intended claim.
4. Use a finite completion contract while leaving advanced topics and the actual-book audit explicit.

[Guided session](../sessions/20_session.md) · [Reference lab](../notebooks/20_lab.ipynb) · [Consolidation](../consolidation/20_lab.ipynb) · [Learner code](../practice/learner/20_practice.ipynb)

## Coverage that remains deliberately open
The supplied book section titles remain mapped in the inherited book audit. No full book text has been inspected. A numerical experiment is not a full proof of a major theorem. Optional Ripser/GUDHI comparison is skipped in this build. Trained VGGT inference, independent physical holdouts, real sports-event labels, unseen-writer evaluation, and production integration are not delivered validations. These distinctions are scope boundaries, not hidden completed tasks.
