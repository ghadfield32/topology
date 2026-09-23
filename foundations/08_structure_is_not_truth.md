# Primer 08 — What a physical guarantee actually guarantees

A claim should have an object, assumptions and a conclusion. "The model conserves energy" leaves all three unclear. Which energy: a fitted scalar, a measured physical quantity, or an invariant of a numerical update? Under which forces, boundary conditions, coordinate choice, time dependence and precision? Along an exact continuous solution or along a discrete simulation?

An **invariant** stays unchanged under a specified transformation or evolution. A **constraint** defines allowed states, such as x²+y²=1. A **conservation balance** includes exchanges: energy can decrease through friction or enter through a motor. A **symmetry** is a transformation that leaves a specified mathematical object unchanged. An **equivariant map** transforms its output consistently when its input is transformed. These ideas are related, but none is interchangeable with the others.

Topology describes continuity and features such as components and cycles. Geometry adds distances, angles and more structure. A phase space describes states such as position and momentum. A symplectic form is additional phase-space structure, not merely a count of holes. Two trajectories can have similar persistence diagrams while having very different phases, speeds, units or causal mechanisms.

**Model error** comes from approximating the system with the wrong equations or parameters. **Numerical error** comes from approximating the solution of those equations. **Measurement error** comes from imperfect observations. **Statistical error** arises when finite observations are used to estimate population-level quantities. Testing only one does not eliminate the others.

Four separate checks keep these distinctions practical. First, test algebraic properties on exact small examples. Second, compare the numerical method with an analytic or independently resolved reference. Third, test predictions against measured holdouts with known provenance. Fourth, test the deployed system with the actual timing, hardware, sensors and users. A green result at one level is not a green result at every level.

For manufactured data, we choose a solution and derive the corresponding equation or observations. This gives an exact answer for debugging, not evidence about the world. For constructed transformations of real data, the starting observations are real but the transformation is ours. For empirical validation, the held-out outcome itself must have been independently measured. All three are useful when labeled correctly.

## Vocabulary to keep separate

A certificate is evidence that a stated condition was met, not a vague feeling of confidence. A tolerance is an allowed numerical deviation with a declared norm and scale. A baseline is a comparison method, not an intentionally crippled competitor. A benchmark is a fixed task and evaluation protocol. A deployment claim concerns an operating environment, not just a notebook. A source audit distinguishes what an author reported from what you verified.

## One counterexample is enough for a universal claim

Suppose someone says every symplectic numerical step conserves the original energy exactly. A single valid symplectic step with nonzero energy change disproves that statement. It does not prove symplectic methods are useless. Conversely, testing a thousand successful trajectories does not prove success for every possible trajectory. Learn to narrow a claim rather than swing between unconditional trust and dismissal.

Practice: an image-derived ball track is smooth after filtering. What does that establish? It establishes a property of the filtered output, not that the ball was observed during occlusion or that smoothing preserved release timing. A learned Hamiltonian stays nearly constant. What is missing? Evidence that it matches the relevant physical energy, plus numerical, parameter, force and observation checks.
