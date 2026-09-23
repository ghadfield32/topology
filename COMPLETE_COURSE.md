# Listening to Shape v12 — Canonical reading volume

Operational setup and current execution evidence: docs/release/FIRST_RUN.md and docs/release/VERIFICATION.md.

One source per selected section. This optional export is not another required course: START_HERE.html links the same source lessons individually. Reference notebooks, answer keys, dataset cards, and deeper primers remain separate. Old cumulative versions are not embedded.


---

Source: `curriculum/START.md`

# Listening to Shape — one learning route

This is the consolidated v12 course. It builds on the previous material instead of adding another required copy of every explanation. The 31 core stages are unchanged. The sports and industry cases are applications of those foundations, not additional prerequisites for beginning topology.

## Start with one stage, not every file
For each stage, open its **stage page**. Read its one primary lesson, predict and run its one primary reference lab, then attempt its learner notebook and reasoning questions. Answers stay separate. Only open a workbook, guided session or primer when the stage identifies a gap. These are optional repair resources, not three additional mandatory readings of the same concept.

A repeated question after a delay is deliberate retrieval practice. An example in a second industry tests transfer. Neither should be mistaken for another first introduction. The catalog gives each primary lesson one stage owner.

## Three connected routes
**Shape and topology, 00–12:** start here. Observations, symbols, algebra, distance, continuity, homotopy, complexes, homology, persistence, algorithms, stability and applications. This is the core aligned to the supplied book outline.

**Spatial geometry, 13–20:** add manifolds, rotations, cameras, measured stereo, learned-geometry concepts, registration, systems timing and interaction hypotheses. Camera pictures and markerless estimates are not automatically metric truth.

**Scientific machine learning, 21–30:** develop calculus and equations before flows, mechanics, integrators, constraints, residual learning, gradient interactions, neural operators and differentiable simulation. Manufactured examples have known answers; real measured systems need independent validation.

Begin from zero unless you can independently pass a stage gate. The dependency entries identify required foundations. Sequential order is a useful default, not a claim that all topology is required to inspect a camera matrix.

## A reliable learning session
1. State what one observation represents and what is known before computation.
2. Define the unfamiliar terms in your own words; give a nonexample.
3. Work a small calculation by hand, with units and assumptions.
4. Predict the code output, run in a fresh workspace, and compare.
5. Change one condition, such as scale, missingness, identity grouping or time.
6. Write what your result supports and a conclusion it cannot justify.
7. Attempt the independent question and revisit it after a delay.

Use shorter sessions when a proof is difficult. Finishing a large notebook without explaining it is not faster learning. A compiler error needs debugging; a wrong definition needs a prerequisite repair; an uninformative dataset needs a better experiment. Use the situation guide to distinguish them.

## Completion means evidence
The record distinguishes reading, guided practice, declared independent demonstration and delayed recall. Tests do not award mastery. A numerical example does not prove a general theorem. Major theorem proofs, the actual-book comparison and independent capstones remain explicit obligations.

## Stage directory

| Stage | Primary topic | Route |
|---|---|---|
| [00](curriculum/stages/00.md) | Start here: how to learn, run, and question the results | Shape and topology |
| [01](curriculum/stages/01.md) | Mathematical language, proofs, and linear algebra | Shape and topology |
| [02](curriculum/stages/02.md) | Closeness, metrics, neighborhoods, and topologies | Shape and topology |
| [03](curriculum/stages/03.md) | Continuity, homeomorphisms, connectedness, and compactness | Shape and topology |
| [04](curriculum/stages/04.md) | Groups, symmetries, paths, loops, and homotopy | Shape and topology |
| [05](curriculum/stages/05.md) | Surfaces, simplices, triangulations, and pixel geometry | Shape and topology |
| [06](curriculum/stages/06.md) | Chains, boundaries, homology, and Betti numbers | Shape and topology |
| [07](curriculum/stages/07.md) | From data to shape: Rips, Čech, alpha, and filtrations | Shape and topology |
| [08](curriculum/stages/08.md) | Persistent homology, persistence modules, and reading diagrams | Shape and topology |
| [09](curriculum/stages/09.md) | Implement persistence, trace the algorithm, and test it independently | Shape and topology |
| [10](curriculum/stages/10.md) | Stability, diagram distances, noise, and scientific uncertainty | Shape and topology |
| [11](curriculum/stages/11.md) | Useful representations, Mapper, time windows, and honest machine learning | Shape and topology |
| [12](curriculum/stages/12.md) | Capstone: reproduce, defend, transfer, and audit the book | Shape and topology |
| [13](curriculum/stages/13.md) | From topology to smooth manifolds | Spatial geometry |
| [14](curriculum/stages/14.md) | Rotations, rigid transforms, and the camera model | Spatial geometry |
| [15](curriculum/stages/15.md) | Measured stereo, calibration, and uncertainty | Spatial geometry |
| [16](curriculum/stages/16.md) | Attention and VGGT, from pixels to proposed geometry | Spatial geometry |
| [17](curriculum/stages/17.md) | Register, validate, and ask topology the right question | Spatial geometry |
| [18](curriculum/stages/18.md) | Make the pipeline efficient without changing the evidence | Spatial geometry |
| [19](curriculum/stages/19.md) | From geometry to cautious interaction hypotheses | Spatial geometry |
| [20](curriculum/stages/20.md) | Independent spatial capstone and continuing mastery | Spatial geometry |
| [21](curriculum/stages/21.md) | Rates, equations, units and what data can identify | Scientific machine learning |
| [22](curriculum/stages/22.md) | Smooth flows, coordinate changes and invertible networks | Scientific machine learning |
| [23](curriculum/stages/23.md) | Mechanics, Hamiltonian networks and Lagrangian networks | Scientific machine learning |
| [24](curriculum/stages/24.md) | Symplectic integration, energy, phase and long rollouts | Scientific machine learning |
| [25](curriculum/stages/25.md) | Constraints, projections, retractions and rank failure | Scientific machine learning |
| [26](curriculum/stages/26.md) | Physics-informed learning and inverse problems | Scientific machine learning |
| [27](curriculum/stages/27.md) | Conflicting gradients, interfaces, separability and PIKANs | Scientific machine learning |
| [28](curriculum/stages/28.md) | Functions to functions: DeepONet, Fourier operators and baselines | Scientific machine learning |
| [29](curriculum/stages/29.md) | Differentiable simulation, graph physics and attention constraints | Scientific machine learning |
| [30](curriculum/stages/30.md) | An independent world-model study: evidence before adoption | Scientific machine learning |

[Industry and sports applications](curriculum/APPLICATIONS.md) · [Which situation am I in?](curriculum/SITUATIONS.md) · [First session](docs/v9/FIRST_SESSION.md) · [Claims and limits](docs/v9/CLAIMS_AND_LIMITS.md)


## Optional continuations without a restart

The five [representation units](representations/lessons/R01.md) reuse the core and build through SIGReg/JEPA concepts to a measured small-encoder experiment. They do not change the existing stage numbers or mark earlier work complete. The [deployment lesson](docs/release/KUBERNETES.md) explains Kubernetes from the beginning and distinguishes project-policy tests from real cluster acceptance. Native Python is sufficient to begin learning.


---

Source: `docs/release/FIRST_RUN.md`

# First run — Listening to Shape v11

## What you are opening

This is a full source project, not the publisher's book and not a model-weight bundle. It preserves 31 primary core lessons, adds a five-unit representation continuation, and provides an optional Kubernetes lesson. There is one current starting page: `START_HERE.html`.

Keep your previous course folder. Extract into a new folder, including dotfiles. Preserve `my_work/`, edited learner notebooks, existing progress files, and evidence paths. Never overwrite personal work with blank templates.

For reading only, open `START_HERE.html`; the lessons and previously executed notebook outputs are included. For fresh execution, continue below. No Docker or Kubernetes installation is needed to learn the mathematics.

## 1. Put the project in Git without replacing an application

For a dedicated repository, the extracted `listening_to_shape_lab` folder is the project root. In an existing repository, place it in a new folder such as `learning/listening-to-shape/`. Do not replace the application's pyproject, lock, Dockerfile, CI, or agent instructions. Keep the course's own pyproject and environment in its subdirectory.

The repository handoff in `AGENT_HANDOFF.md` can be pasted into a coding agent after you identify the destination. It requests inspection, non-overwriting import, validation, and evidence collection; it does not authorize a push or production deployment. Read source/data licenses before publishing a public copy. Personal answers and active progress are ignored by Git; tracked blank templates live in `curriculum/response_templates/` and `progress/templates/`.

## 2. Install the runtime with uv

The tested Python interpreter is 3.13.5. Obtain uv from its official installation guide: https://docs.astral.sh/uv/getting-started/installation/ . After confirming `uv --version`, use:

```bash
uv python install 3.13.5
uv run --no-project --python 3.13.5 python tools/bootstrap.py --profile physics
```

This command is deliberately explicit about the bootstrap interpreter. `core` is sufficient for introductory topology and many data cases. `physics` adds PyTorch for neural physics and the R03/R04 representation work. `full` also requires Ripser and GUDHI comparisons.

Normal bootstrap resolves a genuine `uv.lock` or verifies an existing lock, then uses locked synchronization. It stops if the package index, binary wheel, certificate, or dependency resolution fails. Review the generated lock, run the checks, and commit it. No uv.lock was fabricated for this release: outbound package installation failed in the build environment.

The old `--reuse-installed` diagnostic route is explicitly not an independent installation. Do not relabel it as clean setup. On a machine that already used it, use a fresh extraction/environment for normal locked validation; no automatic environment deletion occurs.

For an already working Python launcher, `python3 tools/bootstrap.py --profile physics` is equivalent. Windows can use `py -3.13 tools/bootstrap.py --profile physics` after the matching interpreter is installed. Commands using `uv run --no-sync` below are the same on Mac, Windows, and Linux once setup succeeds.

## 3. Check the correct layer

```bash
uv run --no-sync python course.py doctor --profile physics
uv run --no-sync python course.py verify --profile physics
uv run --no-sync python course.py test --profile physics --output my_work/tests01
```

`doctor` checks installed prerequisites and reports deployment tools; it does not build Docker. `verify` checks the catalog and required paths; it does not execute every experiment. `test` executes the test suite and records JUnit/log evidence. A missing optional library is not an independent comparison. `full` verification treats skips as incomplete rather than silently passing them.

## 4. Begin one lesson and save your own work

```bash
uv run --no-sync python course.py stage 0
uv run --no-sync python course.py check 0
uv run --no-sync python course.py run --stage 0 --output my_work/stage00_attempt01
uv run --no-sync python course.py practice 0 --output my_work/practice00_attempt01
uv run --no-sync jupyter lab
```

Read the primary lesson before the saved reference. Open your copied `learner.ipynb` under the new practice folder and fill its deliberately unfinished functions. Use `answer.md` to record the observation unit, assumptions, prediction, hand calculation, result, explanation, and unsupported conclusion. The tool copies templates; it does not grade your understanding.

A run makes an isolated workspace, uses the exact launching interpreter for its kernel, records source hashes, and copies fresh outputs into the new result folder. Original data/notebooks/progress are protected by fingerprints. Existing output folders are refused; choose `attempt02` for another run. Errors preserve partial evidence instead of returning a success claim.

## 5. Continue the representation unit without restarting

```bash
uv run --no-sync python course.py cases
uv run --no-sync python course.py run --case r01 --output my_work/r01_attempt01
uv run --no-sync python course.py practice r01 --output my_work/practice_r01_attempt01
```

Proceed through r02, r03, r04, and r05 after their prerequisites. R04 trains the small encoders on real digit images. R05 explicitly reruns R04 before reading its outputs. The two later units need the physics profile. No video weights or full sports corpora are downloaded automatically.

For the complete reference suite:

```bash
uv run --no-sync python course.py run --all --output my_work/all_references01 --jobs 2
```

A full-reference run includes all original answers and new representation answers, not learner functions. Two workers balance resource usage; use `--jobs 1` on constrained machines. A notebook passing does not certify mathematical mastery, a major theorem, or a model's domain validity.

## 6. Read through the local server

```bash
uv run --no-sync python course.py serve
```

Open the address printed by the command. The reader binds to loopback and denies private paths, secrets, external symlinks, and directory listings. It does not serve personal result folders. Open your result notebooks in Jupyter or directly from your own filesystem. Never expose this development server as an authenticated public product.

## 7. Docker, then Kubernetes only when needed

Run `python3 tools/docker_verify.py --profile physics --output my_work/docker01` after a genuine lock and Docker engine exist. Follow `KUBERNETES.md` for the named kind cluster, policy inspection, explicit context, PVC persistence, live Job verification, and export-before-cleanup instructions.

The delivered verification report marks Docker/Kubernetes execution and a fresh uv dependency install as blocked. Included manifests, fixture tests, and ready-to-run commands are not misrepresented as a successful deployment.

## Common first failures

- “command not found”: install the corresponding prerequisite; changing Python code does not install Docker or kubectl.
- Wrong interpreter or missing torch: inspect `doctor` and the kernel provenance, then synchronize the intended profile.
- Package resolution/DNS failure: keep the failure log; do not copy an unrelated lock or silently remove requirements.
- Existing output folder: keep the evidence and choose a new attempt path.
- Learner `NotImplementedError`: complete the exercise or open the separate worked reference; do not include learner notebooks in reference verification.
- Confusing method names: use `representations/TERMINOLOGY.md` and the source audit, not a second duplicate introductory course.

The actual book text, independent domain validation, large model reproductions, and advanced proof obligations remain explicitly outside automatic software completion. Learn until you can explain and defend the result, not until a progress checkbox changes.


---

Source: `lessons/00_lesson.md`

# Stage 00 — Start here: how to learn, run, and question the results

**Starting point:** No prior topology knowledge is assumed.

**Learning cycle:** understand → define → work by hand → predict → run → critique → retrieve later.

## 1. Begin with observations, not unfamiliar terminology
Imagine putting several dots on paper. You can ask where each dot is, which dots are close together, whether they form separated groups, and whether they surround an empty region. These are different questions. A table of measurements can be treated similarly even when its rows have more than two numbers and cannot be drawn faithfully on a page.

An **observation** is one measured item. A **feature** is one measurement of that item. A **dataset** collects observations. In our Iris data, an observation is a flower sample and a feature is a measured length or width. In our digits data, an observation is a small handwriting image. A **label** says which species or digit was recorded; it is not a geometric coordinate unless we deliberately, and usually inappropriately, put it into the distance calculation. See sources D1–D3 for the actual dataset descriptions.

We will start with tiny examples whose answers can be derived exactly. We will then use genuine measured data. Artificial circles are useful controls, not evidence that real populations are circular. Every notebook identifies which kind of example it is using.

**Topology** studies spaces and continuous maps. **Homology** translates part of their shape information into algebra. **Persistence** follows homology classes as a construction changes with a parameter. Those words will become precise one at a time; you do not need to understand them before starting.

## 2. Your two routes through the package
The reading route needs no installation: open `START_HERE.html`, read a stage, and view its saved notebook outputs. The experimentation route uses Python and Jupyter. Follow `README.md` to create one project-specific environment, then open the notebooks in numerical order. A notebook mixes explanatory text with executable code cells. Run cells from the top. Restarting the kernel and running all cells is the best check that the notebook does not depend on forgotten variables.

A terminal is a program into which you type commands. A folder path tells it where a file lives. `cd` changes the working folder. `python` starts the Python interpreter; `python -m pytest` asks Python to run the test module. The virtual environment is a separate package installation area for this course; it is not a new operating system. You do not need a GPU or to modify your production projects.

Python counts positions starting at zero. `x[0]` means the first item. `len(x)` counts items. `print(x)` displays a value. An assignment such as `a = 3` stores a value; `a == 3` asks whether two values are equal. `assert condition` stops execution when the condition is false. An assertion is an automatic check of one statement in a computation, not a proof about all possible inputs.

A NumPy **array** is a structured collection of numbers. A 2D array has rows and columns: a shape of `(150, 4)` means 150 rows and four columns. The expression `X[:, 0]` selects all rows of the first column. `import numpy as np` makes the numerical library available under the short name `np`. You will see these patterns repeatedly.

## 3. Learn in six moves
Read an explanation and say what problem it solves. State the definition. Work one small example on paper. Predict the code output. Run the code and compare. Finally, explain what the output does not establish.

Do not immediately read the solution after a difficulty. Write the exact point at which you became stuck: an unknown word, a missing algebra step, an unclear assumption, or a programming error. Read the relevant hint in the lesson, try again, and then compare with the separate solution. Re-solving a related question after a delay is more informative than recognizing an answer you just saw.

Each stage has a short notebook plus a detailed lesson and worked exercise solutions. The code is already functional: your task is to understand and modify it, not repair intentionally broken starter files. A deeper code-reading task points to a specific function in `src/shape_lab`. The tests under `tests/` check mathematics and software. They do not mark you as mathematically proficient.

## 4. Know the boundaries of the claim
This is an original introductory course aligned to the supplied chapter outline, not the text of *Listening to Shape*. The publisher page could not be retrieved during this build; its March 2027 date remains the user's supplied listing, not a newly confirmed release promise. A final book audit is included for when the actual text is available.

The course's central computation is ordinary homology over the two-element field. It covers essential point-set topology, introductory algebraic topology, one-parameter persistence, and applied evaluation. Advanced topics have an explicit bridge later; no finite archive should pretend to include every theorem in topology.

The core was designed to run with the numerical packages available in the build environment. Ripser and GUDHI are optional cross-checks. Their installation was blocked here, so their checks are labeled NOT RUN, not passed. This is a limitation of the independent validation evidence, not a reason to invent results.

## 5. Your first practical session
Open the Stage 00 notebook. Run the cell that shows array shapes and a few **training** observations. Make a simple plot and locate its saved PNG in `reports/stage_00`. Change one display choice, rerun, and explain what changed. No interpretation of holes is expected yet.

Use the version-3 learner record in `progress/learning_log_v3.json`; see `docs/LEARNING_SYSTEM_V3.md` for recording evidence or preserving an older log. Leave all stages unmastered initially. Record both what you did independently and what you needed help with. When continuing here, paste your stage number, answers, and any error traceback rather than saying only that it did not work.

## Independent exercises

Do these before reading the worked solutions. A copied solution is not an independent pass.

**00.1.** Explain observation, feature, label, and dataset using one handwriting image.

**00.2.** What do the two numbers in an array shape mean? What does X[:, 0] select?

**00.3.** Predict whether `3 == 3` and `3 == 4` are true; explain why assignment is different.

**00.4.** Why do we run an exact synthetic example before a real-data experiment?

**00.5.** What does a passed software test establish, and what does it not establish?

**00.6.** Find the digits split sizes in data/manifest.json and explain why they are not the original UCI split.

## Mastery gate

Run Stage 00, explain its data shapes and provenance, and distinguish code execution from understanding.

Explain one limitation and solve a new variant after a delay. Suggested progression threshold: 85% on the local knowledge check, with every critical error corrected. This is a course rubric, not accreditation.

## Free readings and attribution

Source IDs: D3, R1. See `docs/SOURCES.md` for direct official links and assigned topics. The exposition, examples, code, and solutions here are original course material, not copied textbook chapters.

## Run and continue

Open `notebooks/00_lab.ipynb`. Its saved outputs are also readable from the browser reader. After the lab, compare with `solutions/00_solutions.md`, record what was independent, and continue only when the gate is met.


---

Source: `lessons/01_lesson.md`

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


---

Source: `lessons/02_lesson.md`

# Stage 02 — Closeness, metrics, neighborhoods, and topologies

**Starting point:** Complete the Stage 01 mastery gate first, or use its worked solutions to close a specific gap.

**Learning cycle:** understand → define → work by hand → predict → run → critique → retrieve later.

## 1. A distance must obey rules
A **metric** d assigns a real number to each pair of points. It is nonnegative; zero occurs exactly for identical points; exchanging the points does not change the value; and traveling directly is no longer than going through an intermediate point. The last rule is the triangle inequality: `d(x,z) ≤ d(x,y)+d(y,z)`.

In the plane, Euclidean distance is the square root of the sum of squared coordinate differences. Manhattan distance is the sum of their absolute values. Maximum distance is their largest absolute value. They are different metrics, not different estimates of a uniquely correct distance.

For x=(0,0) and y=(3,4), these distances are 5, 7, and 4 respectively. Squared Euclidean distance is generally not a metric: on points 0, 1 and 2 its direct squared distance is 4 but the two-step sum is 2. It violates the triangle inequality.

A **pseudometric** relaxes the rule that distance zero requires the same point. Repeated measurements can give different sample IDs the same feature vector. We retain such IDs where appropriate and state the distinction; we do not silently pretend all data rows are unique points in a strict metric space.

## 2. Open balls and open sets
The open ball B(x,r) contains points y with `d(x,y)<r`. It excludes points exactly at distance r. In Euclidean geometry a two-dimensional ball is the filled interior of a circle; under Manhattan distance it has a diamond-shaped boundary; under maximum distance it has a square-shaped boundary.

A set U is **open** in a metric space when every x in U has some positive-radius ball contained entirely in U. The available radius can depend on x. On the real line, `(0,1)` is open: choose a radius smaller than the distance to either endpoint. `[0,1]` is not open in R because a neighborhood of zero includes negative numbers. A set is **closed** when its complement is open. Closed does not mean bounded, and open and closed are not mutually exclusive.

For example, the empty set and the entire space are both open and closed. In a disconnected space, other sets can be both. The ambient space matters: `[0,1]` is open in the subspace `[0,1]` because the entire subspace is open in itself.

## 3. A topology keeps the open sets, not every number
A **topology** on X is a family of subsets containing the empty set and X, closed under arbitrary unions and finite intersections. Its members are called open sets. A metric generates a topology, but topology can be defined without supplying a metric.

A **basis** is a collection of open sets from which every open set can be formed as a union. Metric balls form a basis. A **neighborhood** of x is a set containing an open set that contains x; not every neighborhood must itself be open. The subspace topology on A⊆X consists of intersections A∩U with U open in X.

On X={a,b}, the discrete topology contains all four subsets. The indiscrete topology contains only the empty set and X. The family {empty, {a}, X} is also a topology. These finite examples make the axioms testable by exhaustive code. A finite test program for finite sets does not establish the axioms for arbitrary infinite families.

Different metrics can generate the same topology. On finite-dimensional Euclidean space the Euclidean, Manhattan and maximum metrics do so, even though neighborhood shapes and numeric distances differ. That does not mean their Rips persistence coordinates are identical: persistence depends on numerical scale, not only on the abstract topology.

## 4. Why finite data do not already contain a continuous circle
Take a finite set of distinct points in a metric space. Around each point choose a radius smaller than its distance to every other point. Its ball in the finite subspace contains only that point. Thus each singleton is open, and every subset is a union of open singletons. The finite subspace is discrete.

Consequently, a finite point sample that looks like a circle is not itself a connected continuous circle with its induced topology. TDA constructs a scale-dependent representation and, under suitable assumptions, attempts to infer structure of an underlying object. We must distinguish the observations, the chosen distance, the constructed complex, and the unobserved generating shape.

## 5. The real-data metric lab
Iris has four measured features. Compute distances using raw centimeters, then using standardized coordinates. Standardization subtracts a training mean and divides by a training standard deviation in a prediction task. For this stage's clearly labeled exploratory Iris analysis, the full exploratory sample supplies those values.

The nearest neighbors can change because rescaling coordinates changes how much each measurement contributes. Report that change rather than declaring one scale universally correct. Using a species label as another numeric coordinate would inject known answers into the geometry. A plot using two selected columns is a projection, not a view of every distance in four dimensions.

Before running the lab, predict which comparisons are guaranteed: translating all raw coordinates equally preserves raw Euclidean distances; rescaling each coordinate differently usually does not. The notebook checks the former and measures the latter.

## Independent exercises

Do these before reading the worked solutions. A copied solution is not an independent pass.

**02.1.** Check all metric axioms for d(x,y)=|x−y| on R.

**02.2.** Give a numeric counterexample showing squared Euclidean distance is not a metric.

**02.3.** List all open sets of the discrete and indiscrete topologies on {0,1}.

**02.4.** Explain why (0,1] is open in the subspace (0,2) or determine that it is not.

**02.5.** Prove every finite set of distinct metric points is discrete.

**02.6.** If two different sample IDs have the same features, is Euclidean distance on IDs a strict metric?

**02.7.** Explain why equal topology does not imply equal persistence diagrams in distance units.

**02.8.** Run the real-data metric comparison and state which preprocessing decision could change the result.

## Mastery gate

Verify metrics and topology axioms, prove finite discreteness, and distinguish observed points from inferred shape.

Explain one limitation and solve a new variant after a delay. Suggested progression threshold: 85% on the local knowledge check, with every critical error corrected. This is a course rubric, not accreditation.

## Free readings and attribution

Source IDs: R1, R2, R3, D1, D3. See `docs/SOURCES.md` for direct official links and assigned topics. The exposition, examples, code, and solutions here are original course material, not copied textbook chapters.

## Run and continue

Open `notebooks/02_lab.ipynb`. Its saved outputs are also readable from the browser reader. After the lab, compare with `solutions/02_solutions.md`, record what was independent, and continue only when the gate is met.


---

Source: `lessons/03_lesson.md`

# Stage 03 — Continuity, homeomorphisms, connectedness, and compactness

**Starting point:** Complete the Stage 02 mastery gate first, or use its worked solutions to close a specific gap.

**Learning cycle:** understand → define → work by hand → predict → run → critique → retrieve later.

## 1. Continuity is about the relationship between neighborhoods
A map f:X→Y is **continuous** when the inverse image of every open subset of Y is open in X. This general definition does not require distances. For metric spaces it agrees with the familiar epsilon–delta formulation: near each input x, sufficiently small input changes keep the output within any requested positive tolerance of f(x).

The order of the quantifiers matters. The output tolerance is requested first, then an input tolerance must be supplied; it may depend on x. Uniform continuity asks for one input tolerance that works everywhere for each requested output tolerance. We introduce it here to avoid confusing pointwise control with global control.

For f(x)=3x+2 on R, `|f(x)-f(y)|=3|x-y|`. Given an output tolerance ε, choosing δ=ε/3 works at every x. For the general topological proof that compositions preserve continuity, use `(g∘f)⁻¹(U)=f⁻¹(g⁻¹(U))`: first g gives an open inverse image, then f does.

## 2. Invertibility is not enough for topological equivalence
A **homeomorphism** is a bijection that is continuous in both directions. It identifies spaces with the same topological structure. It need not preserve distances, angles or area. The map f:(0,1)→(2,5), f(x)=3x+2, is a homeomorphism with inverse (y−2)/3.

A continuous bijection need not have a continuous inverse. A tiny example avoids difficult calculus: put the discrete topology on {a,b} as the domain and the indiscrete topology on the same set as codomain. The identity function is bijective and continuous in the forward direction. Its inverse is not continuous because a singleton open in the discrete target has a singleton inverse image that is not open in the indiscrete source.

Our finite-topology code checks this example exhaustively. This example is not a claim that all finite spaces are discrete. Only finite subspaces of metric spaces with distinct points were shown discrete in Stage 02; arbitrary topological spaces need not be metrizable.

## 3. Connectedness and paths
A space is **connected** when it cannot be split into two nonempty disjoint open subsets whose union is the whole space. A **path** from x to y is a continuous map from [0,1] to the space with endpoints x and y. A space is **path-connected** when every pair can be joined by such a path.

Path-connected implies connected, but the converse is false for general spaces. For finite simplicial complexes the component picture is especially concrete: connectedness and path-connectedness agree, and components can be found by the edge graph. This useful computational fact must not be promoted to a theorem about every possible topological space.

The continuous image of a connected space is connected. To see why, suppose the image had a separation into two disjoint nonempty relatively open sets. Their inverse images would separate the original space. That contradicts connectedness.

## 4. Compactness is not merely “small”
A space is **compact** if every open cover admits a finite subcover. A cover is a collection whose union contains the space. Compactness does not mean a set has finitely many points. The closed interval [0,1] is compact in the usual topology. The open interval (0,1) is not: the sets `(1/n,1)` for n≥2 cover it, but a finite selection misses points sufficiently near zero.

In Euclidean space, compactness is equivalent to being closed and bounded. That equivalence has hypotheses: it is not a definition valid for every metric space. A **Hausdorff** space allows any two distinct points to be separated by disjoint open neighborhoods. Metric spaces are Hausdorff: sufficiently small balls around two distinct points are disjoint.

A continuous map sends compact spaces to compact spaces because inverse images turn an open cover of the image into one of the domain. A compact subset of a Hausdorff space is closed. Combining these facts gives an important theorem: a continuous bijection from a compact space to a Hausdorff space is a homeomorphism. Indeed, images of closed sets in the compact domain are compact and hence closed in the target. Thus the inverse is continuous.

To deepen the last argument, prove the supporting facts: closed subsets of compact spaces are compact by adding their open complement to a cover; compact subsets of Hausdorff spaces are closed by separating an outside point from each point of the compact subset and extracting finitely many neighborhoods.

## 5. The real-data bridge: transformations versus projections
On Iris measurements, translation is an invertible continuous map of the ambient Euclidean space and preserves distances. An invertible diagonal rescaling is also a homeomorphism of the ambient space but usually changes distances. Projection from four coordinates to two is continuous but is not an invertible map of R⁴ onto R².

The notebook checks distances before and after a translation, compares rescaling, and displays a two-feature projection. These computations illustrate algebraic facts about our particular data. They do not prove continuity on an infinite domain. Moreover, every function from a finite discrete sample is continuous, so using only those samples to certify a meaningful ambient continuity claim would be vacuous.

Use a plot to suggest a question, then use a definition or theorem to answer it. When a projection appears to join two groups, investigate whether the lost coordinates distinguish them rather than declaring that the original geometry changed.

## Independent exercises

Do these before reading the worked solutions. A copied solution is not an independent pass.

**03.1.** Prove the composition of two continuous functions is continuous.

**03.2.** Give a homeomorphism from (0,2) to (5,9) and its inverse.

**03.3.** Explain the continuous-bijection counterexample using two finite topologies.

**03.4.** Why does a path-connected space have to be connected?

**03.5.** Use the given cover to show (0,1) is not compact.

**03.6.** Explain where compactness and the Hausdorff assumption enter the homeomorphism theorem.

**03.7.** Is projection R⁴→R² a homeomorphism? Could its restriction to a particular finite sample be bijective?

**03.8.** Why can finitely many plotted points not establish continuity of a function on all of R?

## Mastery gate

Give correct map definitions and prove the basic continuity and compactness consequences with their hypotheses.

Explain one limitation and solve a new variant after a delay. Suggested progression threshold: 85% on the local knowledge check, with every critical error corrected. This is a course rubric, not accreditation.

## Free readings and attribution

Source IDs: R1, R2, R3. See `docs/SOURCES.md` for direct official links and assigned topics. The exposition, examples, code, and solutions here are original course material, not copied textbook chapters.

## Run and continue

Open `notebooks/03_lab.ipynb`. Its saved outputs are also readable from the browser reader. After the lab, compare with `solutions/03_solutions.md`, record what was independent, and continue only when the gate is met.


---

Source: `lessons/04_lesson.md`

# Stage 04 — Groups, symmetries, paths, loops, and homotopy

**Starting point:** Complete the Stage 03 mastery gate first, or use its worked solutions to close a specific gap.

**Learning cycle:** understand → define → work by hand → predict → run → critique → retrieve later.

## 1. Combining operations
A **group** is a set with an operation satisfying closure, associativity, an identity, and inverses. Associativity says `(ab)c=a(bc)`, not `ab=ba`. A group is abelian when the latter commutativity property also holds.

The integers under addition form a group. Positive integers under addition do not: there is no additive identity inside the set and no additive inverses. A square's symmetries form another group under composition. Rotating by a quarter-turn four times restores the square; reflecting twice restores it. A rotation followed by a reflection need not equal the reverse order.

A **group action** describes how a group operates on another set. The identity must leave every object unchanged, and composing group elements must agree with successive actions. A **homomorphism** preserves the group operation. Its kernel contains elements mapped to the identity; this resembles the zero-output kernel of a linear map, but the identity need not be written zero.

In the notebook, quarter-turns and reflections act on the array positions of a real digit image. These are exact pixel permutations, so composition can be checked without interpolation. They preserve the multiset of intensities, but they need not preserve the semantic digit label. A rotated 6 is a reminder that mathematical symmetry and task invariance are different requirements.

## 2. Deforming maps, not tearing spaces
A **homotopy** between maps f,g:X→Y is a continuous map H:X×[0,1]→Y with H(x,0)=f(x) and H(x,1)=g(x). The extra parameter is the deformation stage. It must be continuous jointly, not merely a set of unrelated pictures.

A disk contracts to its center by H(x,t)=(1−t)x. A **contractible** space has its identity map homotopic to a constant map. A **deformation retraction** moves a space onto a subspace while fixing every point of that subspace throughout the deformation.

Take the closed annulus A={x in R²: 1≤||x||≤2}. Define `H(x,t)=((1−t)+t/||x||)x`. Its radius is `(1−t)||x||+t`, which stays between one and two. At t=0 it is x; at t=1 it lies on the unit circle; points already on the unit circle stay fixed. Division is safe because the annulus excludes the origin. This is a deformation retraction onto the circle.

Two spaces are **homotopy equivalent** if there are maps in both directions whose compositions are homotopic to the respective identity maps. The maps need not be inverse bijections. The annulus and circle are homotopy equivalent but not homeomorphic. Homotopy equivalence preserves less information than homeomorphism, which is precisely why some calculations become easier.

## 3. Loops become an algebraic object
A **based loop** starts and ends at a specified basepoint. We can traverse one loop and then another. Raw concatenation has timing choices, so the group is defined on suitable homotopy classes of based loops, not on unprocessed parametrized curves.

The **fundamental group** π₁(X,x₀) consists of these classes. The constant loop gives the identity; reversing a loop gives its inverse. A space is **simply connected** when it is path-connected and every loop can contract, equivalently its fundamental group is trivial.

For the circle, based loops have an integer winding number. One counterclockwise turn represents +1, one clockwise turn −1, and going around twice +2. The fundamental group is isomorphic to the integers under addition. The disk has trivial fundamental group. The nontrivial circle result needs an argument, such as a lifting or winding-number proof; counting turns in a sampled animation alone is not that proof. Hatcher's introductory fundamental-group material supplies the deeper treatment.

A torus surface has two independent directions for loops, unlike the loose “one hole” language often used for a doughnut. Its first homology over a field has dimension two. A solid torus is a different object and has the homotopy type of a circle. Always declare whether you mean a surface or a filled solid.

## 4. From loops to homology
Homology will be easier to compute than the fundamental group, but it can lose information. In the figure-eight graph, traversing loop a then loop b differs in the fundamental group from traversing b then a. First homology records the abelianized information: the totals along the independent loops. This motivates why a numerical invariant can be useful without completely describing a space.

Do not infer “same shape” from equal values of a single invariant. If an invariant differs, it can disprove a proposed equivalence. If it agrees, other differences may remain. We will repeatedly use this one-way logic.

## 5. What to do in the lab
Verify the square-symmetry identities on an asymmetric training image. Numerically check the annulus deformation at a grid of times and display two stages. State which facts were proved algebraically in the lesson and which were merely sampled by the program. The real image teaches group actions; the synthetic annulus teaches homotopy. Neither is a reconstruction algorithm for an arbitrary camera scene.

## Independent exercises

Do these before reading the worked solutions. A copied solution is not an independent pass.

**04.1.** List the four group axioms and explain why associativity does not imply commutativity.

**04.2.** For a square, give the inverse of a quarter-turn and the inverse of a reflection.

**04.3.** Check the endpoints and fixed-subspace condition of the annulus deformation formula.

**04.4.** Why is the same formula invalid at the center of a disk?

**04.5.** Explain homeomorphism versus homotopy equivalence using the annulus and circle.

**04.6.** What are the winding numbers of two forward turns followed by one reverse turn?

**04.7.** Why does rotating a digit image not automatically produce a valid same-label training example?

**04.8.** What can and cannot be concluded when two spaces have equal Betti numbers?

## Mastery gate

Explain and check a group action, verify a deformation retraction, and distinguish loop classes from raw paths.

Explain one limitation and solve a new variant after a delay. Suggested progression threshold: 85% on the local knowledge check, with every critical error corrected. This is a course rubric, not accreditation.

## Free readings and attribution

Source IDs: R1, R6, R7. See `docs/SOURCES.md` for direct official links and assigned topics. The exposition, examples, code, and solutions here are original course material, not copied textbook chapters.

## Run and continue

Open `notebooks/04_lab.ipynb`. Its saved outputs are also readable from the browser reader. After the lab, compare with `solutions/04_solutions.md`, record what was independent, and continue only when the gate is met.


---

Source: `lessons/05_lesson.md`

# Stage 05 — Surfaces, simplices, triangulations, and pixel geometry

**Starting point:** Complete the Stage 04 mastery gate first, or use its worked solutions to close a specific gap.

**Learning cycle:** understand → define → work by hand → predict → run → critique → retrieve later.

## 1. A surface is locally two-dimensional
A topological **surface** is locally like an open subset of the plane, with the usual additional separation and countability conditions in the standard definition. A surface with boundary may also have neighborhoods modeled on a half-plane. A boundary is not simply the outline in a drawing: a sphere has no boundary as a surface, even though a projection has a visible outline.

A surface is **orientable** when local orientation choices can be made consistently across it. A Möbius strip obstructs such a global choice. An orientable closed connected surface's **genus** counts its handles. The classification theorem for compact connected surfaces is a substantial result; here we learn its statement and examples rather than pretending an animation proves it.

Under its hypotheses, a closed connected orientable surface of genus g has Euler characteristic 2−2g. A compact connected orientable surface with b boundary components has characteristic 2−2g−b. For the nonorientable connected-sum family with k projective-plane factors and b boundary components it is 2−k−b. These formulas concern different classes of spaces and cannot be used interchangeably without checking orientability and boundary.

The sphere is orientable, closed, and genus zero. The torus surface is orientable, closed, and genus one. A cylinder surface with two boundary circles is orientable. The Möbius strip has one boundary circle and is nonorientable. The Klein bottle is a closed nonorientable surface; a self-intersecting picture in R³ is not its intrinsic definition. Use Hatcher's geometric introduction and the surface discussion to deepen these examples.

## 2. Replace continuous shapes by compatible pieces
A **0-simplex** is a vertex, a **1-simplex** is an edge, a **2-simplex** is a filled triangle, and a **3-simplex** is a filled tetrahedron. A simplex's dimension is one less than its number of vertices. A face is formed by selecting some of its vertices.

An **abstract simplicial complex** is a collection of finite vertex subsets closed under taking faces. Our code stores nonempty simplices only; empty-face bookkeeping is implicit. A **geometric realization** draws compatible simplices in Euclidean space. In a geometric simplicial complex, intersections of simplices must be common faces rather than arbitrary crossings.

A triangulation represents a space as the realization of such a complex, up to homeomorphism. An abstract triangle is recorded as `(0,1,2)`, but those IDs do not by themselves specify physical coordinates. Coordinates can change while the combinatorial incidence information stays the same.

If we include triangle (0,1,2), we must also include its edges and vertices. Three edges around a triangle do not force its interior to exist in an arbitrary complex. In a **clique complex**, by contrast, every clique of the edge graph supplies a simplex by definition. This extra rule is what will distinguish a graph from its Rips complex.

## 3. Count pieces without mistaking the count for a full invariant
For a finite complex, the **Euler characteristic** is the alternating simplex count: vertices minus edges plus triangles minus tetrahedra, and so on. A triangle boundary has 3−3=0. A filled triangle has 3−3+1=1. The boundary of a tetrahedron has 4−6+4=2; including its solid interior gives 4−6+4−1=1.

Euler characteristic is invariant under suitable changes of triangulation of the same space, but the raw number of edges is not. Adding a vertex to subdivide an edge changes two counts that cancel in the alternating sum. A full proof of invariance follows from homology or subdivision theory, not from one successful count.

The Euler number does not reveal every Betti number separately. A connected graph with two loops has characteristic −1; a different complex can have the same alternating sum with other dimensions contributing. We will calculate the more informative homology groups next.

## 4. Pixels need a declared geometric model
An 8×8 intensity array is not automatically a continuous surface. In this course we model each pixel as a **closed square** in a rectangular grid. Selecting pixels at a threshold means taking the union of those closed squares. Squares touching at a corner are therefore connected. This convention is different from a rule that only allows edge-neighbor pixel connections.

We split each selected square into two triangles and include every face. The diagonal is an internal subdivision: both triangles and the diagonal enter at the same filtration value. Thus the union at each threshold is the same geometric pixel region, only triangulated. This allows our simplicial code to analyze the square-pixel model. It is not presented as a newly implemented general-purpose cubical library.

No periodic boundary is imposed and no padded exterior is added. All pixels eventually enter, giving a full rectangular region. If a dark central pixel enters after a ring around it, a loop can disappear then. Choosing opposite intensity conventions reverses the order, so the threshold definition must be explicit.

## 5. Work through a real image
The notebook loads a real **training** digit, thresholds it, constructs its complex, counts simplices, and reports Euler characteristic. It also runs exact triangle and tetrahedron examples. A written 8 does not guarantee two measured holes: handwriting, low resolution, intensity threshold, and corner-touch conventions all matter.

Inspect the complex validator. It rejects missing faces rather than silently inventing them. A separate closure function deliberately adds faces when that is the requested construction. These are different operations, and naming them separately makes the analysis auditable.

## Independent exercises

Do these before reading the worked solutions. A copied solution is not an independent pass.

**05.1.** How many vertices, edges, and triangles occur in a filled triangle?

**05.2.** Calculate the Euler characteristics of a triangle boundary, filled triangle, tetrahedron boundary, and solid tetrahedron.

**05.3.** What is wrong with storing a triangle but omitting one edge?

**05.4.** Explain abstract simplex versus geometric realization.

**05.5.** Why do corner-touching foreground pixels connect under this course’s model?

**05.6.** Why can a digit label not be used as the exact ground-truth Betti number of its thresholded image?

**05.7.** For a torus with one open disk removed, calculate Euler characteristic using the surface formula.

**05.8.** Explain why a graph containing a triangle and its clique complex can have different topology.

## Mastery gate

Construct valid complexes, distinguish surfaces from solids, and state the exact pixel-connectivity convention.

Explain one limitation and solve a new variant after a delay. Suggested progression threshold: 85% on the local knowledge check, with every critical error corrected. This is a course rubric, not accreditation.

## Free readings and attribution

Source IDs: R1, R2, R7, L3. See `docs/SOURCES.md` for direct official links and assigned topics. The exposition, examples, code, and solutions here are original course material, not copied textbook chapters.

## Run and continue

Open `notebooks/05_lab.ipynb`. Its saved outputs are also readable from the browser reader. After the lab, compare with `solutions/05_solutions.md`, record what was independent, and continue only when the gate is met.


---

Source: `lessons/06_lesson.md`

# Stage 06 — Chains, boundaries, homology, and Betti numbers

**Starting point:** Complete the Stage 05 mastery gate first, or use its worked solutions to close a specific gap.

**Learning cycle:** understand → define → work by hand → predict → run → critique → retrieve later.

## 1. Turn simplices into algebra
Fix a coefficient field, initially F₂={0,1}. A **k-chain** is a formal sum of k-dimensional simplices with coefficients in the field. Over F₂, adding the same simplex twice cancels it. The chain vector space Cₖ has one basis vector per k-simplex. Its dimension is the number of those simplices, not the number of holes.

The **boundary map** ∂ₖ sends a k-simplex to the sum of its codimension-one faces. Over F₂ no signs are needed. Over other fields, oriented simplices require alternating signs, and reversing orientation negates a simplex. Choosing F₂ makes the arithmetic easier; it does not make coefficient choice universally irrelevant.

For edge [a,b], its boundary over F₂ is a+b. For triangle [a,b,c], its boundary is [a,b]+[a,c]+[b,c]. Apply boundary again: each vertex appears twice, so the result is zero. More generally, each codimension-two face appears twice, yielding `∂ₖ₋₁∂ₖ=0`. With orientation signs, the corresponding pairs have opposite signs.

## 2. Cycles are not necessarily holes
A **cycle** is a chain with zero boundary: `Zₖ=ker ∂ₖ`. A **boundary** is the boundary of some next-dimensional chain: `Bₖ=im ∂ₖ₊₁`. Because boundary-of-boundary is zero, Bₖ is contained in Zₖ.

A cycle around a filled triangle is the boundary of the triangle and is therefore trivial in first homology. The same three-edge cycle without the filled triangle is not the boundary of any available 2-chain. The visual outline alone does not answer whether the cycle represents a hole; the higher-dimensional cells matter.

**Homology** is the quotient `Hₖ=Zₖ/Bₖ`. Two cycles represent the same class when their difference is a boundary. Over a field its dimension is the **Betti number** βₖ. In a finite simplicial complex, β₀ counts components, β₁ counts independent one-dimensional homology classes, and β₂ counts independent two-dimensional classes. Enclosed voids can be a useful picture in familiar embeddings, but that is not the general definition of β₂.

We use ordinary homology. A nonempty connected contractible space has β₀=1, not zero. Reduced homology modifies the zero-dimensional part so that a point has no reduced homology; mixing these conventions causes avoidable disagreements.

## 3. Calculate an entire example by hand
Order triangle vertices as 0,1,2 and edges as 01,02,12. The boundary matrix ∂₁ has columns (1,1,0), (1,0,1), (0,1,1). Its rank over F₂ is two. There are three independent edge coordinates, so its kernel has dimension 3−2=1. The sum of all three edges is the nonzero cycle.

For the unfilled boundary, C₂ is zero and ∂₂ has rank zero. Thus β₁=3−2−0=1. For the filled triangle, ∂₂ has one nonzero column (1,1,1), with rank one. Then β₁=3−2−1=0. In both cases β₀=3−rank(∂₁)=1.

For a general finite complex over a field, rank–nullity yields:

`βₖ = dim(Cₖ) − rank(∂ₖ) − rank(∂ₖ₊₁)`.

Compute both ranks in the same field. A floating-point rank over R is not a substitute for exact elimination over F₂. The function `rank_mod2` uses XOR to perform row operations, and the Stage 01 counterexample demonstrates why this matters.

## 4. Why the checks complement one another
Checking `∂∂=0` verifies an important structural identity. Checking known Betti numbers verifies interpretation and rank calculations. Checking that the alternating Betti sum equals the alternating simplex sum supplies the Euler–Poincaré identity for finite complexes. None alone proves the whole implementation correct, but together they constrain different failure modes.

The equality of alternating sums follows by substituting the rank formula: each boundary rank appears twice with opposite signs and cancels, leaving the alternating chain-space dimensions. This derivation is worth doing on paper rather than memorizing another formula.

Computing H₁ from only edges can overcount loops that triangles would fill. To compute Hₖ for a proposed higher-dimensional complex, include the (k+1)-simplices needed for ∂ₖ₊₁. A graph's homology is valid for the graph; it just need not be the homology of the clique complex you intended to study.

## 5. Real-data calculation and coefficient awareness
Apply the pixel construction to several intensity thresholds of a training digit. Calculate β₀ and β₁. At the final threshold all pixels enter and the rectangular region is contractible, so the expected result is [1,0] for the reported dimensions. At earlier thresholds the outcome is data-dependent.

These are homology values of the specified thresholded pixel model, not a proof of the topology of an ideal handwritten symbol. A low-resolution stroke can join components or close a loop unexpectedly. Include the displayed image, threshold, connectivity convention, and coefficients with the result.

Beyond this stage, learn that integer homology can include torsion, which Betti numbers alone omit. For example, coefficient changes can alter the measured homology of nonorientable spaces. The computational core stays over F₂; the advanced bridge explains what additional theory is needed before generalizing the implementation.

## Independent exercises

Do these before reading the worked solutions. A copied solution is not an independent pass.

**06.1.** Explain the difference between Cₖ, Zₖ, Bₖ, and Hₖ.

**06.2.** Prove ∂₁∂₂=0 for one triangle and explain the general paired-face argument.

**06.3.** Compute β₀ and β₁ of a four-vertex tree with three edges.

**06.4.** Compute β₀ and β₁ of a connected graph with four vertices and five edges, with no triangles filled.

**06.5.** Explain why adding a triangle can decrease β₁ but never disconnect the existing graph.

**06.6.** Derive the Euler–Poincaré identity using the rank formula.

**06.7.** What extra cells are needed to decide whether a two-dimensional cycle is a boundary?

**06.8.** Why do the results state F₂ and ordinary homology explicitly?

## Mastery gate

Calculate small homology groups by hand, prove boundary-of-boundary, and explain every term in the Betti formula.

Explain one limitation and solve a new variant after a delay. Suggested progression threshold: 85% on the local knowledge check, with every critical error corrected. This is a course rubric, not accreditation.

## Free readings and attribution

Source IDs: R1, R2, R7. See `docs/SOURCES.md` for direct official links and assigned topics. The exposition, examples, code, and solutions here are original course material, not copied textbook chapters.

## Run and continue

Open `notebooks/06_lab.ipynb`. Its saved outputs are also readable from the browser reader. After the lab, compare with `solutions/06_solutions.md`, record what was independent, and continue only when the gate is met.


---

Source: `lessons/07_lesson.md`

# Stage 07 — From data to shape: Rips, Čech, alpha, and filtrations

**Starting point:** Complete the Stage 06 mastery gate first, or use its worked solutions to close a specific gap.

**Learning cycle:** understand → define → work by hand → predict → run → critique → retrieve later.

## 1. A point cloud does not dictate a unique complex
To analyze measurements, first choose what a point represents and what distance compares two points. Then choose how nearby points create edges, triangles and higher simplices. Different constructions can be reasonable for different questions. The resulting complex is part of the model, not something observed directly by the camera or measurement instrument.

A **filtration** is a nested family: when the parameter increases, previously included simplices remain included. For finite computations we can record each simplex with its first appearance value. A face must appear no later than a simplex containing it. Equal appearance times are allowed, but a valid reduction order must put faces before their cofaces.

The filtration parameter could be distance, intensity, density-derived value, or time in a suitable nested construction. A sequence of video frames with features appearing and disappearing is not automatically a filtration. Ordinary one-parameter persistence needs inclusions; methods such as zigzag persistence handle other kinds of changes but are outside the executable core.

## 2. Our Rips convention, stated exactly
The Vietoris–Rips complex at ε contains a finite vertex subset precisely when every pair in it is at distance at most ε. Equivalently, its diameter is at most ε. Vertices enter at zero; each higher simplex enters at the length of its longest edge. We call ε the **edge-distance parameter**, not a ball radius.

This is a clique complex. Once three vertices are pairwise joined, the triangular face is present; once four are pairwise joined, the tetrahedral simplex is present if we are building to that dimension. To compute H₁ we build through triangles. To compute H₂ we build through tetrahedra. Omitting such simplices can create artificial surviving classes.

Worked example: three points forming an equilateral triangle of side one. In our Rips convention all edges and the filled triangle enter together at ε=1. There is no positive-length H₁ interval. A sequential implementation might temporarily show a cycle between inserting edges and face at the same numerical value. Its zero-length interval is not a feature present over a nonzero scale range.

## 3. Čech: common intersections are stronger than pairwise ones
For equal-radius closed Euclidean balls of radius r around points, the Čech complex contains a simplex when the entire collection of balls has a common intersection. Pairwise overlap gives edges but need not give a higher-dimensional common intersection.

For the equilateral triangle of side one, pairs of balls first meet at r=1/2. All three first meet at the circumradius r=1/√3. Thus there is a scale range in which the Čech complex contains the three edges without the filled triangle. This is a useful contrast with Rips, not a contradiction: the construction and parameter convention differ.

In Euclidean space, with our conventions, `Čech_r ⊆ Rips_(2r) ⊆ Čech_(2r)`. The first inclusion follows because two centers sharing a point in their radius-r balls are at most 2r apart. For the second, choose one vertex of a Rips simplex; it is at most 2r from every center and lies in their radius-2r balls. Stronger dimension-dependent bounds exist, but these elementary inclusions already show why factors of two must be tracked.

The **nerve** of a cover records which subcollections have nonempty common intersections. A version of the nerve theorem says that a suitable finite good cover, whose nonempty finite intersections are contractible, has a nerve homotopy equivalent to its union. One standard setting uses open good covers; finite covers by closed convex subsets of Euclidean space also have a nerve result. Do not apply the theorem to arbitrary disconnected intersections merely because you have a graph of overlaps.

## 4. Alpha complexes and geometric efficiency
An alpha complex uses a Delaunay/Voronoi construction to represent unions of Euclidean balls more economically than a full Čech enumeration in favorable dimensions. Voronoi cells associate locations with nearest sites; their dual Delaunay structure records adjacency. Intersecting balls with appropriate Voronoi regions leads to the alpha construction.

Its exact filtration values and numerical handling require care. GUDHI's default alpha values are squared radii, not our Rips edge lengths. Comparing a number from one axis directly with the other would mix both units and constructions. The optional script provides an alpha demonstration when GUDHI is installed; this optional result is not claimed as executed in the shipped report.

The core notebook demonstrates the triangle's Čech scales analytically and computationally and constructs Rips filtrations with our explicit code. This is enough to learn the distinction without inventing an untested general-purpose alpha implementation.

## 5. Real-data construction and cost
We use a fixed small subset of Iris observations for the educational Rips builder. Its vertices are flower samples, not individual measurements. All selected feature columns enter Euclidean distance, and the report states their scale. Class labels are not included in the coordinates.

For n points, possible k-simplices number `choose(n,k+1)`. Even H₁ can require enumerating `choose(n,3)` triangles. The code deliberately caps candidate counts and asks for smaller samples or a specialized library rather than freezing a beginner's computer. Small samples are a teaching convenience; they do not establish topology of the full population.

At several thresholds, compare graph components and complex homology. Predict the expected nesting before execution. If a threshold removes an edge while claiming to increase the same filtration parameter, something in the construction or preprocessing has changed and must be investigated.

## Independent exercises

Do these before reading the worked solutions. A copied solution is not an independent pass.

**07.1.** At what value does a Rips simplex enter under the declared convention?

**07.2.** Why does the equilateral triangle have no positive H₁ Rips bar?

**07.3.** Derive the two Čech radii for that same triangle.

**07.4.** Prove the elementary inclusions Čech_r⊆Rips_2r⊆Čech_2r in Euclidean space.

**07.5.** Explain the good-cover assumption in a nerve theorem.

**07.6.** How many candidate edges and triangles exist for 20 observations?

**07.7.** Why does reporting H₁ from an edge-only complex answer a different question?

**07.8.** If an alpha value is 4 in squared-radius units, what is the radius? Is this automatically Rips ε=2?

## Mastery gate

Specify and implement a valid filtration, distinguish Rips/Čech/alpha, and justify parameter units and dimension limits.

Explain one limitation and solve a new variant after a delay. Suggested progression threshold: 85% on the local knowledge check, with every critical error corrected. This is a course rubric, not accreditation.

## Free readings and attribution

Source IDs: R1, R2, R8, L1, L2. See `docs/SOURCES.md` for direct official links and assigned topics. The exposition, examples, code, and solutions here are original course material, not copied textbook chapters.

## Run and continue

Open `notebooks/07_lab.ipynb`. Its saved outputs are also readable from the browser reader. After the lab, compare with `solutions/07_solutions.md`, record what was independent, and continue only when the gate is met.


---

Source: `lessons/08_lesson.md`

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


---

Source: `lessons/09_lesson.md`

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


---

Source: `lessons/10_lesson.md`

# Stage 10 — Stability, diagram distances, noise, and scientific uncertainty

**Starting point:** Complete the Stage 09 mastery gate first, or use its worked solutions to close a specific gap.

**Learning cycle:** understand → define → work by hand → predict → run → critique → retrieve later.

## 1. Comparing diagrams requires more than nearest points
A persistence diagram is a multiset. A distance must consider assignments between its points and allow short features to disappear by matching to the diagonal. For the bottleneck distance, point-to-point cost is the maximum absolute change in birth or death. The distance is the smallest possible largest cost over a complete matching, with diagonal matches allowed.

The distance from (b,d) to the diagonal in this maximum norm is `(d−b)/2`. The best diagonal point is their midpoint: moving either coordinate less than half the lifetime cannot make them equal. A single bar [0,2) therefore has bottleneck distance one from the empty diagram.

The finite-diagram function in the package constructs an augmented matching problem, tests whether a perfect matching exists below a candidate cost, and searches candidate thresholds. It does not minimize total assignment cost and then mislabel that result as bottleneck distance. Multiplicities and empty diagrams are covered by tests.

A p-Wasserstein distance instead aggregates matched costs using a p-power sum followed by a pth root, with a chosen ground norm. Its value depends on p, the norm, and conventions. A bottleneck bound is not automatically the same numeric bound for every finite-p Wasserstein distance. Essential intervals require separate handling; our explicitly named `finite_bottleneck` rejects infinity rather than dropping it silently.

## 2. What a stability theorem actually says
Let f and g be finite filtration-value functions on the same finite simplicial complex, each nondecreasing from faces to cofaces. If `|f(σ)−g(σ)|≤δ` for every simplex, then the associated one-parameter persistence modules are δ-interleaved: every f-sublevel complex at t is contained in the g-sublevel complex at t+δ, and vice versa. For these finite constructible modules, the corresponding diagrams have bottleneck distance at most δ, with essential classes handled consistently.

The easy part to prove is the inclusion: f(σ)≤t implies g(σ)≤f(σ)+δ≤t+δ. The step from an interleaving to a matched diagram bound is a substantial algebraic-stability result. We state it with its hypotheses and learn its proof structure; an observed inequality on a few arrays is not its proof.

For our fixed pixel grid, assign each square a scalar value and its faces the minimum of incident square/triangle values. If every pixel value changes by at most δ, every induced simplex value also changes by at most δ. Thus the theorem applies to this fixed combinatorial model. Its completed H₁ diagram is finite because the final rectangle is contractible, making our finite-only bottleneck routine suitable for the Stage 10 H₁ experiment.

For Rips data, changes in pairwise distances bound changes in each simplex's diameter. If corresponding coordinates move by at most η, Euclidean pairwise distances change by at most 2η by the triangle inequality. Keep this distance-change argument separate from the fixed-grid intensity argument; the units and constants differ.

## 3. Stability is not significance
A stable descriptor changes little under certain bounded perturbations. That does not make every detected feature meaningful. A feature can be stable in a biased dataset, caused by a systematic preprocessing artifact, or unrelated to the scientific target.

Statistical questions require a data-generating or resampling model. What is the independent unit? What variation is plausible? Which null hypothesis is being tested? What happens under different sample sizes or density patterns? A long bar is not automatically a p-value, a confidence interval, or evidence of a causal mechanism.

A point-cloud bootstrap samples observations with replacement. That changes multiplicities and can create duplicate coordinates; whether it is appropriate depends on the inferential target. Frame-level resampling of strongly dependent videos is not equivalent to resampling independent recordings. Likewise, perturbing one image estimates sensitivity to the chosen corruption, not uncertainty over all future handwriting styles.

## 4. Design informative negative controls
Use exact clean shapes to check interpretation, then perturb coordinates, remove observations, add outliers, or alter sampling density. Change one condition at a time and record the actual parameter. Some operations do not preserve the intended object, so the resulting change is not necessarily algorithm failure.

A useful null could destroy the structure being tested while preserving specified marginal properties, but the details must match the scientific question. Shuffling labels tests a different claim from shuffling pixels. Neither automatically validates a “shape significance” statement. The included notebook uses controlled corruption and sensitivity reports, not a fabricated hypothesis test.

## 5. Real handwriting stability experiment
Select one training digit. Convert intensities to f=1−image/16. Add a reproducible bounded intensity perturbation and clip to [0,1]. Calculate the actual maximum perturbation after clipping, not just the requested noise amplitude. Compute H₁ diagrams before and after and their bottleneck distance. Verify the applicable bound.

Repeat over several declared amplitudes and inspect both the numeric report and images. A failed inequality can indicate a bug, a convention mismatch, or an invalid application of the theorem. A successful inequality establishes the stated computation on the selected fixed-grid examples, not broad classification robustness.

Finally, compare the meaning of a saved diagram, an invariance test, a perturbation test, and a holdout metric. Each answers a different question. This distinction is central to using topology responsibly in data science.

## Independent exercises

Do these before reading the worked solutions. A copied solution is not an independent pass.

**10.1.** Find the bottleneck distance between a one-point diagram {(0,4)} and the empty diagram.

**10.2.** Compare diagrams {(0,2)} and {(0.1,2.1)}: exhibit a matching of cost 0.1.

**10.3.** Prove the sublevel-set inclusions from a uniform filtration-value bound δ.

**10.4.** Why does a pixel perturbation bound also bound the minimum value on shared faces?

**10.5.** Why are essential bars rejected by our finite-only distance function?

**10.6.** Explain why a long barcode interval is not a statistical p-value.

**10.7.** Give an example where frame-level random splits would exaggerate model generalization.

**10.8.** What does the Stage 10 corruption experiment establish and not establish?

## Mastery gate

Apply a precise stability statement, compute a diagram distance, and separate robustness from statistical significance.

Explain one limitation and solve a new variant after a delay. Suggested progression threshold: 85% on the local knowledge check, with every critical error corrected. This is a course rubric, not accreditation.

## Free readings and attribution

Source IDs: R2, R8, L3, R9. See `docs/SOURCES.md` for direct official links and assigned topics. The exposition, examples, code, and solutions here are original course material, not copied textbook chapters.

## Run and continue

Open `notebooks/10_lab.ipynb`. Its saved outputs are also readable from the browser reader. After the lab, compare with `solutions/10_solutions.md`, record what was independent, and continue only when the gate is met.


---

Source: `lessons/11_lesson.md`

# Stage 11 — Useful representations, Mapper, time windows, and honest machine learning

**Starting point:** Complete the Stage 10 mastery gate first, or use its worked solutions to close a specific gap.

**Learning cycle:** understand → define → work by hand → predict → run → critique → retrieve later.

## 1. A variable-size diagram is not yet a model-ready feature vector
Different observations can produce different numbers of intervals. Many familiar prediction models expect a fixed number of input features. We therefore need a declared representation of each diagram. A representation is another modeling choice: it can discard information, introduce parameters, and change sensitivity.

A **Betti curve** counts live classes at each threshold. It is simple but does not uniquely determine a barcode. A **persistence landscape** converts every finite interval [b,d) into the tent function `max(0,min(t−b,d−t))`. At each t, sort the tent heights; the largest forms landscape level one, the next level two, and so on. Sample chosen levels on a declared grid to obtain a vector.

A **persistence image** is not the handwritten image. It is a vector representation of a diagram. Change coordinates from (birth,death) to (birth,lifetime), place weighted smooth kernels there, and integrate the resulting surface over grid cells. Our implementation uses lifetime weights and Gaussian kernels with a specified bandwidth, integrating with normal-distribution CDF differences. A finite grid may omit some mass. Essential bars need a separate policy because their lifetime is infinite.

Simple summaries can also be useful: finite-interval count, maximum lifetime, total lifetime, mean lifetime, and sum of squared lifetimes. Our classifier uses these five summaries plus five fixed Betti-curve samples in each of H₀ and H₁, producing 20 features. Finite lifetimes exclude infinite intervals; Betti counts include intervals alive at the threshold, including essential H₀.

No universal theorem says these summaries are optimal or that counting all short intervals is robust. In fact, finite-interval count can change under small perturbations near the diagonal. The pedagogical vector is deliberately understandable; the stability of a diagram must not be confused with the stability of every possible summary.

## 2. Prediction needs a separate evaluation design
A **classifier** learns a rule from features to labels. Logistic regression fits linear class scores and converts them to probabilities using a logistic/softmax model. Its regularization discourages overly large coefficients; in scikit-learn the parameter C controls inverse regularization strength. We use it as a simple baseline, not because topology requires this model.

Training data fit parameters. Validation data choose between prespecified alternatives. Test data estimate performance after those choices are fixed. Learned transformations such as means, standard deviations, PCA directions, image bandwidths chosen from the data, or feature selection must be fitted on the appropriate training portion only. A pipeline groups transformations and the model so this sequence is explicit.

This course freezes a 1,077/360/360 per-image digits split. Early notebooks view only training images. Stage 11 compares C values 0.1, 1 and 10 on validation data for three representations: 64 raw pixels, 20 topological features, and their concatenation. Each fitted pipeline learns its scaling from training rows only. The H₀/H₁ extraction for one image uses only that image and fixed constants, so it can be computed independently without learning population statistics.

The final test is not used in this stage. The split is not writer-disjoint: the snapshot has no writer IDs. The dataset is small and commonly studied. Treat this as a reproducible learning experiment, not a production claim about unseen handwriting populations. See D3 and R9.

## 3. Mapper gives a graph of overlapping local summaries
A **lens** maps observations to one or more explanatory values. For our scalar example it is a measured Iris feature. Cover the lens range with overlapping intervals. Pull each interval back to the observations whose lens values fall inside. Cluster points within each pullback using the declared feature-space metric. Each cluster becomes a node; connect nodes that share original observations.

The full nerve can have higher simplices when several nodes share observations. Our plotted **Mapper graph is only its 1-skeleton**. It is not automatically a clique-complex homology calculation. A **Reeb graph**, in contrast, identifies points in the same connected component of a continuous function's level set. Mapper approximates related structure under additional conditions, not merely because it looks like a Reeb graph.

The notebook varies cover overlap and clustering radius. Report changing node and edge counts as parameter sensitivity, not as newly discovered population subtypes. Labels are not used to choose the graph's geometry in this demonstration. A useful exploratory visualization remains different from a validated predictive feature or scientific conclusion.

## 4. Time windows and what their geometry can mean
A delay embedding turns a series into vectors such as `(x_t,x_(t+lag),x_(t+2lag))`. Periodic signals can create loop-like point clouds. Takens-type reconstruction results require specific dynamical and observation assumptions; arbitrary noisy short data do not automatically satisfy them.

Our executable demonstration uses a labeled synthetic sinusoid and a real digit's column-intensity profile as an ordered **spatial** sequence. The latter is not a measured temporal process and must not be described as one. The same array operation is useful in both cases, but the scientific interpretation differs.

A forward window is not available until its final sample has arrived. In predictive work, assign its availability time accordingly and split groups or time periods before creating overlapping windows. Otherwise near-duplicate windows can cross training and test boundaries, and future values can leak into supposedly early predictions.

## 5. What to inspect after the lab
Inspect the landscape and persistence image for the same finite barcode and explain how their coordinates differ. Inspect Mapper under more than one setting. Review validation accuracy for all three model inputs, including a majority-class baseline. The experiment is successful as a learning exercise even when topological features are worse than raw pixels.

Save the selected C values, train/validation IDs, definitions of every feature, and the full validation table. Do not cherry-pick one good setting and erase the alternatives. Stage 12 will use this record to run the final comparison once.

## Independent exercises

Do these before reading the worked solutions. A copied solution is not an independent pass.

**11.1.** Calculate a tent function for [0,2) at t=0, 0.5, 1, 1.5 and 2.

**11.2.** Explain the coordinate systems of an original digit image, a persistence diagram, and a persistence image.

**11.3.** Why can a finite-interval count be unstable even when the diagram is stable?

**11.4.** What is the role of each of training, validation and test data?

**11.5.** Why is fitting a standardizer on all images before splitting a leakage problem?

**11.6.** Explain every step of the scalar-lens Mapper construction.

**11.7.** When is the forward delay vector (x_t,x_(t+2),x_(t+4)) available?

**11.8.** Why would equal or worse performance from topology still be an informative result?

## Mastery gate

Build declared representations, explain Mapper and window availability, and select models using validation rather than test data.

Explain one limitation and solve a new variant after a delay. Suggested progression threshold: 85% on the local knowledge check, with every critical error corrected. This is a course rubric, not accreditation.

## Free readings and attribution

Source IDs: R2, R8, R9, D3. See `docs/SOURCES.md` for direct official links and assigned topics. The exposition, examples, code, and solutions here are original course material, not copied textbook chapters.

## Run and continue

Open `notebooks/11_lab.ipynb`. Its saved outputs are also readable from the browser reader. After the lab, compare with `solutions/11_solutions.md`, record what was independent, and continue only when the gate is met.


---

Source: `lessons/12_lesson.md`

# Stage 12 — Capstone: reproduce, defend, transfer, and audit the book

**Starting point:** Complete the Stage 11 mastery gate first, or use its worked solutions to close a specific gap.

**Learning cycle:** understand → define → work by hand → predict → run → critique → retrieve later.

## 1. Complete a question, not just a notebook
The worked capstone question is: **On the frozen per-image digits split, how do fixed topological summaries compare with raw pixels for recognizing the recorded digit label?** This is deliberately narrower than asking whether topology improves all computer vision.

State the observation unit, input data, labels, hypothesis and evaluation metric before opening the test results. A **baseline** supplies a comparison that could plausibly solve the task without the new technique. Here we include a majority-class classifier, raw pixels, topology alone, and their combination. The same test rows are used for all methods so their errors can be compared directly.

The primary reported metric is accuracy: the fraction of test labels predicted correctly. Also record per-class recall and a confusion matrix, which show which classes are mistaken for which. A single aggregate score can hide differences between common and rare classes. The dataset classes are reasonably represented in the frozen splits, but we still inspect all of them.

## 2. Freeze the procedure before opening the holdout
Stage 11 records the validation-selected regularization value for each representation. For this worked example, refit each selected pipeline on training plus validation rows. Refit the scaler on that combined development set; do not carry over a scaler fitted on the whole dataset. Predict the held-out test rows and record every result together with sample IDs.

The deterministic topology transform uses `f=1−intensity/16`, closed square pixels, a filtration-preserving triangulation, F₂ coefficients, ordinary H₀/H₁, positive finite intervals for lifetime sums, and fixed Betti sample thresholds. The experiment does not tune these choices on test images. Altering them after seeing test results requires treating the existing holdout as exposed and obtaining new evidence.

The bundled 1,797-image collection corresponds to the original UCI test snapshot distributed with scikit-learn. Our internal train/validation/test partition is newly created for learning and lacks writer IDs. Consequently, test accuracy is **image-level accuracy on this split**, not an estimate certified for unseen writers. The official UCI full training set is not bundled and was not secretly substituted.

## 3. Write an evidence-based conclusion
Use a conclusion with this structure: “Under the specified split, representation, model class and preprocessing, method A achieved the recorded result. Relative to the baseline, the observed change was this many correct images. This experiment does not establish these broader claims.” Include worse results and equal results; do not define success as obtaining a topology improvement.

The provided reports contain actual execution outputs, not invented performance targets. Rounded floating-point results can vary slightly with numerical environments. Dataset IDs, splits, counts, exact constructions and major expected behaviors should remain consistent. A discrepancy is a reason to investigate, not overwrite the saved benchmark.

A formal confidence interval or hypothesis test would require additional inferential choices and attention to dependence. Writer-level dependence is not observable here. We therefore avoid presenting a small score difference as statistically significant or as a general performance advantage. The point is a transparent experiment with known limits.

## 4. Your independent capstone
After reproducing the worked example, choose a substantially new task. A sports option is to compare motion-window features with and without topological summaries, splitting by athlete and session and ensuring every feature is available at the prediction cutoff. A reconstruction option is to measure how controlled occlusion or geometric defects change shape descriptors, compared with direct geometric baselines.

These are proposed research designs, not demonstrated benefits for WMS. Begin with well-defined observations, calibrated units, and ground truth appropriate to the target. Homography on a ground plane does not automatically license metric positions of airborne objects; learned monocular depth is not automatically calibrated geometry. Do not feed uncertain geometric outputs into TDA and then interpret a stable diagram as proof that upstream calibration is correct.

Use the independent-capstone protocol in `docs/CAPSTONE_PROTOCOL.md`. It requires a question, observation unit, data provenance, inclusion rules, leakage plan, metric and filtration choices, expected failure modes, frozen evaluation, reproducible code, and a conclusion that could honestly be negative.

## 5. Explain the whole chain without hiding behind software
Your oral defense should connect every step: why this distance; why this complex; why these coefficients; why these dimensions; why this scale; what the diagram records; what it discards; how the representation was chosen; how the test split matches deployment; and what the data cannot answer.

You should be able to compute one small example by hand, trace one reduction, prove boundary-of-boundary is zero, and identify an invalid inference. These demonstrations establish a deeper form of completion than viewing every notebook output. The progress ledger distinguishes reading, guided practice, independent solving and delayed retention.

## 6. Audit the actual book when available
The coverage map aligns the supplied chapter titles to lessons, labs, proof depth and limitations. It does not claim that the unpublished/full book text has been examined. When you have the book, compare each actual section, definition, example and exercise type with the course. Add any missing item to the gap log and work it explicitly. Do not silently mark an unfamiliar argument as “covered” because a chapter title sounds familiar.

Read the author's freely available paper as an example to critique, not as an authority that makes every proposed statistic standard. Record its metric, filtration, evidence and validation. Proposed stability summaries should not be confused with the mathematical stability theorem or with statistical significance.

## 7. What follows the introductory core
The advanced bridge names integer homology and torsion, cohomology and cup products, fundamental-group methods, manifold inference, optimal representatives, robust distance-to-measure constructions, zigzag persistence, multiparameter persistence and differentiable topological learning. These are not all required to master the present scope. Each needs its own assumptions, algorithms and validation.

Finish by solving the final assessment without notes, correcting every critical error, and returning to related questions after a delay. No script should award mastery merely because Python ran. You complete this course by being able to explain, derive, compute, test and appropriately limit its conclusions.

## Independent exercises

Do these before reading the worked solutions. A copied solution is not an independent pass.

**12.1.** Write the complete worked-capstone question in one sentence without making a broad claim about all computer vision.

**12.2.** Why is it legitimate to refit on training plus validation before the final test?

**12.3.** List the frozen topological construction and feature choices.

**12.4.** Why is the current test not an unseen-writer test?

**12.5.** What must change in the evidence plan after adapting the method to improve a viewed test score?

**12.6.** Propose a subject/session-safe split for a sports-motion study.

**12.7.** Explain why equal Euler characteristic does not establish equal topology.

**12.8.** Name the evidence required to mark this course and the book audit complete.

## Mastery gate

Reproduce and defend the worked capstone, complete an independent application, and retain an explicit book-audit gap log.

Explain one limitation and solve a new variant after a delay. Suggested progression threshold: 85% on the local knowledge check, with every critical error corrected. This is a course rubric, not accreditation.

## Free readings and attribution

Source IDs: D1, D2, D3, R9, R10. See `docs/SOURCES.md` for direct official links and assigned topics. The exposition, examples, code, and solutions here are original course material, not copied textbook chapters.

## Run and continue

Open `notebooks/12_lab.ipynb`. Its saved outputs are also readable from the browser reader. After the lab, compare with `solutions/12_solutions.md`, record what was independent, and continue only when the gate is met.


---

Source: `lessons/13_lesson.md`

# Stage 13 — From topology to smooth manifolds

Local coordinates, tangent directions, and why a camera image is not a global chart.

**Track:** applied geometry continuation, not a claimed chapter of the book. **Prerequisites:** Stage 01, Stage 02, Stage 03, Stage 04.

## 1. What changes after the topology course?
Topology asks which properties are preserved by an appropriate continuous equivalence. Smooth geometry adds a way to differentiate. A distance or Riemannian metric adds measurements of length and angle. These are related structures, not interchangeable words.

Picture the Earth's surface without assuming geography knowledge: near a point on a sphere, a small patch behaves like a two-dimensional sheet. A single global flat coordinate map cannot describe that entire sphere as one open subset of the plane. Several overlapping patches solve the problem. We do not cut the object into disconnected physical pieces; we change the way we label points.

A topological n-manifold, in the convention used here, is Hausdorff, second countable, and locally homeomorphic to open subsets of Rⁿ. The local requirement explains dimension; the two global conditions rule out pathological spaces. Manifolds with boundary have a different local half-space model. A point cloud from a sensor is not automatically a manifold simply because a smooth surface is an attractive explanation for it.

## 2. Charts and atlases from zero
A chart `(U, φ)` consists of an open region U of the manifold and a homeomorphism φ from U onto an open subset of Rⁿ. Its output is a list of coordinates. An atlas is a collection of charts whose regions cover the manifold.

On an overlap, the same physical point p has two coordinate descriptions: a=φ(p) and b=ψ(p). To convert a into b, first undo φ and then apply ψ:

```text
b = ψ(φ⁻¹(a))
ψ ∘ φ⁻¹ : φ(U ∩ V) → ψ(U ∩ V)
```

The domains matter. This formula is not defined for arbitrary points outside the overlap. A smooth atlas requires smooth transition maps. A smooth structure can be described using a maximal compatible smooth atlas. These definitions are the mathematical foundation of the chart-transition exercise, not a claim about a learned embedding. [G01]

## 3. An explicit sphere calculation
Let p=(x,y,z) be on the unit sphere `x²+y²+z²=1`. Remove the north pole `(0,0,1)`. The north-pole stereographic chart is

```text
φ_N(p) = (x/(1-z), y/(1-z)).
```

For a=(u,v), write q=u²+v². The inverse is

```text
φ_N⁻¹(a) = (2u/(1+q), 2v/(1+q), (q-1)/(1+q)).
```

Check the formula rather than memorize it. The squared norm of the numerator is `4q+(q-1)²=(q+1)²`, so its output lies on the sphere. Substitution into the chart returns u and v. The denominator `1+q` is positive everywhere. The north pole never appears for a finite a, exactly as the chart definition requires.

The south-pole chart uses denominator `1+z` and its inverse negates the final coordinate above. On the overlap, `φ_S(φ_N⁻¹(a))=a/||a||²`, with a≠0. Derive that cancellation by hand. The origin in the north chart describes the south pole, which is excluded by the south chart.

## 4. Tangent vectors are constrained local changes
If a differentiable curve p(t) stays on the sphere, differentiate `p(t)ᵀp(t)=1`. The result is `2p(t)ᵀp′(t)=0`. Thus a tangent vector at p is orthogonal to p:

```text
T_p S² = {v in R³ : pᵀv = 0}.
```

For nonzero tangent v, the curve `cos(t||v||)p + sin(t||v||)v/||v||` remains on the sphere and has initial derivative v. This also shows why the stated tangent plane contains all permissible initial directions, not merely some of them.

A local derivative needs a chart or an equivalent embedded calculation. Our lab compares analytic derivatives to finite differences. That comparison catches coding errors; it does not replace the analytic reasoning or prove smoothness for every input.

## 5. Use the real stereo data without changing its meaning
The notebook turns benchmark-derived 3D points into unit viewing directions `p/||p||`. These directions lie on a sphere by construction. You will map them between charts and recover them. You will also see why a chart near its excluded pole can become numerically awkward.

This does not prove that the original scene is spherical. Normalization deliberately removes distance along the ray. Two objects at different ranges can yield the same direction. The calculation is a real-data example of a coordinate representation, not a discovery of scene topology.

## 6. Why an image is not generally a chart of the whole scene
Perspective projection sends `(X,Y,Z)` to quantities involving X/Z and Y/Z. Multiplying all three coordinates by the same positive number gives the same pixel. Therefore the map is not one-to-one over a three-dimensional scene. Occlusion and limited field of view lose still more information.

A camera may parameterize a suitable visible surface patch under additional conditions, but ordinary projection is not an invertible chart of arbitrary 3D space. Neither manifold terminology nor a transformer removes this ambiguity.

## 7. Keep the hierarchy clear
A topological manifold supplies local topological coordinates. A smooth structure permits derivatives. A Riemannian metric measures tangent-vector lengths. A Lie group combines smooth structure with compatible group operations. Stage 14 uses this last idea for rotations. There is no need to implement a general manifold library before you understand the explicit sphere example.

## Independent conceptual exercises

1. Define a chart, an atlas, and the domain of a transition map.
2. Compute the two chart coordinates of (0.6,0,0.8) and invert them.
3. Prove that the inverse stereographic formula lies on the unit sphere.
4. Derive the equation pᵀv=0 for tangent vectors.
5. Why does normalizing a real point cloud to unit vectors discard depth?
6. Explain why perspective projection is not generally a chart of 3D space.

## Mastery gate

Independently derive a chart round trip and explain the information normalization removes.

Readings: G01, G02. See the [source ledger](docs/SOURCES_V3.md) for checked links, evidence status and source differences.


---

Source: `lessons/14_lesson.md`

# Stage 14 — Rotations, rigid transforms, and the camera model

A point must carry its frame, units, and projection convention.

**Track:** applied geometry continuation, not a claimed chapter of the book. **Prerequisites:** Stage 13.

## 1. Start with a coordinate frame
A coordinate frame specifies an origin and three directed axes. The same point has different numbers in two frames. The point does not move merely because we change its coordinates. Confusing an active motion of an object with a passive change of coordinates is a common source of inverses in the wrong place.

Our convention is explicit: `p_B = R_BA p_A + t_BA`, using column vectors. `T_BA` means “coordinates in B from coordinates in A.” The code stores N points as rows, so it calculates `points @ R.T + t`. The transpose is an implementation consequence of the table layout, not a different rotation convention.

## 2. Valid rotations cannot be arbitrary matrices
A proper three-dimensional rotation satisfies `RᵀR=I` and `det R=+1`. Orthogonality preserves dot products and lengths. The positive determinant excludes reflections. The set of these matrices is SO(3). Although a matrix contains nine entries, a rotation has three local degrees of freedom. [G02]

Take a quarter turn around z. It maps (1,0,0) to (0,1,0) in our right-handed convention. Apply a turn about x and then a turn about z; reverse their order. You will usually obtain different results. Matrix multiplication is not generally commutative.

## 3. From a local rotation vector to a valid matrix
A rotation vector w points along a rotation axis and has magnitude θ equal to the angle in radians. Define `[w]×` so that `[w]×v=w×v`. Rodrigues' formula is

```text
R = I + (sin θ / θ)[w]× + ((1-cos θ)/θ²)[w]×².
```

At zero, the limiting coefficients are 1 and 1/2. The implementation uses short Taylor expansions near zero to avoid numerical cancellation. You will compare it with SciPy's rotation-vector implementation and check both orthogonality and determinant. [G03]

A small update may be multiplied on the left or right; these express changes in different frames. Always name the convention. Adding independent values to nine matrix entries does not preserve SO(3).

## 4. Quaternions do not remove conventions
A unit quaternion is another rotation representation. q and -q describe the same rotation, so Euclidean differences between quaternion components can mislead. Libraries differ on scalar-first `(w,x,y,z)` versus scalar-last `(x,y,z,w)` ordering. Ceres explicitly distinguishes its quaternion layouts. [G04]

Our numerical labs use rotation matrices and vectors. The quaternion reading is a representation audit, not a claim that all quaternion conventions are interchangeable. For two valid rotations, the relative rotation angle can be computed from the trace of `R₁ᵀR₂`; clamp the cosine argument to [-1,1] for floating-point roundoff.

## 5. Translation and homogeneous transforms
A rigid transform belongs to SE(3) and can be written

```text
T_BA = [[R_BA, t_BA],
        [0 0 0, 1]].
```

Composition follows the labels: `T_CA = T_CB T_BA`. The inverse is `[[Rᵀ,-Rᵀt],[0,1]]`. Derive it by solving `p_B=Rp_A+t` for p_A. Translation is not simply negated unless the rotation is identity. [G05]

If a camera uses extrinsics `p_camera=R p_world+t`, its centre in world coordinates is `C=-Rᵀt`. The extrinsic translation is not the camera centre. The lab checks this relationship with a real benchmark-derived cloud and a deliberately chosen frame change.

## 6. The pinhole camera from similar triangles
A point with camera coordinates `(X,Y,Z)` and positive Z projects as

```text
u = fx X/Z + cx
v = fy Y/Z + cy.
```

The intrinsic matrix K contains focal lengths in pixels and a principal point. Here u means column and v means row. The camera axes are x right, y down, z forward. The matrix formula is `λ[u,v,1]ᵀ=K[X,Y,Z]ᵀ`. [G06]

Backprojection needs depth. If the depth means camera-axis Z, multiply `K⁻¹[u,v,1]ᵀ` by Z. If a sensor instead supplies radial distance to the camera centre, the ray must be normalized before multiplication. Interchanging those definitions creates systematic off-axis errors.

## 7. Pixels change when preprocessing changes
Cropping or resizing images changes pixel coordinates. For a declared image-coordinate affine map A, the corresponding intrinsics transform as `K′=AK`. Actual resizing libraries may use different pixel-centre conventions; record the precise transform, not just the new width. Extrinsics do not change merely because an image is cropped.

Lens distortion is separate from the ideal pinhole model. A raw fisheye image is not an undistorted pinhole image. Our reference pair is already rectified; the lab does not demonstrate raw-camera distortion calibration. The OpenCV calibration resource is the practical next reading for estimating intrinsic and distortion parameters. [G07]

## 8. The scale ambiguity you must remember
Projection of p and projection of sp agree for any positive scalar s. If camera translations and scene points scale together, the image evidence can remain identical. Recovering metre units needs an appropriate measured baseline, landmark distance, or another trusted scale cue. A predicted depth map is not a measured ruler.

## Independent conceptual exercises

1. Explain the meaning of T_BA and compose T_CB with T_BA.
2. Derive the rigid-transform inverse and camera-centre formula.
3. Why is det R=+1 necessary in addition to RᵀR=I?
4. Project (0.2,0.1,2) with f=800 and principal point (320,240).
5. Distinguish optical-axis depth, radial range, and disparity.
6. Explain which parameters must change when a calibrated image is cropped.

## Mastery gate

Demonstrate frame round trips and identify a projection ambiguity without a library.

Readings: G02, G03, G04, G05, G06, G07. See the [source ledger](docs/SOURCES_V3.md) for checked links, evidence status and source differences.


---

Source: `lessons/15_lesson.md`

# Stage 15 — Measured stereo, calibration, and uncertainty

Use two images to estimate depth, then test what the estimate really supports.

**Track:** applied geometry continuation, not a claimed chapter of the book. **Prerequisites:** Stage 14.

## 1. What rectification buys you
Two cameras see a static point from different places. With known calibration, corresponding image locations constrain viewing rays. Stereo rectification warps the images so corresponding points are sought on the same scanline in the ideal rectified model. That simplifies matching from a two-dimensional search to a horizontal one. It does not make every pixel matchable: occlusion, repetitive texture, reflections and missing reference data remain.

Our real example is the Middlebury 2014 motorcycle pair distributed with scikit-image. It is a downsampled, already rectified pair. The course preserves its stated calibration and observes the arrays directly: two 500×741 RGB images and a 500×741 disparity array. The documentation's displayed disparity shape contains a trailing-channel inconsistency; the loader and manifest record the actual 2D array instead. This is an explicit source/data reconciliation, not a silent substitution. [D04]

## 2. Derive the depth formula, including the offset
Let baseline B separate the cameras horizontally; use the left camera as the reference. For a point (X,Y,Z),

```text
u_left  = f X/Z + cx_left
u_right = f (X-B)/Z + cx_right.
```

Subtract to get disparity `d=u_left-u_right=fB/Z+cx_left-cx_right`. Define `doffs=cx_right-cx_left`. Solving gives

```text
Z = f B / (d + doffs).
```

The `fB/d` simplification is valid only when this principal-point difference is zero. For the bundled downsampled pair, f=994.978 pixels, B=0.193001 metres and doffs=31.086 pixels. [D04, D05]

The source expresses baseline as 193.001 millimetres. We convert once to metres and label the result. Nonfinite disparity and nonpositive denominator values are missing, not zero-depth observations. Never fill them merely to make a point cloud look complete.

## 3. A simple matching algorithm you can inspect
For a selected pixel, take a square patch from the left image. Compare it with patches on the same row in the right image for integer disparities from 0 to a declared maximum. Sum or average the absolute intensity differences; choose the lowest cost. This is a sum-absolute-difference baseline, abbreviated SAD.

The prediction function receives images and selected pixel coordinates. It never receives the reference disparities. Its parameters are fixed for the demonstration before error measurement. Ties choose the smaller disparity; the margin between the two lowest costs is an ambiguity indicator, not a probability.

This deliberately simple model lacks subpixel refinement, a full occlusion treatment, and a learned feature representation. It is valuable precisely because you can understand why it fails. A comparison to a sophisticated model should include this baseline but should not pretend the baseline is state of the art.

## 4. Measure errors without hiding missing predictions
Evaluate predicted disparities at pixels where a reference is available. Report the number eligible, number evaluated, coverage, mean and median absolute pixel error, and the fraction exceeding a declared threshold. A lower error on a sharply reduced mask can be less useful than a slightly higher error with broad coverage. Show both.

Converting prediction and reference to depth gives an additional metre-error view. This is still agreement with the supplied disparity/calibration reference. It is not an independent measurement of the motorcycle, and it is not an unseen-scene evaluation.

## 5. Triangulation beyond the simplified formula
With general projection matrices P₁ and P₂ and corresponding undistorted pixels, a homogeneous point X satisfies cross-product equations. For each view, use rows like `u P[2]-P[0]` and `v P[2]-P[1]`. Stack them in A and solve `AX≈0` using the last right singular vector; then divide by its homogeneous coordinate.

This linear DLT algorithm minimizes an algebraic quantity. Nonlinear reprojection-error refinement is a different step. Check positive depth in both cameras, geometric conditioning, and correspondence validity. Parallel or coincident rays may not determine a stable finite point. Our tests compare a clean case with OpenCV when available. [G06]

## 6. What calibration itself requires
Intrinsic calibration estimates how camera-frame directions map to pixels, including an appropriate distortion model. Extrinsic calibration determines frame relationships. A known target supplies geometric constraints; varied target poses help constrain the parameters. Independent distances or target observations should evaluate the result instead of reusing every fitted observation as a validation claim. [G07]

The notebook includes a controlled synthetic fit for a simple known-pinhole model. Its world points and answers are generated for a mathematical exercise. The real stereo calibration is supplied by the dataset, not estimated afresh by this lesson. A real phone calibration remains a separate capture-and-evaluation exercise.

## 7. Sensitivity grows at small effective disparity
Differentiate the derived formula: `dZ/dd = -fB/(d+doffs)²`. Small pixel changes can make large depth changes when effective disparity is small. For a small assumed disparity standard deviation σ_d, first-order propagation gives approximately `σ_Z=|dZ/dd|σ_d`, assuming f, B, and doffs are fixed. Their actual uncertainty would need additional terms and correlations.

The lab compares this local approximation with a controlled Monte Carlo experiment. The random perturbations are generated noise, not observed sensor-error statistics.

## 8. Timing is part of geometry
A moving point captured at two different instants is not the same static point. Triangulating those observations under a simultaneous-static assumption can produce a plausible false position. An image timestamp, clock synchronization, exposure timing and rolling-shutter model can all matter. The synthetic timing experiment demonstrates the assumption; it does not measure synchronization on your cameras.

## Independent conceptual exercises

1. Derive Z=fB/(d+doffs) from the two pixel equations.
2. Calculate why the principal-point offset cannot be omitted here.
3. Which inputs does the SAD predictor receive, and which are reserved for evaluation?
4. What is the difference between DLT and nonlinear reprojection refinement?
5. Derive the local depth uncertainty for a fixed calibrated stereo model.
6. Why does a low reprojection residual not establish correct synchronization or scale?

## Mastery gate

Run the baseline, explain its denominators and missing values, and derive the uncertainty approximation.

Readings: D04, D05, G06, G07. See the [source ledger](docs/SOURCES_V3.md) for checked links, evidence status and source differences.


---

Source: `lessons/16_lesson.md`

# Stage 16 — Attention and VGGT, from pixels to proposed geometry

Understand the network idea without confusing a toy attention lab with trained inference.

**Track:** applied geometry continuation, not a claimed chapter of the book. **Prerequisites:** Stage 14, Stage 15.

## 1. Why a geometry model is an extension, not the foundation
The previous stages showed how calibrated projections constrain a scene. A learned model also uses patterns acquired from training data. Those patterns can produce a useful hypothesis when direct geometric evidence is incomplete. They do not turn an ambiguous observation into a guaranteed measurement.

Keep three layers separate: what a camera observed, what a mathematical model permits, and what a trained network predicts. Our small attention experiment teaches a computation. The optional VGGT runner performs a separate model experiment only after you supply an appropriate checkpoint and environment.

## 2. Tokens are pieces of an image represented as vectors
An RGB image is a height-by-width array with three channels. Divide it into patches; flatten each patch or map it through a learned feature extractor to obtain a token vector. A token is not a word here. Its source location and image identity must remain traceable.

Suppose there are N tokens of dimension d. Place them in a matrix X. Learnable linear maps can form queries Q, keys K and values V. The scaled dot-product attention calculation is

```text
scores  = Q Kᵀ / sqrt(d)
weights = softmax(scores, row by row)
output  = weights V.
```

A query asks which other representations should contribute. A key supplies information for the comparison. A value supplies the content being mixed. These descriptions are teaching analogies for matrix operations, not evidence that the model reasons in human sentences.

## 3. Work a tiny softmax example
For scores [0,log 3], exponentiation produces [1,3], and normalization gives weights [1/4,3/4]. If the values are [2,10], the weighted output is 8. Subtracting the same constant from all row scores leaves softmax unchanged; subtracting the maximum helps prevent overflow.

A mask restricts which keys a query may use. A row with no allowed keys is invalid in our implementation. A masked attention calculation can mix representations, but it does not by itself triangulate a point, establish a correspondence, or prove causality.

## 4. Frame attention versus global attention
Frame-wise self-attention allows tokens to mix only within the same input image. Global self-attention allows mixing across the entire image collection. The original VGGT alternates these two forms, with image features, camera tokens, and prediction heads for camera and dense outputs. This is cross-view information exchange implemented with self-attention; it is not an architectural claim that the paper uses separate cross-attention blocks. [V01, V02]

In the notebook, real motorcycle-image patches become tokens. We compare the two masks and inspect row sums and prohibited weights. The features are deliberately simple and untrained. An attention image from this toy is not a VGGT attention visualization, a depth map, or proof of a matched physical object.

## 5. Read the actual model output contract
The original repository documents image tensors as `[S,3,H,W]` or `[B,S,3,H,W]`. Its returned arrays include a camera encoding, depth, confidence, and world-point maps. When query points are provided, the tracking output has shape `[B,S,N,2]`: those are 2D pixel correspondences. [V03]

A **depth map** gives a scalar per pixel under its depth convention. A **point map** gives a 3D coordinate per pixel in a chosen frame. A **track** links an identity across images or times. Turning corresponding pixels and depths into a metric 3D trajectory requires consistent frames, scale, timestamped evidence, and an appropriate dynamic-scene model.

The original paper uses the first camera as its reference and normalized scene scale, assumes a centred principal point, and describes limitations for fisheye/panoramic input and substantial non-rigid deformation. These qualifications are central to a sports application. [V02]

## 6. Use an opt-in runner, not an implicit model download
The package includes `optional/run_vggt_local.py` for the original model API. It requires an existing repository, an exact expected commit, a local checkpoint, a licence-review acknowledgement, and an ordered list of image paths. It records input hashes, checkpoint hash, code revision, processed-image dimensions, timing, and GPU memory. It does not download weights, accept access terms for you, or claim this environment ran inference.

The original repository distinguishes the original non-commercial checkpoint from a separately released commercial-use checkpoint. A code repository's name does not settle the permissions of every weight file. Record the actual checkpoint and applicable terms. [V04]

The runner is not an Omega adapter. Different model generations can have different packages, outputs and preprocessing. Silent substitution would make comparisons uninterpretable.

## 7. What the Omega source update teaches
The supplied source highlights VGGT-Ω. Independent checking found a date discrepancy: the project page labels its training/checkpoint notice September 18, 2026, while the official README labels the corresponding notice September 8. We retain both statements rather than invent a corrected release date. The README identifies a 416-resolution reproduction checkpoint for benchmark comparisons and distinguishes it from other checkpoints. [V05, V06]

Omega's compact register-based exchange is a worthwhile later reading. Training-memory claims and inference-memory measurements are different quantities. Neither is a benchmark on your own GPU unless measured there. [V05, V06]

## 8. What you should be able to say
“Here is the tensor contract. Here is the reference frame. Here is what was learned rather than measured. Here is the preprocessing. Here is the checkpoint. Here are the failure cases. Here is what has actually run.” That description is more useful than “the model understands 3D” when you need accurate measurements.

## Independent conceptual exercises

1. Calculate softmax([0, log 3]) and its weighted average of [2,10].
2. Distinguish frame-wise and global self-attention and describe the mask.
3. Why is the toy patch experiment not a VGGT reconstruction?
4. What does a track tensor ending in dimension two represent?
5. Why do normalized scene coordinates not establish metre accuracy?
6. How should the conflicting Omega update dates be recorded?

## Mastery gate

Explain attention by hand and complete a model-output/source audit before attempting inference.

Readings: V01, V02, V03, V04, V05, V06. See the [source ledger](docs/SOURCES_V3.md) for checked links, evidence status and source differences.


---

Source: `lessons/17_lesson.md`

# Stage 17 — Register, validate, and ask topology the right question

Frame agreement is necessary; it is not independent physical truth.

**Track:** applied geometry continuation, not a claimed chapter of the book. **Prerequisites:** Stage 06, Stage 07, Stage 08, Stage 10, Stage 15, Stage 16.

## 1. Registration aligns descriptions
Two reconstructions may differ by a global rotation, translation and scale. A similarity transform writes `y=sRx+t`, with s positive and R a proper rotation. Finding these parameters from paired landmarks is registration. It does not repair every local shape error and does not discover correct point correspondences on its own.

Our fit first subtracts the point-set means. It uses a singular-value decomposition of a cross-covariance matrix to determine the proper rotation, then solves for scale and translation. Reflection is explicitly excluded. Non-collinear paired anchors are required in this educational implementation. Collinear anchors leave rotation around the line unconstrained.

## 2. Fit and evaluate on different evidence
Choose registration anchors before assessing the held-out error. Fit only to those anchors. Apply the same fitted transform to the remaining correspondences. If you fit to every point and report its fit residual as “held-out accuracy,” the label is wrong even when the residual is small.

The real-data lab creates a known transformed version of the benchmark-derived cloud, fits on one subset, and checks the remaining subset. It verifies recovery of an imposed coordinate change on real-shaped data. Because we imposed the transformation, it is not a measurement of VGGT quality. A second controlled experiment perturbs only unregistered points to demonstrate why a perfect anchor fit can hide local errors.

## 3. There are several kinds of error
A paired-point error compares corresponding 3D coordinates. A distance error compares lengths between specified landmarks. A camera rotation error compares orientations. Reprojection error compares predicted pixels against observed pixels. Completeness asks what valid support remains. Scale consistency asks whether metric scale stays appropriate across views or independent subsets.

These metrics answer different questions. A nearest-neighbour cloud distance can be low even with incorrect identities, missing regions, or surfaces shifted onto a nearby structure. Rigid alignment can remove an arbitrary pose difference but must not be used to conceal a calibration requirement that the experiment intended to test.

Our lesson does not set a universal “good enough” threshold. Acceptance thresholds must come from the application's measurement needs and be specified before the final evaluation.

## 4. What topology contributes
Persistent homology describes the shape of a chosen complex or filtration. It does not determine which point is a hand, which loop is a basketball rim, or whether coordinates are physically accurate. A Rips diagram uses metric distances; rigid transforms preserve them, positive scaling rescales its filtration coordinates, and local warping can change them.

The notebook checks this on a small, fixed sample of the real cloud. It uses the existing course implementation and a deliberately small sample rather than constructing an enormous Rips complex. That is a controlled mathematical diagnostic, not a complete reconstruction-quality score.

A cloud can have convincing topology while being badly stretched. Conversely, removing unseen or invalid points can change a diagram without proving a physical structure appeared or disappeared. Before interpretation, state the sampling, mask, metric, coefficients, maximum simplex dimension and scale interval.

## 5. A reconstruction hole is not automatically a physical hole
Imagine a camera misses a patch of a wall. A hole in the observed sample may reflect occlusion rather than an opening in the wall. Additional views may fill it. If a method inpaints the area, a visually closed surface is a model-generated hypothesis. Label observed, inferred and unavailable regions differently.

Do not let a descriptor retroactively promote inferred pixels into observed evidence. The reconstruction should retain source IDs and confidence/visibility metadata so you can inspect where a claimed structure came from.

## 6. A useful paired acceptance protocol
For a future captured scene, choose independent measured landmarks, reserve some for evaluation, and keep the original image evidence. Compare a classical calibrated baseline, a registered learned proposal, and any refinement initialized by the proposal. Save all variants. Match sampling and masks for a fair comparison, and report coverage changes explicitly.

A result can be useful without replacing the authoritative calibration. It can initialize optimization, suggest correspondences, expose missing views or prioritize review. The output should enter the existing state only under its allowed evidence status.

## 7. What remains outside this lab
There is no new human-subject capture, independently measured basketball scene, or executed VGGT checkpoint in the reference notebook. The code establishes registration and invariance behaviour. The capstone protocol makes the missing external measurement work concrete rather than pretending it happened.

## Independent conceptual exercises

1. What information is needed before fitting a similarity transform?
2. Why do collinear anchors fail to constrain all orientation freedom?
3. Distinguish registration residual from held-out measurement error.
4. How do translation, rotation and uniform scaling affect a Rips filtration?
5. Why can a reconstructed hole be an observation failure rather than a physical hole?
6. What does this stage prove, and what does it not prove about VGGT?

## Mastery gate

Defend the fit/evaluation split and distinguish metric evidence from topology diagnostics.

Readings: G06, D04, T01. See the [source ledger](docs/SOURCES_V3.md) for checked links, evidence status and source differences.


---

Source: `lessons/18_lesson.md`

# Stage 18 — Make the pipeline efficient without changing the evidence

Measure conversion, queues, age and output—not just the model call.

**Track:** applied geometry continuation, not a claimed chapter of the book. **Prerequisites:** Stage 14, Stage 15.

## 1. Throughput and latency answer different questions
Throughput counts completed items per time interval. Latency measures elapsed time from a declared start to a declared finish for one item. A pipeline can process many frames per second while displaying results from long ago if a queue grows. A high frame rate does not guarantee a useful live experience.

Name the boundaries: capture, arrival, queue entry, processing start, preprocessing, device transfer, inference, geometry, serialization, and display. A CPU timer around one function covers only that function. It does not cover phone exposure or browser display unless those timestamps are actually included.

## 2. The attached source gives a hypothesis, not our benchmark
The supplied ROS2/PointPillars account attributes speed improvement to point-cloud conversion and reports its author's timing. We retain that as a reported example. Our lab neither reproduced that hardware pipeline nor measured its claimed frame rate. The transferable hypothesis is that representation conversion can dominate useful work.

The ROS2 source provides structured-array conversion and an equally typed-field NumPy path. Field names, data types, byte order, padding and organization matter. Treating every buffer as contiguous xyz float32 data without inspecting its layout is not a general PointCloud2 parser. [S01]

## 3. Vectorization with a semantic equality check
Our real-data lab transforms a benchmark-derived point cloud using an explicit per-point loop and an array operation. Both compute the same formula. First compare their outputs to numerical tolerance, then time repeated runs. An optimization is not an improvement if it quietly changes invalid-value policy, units, ordering or precision.

Use a monotonic performance timer, a warm-up, multiple repetitions, and a distribution summary. A single lucky run is not a reliable comparison. The saved results describe this build environment only. Your Mac or GPU may behave differently, and pure CPU microbenchmarks say little about a full capture-to-display pipeline.

## 4. Simulate the queue before blaming inference
For a single FIFO server, let aᵢ be an arrival and sᵢ its service time. The completion recurrence is

```text
finish_i = max(arrival_i, finish_(i-1)) + service_i
latency_i = finish_i - arrival_i.
```

If a frame arrives every 10 milliseconds but service always takes 20 milliseconds, delay grows. Batching, dropping stale work, reducing processing, or changing the capture rate have different trade-offs. A latest-frame policy may reduce age while discarding temporal evidence needed for an event. There is no universally correct queue policy independent of the task.

The notebook's queue trace is a simulation with chosen times. It is not a hardware trace. We print that status alongside its p50, p95 and maximum values.

## 5. Timestamps are data
For several devices, timestamps may have offset and drift. A simple model relates a device clock to a reference by `t_ref = a t_device + b`. Estimating both a and b requires appropriate shared timing evidence over a sufficient interval. Matching numeric timestamp values alone does not synchronize clocks.

Keep source frame IDs, presentation timestamps, time base, dropped-frame information and any mapping uncertainty. Never reorder observations silently to make a trace look smoother. Offline preprocessing can use the whole sequence; a live method must respect the observation availability cutoff.

## 6. Device timing needs synchronization
Accelerator work may be asynchronous. Timing only the CPU call can measure scheduling rather than completion. The optional runner places device synchronization around its timed forward pass and separately labels load, preprocess, forward and serialization durations. Those remain model-run boundaries, not capture-to-display latency. [S02]

Peak allocated and reserved GPU memory are different statistics. Baseline model storage, activations, head choices, precision, resolution and frame count all matter. Start with a small run and measure instead of extrapolating a paper's different hardware configuration.

## 7. Preserve evidence while optimizing
A useful event record keeps the source identity, observation timestamp, availability time, model/checkpoint version, calibration version, inferred/observed state and uncertainty. Lightweight tracking and heavier geometry may run at different rates; their outputs still need compatible identities and times.

No ROS2 installation or production rewrite is required to learn these principles. The core exercise is a controlled CPU comparison plus a queue model, with clear boundaries on what was and was not measured.

## Independent conceptual exercises

1. Distinguish throughput, service time, latency, and stale-result age.
2. Calculate the FIFO recurrence for the supplied three-frame example.
3. What must be checked before trusting a vectorized replacement?
4. Why can a CPU timer undermeasure GPU work?
5. What does t_ref=a t_device+b represent?
6. Why is a latest-frame queue not automatically best for event detection?

## Mastery gate

Report a reproducible local benchmark and explain why it is not end-to-end live-system evidence.

Readings: S01, S02. See the [source ledger](docs/SOURCES_V3.md) for checked links, evidence status and source differences.


---

Source: `lessons/19_lesson.md`

# Stage 19 — From geometry to cautious interaction hypotheses

Proximity is evidence to inspect—not proof of contact, possession or release.

**Track:** applied geometry continuation, not a claimed chapter of the book. **Prerequisites:** Stage 15, Stage 18.

## 1. A frame is not an event
An event describes change over time. “The ball is near the hand” is a relation at one moment. “The player released the ball” is an interpretation of a sequence, including control, separation and subsequent motion. A detector should not silently convert a relation into a stronger claim.

Begin with shared frames, units, identities and timestamps. A hand estimate from one player cannot be combined with a ball track from another time and treated as a valid interaction. Invisible or inferred observations need explicit status.

## 2. Build the smallest causal hypothesis
Our exercise uses a distance stream and visibility flags. After several observed near samples, the detector becomes armed. If several observed far samples then occur, it emits a `separation_candidate`. The name matters: it does not say “contact confirmed” or “release measured.” Missing evidence or an excessive time gap resets the state conservatively.

Two thresholds create hysteresis: the “near” threshold is smaller than the “far” threshold. An intermediate band avoids some threshold chatter. Minimum consecutive observations reduce isolated fluctuations but introduce confirmation delay. The threshold and count choices are demonstration settings, not validated basketball operating limits.

## 3. Onset is not decision time
If the first far observation is at .03 seconds and two far observations are required, the detector may make its decision at .04 seconds. Its reported candidate onset can be .03 while availability is .04. That is not time travel: the label is emitted later and refers to an earlier observed boundary.

A live metric must include the decision delay. Comparing this output to an offline sequence model that can inspect every future frame without disclosing the difference is not a fair live-performance comparison.

## 4. Test causality by changing the future
For each prefix of an input sequence, run the detector using only that prefix. Its emitted decisions should equal the subset of full-sequence decisions available by that prefix's last timestamp. This is a powerful test for accidental future access.

It is not enough for the code to be placed in a loop. Precomputed smoothed positions, globally normalized time-series features or future-filled gaps can already contain later evidence. The availability cutoff applies to upstream features as well.

## 5. What the real and simulated examples mean
The real stereo sample provides a static cloud. The lab uses distances between selected reconstructed scene points to show why proximity requires declared units and a compatible frame, while a common rigid frame change preserves distance. It contains no labelled hand–ball interactions. No real basketball-event precision or recall can be estimated from that dataset.

The event sequences are explicitly generated controls: near then far, near miss without a sustained near history, missing evidence near the transition, and a clock-gap case. They test software semantics under known conditions. They are not disguised captured trajectories, and they establish no production sports accuracy.

For genuine event evaluation, collect independent annotated sequences, including hard negatives: a hand passing near a ball without controlling it, brief occlusion, two players crossing, and track swaps. Record annotation uncertainty and disagreements instead of calling every boundary exact.

## 6. Match events one to one
Predicted and reference onsets should be matched under a stated tolerance, using each event at most once. Otherwise several predictions near one true event can all be counted as correct. Count true positives, false positives and false negatives, and state the matching rule. Precision is TP/(TP+FP); recall is TP/(TP+FN). With a zero denominator the corresponding rate is undefined, not automatically perfect.

Our small matcher chooses earliest feasible chronological pairs and maximizes the number of matches for sorted one-dimensional onsets with a fixed tolerance. It does not minimize timing error among all maximum-size matchings. Report its convention rather than hiding this distinction.

## 7. Extend evidence without overclaiming
A stronger basketball model might combine hand–ball distance, relative velocity, motion consistency, pose, visibility and identity continuity. Such features still need reliable measurements and annotation. No threshold alone certifies physical contact. A causal state estimator can preserve a hypothesis during short occlusion, but the output must remain inferred rather than directly observed.

The supplied human–object interaction account motivates this separation. It did not establish metric accuracy, event precision/recall, or a minimum reliable processing rate. Those remain experiments to conduct, not facts to fill in.

## Independent conceptual exercises

1. Why is a near-to-far transition not sufficient proof of release?
2. For the supplied five samples, state onset and decision time.
3. What should missing observations do in this conservative baseline?
4. Describe a prefix test for causality and one upstream leakage failure.
5. Calculate precision and recall for two predictions matched to one reference.
6. What real event evidence is missing from the bundled stereo data?

## Mastery gate

Demonstrate prefix invariance and explain why every emitted label remains a hypothesis.

Readings: U01, S01. See the [source ledger](docs/SOURCES_V3.md) for checked links, evidence status and source differences.


---

Source: `lessons/20_lesson.md`

# Stage 20 — Independent spatial capstone and continuing mastery

One evidence chain from observations to a justified conclusion.

**Track:** applied geometry continuation, not a claimed chapter of the book. **Prerequisites:** Stage 12, Stage 13, Stage 14, Stage 15, Stage 16, Stage 17, Stage 18, Stage 19.

## 1. The capstone is a new question, not another rerun
The supplied notebooks are demonstrations with visible answers. Finishing them gives practice, not an independent result. For your own capstone, select a question whose answer is not already exposed by the reference notebook. Start small enough that an incorrect assumption can be found and corrected.

A suitable first spatial question is: “On a measured static scene, does a learned proposal improve reconstruction or initialization compared with the calibrated baseline under a declared error and coverage requirement?” A topology-focused alternative is: “Does this descriptor add information beyond simpler geometric features under independent evaluation?” Either can legitimately end in a negative result.

## 2. Write the protocol before examining the final outcome
Specify the observation unit, capture conditions, camera model, clock assumptions, coordinate frame, metric units, calibration references, registration anchors, holdouts, masks, selection rules, metrics and thresholds. Name which data may fit parameters and which must remain untouched until evaluation.

Also state the claim you are not making. A static-scene result is not a fast-motion sports result. A small CPU transformation benchmark is not live application latency. A learned latent representation is not a calibrated map. A stable topological feature is not a semantic object label.

## 3. Use a declared sequence of acceptance tests
First establish the numerical contracts: dimensions, units, transforms, finite values and identities. Then test geometric consistency such as reprojection. Then test independent measured references. Finally evaluate generalization across independent scenes or sessions when that is the intended claim. A later test does not erase a failed earlier assumption.

The package's final bridge notebook builds an evidence summary from the executed stage reports. It checks those reports are present and states the scope of their results. It does not turn every source status into a green production acceptance badge. GPU inference and real hand–ball annotation remain unexecuted requirements until supplied.

## 4. A practical static-scene collection
Choose an object or room with visible stationary landmarks and measured distances. Capture overlapping views with a fixed documented camera mode. Preserve original images, image sizes and timestamps. Reserve some measurements from all fitting steps. Record measurement uncertainty and repeat a small subset to expose mistakes.

Start without moving people. Once static geometry is supported, introduce a stationary person, then controlled slow movement, occlusion and fast motion as separate experiments. Each new condition changes the assumptions. The attachment's staged integration boundary is retained: learned output is a proposal evaluated within the existing metric state, not a replacement world definition.

## 5. Evaluate a model without losing reproducibility
Record the exact repository revision, checkpoint hash, model family, preprocessing, precision, device, head selection, input order and image hashes. Preserve raw predictions separately from registered/refined outputs. An unknown checkpoint or unrecorded image crop makes later comparison unreliable even if the diagram looks familiar.

The included optional runner creates prediction arrays and provenance for the original VGGT API. It does not automatically align those results to metre ground truth. Registration and holdout measurement are explicit subsequent steps. The normal course notebooks do not invoke that runner.

## 6. Learning continues through evidence, not an expanding to-do list
Keep the original 00–12 core in sequence. Append 13–20 only when their prerequisites are understood. Use the progress log to distinguish practiced, independently demonstrated, retained and needing review. A demonstrated stage can later require review; this is not failure of the system but a more accurate description of learning.

The review intervals are a course policy, not a personalized scientifically optimal schedule. No timer runs in the background. The CLI prints due items when you call it. Record actual attempts and attach evidence files rather than writing future completion dates.

## 7. What “complete” can reasonably mean
Completion means all agreed outcomes have evidence: definitions, hand calculations, elementary proofs, algorithms, real-data interpretation, independent work and delayed recall. It does not mean every branch of mathematics or every deployment is mastered forever.

The actual book has not been read in full. Its supplied section titles remain an audit map. When you obtain the text, check its definitions, examples, arguments and exercises against this course and record any gaps. Do not infer full chapter coverage from a similar title.

## 8. Where to deepen next
For pure mathematics, continue with covering spaces, fuller surface classification, cohomology and more of algebraic topology. For TDA, study statistical inference, sampling guarantees and multiparameter persistence. For geometry, deepen differential geometry, bundle adjustment, robust estimation and observability. For systems, study synchronization, uncertainty-aware fusion and causal event evaluation.

Those are explicit next tracks with prerequisites. They are not hidden prerequisites that block finishing the agreed introductory course, and they are not claims that a few extra notebooks exhaust the fields.

## Independent conceptual exercises

1. Formulate a falsifiable spatial-reconstruction or TDA question.
2. Which evidence must be reserved from registration and parameter selection?
3. Why is the reference notebook not an independent capstone?
4. Name the required model and input provenance for a reproducible run.
5. What changes when moving from static reconstruction to live interaction detection?
6. What is still required to claim coverage of the actual book?

## Mastery gate

Defend an independent protocol and retain an honest list of external experiments and book-audit work still required.

Readings: U01, T01, V04. See the [source ledger](docs/SOURCES_V3.md) for checked links, evidence status and source differences.


---

Source: `physics/lessons/21.md`

# Stage 21 — Rates, equations, units and what data can identify

**Before this stage:** Stages 01, 10 and the rates primer. Review matrices and the chain rule; no prior mechanics is assumed.

**Evidence used:** Observed NIST copper measurements; manufactured cosine derivative checks. Temperature is not a time axis.

## The question we are answering

Before asking a neural network to learn physics, decide what the inputs, outputs and equations mean. A table with two numerical columns does not tell you whether one is time, whether a system is in equilibrium, or which quantities are unobserved. This stage connects your earlier data-provenance lessons to differential equations.

An independent variable is something with respect to which a function is described. In y(T), temperature T is an independent variable. In q(t), time t is the independent variable. The derivatives dy/dT and dq/dt have different interpretations and units. Sorting rows by temperature cannot convert a static material curve into a motion trajectory.

## Step 1 — derive a rate instead of naming one

For q(t)=cos(t), compute q'(t)=-sin(t). At t=0.7, approximate this using the centered difference [q(t+h)-q(t-h)]/(2h). Taylor expansion gives q(t+h)=q(t)+hq'(t)+h²q''(t)/2+h³q‴(t)/6+..., with alternating odd terms at t-h. Subtract and divide by 2h. The leading error is proportional to h² when the derivatives are smooth enough. Halving h should reduce that truncation term by about four, until floating-point or measurement noise dominates.

This is a conditional prediction, not a universal monotonic rule. With noisy measurements of fixed variance, dividing a noisy difference by a smaller h amplifies the noise. A smaller interval is not automatically a better derivative estimate.

## Step 2 — turn a second-order equation into a state

The oscillator equation is q''=-q in the dimensionless example. Introduce p=q'. Then z=(q,p) and f(z)=(p,-q). We can now say what an initial condition supplies: both position and velocity. At q=0, states (0,1) and (0,-1) have identical position but move in opposite directions. A model supplied only q cannot choose between them without additional information.

For physical units, m*q''=-k*q is different notation for a mass-spring model. The frequency squared is k/m. A trajectory may identify that ratio while failing to identify mass and stiffness separately. Multiplying both m and k by the same positive constant leaves q'' unchanged. This is structural non-identifiability, not a shortage of training steps.

## Step 3 — distinguish an equation residual from an answer error

The residual of a proposed function u for -u''=f is -u''-f. If f=0, every affine u=ax+b has zero interior residual. Without boundary information, zero residual does not select one solution. Even with boundaries, evaluating only a finite collocation set leaves untested locations. Uniform error bounds require assumptions and analysis beyond a low mean loss.

Use four labels in your notebook: observation error, residual error, reference-solution error and parameter error. They have different denominators and units. Never combine their squared values into one objective without stating scaling choices.

## Step 4 — inspect actual measurements

The bundled Hahn1 excerpt contains 56 observed pairs from NIST's 236-observation copper study [NIST]. Temperature is in kelvin. The response is the source's expansion coefficient scale; the file does not specify its multiplier. We therefore leave that response scale unchanged and do not invent a conversion.

Plot the observations, retain original source indices, and examine temperature differences between nearby sorted points. The curve is not a supplied time-dependent temperature field. It does not identify thermal diffusivity, heat flux, mass or a Hamiltonian. You can fit a material-response relationship and evaluate held-out response predictions under a declared protocol. That is already a legitimate task.

## Hand calculation and code connection

From the first two observations, calculate (1.547-0.591)/(34.82-24.41). The answer is about 0.09183 response-scale units per kelvin. Call it a two-point secant slope. It is not a measured time derivative, a universal material constant, or an exact derivative of the unknown response function.

Run the lab's centered differences on cos(t), then its empirical secant calculation. Explain why the first has an analytic derivative for comparison but the second does not. Inspect `classical.py` to see that finite input checks are explicit and no synthetic fallback substitutes for missing measurements.

## Go deeper without getting lost

Learn the distinction between local and global existence, conditioning, well-posedness and identifiability. For an ODE, local Lipschitz regularity in state is a standard sufficient condition for local uniqueness; smoothness does not promise existence at every time. Stage 22 supplies a blow-up example. For PDEs, existence, uniqueness and stability depend on the equation, domain and boundary/initial conditions. Avoid calling every residual-trained network a solver for a well-posed problem before these are specified.

**Stop condition:** you can tell another learner what each column represents, derive a finite difference, supply a non-identifiability example, and identify the missing information before fitting a physical model.

## Independent questions

**21.Q1.** Why is the first-column ordering not enough to define a time axis?

**21.Q2.** Derive the centered-difference leading order for a smooth function.

**21.Q3.** Which part of m and k can the unit mass-spring acceleration identify?

**21.Q4.** Give a zero-residual but wrong-answer example.

**21.Q5.** What is the NIST excerpt suitable for and unsuitable for?

**21.Q6.** What happens if observation noise stays fixed while difference spacing shrinks?

Attempt these before reading the [answer criteria](physics/solutions/21.md). Then complete the separate learner notebook. To pass, explain the assumptions as well as obtaining a number. An independent score of at least 85% is our course policy, not accreditation; correct all critical conceptual errors.

## Delayed recall

**21.R1.** What are state, residual and identifiability?

**21.R2.** When is halving h useful?

**21.R3.** What quantity is missing from the copper table for an ODE trajectory?

Return to [the stage index](stages/21/README.md) for code, outputs and follow-on work. Primary resource IDs refer to [the source registry](docs/v5/SOURCES.md).


---

Source: `physics/lessons/22.md`

# Stage 22 — Smooth flows, coordinate changes and invertible networks

**Before this stage:** Stage 13 and Stage 21; remember the difference between a function and its inverse.

**Evidence used:** Measured Iris feature pairs transformed by a chosen invertible map; the flow itself is a mathematical construction.

## Start with the same point in two descriptions

A chart maps an open manifold patch to an open coordinate set. If phi and psi describe the same region, psi composed with phi inverse converts one coordinate representation into the other. You do not move the underlying point merely by changing its coordinates. A smooth manifold uses compatible smooth transition maps; a diffeomorphism is a smooth invertible map with a smooth inverse.

The supplied chart post introduces this local idea. Here we add its domain assumptions and connect it to actual computations. Smooth inverse is stronger than continuous inverse: f(x)=x³ is a smooth bijection of the real line, but its inverse has an unbounded derivative at zero. It is a homeomorphism, not a diffeomorphism with the usual smooth structures.

## Vector fields generate motion

A vector field assigns a tangent direction and rate at each state. Solving z'=f(z) for time t defines a flow map phi_t wherever that solution exists. Local uniqueness gives a locally reversible description: evolving by t and then by -t returns to the starting state on the common domain. Smoothness gives a smooth local flow. These statements have domains; they are not permissions to evolve indefinitely.

Take x'=x². Separating variables gives -1/x=t+C. Enforcing x(0)=x0 yields phi_t(x0)=x0/(1-t*x0). For positive x0 the solution diverges at t=1/x0. The denominator must stay positive on the solution interval containing zero. Merely obtaining a finite algebraic value after the singularity does not mean the original trajectory crossed the blow-up safely.

The derivative with respect to x0 is 1/(1-t*x0)² on that domain. It is positive and nonzero, so the map is locally invertible there. Our implementation rejects times that cross the singularity. Test phi_-t(phi_t(x))=x on valid points, and test that invalid points fail rather than silently producing plausible numbers.

## A numerical update is a different map

An exact flow can be a diffeomorphism while a chosen discrete approximation fails to be one globally. The explicit Euler update for x'=x² is x+h*x². Its derivative 1+2hx vanishes at x=-1/(2h), so it is not a global diffeomorphism. This is an example of the continuous model/numerical method distinction from the uncertainty primer.

A projection can lose even more information. Sending every nonzero vector to the unit sphere by normalization maps different radii to the same point. It cannot have an inverse on the whole ambient space. Do not call it an invertible normalizing flow simply because it maps onto a manifold.

## Construct an invertible coupling yourself

Let F(x,y)=(x, exp(s(x))*y+b(x)), with s(x)=0.2*tanh(x) and b(x)=0.5*sin(x). The first coordinate is unchanged. Therefore the inverse first recovers x directly, then solves y=(y_new-b(x))*exp(-s(x)). Its Jacobian is triangular and has determinant exp(s(x)), which is strictly positive. The log absolute determinant is s(x).

This is the elementary mechanism behind affine coupling in Real NVP [NVP]. We do not train a density model here. We test an explicit transform whose inverse and Jacobian are known, then examine what applying it to observations actually means.

If Y=F(X), probability densities transform by p_Y(y)=p_X(F_inverse(y))*abs(det D F_inverse(y)). Equivalently, at y=F(x), log p_Y(y)=log p_X(x)-log abs(det DF(x)). Density and point coordinates are different objects. Forgetting the determinant generally fails to preserve total probability.

## Use a real table without inventing a physical process

Take the two sepal measurements in Iris, record their units, and standardize them for this exploration. Standardization parameters are computed on the displayed exploratory sample, so this is not a train/test predictive evaluation. Apply F and its inverse. Report maximum round-trip error and visualize the transformed coordinates.

The small round-trip error supports correctness of the implemented inverse on those inputs. It does not prove a biological dynamics model. Geometry changed: ordinary distances and densities may change, even though the transformation is invertible. Your earlier persistence lessons explain why a diagram based on Euclidean distances need not remain numerically identical after a general diffeomorphism.

## Depth ladder

First be able to invert the coupling by hand. Next calculate its Jacobian. Then derive the change-of-variables density formula by relating small volumes. Finally study complete vector fields, Lie derivatives and neural continuous normalizing flows as further reading. These advanced developments are not silently counted as implemented just because a two-dimensional coupling passes tests.

**Stop condition:** explain the differences among chart change, physical flow, numerical update, projection and probability-density transformation, with one domain-limited counterexample.

## Independent questions

**22.Q1.** Why is x³ not a diffeomorphism of the usual smooth real line?

**22.Q2.** For x0=2, can the flow of x′=x² be evaluated at t=1 along its original solution?

**22.Q3.** Write the inverse affine coupling.

**22.Q4.** Derive the log determinant of the coupling.

**22.Q5.** Does a good round trip on Iris establish a biological flow?

**22.Q6.** Does an invertible nonlinear transformation preserve a Euclidean persistence diagram exactly?

Attempt these before reading the [answer criteria](physics/solutions/22.md). Then complete the separate learner notebook. To pass, explain the assumptions as well as obtaining a number. An independent score of at least 85% is our course policy, not accreditation; correct all critical conceptual errors.

## Delayed recall

**22.R1.** What extra assumption turns local flow into all-time flow?

**22.R2.** Why does normalization not have an ambient inverse?

**22.R3.** What sign accompanies log determinant in the transformed density?

Return to [the stage index](stages/22/README.md) for code, outputs and follow-on work. Primary resource IDs refer to [the source registry](docs/v5/SOURCES.md).


---

Source: `physics/lessons/23.md`

# Stage 23 — Mechanics, Hamiltonian networks and Lagrangian networks

**Before this stage:** Stages 01, 13, 21 and the neural-network paragraph in Primer 07.

**Evidence used:** Manufactured oscillator derivative data for training; observed copper data used to examine what is and is not identifiable.

## Two ways to describe the same simple motion

For a particle with coordinate q and velocity v, kinetic energy is T=m*v²/2 and a spring potential is V=k*q²/2. A Lagrangian for this system is L=T-V. The action is the integral of L along a candidate path. Requiring the first variation of this action to vanish, with endpoint variations fixed at zero, gives d/dt(partial L/partial v)-partial L/partial q=0. This is the Euler–Lagrange equation for the stated unforced model.

For this L, partial L/partial v=m*v. Its time derivative is m*a. Also partial L/partial q=-k*q. Substitution gives m*a+k*q=0. You have recovered the familiar spring equation from a scalar function rather than directly guessing an acceleration function.

The canonical momentum is p=partial L/partial v. Here it equals m*v, not v unless m=1. If the mapping between v and p is invertible, define H=p*v-L after expressing v in terms of q,p. This Legendre transform gives H=p²/(2m)+k*q²/2. Hamilton's equations are q'=partial H/partial p and p'=-partial H/partial q. They reproduce the same mechanics under these regularity conditions.

## What the networks learn

An HNN parameterizes a scalar H_theta and constructs its vector field from derivatives rather than predicting each velocity component independently [HNN]. If H_theta is differentiable and autonomous and the exact continuous dynamics is z'=J*grad H_theta, then dH_theta/dt=(grad H_theta)^T J grad H_theta=0, because J is skew-symmetric. The statement concerns the learned scalar along its exact generated flow. It does not prove that scalar is the actual physical energy or that the numerical solver preserves it exactly.

An LNN parameterizes L_theta and constructs acceleration from Euler–Lagrange equations [LNN]. For one autonomous degree of freedom, let L_vv be the second derivative with respect to velocity and L_vq the mixed derivative. Expanding d/dt L_v gives L_vq*v+L_vv*a. Therefore a=(L_q-L_vq*v)/L_vv when L_vv is nonzero. For several degrees of freedom, a velocity-Hessian matrix must be solved against the corresponding vector. Singular cases require another formulation rather than dividing by zero.

## Learn the formula before training

Take L=v²-1.5*q². This represents m=2 and k=3. At q=2, velocity arbitrary, L_q=-6, L_vq=0 and L_vv=2. The acceleration is -3. Implement this with automatic differentiation and compare with your hand result. Then try L=q+v: the velocity Hessian is zero. The regular formula must report that its assumption failed.

Our trained L example deliberately fixes the kinetic term: L_theta(q,v)=v²/2-V_theta(q). Its acceleration is simply -V_theta'(q). This is a useful, inspectable restricted LNN, not a general unconstrained Lagrangian identification benchmark. The general one-coordinate Hessian formula is tested separately.

## Run the actual learning experiment

We draw independent phase-space training states from a declared box and derive exact unit-oscillator derivatives. A tanh network learns H; a second network learns V in the restricted L formulation. The notebook records seed, architecture, iteration budget and derivative errors at independent manufactured states. Training curves and predicted-versus-known derivatives are shown.

The analytic equation is also a baseline: since we generated the data from it, it has no parameter-learning task. There is no reason to expect a trained network to beat an exact oracle on that same noiseless manufactured problem. The learning result tests the implementation and representation, not scientific novelty.

## Gauge freedoms and missing observations

Adding a constant to H leaves its gradient unchanged. Derivative data cannot determine that constant. Adding a total time derivative to L leaves the Euler–Lagrange equations unchanged under the usual variational conditions. Non-uniqueness can remain even with excellent prediction. Measured q(t) without mass information also does not automatically supply canonical p(t).

Now examine the real copper table. It contains neither momentum nor velocity samples, neither trajectory timestamps nor applied forces. It cannot be passed off as measured HNN training data merely because it concerns a physical material. Use the source metadata to write a rejection reason for that proposed inference, while retaining the valid static-regression task for Stage 26.

## Where the conservative picture stops

For q'=p and p'=-q-gamma*p, the unit oscillator energy satisfies H'=-gamma*p². A model forced to keep this H constant would conflict with the intended damping. Basketball adds active muscles, drag, ground contact, ball deformation and impacts. Time-dependent forcing and contact changes require explicit treatment; they are not harmless noise around a universal energy-conservation rule.

**Stop condition:** derive both formulations for a mass-spring system, compute one Hessian-based acceleration, state the coordinate and regularity assumptions, and explain exactly which model was trained and on which data.

## Independent questions

**23.Q1.** With m=2 and v=3, what is p?

**23.Q2.** Derive H for the quadratic spring Lagrangian.

**23.Q3.** What condition allows the regular LNN acceleration formula?

**23.Q4.** Which constant cannot derivative supervision identify in H?

**23.Q5.** Why can conserved learned H still describe wrong dynamics?

**23.Q6.** What is deliberately restricted in the trained LNN?

Attempt these before reading the [answer criteria](physics/solutions/23.md). Then complete the separate learner notebook. To pass, explain the assumptions as well as obtaining a number. An independent score of at least 85% is our course policy, not accreditation; correct all critical conceptual errors.

## Delayed recall

**23.R1.** Explain canonical momentum without saying it is always velocity.

**23.R2.** What is conserved by the exact autonomous HNN flow?

**23.R3.** What is the damping energy balance?

Return to [the stage index](stages/23/README.md) for code, outputs and follow-on work. Primary resource IDs refer to [the source registry](docs/v5/SOURCES.md).


---

Source: `physics/lessons/24.md`

# Stage 24 — Symplectic integration, energy, phase and long rollouts

**Before this stage:** Stages 14 and 23; matrix multiplication and determinant checks.

**Evidence used:** Manufactured oscillator trajectories with exact reference; a measured sunspot delay cloud used as a negative control against invented energy claims.

## Why a correct differential equation still needs a numerical method

A computer usually advances a state by finite steps. The resulting map is not identical to the exact continuous flow. A method can preserve one mathematical structure while introducing error in another quantity. This stage makes that distinction visible rather than reducing it to a warning sentence.

For z=(q,p), define J=[[0,1],[-1,0]]. A differentiable update Phi is symplectic if D(Phi)^T J D(Phi)=J. For a linear update z_new=M*z, this becomes M^T J M=J. Symplecticity is not defined as "energy remains unchanged." It concerns a bilinear phase-space structure. In two dimensions it is equivalent to determinant one; in higher even dimensions determinant one alone is insufficient.

## What the exact continuous equations preserve

For a time-independent, twice continuously differentiable Hamiltonian H on a canonical phase-space domain, z_dot=J grad(H), with constant skew-symmetric J. Along an exact solution,

dH/dt=grad(H)^T J grad(H)=0,

because a real scalar equals its transpose and J^T=-J. If H depends explicitly on time, the derivative instead includes partial H/partial t. Dissipation or external forces also change the model.

The vector field has divergence trace(J Hess(H))=0: a skew-symmetric matrix paired with a symmetric Hessian has zero trace. With the regularity and existence needed for its flow, this gives preservation of canonical phase-space volume (Liouville's theorem). It does not make every atmospheric or viscous-fluid model a finite-dimensional canonical conservative system. Physical-space incompressibility, symplecticity, phase volume, and constant energy are related only under stated assumptions; they are not interchangeable definitions.

A numerical step is a different map. The calculation below tests the source post's discrete claim without disputing the exact continuous argument.

## An exact counterexample by hand

Use H=(q²+p²)/2 and a kick-drift symplectic Euler step:

p_new=p-h*q, then q_new=q+h*p_new.

Its matrix is M=[[1-h²,h],[-h,1]]. Multiply M^T J M to recover J. At (q,p)=(1,0) with h=0.2, the new state is (0.96,-0.2). The old H is 0.5; the new H is (0.9216+0.04)/2=0.4808. This is a valid symplectic update with an energy change of -0.0192.

This single example disproves the source post's universal discrete exact-energy implication. It does not show that symplectic integrators are poor methods. For many suitable Hamiltonian problems with appropriate steps, their long-time behavior is much better than a naive alternative. The relevant claim must mention the method, problem, step and time horizon.

## Compare five maps

Explicit Euler uses q_new=q+h*p and p_new=p-h*q. Its determinant is 1+h². For the unit oscillator, every step multiplies squared radius by 1+h², so energy grows geometrically.

Symplectic Euler uses the updated momentum for position. Its energy typically oscillates rather than staying exactly fixed in this stable linear example.

Velocity Verlet performs a half momentum kick, a full position drift and a second half kick. It is symmetric and symplectic for a separable Hamiltonian under the usual composition, but not generally exactly energy preserving. The unit-oscillator stable range is |h|<2; a structure-preserving formula does not make every step size safe.

Implicit midpoint for this linear oscillator has the Cayley matrix (I-hJ/2)^(-1)(I+hJ/2). It preserves this quadratic energy, yet its rotation angle per step is 2*atan(h/2), not h. Exact energy therefore does not imply exact phase. General nonlinear Hamiltonians do not inherit this quadratic special case automatically.

The exact oscillator map rotates by h. It supplies a controlled reference, not a numerical method for arbitrary unknown dynamics.

## Tests should measure more than one error

For each method, record symplectic defect, determinant, energy error and state error against the exact flow at matched times. Plot energy against time. Repeat with smaller h while holding physical horizon fixed. Comparing 100 steps at h=0.1 with 100 steps at h=0.01 changes both accuracy and horizon; it is not a clean convergence experiment.

In four dimensions, diag(2,0.5,1,1) has determinant one in the ordering (q1,q2,p1,p2), but does not preserve J. This prevents an attractive shortcut—checking only volume—from becoming a false symplectic certificate.

## The data interpretation check

Make a past-only delay cloud from measured annual sunspot activity: (s(t),s(t-1)). It is a representation of a real time series, not automatically a canonical (q,p) system. Its radius squared is not justified as solar energy. Plotting something that resembles a loop cannot supply canonical coordinates, a Hamiltonian or an energy calibration.

Topology still has a role. You can compare persistence of sampled exact and distorted oscillator curves, but a loop count cannot certify correct phase, conserved energy, metric units or long-horizon prediction. A topologically circular trajectory can rotate at the wrong speed. Keep descriptive topology and physical validation as separate reports.

## Deeper theory

Backward-error analysis studies a numerical method by relating it to a modified differential equation, under specific smoothness, step and time assumptions. Learn its purpose before reading a theorem as a universal promise. Resonances, unstable step sizes, finite precision, non-smooth contact and time dependence can change the situation. Hardware precision is part of the experiment, not an afterthought.

**Stop condition:** reproduce the 0.4808 counterexample, distinguish energy from phase and symplecticity, and state why the real delay cloud does not by itself support a Hamiltonian interpretation.

## Independent questions

**24.Q1.** Compute one symplectic Euler step from (1,0), h=0.2.

**24.Q2.** What exactly does M^T J M=J establish?

**24.Q3.** Why is determinant one insufficient in four dimensions?

**24.Q4.** Can exact energy coexist with phase error?

**24.Q5.** Why hold the horizon fixed when testing convergence?

**24.Q6.** Does a sunspot delay-loop radius represent energy?

Attempt these before reading the [answer criteria](physics/solutions/24.md). Then complete the separate learner notebook. To pass, explain the assumptions as well as obtaining a number. An independent score of at least 85% is our course policy, not accreditation; correct all critical conceptual errors.

## Delayed recall

**24.R1.** Name three independent rollout diagnostics.

**24.R2.** Does symplectic mean every step size is stable?

**24.R3.** What is the exact continuous Hamiltonian conservation argument?

Return to [the stage index](stages/24/README.md) for code, outputs and follow-on work. Primary resource IDs refer to [the source registry](docs/v5/SOURCES.md).


---

Source: `physics/lessons/25.md`

# Stage 25 — Constraints, projections, retractions and rank failure

**Before this stage:** Stages 13, 14, 23 and 24; review kernels, rank and tangent spaces.

**Evidence used:** Measured Iris vectors subjected to an explicitly chosen unit-sphere normalization; exact and nonlinear constraint counterexamples.

## What a constraint means

A constraint C(z)=0 defines allowed states. For a unit circle, C(x,y)=x²+y²-1. At a point where its derivative has full rank, tangent directions v satisfy DC(z)*v=0. The Jacobian DC is a local linear description of how constraints change. It is not the canonical skew matrix from Hamiltonian mechanics; we write A=DC to avoid the source post's overloaded J notation.

A tentative numerical update z_tilde may violate the constraint. One way to correct it is to linearize C(z_tilde+delta) approximately as C(z_tilde)+A*delta. Setting this approximation to zero and choosing the smallest Euclidean correction gives delta=-A^T(AA^T)^(-1)C(z_tilde) when A has full row rank. In code, solve the small system rather than explicitly form the inverse.

## Derive where exactness comes from

For an affine constraint C(z)=Az-b, the linearization is exact. Applying the correction gives A*z_new-b=C-A*A^T*(AA^T)^(-1)*C=0, apart from finite-precision effects. This supports a precise affine statement.

For a nonlinear constraint, omitted higher-order terms remain. Let z_tilde=(2,0). Then C=3 and A=[4,0]. The correction is (-0.75,0), giving z_new=(1.25,0). Its residual is 1.25²-1=0.5625, not zero. The same displayed formula that is exact in the affine case is only a local correction here.

Repeat the correction until the chosen residual tolerance is met. Record every residual and the iteration count. Failure to converge is a result, not a reason to label the output feasible. At the origin, the sphere Jacobian is zero, so the full-row-rank assumption fails. Our routine reports that failure.

## Projection and retraction are different jobs

For a nonzero point in ordinary Euclidean space, radial normalization gives the nearest unit-sphere point. The origin has no unique nearest direction. The map discards radius and is therefore not globally invertible in the ambient space.

A sphere retraction starts with a point q on the sphere and a tangent vector v satisfying q dot v=0, then maps back by R_q(v)=(q+v)/||q+v||. It agrees with a tangent step to first order and stays on the sphere. It is not generally the exact sphere geodesic at finite v. An exponential map would follow the geodesic using the manifold metric; the inexpensive normalization formula approximates that role locally.

A generic nearest-point projection is also not automatically symplectic. It may collapse dimensions or change momenta inconsistently. Constraint-aware mechanical integrators such as SHAKE/RATTLE require the actual position and velocity constraints and a derived update. We link explicit-constraint HNN/LNN work [CONSTRAINED] for further study, but do not mislabel our local Newton correction as a full mechanical integrator.

## Feasibility is not all the physics

A trajectory can remain on a circle while traversing it at the wrong speed or gaining the wrong energy. In a constrained mechanical system, valid initial velocity, constraint forces and momentum consistency matter. In camera estimation, maintaining R^T R=I is necessary for a rotation matrix, but says nothing by itself about whether that rotation matches measured image correspondences.

If constraints are incompatible, no algorithm can satisfy all of them. If their Jacobian is nearly singular, a small residual can demand a very large correction. Log the rank, conditioning, step norm and convergence criterion. Do not hide such issues behind an unconditional matrix pseudo-inverse; a least-squares correction can be useful but answers a different question that must be named.

## Examine real observations under a chosen geometric constraint

Take centered, standardized Iris measurements and normalize each nonzero feature vector onto a unit sphere. Plot or tabulate original norms, correction magnitudes and final norm residuals. A tiny final residual verifies the normalization operation, not a law that flower measurements should have unit magnitude.

The normalization removes amplitude information. Two feature vectors pointing in the same direction but having different size become identical. Relate that to previous lessons on information loss, distances and topology. Whether normalization is scientifically useful depends on the question; it is not automatically a better representation.

## Accuracy and hardware

The claim that a closed formula removes every nonlinear solve should now have a visible counterexample. Matrix operations can be fast, but nonlinear constraints can require repeated evaluations and rank-aware solves. Low precision may be acceptable for one tolerance and unacceptable for another. Measure the actual residual and timing before invoking hardware labels such as Tensor Cores or petascale throughput.

**Stop condition:** derive the full-rank affine correction, show its nonlinear failure in one step, distinguish projection/retraction/geodesic, and state which physical quantities the operation does not certify.

## Independent questions

**25.Q1.** For z=(2,0), calculate one unit-circle correction and the remaining residual.

**25.Q2.** When is the linear correction exact?

**25.Q3.** Why reject the sphere origin?

**25.Q4.** What is required of v in the sphere retraction?

**25.Q5.** Does unit norm of the normalized Iris data verify a biological law?

**25.Q6.** Why is a generic projection not a symplectic integrator?

Attempt these before reading the [answer criteria](physics/solutions/25.md). Then complete the separate learner notebook. To pass, explain the assumptions as well as obtaining a number. An independent score of at least 85% is our course policy, not accreditation; correct all critical conceptual errors.

## Delayed recall

**25.R1.** What symbol do we use for the constraint Jacobian?

**25.R2.** Name three projection failure checks.

**25.R3.** Does feasibility imply correct motion?

Return to [the stage index](stages/25/README.md) for code, outputs and follow-on work. Primary resource IDs refer to [the source registry](docs/v5/SOURCES.md).


---

Source: `physics/lessons/26.md`

# Stage 26 — Physics-informed learning and inverse problems

**Before this stage:** Stages 21–25; derivatives, matrix solves, loss and training/evaluation splits.

**Evidence used:** Actual residual-trained network on a manufactured Poisson problem; separate measured NIST response-regression exercise.

## Start with a problem small enough to solve another way

On 0≤x≤1, consider -u″(x)=pi²*sin(pi*x), with u(0)=u(1)=0. Differentiate sin(pi*x) twice to verify the exact solution. This manufactured problem provides an independent target for testing. It is not a measured temperature field or a discovery that a neural network made about nature.

A conventional finite-difference method samples the unknown solution at grid points. Replacing u″ by (u_left-2u_center+u_right)/h² gives a tridiagonal linear system. The boundary values contribute known terms. Solve it and compare with the analytic solution. This baseline is inexpensive and appropriate; do not omit it merely because the course is about machine learning.

## What a PINN changes

A physics-informed neural network represents u by u_theta(x), differentiates it, and adjusts theta to reduce equation and observation violations [PINN]. A basic objective might be the mean square of -u_theta″-f at interior collocation points plus penalties for endpoint mismatch. A collocation point is a location where we ask the network to satisfy the equation; it is not automatically an observed label.

Automatic differentiation computes derivatives of the network function through its actual operations. When training through a derivative, the program must retain a derivative computation graph. In our PyTorch code this is why `create_graph=True` appears. A missing graph can break learning through second derivatives; a correct graph still cannot fix an incorrectly signed residual.

## Soft and hard constraints

A soft endpoint penalty discourages nonzero boundary values without making them impossible. A hard parameterization can enforce these particular boundary values: u_theta(x)=x*(1-x)*N_theta(x). It is zero at both endpoints for every finite network output. The interior equation is still only optimized approximately. The boundary factor also changes the optimization landscape, so hard enforcement is not automatically faster or more accurate on every problem.

Different boundary types require different constructions. Dirichlet specifies values; Neumann specifies normal derivatives; Robin combines them. Initial conditions specify a field at a starting time. A nonhomogeneous boundary needs an ansatz that includes an appropriate lifting term rather than blindly multiplying by x*(1-x).

## A one-variable proof that a finite penalty need not be exact

Suppose data favor x=1 but the desired constraint is x=0. Minimize L(x)=(x-1)^2+lambda*x^2 with a finite positive lambda. Setting its derivative to zero gives 2(x-1)+2*lambda*x=0, hence x=1/(1+lambda). For lambda=9 the optimum is x=0.1, not zero. The optimum is unique because the second derivative is 2(1+lambda)>0. Increasing lambda reduces the violation in this example; it does not make the constraint exact at any finite lambda.

This is a counterexample to a universal guarantee, not a proof that all penalty methods are unsuitable. The hard endpoint construction above is exact for the two stated boundary values, while its PDE residual remains an optimization problem. Report each property separately.

## Inspect the real training program

The supplied lab trains a small tanh network in double precision using the hard-zero ansatz. It reports the iteration budget, seed, interior collocation count, evaluation grid, relative solution error, residual error and endpoint error. Compare its predicted curve with the analytic solution and finite-difference result. The source module is short enough to inspect in full.

Do not confuse the residual and error curves. A small residual at fixed points does not certify a maximum error between them. The fine evaluation grid is a stronger diagnostic, not a theorem. A proper stability/error estimate depends on the operator, boundary conditions, norm and approximation error. The failure-mode reading [FAIL] motivates taking these distinctions seriously.

## Inverse problems need information

A forward problem gives a coefficient, equation and conditions, then predicts u. An inverse problem estimates unknown coefficients or source terms from observations. If -nu*u″=f and both nu and f are unknown, there can be a scaling ambiguity. Additional observations or assumptions are needed. A low optimizer loss does not remove this ambiguity.

Nondimensionalization makes variable and residual scales explicit. If x=L*x_hat and u=U*u_hat, then u″=(U/L²)*u_hat″. Forgetting that factor changes the equation. A chart transformation on a manifold can require still more than a scale factor: the metric, volume element and coordinate Jacobian enter geometric differential operators. For example, the Laplace–Beltrami operator involves the inverse metric and its determinant. General manifold PDE implementation is a further project, not something supplied by an ordinary flat-space `u_xx` call.

## Use measured data for the question it actually supports

Return to NIST's observed expansion response versus temperature [NIST]. Fit two predeclared simple regression candidates on a fixed training subset, select using validation points and evaluate once on test points. Store source indices, predictions and the response scale. This tests a static empirical relationship, not the Poisson network.

The 56-row excerpt is not the complete 236-row rational-regression benchmark. Do not compare its residual sum of squares with the official full-data certified value. Replicate identifiers and uncertainty metadata are unavailable in this excerpt, so a random row split does not establish a new independent material-study validation. The notebook describes its split as an educational within-excerpt comparison. Once published here, its test outcomes are exposed.

## What to do when a PINN fails

First verify signs, derivatives, units and conditions. Test the residual on the analytic answer. Then inspect collocation coverage, boundary errors, optimizer gradients and conditioning. Change one factor at a time, retaining the conventional baseline. Architecture changes come after diagnosing the failure, not before. Stage 27 examines a specific cause: competing objective gradients.

**Stop condition:** derive the residual, explain why the endpoint ansatz works, run the conventional baseline, and distinguish measured regression evidence from a manufactured PDE experiment.

## Independent questions

**26.Q1.** Verify the manufactured Poisson solution.

**26.Q2.** Which condition does x(1-x)N(x) enforce exactly?

**26.Q3.** Why is create_graph needed for residual training through derivatives?

**26.Q4.** What information can a low training residual fail to provide?

**26.Q5.** If x=L*x_hat and u=U*u_hat, how does u″ scale?

**26.Q6.** Why not compare the NIST excerpt SSE with the published certified full-data SSE?

Attempt these before reading the [answer criteria](physics/solutions/26.md). Then complete the separate learner notebook. To pass, explain the assumptions as well as obtaining a number. An independent score of at least 85% is our course policy, not accreditation; correct all critical conceptual errors.

## Delayed recall

**26.R1.** What is a collocation point?

**26.R2.** What baseline should precede a neural PDE claim here?

**26.R3.** Does a hard boundary ansatz prove a correct PDE solution?

Return to [the stage index](stages/26/README.md) for code, outputs and follow-on work. Primary resource IDs refer to [the source registry](docs/v5/SOURCES.md).


---

Source: `physics/lessons/27.md`

# Stage 27 — Conflicting gradients, interfaces, separability and PIKANs

**Before this stage:** Stages 21 and 26; inner products, gradients and simple linear regression.

**Evidence used:** Exact gradient examples and manufactured subdomain seams; opposing objectives derived from observed NIST regression groups.

## Why adding losses can create competition

Let theta be shared model parameters. A residual loss, boundary loss and interface loss each has its own gradient g_i. If we update theta_new=theta-eta*d, a first-order Taylor expansion gives L_i(theta_new) approximately L_i(theta)-eta*g_i dot d. Positive g_i dot d therefore predicts local decrease for sufficiently small steps under smoothness. It is not a finite-step guarantee for arbitrary eta.

A negative dot product between two objective gradients signals local conflict: a descent direction for one can increase the other. Rescaling losses changes gradient magnitudes but does not necessarily resolve their opposing directions. This is the issue emphasized by the attached PINN/PIKAN post.

## Work two vectors by hand

Let g1=(1,0) and g2=(-1,1). Their dot product is -1. Project g1 away from its conflicting component along g2: g1_tilde=g1-(g1 dot g2)/(g2 dot g2)*g2=(0.5,0.5). Project g2 against the original g1: g2_tilde=(0,1). PCGrad sums the projected directions in our implementation [PCGRAD]. Here the resulting vector is (0.5,1.5), with positive inner products against both originals.

Norm-PCGrad, as Algorithm 1 in the September 2026 preprint specifies, normalizes the projected rows before aggregation [NORM]. That gives (1/sqrt(2),1+1/sqrt(2)) for this example. Normalizing the original inputs and then applying a different operation is not the same declared algorithm. Zero projected rows need an explicit rule; ours contribute zero.

## ConFIG and the edge cases hidden by a name

ConFIG's equal-alignment construction can be examined through a matrix U whose rows are normalized nonzero gradients. Solving U*v=ones asks for a vector with equal positive alignment with these normalized rows [CONFIG]. Our educational implementation checks the solve residual and reports whether that particular system is compatible. It also reports zero rows and every original dot product.

If g2=-g1 and g1 is nonzero, strict common descent is impossible: g1 dot d>0 and -g1 dot d>0 cannot both hold. A zero objective gradient also cannot have strictly positive alignment with any direction. A least-squares solution to an incompatible system is not an exact guarantee. Furthermore, incompatibility of equal alignment does not itself prove that no other common descent direction exists; those are different questions.

With more than two losses, sequential projections depend on order and can reintroduce conflicts with earlier directions. The source paper's two-gradient analysis must not be silently promoted into an unconditional statement for all multi-gradient inputs. The notebook exposes dot products and order seeds rather than declaring every output conflict-free by construction.

## Use actual regression gradients

Split the NIST excerpt into lower- and higher-temperature groups and fit a shared linear model. At the optimum of their equally weighted total squared error, the two nonzero group gradients can oppose each other. Compute them analytically as 2*X_transpose*(X*theta-y)/n. Compare this with the overall normal-equation condition.

This is a real-data demonstration of objective competition, not a PINN benchmark. There may simply be no direction that improves both groups at that compromise point. A more appropriate representation, a different question, or additional evidence can matter more than gradient surgery. Do not present an optimizer change as having solved an impossible set of local demands.

## Domain decomposition introduces additional conditions

Suppose one network describes x in [0,0.5] and another describes [0.5,1]. Their interior PDE residuals can both be zero while the assembled field is discontinuous. For -u″=pi² sin(pi*x), choose u_left=sin(pi*x), and u_right=sin(pi*x)+0.2*(1-x). Both satisfy the same interior residual and the external zero endpoints, but their values differ by 0.1 at the interface and their slopes differ by -0.2.

For the constant-coefficient diffusion/Poisson case without an interface source, appropriate solution and flux matching matter. More general PDEs, materials and weak formulations need their own interface laws. The lab illustrates the issue; it does not train a complete XPINN system. Gradient changes cannot repair incorrectly specified interface physics.

## SPINN and PIKAN: learn what changes

SPINN uses per-axis representations and separability to reduce repeated network evaluations [SPINN]. A rank-r two-dimensional field can be written sum_j a_j(x)*b_j(y). Computing the factor values costs roughly r*(nx+ny) outputs, but explicitly constructing a dense nx-by-ny field still requires nx*ny entries. Do not translate an axis-evaluation saving into a blanket linear cost for every stage of a full solver.

KAN architectures parameterize learned univariate edge functions rather than using only fixed node activations [KAN]. PIKAN refers to applying a physics-informed objective to such architectures. The theorem motivating a representation is not a guarantee that training succeeds. Our extension explains these distinctions and runs a separable factorization example. It does not claim trained SPINN/PIKAN benchmark reproduction or measured hardware speedups.

**Stop condition:** implement the declared vector operations, handle exact opposition, derive the interface counterexample, and separate architecture, objective and optimizer choices.

## Paper revisions and the next optimizer question

The final source check also examined Algorithm 1 in v2 (16 September 2026), which retains normalization of the projected gradients. Its additional curvature-aware optimizer comparisons, including SSBroyden, are deeper reading rather than a shipped benchmark. Gradient projection changes a proposed direction; a quasi-Newton method also approximates curvature from successive changes. Neither mechanism fixes a missing boundary condition or makes incompatible objectives compatible. Record the paper revision when reproducing its results.

## Independent questions

**27.Q1.** What sign of g_i dot d predicts local improvement under theta-eta*d?

**27.Q2.** What is normalized in the supplied Norm-PCGrad implementation?

**27.Q3.** Prove that exact opposing nonzero gradients have no strict common descent.

**27.Q4.** Why inspect sequential multi-gradient outputs rather than trust a label?

**27.Q5.** Calculate the interface jump for the two Poisson functions.

**27.Q6.** Does a separable network make a dense nx-by-ny output linear in grid length?

Attempt these before reading the [answer criteria](physics/solutions/27.md). Then complete the separate learner notebook. To pass, explain the assumptions as well as obtaining a number. An independent score of at least 85% is our course policy, not accreditation; correct all critical conceptual errors.

## Delayed recall

**27.R1.** Distinguish architecture, loss and optimizer.

**27.R2.** Does least-squares ConFIG compatibility decide every possible common-descent question?

**27.R3.** Which published experiments did we reproduce?

Return to [the stage index](stages/27/README.md) for code, outputs and follow-on work. Primary resource IDs refer to [the source registry](docs/v5/SOURCES.md).


---

Source: `physics/lessons/28.md`

# Stage 28 — Functions to functions: DeepONet, Fourier operators and baselines

**Before this stage:** Stages 07, 11, 16, 21 and 26; review vectors, Fourier modes and validation splits.

**Evidence used:** Manufactured periodic heat-function family for actual training; a measured digit row used as an input to a constructed smoothing operator.

## A function, a field and an operator

A scalar function might take x and return u(x). An operator takes a whole function as input and returns another function. For a heat equation, the input can be an initial temperature field and the output the field at a later time. On a computer both are sampled arrays, but the intended mapping is between fields rather than between unrelated rows.

We use the periodic heat equation u_t=nu*u_xx on a unit interval, at a fixed positive nu and final time. Periodic means the endpoints connect; it is not the same as insulating or zero-temperature boundaries. This is a deliberately small family whose correct evolution is known in Fourier coordinates.

## Derive the reference before building a network

Write the initial field as a sum of Fourier modes. For a mode exp(i*2*pi*k*x), taking two spatial derivatives multiplies by -(2*pi*k)². Its amplitude therefore evolves as exp(-nu*(2*pi*k)²*t). The zero-frequency mode stays unchanged, preserving the spatial mean. Higher-frequency modes decay faster. This also explains smoothing.

The implemented `heat_step` applies these factors to the discrete Fourier coefficients and inverts the transform. It is an exact evolution for the represented band-limited periodic modes up to numerical precision, not a learned FNO. It is the strongest baseline for data generated by this same known operator.

## DeepONet: branch information and a coordinate basis

Our small DeepONet takes samples of the input function at fixed sensor positions into a branch network. A trunk network takes an output coordinate. Their feature vectors are combined by an inner product and a bias [DEEPONET]. Intuitively, the branch selects coefficients while the trunk supplies coordinate-dependent basis functions.

This representation can express many function-to-function mappings. A universal approximation result does not mean an arbitrary finite network, sensor set, optimizer and training set will recover the operator. If two distinct input functions agree at every sensor, the branch cannot distinguish them from those measurements alone. Sensor coverage and frequency content matter.

## FNO: a learned operator in Fourier coordinates

A Fourier neural operator layer transforms features to frequency space, mixes retained modes using learned weights, transforms back, and combines with a local learned map and a nonlinearity [FNO]. Our TinyFNO uses two such layers in a one-dimensional periodic setting. Its weights are actually optimized in the lab.

Contrast this with the fixed heat multiplier. The FNO is trying to approximate a known mapping from examples; the reference solver is given the mapping analytically. Calling every FFT-based procedure an FNO would erase the distinction between a learned operator and a numerical transform.

Parameter counts involving complex weights are reported as complex tensor elements in this implementation. Each complex scalar represents two real degrees of freedom. Use an explicitly matched convention before comparing model sizes across systems.

## Split by the unit of generalization

We generate 160 independently sampled input functions from a fixed low-frequency family. The split is 96 whole functions for training, 32 for validation and 32 for test. Spatial points from one function do not straddle those roles. The time, diffusivity, grid and family are fixed before training. Validation selects saved checkpoints; test data is evaluated after that selection.

Report model error, identity-baseline error, analytic-reference error and the configuration. A favorable result is specific to this family and protocol. It does not prove climate prediction, different boundary conditions, different parameters, grid independence or unseen-frequency generalization. Those are additional tests, not automatic properties of the architecture name.

## Use a measured image without inventing thermal observations

Take a row from a real handwritten-digit image and apply the periodic heat operator to that pixel-intensity signal. Compare its input and smoothed output, and check the discrete mean. The starting observations are real; the later smoothed signal is generated. This is a construction for learning operators, not a camera measurement of actual heat flow through ink.

Discuss what the periodic boundary assumption means at the row ends. A dark-to-bright jump across that artificial wrap can affect the result. In image processing, the chosen adjacency and boundary treatment are part of the model. Your previous topology and image-connectivity lessons are directly relevant.

## A reliable deeper route

First derive the Fourier multiplier for a single sine wave. Next implement branch/trunk combination and one spectral layer. Then test a changed grid, boundary law, diffusivity, function family or noise process one at a time. Rebuild independent function-level splits for a new evaluation. For operator learning on variable geometries, coordinate maps and measures must be considered rather than feeding arbitrary domains into a fixed periodic transform.

**Stop condition:** distinguish learned operators from exact solvers, derive one mode's decay, explain the train/validation/test unit, and state which form of generalization was not evaluated.

## Independent questions

**28.Q1.** How does a function-to-function task differ from scalar regression?

**28.Q2.** What happens to the zero Fourier mode in periodic heat evolution?

**28.Q3.** What are the branch and trunk roles?

**28.Q4.** Why is the heat FFT reference not an FNO?

**28.Q5.** Why split whole input functions?

**28.Q6.** Does the real digit smoothing example validate physical heat diffusion?

Attempt these before reading the [answer criteria](physics/solutions/28.md). Then complete the separate learner notebook. To pass, explain the assumptions as well as obtaining a number. An independent score of at least 85% is our course policy, not accreditation; correct all critical conceptual errors.

## Delayed recall

**28.R1.** What defines a new operator task here?

**28.R2.** What exactly did our checkpoint selection use?

**28.R3.** Why retain the analytic baseline?

Return to [the stage index](stages/28/README.md) for code, outputs and follow-on work. Primary resource IDs refer to [the source registry](docs/v5/SOURCES.md).


---

Source: `physics/lessons/29.md`

# Stage 29 — Differentiable simulation, graph physics and attention constraints

**Before this stage:** Stages 16, 18, 21–28; derivatives of composed functions and causal timing.

**Evidence used:** Differentiable manufactured oscillator simulation; a graph built from an observed digit image; explicit attention and force counterexamples.

## Differentiate the program you actually ran

A simulation combines many updates. If each is differentiable, the chain rule can propagate a sensitivity from a final loss back to a parameter. For a simple decay z'=-a*z with z(0)=1, the exact final value at t=1 is exp(-a), and its derivative with respect to a is -exp(-a). Implement fixed-step Runge–Kutta and compare automatic differentiation of the discrete program with that exact sensitivity.

This is differentiable physics in a small controlled setting. The gradient is the derivative of the discretized computation. It is not automatically the derivative of the exact continuum solution, although a consistent convergent method can approximate it under suitable conditions. Step-size comparisons help reveal numerical sensitivity errors.

A Neural ODE replaces a fixed right-hand side with a parameterized learned function [NODE]. This differs from taking an arbitrary finite-layer network and calling it an exact physical flow. Adjoint sensitivity methods and direct backpropagation have different numerical and memory tradeoffs. Our implementation uses direct differentiation through RK4 steps; no continuous-adjoint or adaptive-solver implementation is claimed.

## Learn one parameter, then challenge the result

The worked simulation estimates a damping coefficient from a manufactured trajectory while keeping the other oscillator assumptions fixed. The parameterization keeps the damping positive. The notebook records the known generating value, recovered value, loss and data origin. This tests an inverse-simulation path; it is not a calibrated model of an athlete.

Consider failure cases: incorrect mass, missing force, noisy position-only observations, long chaotic rollouts, discontinuous contact, and adaptive events. A mathematically available gradient can be ill-conditioned or answer the wrong question. Derivatives through a smooth relaxation of impact need not equal the sensitivity of an actual hard-contact process. Finite-difference checks test a specified discretized program, not an entire scientific claim.

## Graphs make local interactions explicit

A graph has nodes and edges. Nodes can hold positions, velocities or scalar fields. Edges define which pairs interact. A learned graph simulator [GNS] can parameterize messages between nodes, but not every message-passing architecture automatically conserves momentum or respects rotation.

Construct a simple pair law F_ij=k_ij*(x_j-x_i). Add F_ij to node i and its negative to node j, listing each undirected pair once. Summing over all nodes cancels every internal pair, giving zero net internal force. Under a common rotation R, the coordinate difference rotates, so the output force rotates as well when k is a scalar invariant. These properties follow from the chosen algebra, not from the word "graph."

Unequal masses still require acceleration F_i/m_i. External forces and boundary exchanges belong in the balance. Conservation of total internal force does not prove correct potential energy, time integration, contact mechanics or measured trajectories.

## Build a graph from real pixels

Treat each pixel in a real digit image as a node containing a scalar intensity. Connect horizontal and vertical neighbors. Equal-and-opposite edge exchanges yield a graph-diffusion update. Check the sum of the updates and the resulting intensity sum. At a suitably small explicit step the operation smooths the field; step-size restrictions matter for positivity and stability.

This is a constructed operation on measured pixels, not a physical force measurement. It connects topology's adjacency choices to dynamics: changing the graph changes what counts as a local interaction. The total-sum identity remains algebraic, while usefulness for classification or image reconstruction requires independent evaluation.

## Attention does not automatically conserve mass

A standard row-stochastic attention matrix has rows summing to one. Consequently it preserves a constant input vector. Preserving the sum of an arbitrary vector requires columns summing to one as well. For A=[[1,0],[1,0]], rows sum to one, but applying A to (1,0) gives (1,1), doubling the sum. This limiting attention example is enough to refute a row-sum-only conservation claim; finite softmax examples can show the same issue approximately.

A mean-correction step can restore a chosen total, but it may change other properties such as positivity or locality. If mass conservation is a requirement, design and test it explicitly. A physics-informed transformer such as PINNsFormer [PINNSFORMER] is a specific architecture/objective, not proof that every transformer obeys all physical laws. We teach that paper's motivation and prerequisites; its benchmark training is not reproduced here.

## Measure performance at the right boundary

Time data conversion, device movement, derivative construction, forward evaluation, backward evaluation, constraint solves and output use separately. Report batch size, precision, hardware, error tolerances and synchronization. Throughput, p95 latency, age of information and peak memory are different quantities. This extends Stage 18's engineering lessons without claiming Tensor Core results from CPU experiments.

**Stop condition:** check a discrete gradient, derive pairwise cancellation, provide the attention counterexample, and distinguish a mathematical guarantee from a trained or deployed system claim.

## Independent questions

**29.Q1.** What derivative does backpropagation through RK4 compute?

**29.Q2.** Why is positive damping not the same as a correct physical model?

**29.Q3.** Derive zero net internal force for the pair update.

**29.Q4.** Does zero total force imply correct acceleration for unequal masses?

**29.Q5.** What additional attention condition preserves arbitrary global sums?

**29.Q6.** What is not implemented under the physics-informed transformer heading?

Attempt these before reading the [answer criteria](physics/solutions/29.md). Then complete the separate learner notebook. To pass, explain the assumptions as well as obtaining a number. An independent score of at least 85% is our course policy, not accreditation; correct all critical conceptual errors.

## Delayed recall

**29.R1.** What three checks accompany a differentiable simulation?

**29.R2.** Why can mean correction be insufficient?

**29.R3.** What separates our graph example from a trained simulator?

Return to [the stage index](stages/29/README.md) for code, outputs and follow-on work. Primary resource IDs refer to [the source registry](docs/v5/SOURCES.md).


---

Source: `physics/lessons/30.md`

# Stage 30 — An independent world-model study: evidence before adoption

**Before this stage:** All earlier selected-track stages; no need to restart stages already independently demonstrated.

**Evidence used:** An evidence audit of every new executed lab, plus a fully specified real-data regression protocol. Sports/clinical/climate validation remains a separate project.

## Choose a question small enough to answer honestly

The capstone is not "build the best world model." It is a question with observations, a prediction target, a baseline and a decision rule. Examples include whether a topology descriptor adds held-out information, whether a geometry prior improves measured reconstruction, or whether a physical parameterization improves a particular forecast at an acceptable computational cost.

Choose one question. Specify the observation unit: a person, recording, physical trial, input function or study sample. State what is available at prediction time. Preserve identifiers, timestamps, units and provenance from acquisition to result. A model should not convert inferred states into observed facts simply by passing through another component.

## Reconstruct the complete evidence chain

The earlier course taught observations → geometry → representation → inference → validation. This extension adds dynamics, physical constraints and gradient-based learning, but the sequence does not eliminate uncertainty. Learned camera geometry needs metric alignment and independent holdouts. A Hamiltonian formulation needs justified states and forces. A low residual needs an appropriate equation and conditions. A classifier improvement needs a valid independent split.

Use the Stage 30 notebook to inspect the saved results of Stages 21–29. Each result identifies data origin, numerical checks and limits. A missing result stays missing. A mathematical counterexample is not relabeled as a measured benchmark, and a neural training run is not relabeled as a physical deployment test.

## A concrete measured-data capstone route

The copper excerpt supports a modest task: predict expansion response from temperature within the observed range. The existing example provides a frozen educational split, simple regression alternatives, per-sample predictions and source indices. Replicate it, explain why the response scale is retained, and compare errors across temperature regions.

Then propose a genuinely new study. It needs additional independently sourced observations or a preregistered new evaluation unit, not repeated tuning on the disclosed example. Full Hahn1 regression is a separate reproducibility exercise with 236 rows and the specified rational model; our 56-row subset is not a substitute for that official benchmark. Neither task establishes measured PDE evolution or a material conservation law.

Your report should contain the raw-data checksum, selection rule, preprocessing fit subset, model configurations, optimizer budget, validation selection, test predictions, uncertainty limitations, runtime boundaries and a negative result that would change the adoption decision. A result can be useful even when the simpler baseline wins.

## A geometry-to-physics route for sports

Begin with a static measured scene. Validate camera transforms, units, timing and held-out distances before modeling fast motion. Next use a slow, controlled motion with independently measured reference information. Compare a simple kinematic baseline with a structured dynamics candidate. Separate observed positions from smoothed positions, fitted velocities and inferred forces.

For ball flight, test a stated regime before adding contacts: no impact during the modeled interval, a justified observation model, known timestamps, and explicit assumptions about forces. An athlete's full motion is an actively controlled, dissipative and contact-rich system, not automatically a closed conservative oscillator. Use held-out people or sessions when the intended application requires such transfer.

Integrate results into the existing timestamped WMS state only after validation. This archive changes no production service and creates no competing authoritative world state. The code examples are a learning environment, not a deployment authorization or an injury-risk assessment tool.

## The wider concepts and their boundaries

Topological invariants help describe shape but do not supply metric scale. Smooth manifolds support local coordinates but do not make monocular depth identifiable. Symplecticity preserves a particular form but not every energy. Constraints limit feasible states but do not prove dynamics. PINNs encode an equation but may optimize poorly or identify an ambiguous problem. Neural operators approximate a family but do not automatically generalize to a new family. Graphs and attention organize information but need explicit laws for physical guarantees.

Every one of these ideas can be useful. The reliable approach is to state what each contributes, test its actual obligation, and avoid transferring a guarantee across levels where its assumptions no longer hold. The supplied source-audit document shows this process on the four posts rather than discarding them or accepting them wholesale.

## Completion and continuing learning

A stage is practiced after guided work; independently demonstrated after an unfamiliar assessment with evidence; retained after delayed recall under our declared course policy. A completed notebook is not a learner grade. Keep old attempts, changed answers and unresolved misconceptions. The v5 progress migration adds ten unassessed stages without resetting the previous 21.

The full book remains unaudited until its actual text can be compared with the curriculum. Deeper research branches—global differential geometry, advanced constrained mechanics, full operator approximation theory, manifold PDEs and paper-scale reproductions—have explicit reading and experiment requirements in the coverage map. They are not hidden behind a universal "100%" claim.

## Final oral defense

Present one result in five minutes without code. State the question, data, assumptions, baseline, result and limitation. Then explain a counterexample to the broadest claim someone might mistakenly make from your result. Finally show the smallest reproducible script or notebook that supports the measured conclusion. A strong defense can recommend not adopting the method.

**Stop condition:** the independent report can be rerun, its scope is accurate, every material claim has an appropriate source or experiment, and you can explain both success and failure without borrowing the tutorial's wording.

## Independent questions

**30.Q1.** What makes a capstone question testable?

**30.Q2.** How do you avoid turning repeated example analysis into a new test?

**30.Q3.** Can the copper data validate learned ball dynamics?

**30.Q4.** What information must travel with inferred sports states?

**30.Q5.** What is an acceptable negative result?

**30.Q6.** What remains beyond this archive?

Attempt these before reading the [answer criteria](physics/solutions/30.md). Then complete the separate learner notebook. To pass, explain the assumptions as well as obtaining a number. An independent score of at least 85% is our course policy, not accreditation; correct all critical conceptual errors.

## Delayed recall

**30.R1.** Name the four evidence levels we keep distinct.

**30.R2.** What should a source audit preserve?

**30.R3.** What is the next task after a failed mastery check?

Return to [the stage index](stages/30/README.md) for code, outputs and follow-on work. Primary resource IDs refer to [the source registry](docs/v5/SOURCES.md).


---

Source: `representations/lessons/R01.md`

# R01 — From observations to distributions: what an embedding can and cannot tell you

**Route:** core Stage 01 (vectors and linear maps), Stage 02 (distance), then this lesson. Use the existing notation/Python/linear-algebra primers only when needed. Do not restart all 31 stages. This is the first of five representation-learning units, not a replacement for topology.

**Outcome:** explain a numerical representation, calculate its mean and covariance, fit whitening without using evaluation data, and give a counterexample to “well spread means informative.”

## 1. Start with one observation

A digit image is an 8 by 8 array. Flattening lists its 64 intensities in a fixed order. Nothing has been learned yet. An encoder is a function that transforms those 64 values into, for example, 12 numbers. Its output is an **embedding**. A latent representation is an internal description rather than a directly measured physical state.

One source image, two corrupted views, and 12 output coordinates are three different axes. In a batch tensor shaped `[B, V, D]`, B is the number of source observations, V the views per source, and D the feature coordinates. Two crops do not create two independently observed people. Twelve coordinates are not twelve trials.

For sports, one row might be a frame, trial, athlete-season, or player-position aggregate. Name the row before making a matrix. The bundled soccer example contains repeated athletes; an ID is a join key, not automatically a numerical feature. In the Iris lab we select the four named centimetre measurements, not every numeric column: the file also contains identity and label columns.

**Regression versus regularization.** A regression model predicts an outcome. A regularizer adds a preference to an objective. Logistic regression is conventionally used for classification despite its name. SIGReg's “Reg” refers to regularization. An encoder can be trained without a human class label; that does not remove the need to evaluate whether its representations are useful.

## 2. Read a distribution as a rule for repeated outcomes

A probability distribution describes how values vary under a sampling process. A histogram describes the sample you collected. These are related, not identical. A population mean is an expectation; a sample mean estimates it.

For scalar observations x₁,…,xₙ, the sample mean is their sum divided by n. For a data matrix X with n rows and d columns, calculate one mean per column. Centering subtracts the corresponding mean from every row. We use the **sample covariance** convention:

```text
C = (X - mean).T @ (X - mean) / (n - 1)
```

C has shape d by d. A diagonal entry measures variation of one coordinate; an off-diagonal entry measures paired linear co-variation. It is not a causal relationship. The denominator matters: this course states when a method instead uses n.

### Work one example by hand

Take rows (1,2), (3,4), and (5,6). Their mean is (3,4), so the centered rows are (-2,-2), (0,0), (2,2). Each centered coordinate has squared sum 8. Dividing by 2 gives:

```text
C = [[4, 4],
     [4, 4]]
```

Both diagonal variances are nonzero, yet the second coordinate copies the first after a shift. The covariance has rank one. “Every dimension varies” does not rule out dimensional collapse.

## 3. Gaussian, standard Gaussian, and isotropy

A scalar Gaussian has a mean and variance. A multivariate Gaussian has a mean vector μ and covariance matrix Σ. A standard multivariate Gaussian is N(0,I): zero mean and identity covariance.

For a Gaussian, isotropy about its mean means covariance σ²I: every direction has the same variance. The standard target used here additionally sets σ²=1 and μ=0. The attachment's N(0,I) illustration is the intended target, not the most general definition of an isotropic Gaussian.

For a jointly Gaussian vector, uncorrelated coordinates are independent. Outside that family, zero covariance does not generally establish independence. Likewise, matching only a mean and covariance does not establish a Gaussian distribution.

### Exact counterexample

Choose each coordinate independently from {-1,+1} with equal probability. The population mean is zero and covariance is identity, but only four points are possible in two dimensions. A continuous Gaussian does not concentrate on those four atoms. Our notebook constructs a balanced sample and whitens it under the stated sample-covariance convention; its empirical covariance becomes identity while its discrete character remains.

## 4. Whitening is a fitted transformation

For full-rank sample covariance C, write C = Q Λ Qᵀ with orthonormal eigenvectors Q and positive eigenvalues Λ. ZCA whitening uses:

```text
W = Q @ diag(1 / sqrt(eigenvalues)) @ Q.T
Z = (X - training_mean) @ W
```

The transformed training sample has identity sample covariance, up to floating-point error. Fit the mean and W on the training observations, then apply those same values to new observations. Re-fitting on test data answers a different, transductive question and can invalidate an ordinary holdout evaluation.

If a covariance is singular, the inverse square root is unavailable. Centering also limits rank to at most n−1. With more coordinates than independent observations, full-rank sample whitening is impossible. Our function rejects rank deficiency rather than quietly calling a regularized transform exact whitening. PCA dimension reduction or a declared regularization floor are alternatives, but their effects must be described separately.

**Standardization is different.** Dividing each coordinate by its standard deviation fixes marginal scales but does not remove cross-covariances. A library may use population variance for standardization and this course may report sample covariance afterward; a small discrepancy from one can therefore be expected rather than a bug.

## 5. Spread, information, and meaning are separate checks

A constant encoder maps every image to the same vector. It achieves perfect agreement between two views but cannot distinguish images. That is complete representation collapse. A rank-deficient encoder may retain some information while losing dimensions.

At the other extreme, independent Gaussian noise has excellent-looking marginal geometry and no intended relationship to the digit identity. It is not a useful learned representation merely because it occupies space. R04 includes this control explicitly.

We report the mean coordinate standard deviation and covariance spectrum. We also compute entropy effective rank: normalize nonnegative covariance eigenvalues to probabilities p, then calculate exp(-sum(p log p)). It ranges from approximately one for a one-direction cloud toward d for equal nonzero eigenvalues; our zero-covariance convention returns zero. Effective rank is scale-insensitive, so report magnitude too. Tiny equal variances can produce high effective rank while being practically near-constant.

## 6. Run, inspect, and change one thing

Run `python course.py run --case r01 --output my_work/r01_attempt01`. The lab uses actual Iris measurements and separately labeled Gaussian/discrete controls. It fits the transform on the first 100 observations and applies it to the final 50. That ordering is deliberately visible and is not a randomized predictive evaluation. No biological conclusion should follow from this transform demonstration.

Before running, predict which covariance becomes identity. After running, explain why the held-out means need not be zero. Add 100 to the held-out inputs without refitting: the transformed mean should change. Finally, replace an input feature with a copy of another and observe the explicit rank-deficiency error.

## Independent work and mastery

Implement `center_columns`, `sample_covariance`, and `apply_fitted_whitening` in the learner notebook. Do the three-point covariance example without software. Explain why standardization, whitening, Gaussianity, and semantic information are four different statements.

**Gate:** give one data-contract error, one mathematical counterexample, and one experiment that separates distributional appearance from downstream usefulness. Merely obtaining an identity matrix is not a pass.

**Further depth:** the existing linear-algebra primer supplies eigendecomposition; R02 supplies a distributional comparison beyond moments. The course's homology lessons explain what topological invariants do and do not retain. A learned encoder is not assumed to be a homeomorphism or distance-preserving map.

**Sources and provenance:** this is an original lesson extending the user's supplied SIGReg notes. The distinction between standardization and fitted transforms follows their explicit definitions here. Primary representation-learning readings and the corrections to the supplied notes are in `../SOURCE_AUDIT.md`; dataset descriptions remain in the existing data cards. No external textbook is reproduced.


---

Source: `representations/lessons/R02.md`

# R02 — Characteristic functions, random projections, and SIGReg

**Before this unit:** finish R01 and be comfortable multiplying an n by d matrix by a d-vector. You need elementary sine, cosine, averages, and numerical integration—not prior familiarity with hypothesis testing. Review the existing calculus primer only as needed.

**Outcome:** derive and calculate the loss used in our educational SIGReg implementation; distinguish sampling, sketching, and quadrature errors; demonstrate a failure of limited projections.

## 1. Look at a cloud from one direction

Let z be a d-dimensional embedding and a a unit vector. The scalar aᵀz is its projection onto that direction. For a matrix Z of n embeddings and a matrix A with m unit-vector columns, `Z @ A` has shape n by m. Normalizing the columns matters: a unit projection of N(0,I) has variance one; multiplying a by two multiplies projected variance by four.

The Cramér–Wold result characterizes a joint distribution through **all** one-dimensional linear projections. It does not say that 32 selected directions and a finite batch certify Gaussianity. A random sketch can be a practical training signal while remaining an approximation to a distributional target.

Hand example: project (3,4) onto (1,0), (0,1), and (1,1)/sqrt(2). The results are 3, 4, and 7/sqrt(2). Check the matrix shapes before doing all projections at once.

## 2. A characteristic function records oscillating averages

For a scalar random variable U, define its characteristic function as E[exp(i t U)], where i²=-1 and t is a frequency. Euler's identity gives exp(iθ)=cos(θ)+i sin(θ). Therefore you can understand the calculation as two ordinary averages:

```text
real_part(t) = mean(cos(t * samples))
imag_part(t) = mean(sin(t * samples))
```

This is the empirical characteristic function, ECF. At t=0 it is exactly one. Its magnitude is at most one. A standard Gaussian's characteristic function is exp(-t²/2), with imaginary part zero.

For the two atoms -1 and +1 with equal weights, the ECF is cos(t): the imaginary terms cancel. At t=1, cos(1) is not exp(-1/2). This is a concrete way to distinguish distributions that have equal first two moments.

This unit does not require treating a complex number as mysterious data. It is a pair of real numbers with defined arithmetic. The squared magnitude of r+i s is r²+s², which is exactly what the loss computes.

## 3. State the objective completely

For projection a and n samples, our statistic is:

```text
D_a = n * integral_over_t [
          (mean cos(t * aᵀz) - exp(-t²/2))²
        + (mean sin(t * aᵀz))²
      ] * exp(-t²/2) dt
score = average over the selected directions a
```

The integration weight downweights high frequencies. We use a trapezoidal approximation on 17 equally spaced frequencies from -5 to 5 for the teaching/training default. We also implement a finer-grid check. These choices follow the paper's Epps–Pulley sketching construction, but the code is an original, single-process teaching implementation, not a copy of or verified substitute for the official library.

Every convention is explicit: standard-normal target; unit directions; no per-batch centering or variance normalization before the loss; average over directions; multiply by the number of observations within each view. Calling `score` on two stacked views changes n and the dependence structure. Our training experiment instead averages the two per-view penalties.

Do not silently whiten first: doing so would hide mean and variance failures from the very loss supposed to detect them.

## 4. Verify the integral with a different algorithm

For a tiny scalar sample x₁,…,xₙ, the Gaussian integral has a closed form under our chosen weight:

```text
n * [ sqrt(2π) * mean_ij exp(-(x_i-x_j)²/2)
    - 2 sqrt(π) * mean_i exp(-x_i²/4)
    + sqrt(2π/3) ]
```

To derive it, expand the squared characteristic-function difference into three terms. The first is an average over differences x_i−x_j. The second combines the Gaussian target with the Gaussian weight. The third integrates exp(-3t²/2). Use the Gaussian Fourier integral for each term.

This closed form takes quadratic work in sample count, so we reserve it for small correctness controls. The main sketch computes a sample-by-direction-by-frequency array. Its time and memory scale with n×m×number_of_frequencies in this explicit implementation. “Linear in n” assumes the sketch and frequency count are fixed; increasing every dimension simultaneously changes actual cost.

Predict how a 17-point grid differs from 1,025 points on the same integration range. Run the notebook's 17/65/257/1025 comparison. Agreement with an analytic expression is evidence about a numerical calculation, not evidence of learned semantics.

## 5. Three approximation questions

**Sampling:** a finite Gaussian sample need not have zero empirical score. A different batch changes the statistic. Consecutive frames of the same athlete are not independent draws simply because they occupy different rows.

**Sketching:** a flat cloud `(normal_value, 0)` can look normal along the first coordinate and completely collapsed along the second. The notebook calculates both. Even random directions need adequate coverage and a stated random seed.

**Quadrature:** truncating an integral and sampling a grid introduce numerical error. Coarse periodic sampling can miss behavior between frequencies. Use a finer grid or the small exact control to inspect this error.

Do not label the score a p-value. We do not supply a calibrated null distribution, critical value, or significance level. Optimizing the score also changes the samples in response to the statistic. A training penalty and an independent statistical test are different experimental roles.

## 6. A positive penalty may have zero gradient

At an exactly zero cloud, all projected values are zero. The mismatch with the standard-normal target is positive away from zero frequency. However, derivatives of cosine vanish at zero, and the squared imaginary-mean term also has zero derivative there. Consequently this smooth implementation can have positive loss and exactly zero first derivative at the symmetric collapsed state.

The notebook and test suite calculate this explicitly in R03. It does not refute a theorem about optima; it prevents the mistaken implementation claim that any initialization must immediately escape any collapsed state. Initialization, architecture, numerical behavior, and the complete objective still matter.

## 7. Apply a diagnostic to real observations

The lab fits an eight-coordinate PCA representation to the bundled digit **training split only**. PCA is not SIGReg training. It creates a real-data representation on which you inspect shape and variability, while keeping the synthetic normal/discrete controls clearly separate. Labels are not used to fit the PCA transformation.

Run `python course.py run --case r02 --output my_work/r02_attempt01`. Predict the first-axis/second-axis scores for the flat cloud, then explain their difference. Change one direction seed while holding the observations fixed. Finally, change the grid while holding the directions fixed.

## Independent work and mastery

Implement `normalize_columns`, `ecf_parts`, and `integrate_discrepancy`. Check your ECF on {-1,+1} against cos(t), and your trapezoidal integral against the separate closed form. Explain why comparing different sample counts or unreported weights may change score magnitudes.

**Gate:** distinguish all three approximation errors and give a counterexample to “a low finite-slice score proves an informative multivariate Gaussian.” The next unit explains why the distributional criterion must be coupled to a meaningful learning task.

**Primary reading:** Balestriero and LeCun, *LeJEPA*, Sections 4–5, arXiv:2511.08544v3. Full bibliographic links and source-versus-course distinctions are in `../SOURCE_AUDIT.md`.


---

Source: `representations/lessons/R03.md`

# R03 — Agreement without collapse: objectives and training mechanisms

**Prerequisites:** R01–R02 and the existing differentiation primer. The lab uses real training digit images, fixed random projections, and separately labeled artificial perturbations. It does not train the full named methods in this lesson.

**Outcome:** explain what each objective measures, follow which parameters receive gradients, and avoid treating an implementation mechanism as a universal guarantee.

## 1. Separate representation, prediction, loss, and regularization

An encoder transforms an observation into a representation. A predictor maps that representation to a target. A loss assigns a numerical disagreement. A regularizer adds a preference about parameters, representations, or function behavior. Those four roles are easier to reason about than a list of acronyms.

For scalar regression, mean squared error averages squared residuals; mean absolute error averages absolute residuals. Squaring weights large residuals more heavily. For probabilistic predictions, negative log likelihood penalizes low probability assigned to the observed outcome. Binary and multiclass cross-entropy are particular probability-based losses when the outcome representation and likelihood have been specified correctly.

L1 and L2 parameter penalties differ from representation regularizers. L1 promotes sparsity in appropriate optimization settings; it does not make arbitrary neural parameters exactly zero under every optimizer. L2 shrinks parameters. Decoupled weight decay in AdamW is not generally identical to adding an L2 term to an adaptive optimizer's objective. Dropout changes training activations; inference behavior and scaling must be specified.

These are not interchangeable settings that all “prevent overfitting” in the same way. In the lab, changing one loss coefficient changes an explicitly defined objective. It does not automatically justify changing learning rate, architecture, or evaluation data as well.

## 2. Why agreement alone admits collapse

Let f(x) be an encoder and v₁(x),v₂(x) two views. A simple objective is the mean squared difference between f(v₁(x)) and f(v₂(x)). A constant f makes that loss zero. This proves that agreement alone is insufficient to rule out a constant solution; it does not prove that every training run must end at that solution.

Our digit views add small noise and randomly mask a small fraction of pixels. No human class labels enter pretraining. The choice still encodes a hypothesis: these corruptions should usually retain useful digit information. Extreme cropping, rotation, or erasing can violate it. For sports, treating two different game moments as equivalent can erase the action or timing information you hoped to learn.

A related view is not necessarily an interchangeable target. Camera changes may preserve an identity while changing pixel coordinates. Predicting coordinates may require an equivariant transformation rather than strict numerical invariance.

## 3. VICReg: three terms with different jobs

VICReg combines view agreement, a variance floor, and a covariance penalty. In our implementation:

- The invariance term averages squared paired-coordinate differences.
- The variance term penalizes each coordinate's standard deviation falling below one, using sample variance and a small stated numerical epsilon.
- The covariance term sums squared off-diagonal entries of each view's sample covariance, divided by embedding dimension.

The configured weights are 25, 25, and 1. Those are implementation conventions, not universal best values. The variance term does not directly demand a Gaussian distribution. The covariance term suppresses linear redundancy, not every statistical dependence.

Work an exact failure case: all embedding rows are the same. Agreement is zero; variance is zero, so the variance-floor penalty is positive. Now duplicate one varying coordinate: the variance floor may be satisfied while the covariance penalty detects redundancy.

## 4. Barlow Twins: cross-correlation rather than within-view covariance

Standardize corresponding coordinates within each view and calculate the cross-correlation matrix C between the two views. Barlow Twins encourages diagonal entries toward one and off-diagonal entries toward zero. The diagonal concerns corresponding-coordinate agreement; off-diagonal entries concern cross-view redundancy.

In the teaching function, we use population variance for this standardization and an explicit epsilon. A matrix called a “correlation” should not be silently calculated with incompatible normalization conventions.

It is not identical to VICReg: the quantities compared and their penalties differ. Also, finite matrices have rank limits. If too many embedding dimensions are demanded from too few independent centered observations, an exact identity cross-correlation matrix may be impossible. Numerical training does not repeal that linear algebra.

## 5. Contrastive learning and the denominator

For SimCLR-style two-view training, each source observation produces a positive pair; other observations in the batch supply candidate negatives. Our NT-Xent/InfoNCE-style function concatenates the two batches, normalizes each vector, and compares cosine similarities divided by a positive temperature.

For anchor i, its own entry is removed from the denominator. The matching view is the target index. If the first B rows are view A and the next B rows view B, the positive index is `(i+B) mod (2B)`. That explicit indexing is more important than memorizing the acronym.

A hand check with four orthogonal one-hot vectors makes matching pairs easy. Shuffling only the second view should make the declared positives worse and increase the loss. A batch containing only one pair has no nontrivial negatives under this construction, so our function rejects it.

A different image is not always semantically negative. Two athletes may share the same movement, or adjacent clips may overlap. Negative selection and identity grouping are part of the learning assumptions.

## 6. BYOL, EMA, stop-gradient, and DINO

BYOL uses online and target paths, including a predictor and a slowly updated target. An exponential moving average updates target parameters as `tau * old + (1-tau) * online`. If old=1, online=3, and tau=.75, the result is 1.5. This calculation is not gradient descent on the target.

Stop-gradient uses a numerical value in the forward calculation but blocks differentiation through that path. For `(u - stop_gradient(v))²`, u receives the usual derivative; v receives no gradient from this operation. The notebook verifies both facts. Not updating v through that loss does not mean v must remain fixed forever: a separate EMA update can change it.

DINO is another teacher/student family, using probability-like outputs and different training mechanisms such as centering and sharpening in its original formulation. “Teacher/student” describes roles, not a single objective. Distillation may use a pretrained teacher or one updated during training. Our small mechanism tests are not reproductions of BYOL or DINO training.

An EMA target or a detach call alone is not a proof of representation quality. You must assess the full objective, architecture, data augmentations, and training dynamics.

## 7. JEPA family: do not confuse every target with the future

JEPA refers to predicting a target representation from context rather than necessarily reconstructing raw pixels. The target can be a masked region, another view, or a later state, depending on the task. I-JEPA studies image-region representations. Video JEPA approaches can use spatiotemporal masking; masked-video prediction is not automatically a strictly causal forecasting setup.

For a live basketball use case, explicitly state the time cutoff for every observation available to the encoder. If future frames were used by smoothing, interpolation, tracking, or a teacher target construction, that can be appropriate for offline analysis but cannot silently become a past-only forecast.

The supplied notes expand LeJEPA as “Lean JEPA.” The checked paper explicitly names it **Latent-Euclidean JEPA**, while also calling the approach lean. We preserve that distinction in the source audit. Our R04 objective is a small two-view agreement plus SIGReg experiment inspired by its construction; it does not reproduce every paper-specific training/evaluation detail.

## 8. Compare mechanisms without inventing a winner

Run `python course.py run --case r03 --output my_work/r03_attempt01`. The lab prints agreement, VICReg, Barlow, and contrastive values on controlled embeddings of real digit images. Their numerical magnitudes are not directly comparable scores of model quality: the losses have different definitions and scales.

Inspect the exactly-zero cloud test. It has positive SIGReg penalty and zero derivative. Explain why this statement is compatible with a claim that collapsed embeddings are not a global minimizer. A stationary point and a global optimum are not the same concept.

## Independent work and mastery

Implement `paired_mse`, `ema_update`, and `positive_pair_indices` in the separate learner notebook. Derive the gradient of paired MSE for one coordinate. Identify which paths receive gradients before running the stop-gradient example.

**Gate:** design one meaningful pair and one bad pair in both image classification and sports. Explain which mechanism targets variance, cross-correlation, negative separation, or target evolution. State which methods you have calculated versus actually trained.

**Primary readings:** VICReg (arXiv:2105.04906), Barlow Twins (2103.03230), SimCLR (2002.05709), BYOL (2006.07733), DINO (2104.14294), I-JEPA (2301.08243), and LeJEPA (2511.08544). Full links and version notes appear once in `../SOURCE_AUDIT.md`.


---

Source: `representations/lessons/R04.md`

# R04 — Train and evaluate representations on real handwritten digits

**Prerequisites:** R01–R03 and core Stage 11's evaluation lesson. This unit trains models, not merely computes a loss. Use the existing Python primer for arrays/functions and the differentiation primer for gradients. CPU execution is sufficient.

**Outcome:** reproduce a complete, bounded self-supervised experiment, inspect its predictions, and separate representation spread from predictive usefulness.

## 1. Specify the experiment before its result

The bundled dataset contains historical 8×8 handwritten-digit images. Pixel values are divided by 16, an explicit intensity conversion, not a scaler fitted to the full dataset. The existing train/validation/test sample IDs are retained. The test partition has already been exposed in earlier course versions; this is a reproducible teaching comparison, not a new untouched research benchmark.

The dataset does not provide writer identities in the bundled snapshot. We therefore cannot demonstrate writer-disjoint generalization. Class labels are available for downstream evaluation, but never enter the self-supervised pretraining loss.

Our question is deliberately narrow: under this fixed architecture and view recipe, how do agreement-only and agreement-plus-SIGReg embeddings compare with simple baselines? We are not testing whether LeJEPA universally beats other methods or whether a trained encoder understands basketball.

## 2. Define the observation and two views

Each source image gives a 64-coordinate input vector. Independently for each of its two views, add Gaussian noise with standard deviation .08 and set each coordinate to zero with probability .05. Clip to [0,1]. These changes are proposed mild corruptions, not proven label-preserving transformations. The example does not rotate digits, because rotations can alter class meaning.

Both training methods receive the same observation order and the same augmentation random stream for a given seed. A separate random generator produces projection directions, preventing an extra loss from silently changing the view sequence. This is a fairer comparison than giving each objective unrelated data perturbations.

Adjacent video frames, multiple crops, and duplicated images must still retain their source identities in larger applications. Data augmentation increases training variety, not the number of independently observed subjects.

## 3. Read the network architecture

The encoder maps 64 inputs to a hidden layer of width 64, applies GELU, then produces 12 output coordinates. There is no separate predictor, batch normalization, EMA teacher, or frozen pretrained backbone. Both objectives start from the same parameters for each seed.

Two seeds, 11 and 23, are run. Each method trains for 25 epochs with batches of at most 128 observations, AdamW learning rate .002, and weight decay .0001. The final epoch is fixed in advance rather than selected after looking at test accuracy.

The agreement-only objective is mean squared paired-coordinate difference. The second objective is:

```text
0.5 * agreement + 0.5 * average(SIGReg(view_a), SIGReg(view_b))
```

Each view's SIGReg uses its actual batch count, 32 fresh unit directions, and 17 frequencies in [-5,5]. Do not combine the two views into a doubled independent batch without changing the stated statistic. There is no distributed all-reduce in this educational code.

We also evaluate raw pixels, 12-dimensional PCA, the untrained encoder for each seed, and independent Gaussian vectors. PCA is fitted to training images only. The Gaussian vectors are a deliberately uninformative control, not a usable deployment feature extractor.

## 4. What “frozen linear probe” means

After pretraining, freeze the encoder. Train logistic regression on its outputs using the training labels. Standardize probe features using training statistics. Select the probe's regularization value C from [.1, 1, 10] using validation accuracy; ties select the first, smaller C. Evaluate the selected probe on test data without refitting the encoder or scaler.

Each representation uses the same training labels, validation partition, test partition, and C-selection policy. Architectures and representation dimensions still differ, so the comparison is not a perfectly controlled attribution of every cause. For example, raw pixels retain 64 dimensions whereas the learned outputs have 12.

A useful hand calculation: if a model gets 323 of 360 images correct, its accuracy is 323/360. Count mistakes too. Two models with similar accuracies may fail on different images, so the package saves sample-level predictions rather than only an aggregate percentage.

The probe uses labels: “self-supervised” refers to the encoder's pretraining, not to the complete absence of supervision in its evaluation.

## 5. Inspect training and geometry together

The lab saves objective, agreement, and SIGReg values for every epoch. These are observed optimization curves, not interchangeable measures of downstream quality. An agreement-only network can reduce its output magnitude and obtain a small loss. Mean coordinate standard deviation helps reveal this behavior; effective rank alone is not enough.

After training, compare variance magnitude, effective rank, validation accuracy, and test outcomes. Independent Gaussian vectors can have nearly unit variance while classifying poorly. A representation can also retain useful information despite failing an idealized geometry target. Neither one plot nor one scalar resolves every question.

We deliberately do not assert a required accuracy threshold in correctness tests. If an experiment fails to outperform a baseline, that is a result to explain, not a reason to change the test until the desired story passes. The invariant checks instead verify split disjointness, finite arithmetic, shapes, deterministic protocol, and exact controls.

## 6. Run and find the evidence

```bash
python course.py run --case r04 --output my_work/r04_attempt01
```

Use the uv prefix after setup when working in that environment. The runner makes an isolated workspace, executes the reference notebook, and copies generated artifacts into the selected output directory. The relevant subtree is `artifacts/reports/representations/r04/`.

Files include `protocol.json`, `training_history.csv`, `predictions.csv`, `results.json`, and NumPy weight archives for each trained encoder. The weight files contain arrays only; loading does not require unpickling an arbitrary Python object. The protocol contains sample IDs, source hash, augmentation recipe, seeds, architecture, optimizer, loss definition, selection rule, and limitations.

To explore, change one thing at a time and use a new run directory. First change augmentation severity while preserving the split. Then compare projection counts or embedding dimension. Keep the original protocol and results as the baseline. Looking at the test after every change turns it into development data; a later confirmatory study needs a new predeclared holdout.

## 7. Understand what this does not establish

This is not official-library parity, an ImageNet reproduction, a vision transformer, a calibrated normality test, a causal world model, or evidence about athlete outcomes. It uses two training seeds, not enough to support broad distributional claims about model performance. Random seeds control certain sources of variation; they do not make CPU, GPU, library, and platform behavior universally identical.

A sports extension requires actual independent trials and clear timestamps, not treating the 12-frame excerpt as a training corpus. The next unit maps these requirements without inventing a successful transfer experiment.

## Independent work and mastery

Implement `accuracy_count`, `select_probe`, and `variance_magnitude` in the learner notebook. Prove that a constant representation cannot separate mixed labels through a deterministic classifier except by a class-prior decision. Compare that theoretical fact with near-constant, finite-precision embeddings whose probe can still exploit small differences.

**Gate:** reproduce all model rows, locate the individual errors, explain the train/validation/test roles, and state one conclusion that remains unsupported even when the code and test suite pass.

**Deeper assignment:** reimplement the encoder and loader from the saved protocol, then compare results before exploring more advanced architectures. Consult the primary-paper/source audit for distinctions between this small ablation and complete LeJEPA training.


---

Source: `representations/lessons/R05.md`

# R05 — Transfer to sports, science, and a defensible world-model study

**Prerequisites:** core Stage 11 (evaluation), Stage 14 (frames and transformations), Stage 19 (past-only reasoning), and R01–R04. Read the sports data cards before interpreting their fields. This unit does not require GPU training or a cluster.

**Outcome:** choose the observation, target, grouping, geometry, and failure criteria for a new study without confusing a representation with a validated physical state.

## 1. Start with the question, not the newest dataset

Three datasets can all be called “basketball data” while supporting different tasks. Tracking supplies time-indexed locations with detection/interpolation flags. Pose provides landmarks and their conventions. Events assign discrete actions or outcomes. Season aggregates summarize many observations. Images or synchronized videos supply another observation process.

A player-season profile cannot be differentiated to obtain frame-level acceleration. A camera's predicted depth is not automatically measured metres. A frame index becomes seconds only after you establish timestamp or sampling-rate semantics. Use the existing sports lessons for these definitions instead of learning a second vocabulary here.

Our runnable transfer example uses 12 selected soccer profile rows from eight athletes. It selects three provider-named physical-summary features and groups all rows from each athlete into one partition. The first four observed IDs supply the demonstration training group; the remaining four supply a descriptive comparison. No classifier, injury-risk estimator, or athlete ranking is trained.

## 2. Fit preprocessing where it belongs

Fit `StandardScaler` only on the training group, then transform both groups. Inspect training and held-out covariance and coordinate scales. StandardScaler uses population variance; our covariance diagnostic uses the sample denominator n−1. With six training rows, standardizing the population variances to one gives sample standard deviations sqrt(6/5), not exactly one. This is an excellent example of explaining a number instead of treating any deviation as failure.

A holdout mean differing from zero can reflect real distribution differences, selection, or small-sample noise. It is not proof of a sport-specific causal effect. Feature-scale choices define which differences count as close. Never let identity or an outcome code enter automatically because it has numeric dtype.

The same calculation applies to flower measurements, mixture proportions, financial panel features, or sensor windows. That transfers the method of inspection—not the fitted scaler, model, or scientific interpretation.

## 3. A representation is not necessarily a metric world state

A latent vector can be predictive without encoding explicit position, orientation, or velocity. Its coordinates can be transformed while preserving some downstream performance. If a system requires metres, seconds, or a valid rotation, impose an explicit output contract and validate against independent physical references.

Likewise, a distributional regularizer does not preserve topology automatically. Whitening is an invertible linear map only when its full-rank assumptions hold. A dimension-reducing PCA or neural encoder can merge distinct points. Calling its output “shape” does not license an assertion that all holes, distances, or anatomical relations have been preserved.

For WMS-style work, keep observed landmarks, learned embeddings, reconstructed geometry, and event hypotheses distinct. Derived estimates should retain their source IDs, timestamps, units, uncertainty, and validation status. There is no need to create a second authoritative physical state just to experiment with a representation.

## 4. Decide invariance versus equivariance

An invariant representation should stay unchanged under a chosen transformation. An equivariant output should change in a predictable way. Athlete identity may be invariant to a camera rotation; a coordinate prediction must transform with the frame. A mirrored court image might preserve “a player exists” while changing handedness or left-right tactical information.

Before constructing positive pairs, write the property you intend to preserve. Then include a counterexample: two nearby frames can straddle release, and forcing them identical may erase release timing. A ball and hand appearing close need not be in contact. These are the same event-evidence boundaries developed in Stage 19, now applied to representation objectives.

## 5. Design a causal prediction study

Define an observation cutoff t₀ and a target horizon. The context can use only measurements that would have been available by t₀, including actual arrival times when latency matters. An offline smoother can incorporate future frames; a recorded coordinate at t₀ may therefore contain future information even if its timestamp looks causal.

A target encoder can examine the future during training to provide a target representation, provided the deployed context path does not receive it. That does not make test-time teacher forcing or future-aware preprocessing valid. Record the intended distinction between training supervision, evaluation construction, and live inference inputs.

Start with simple baselines: persistence of the last state, constant velocity under appropriate coordinates, or a small linear autoregression. Predictive performance, calibration, geometric accuracy, event precision, and runtime are different outputs. A low latent-space loss without a validated decoder or useful downstream probe does not prove that the model predicts meaningful physical futures.

## 6. Use contemporary datasets deliberately

The retained sports catalogue includes SPL, SkillCorner soccer and ACB basketball, wearable/video activity recognition, multiview sports, tracking/identification, and OpenBiomechanics acquisition routes. This release rechecks the three central official source descriptions but does not claim to re-download all payloads or independently rank every modern dataset.

A useful selection checklist is: match to the task; independent subjects/sessions; complete clock and coordinate definitions; ground-truth provenance; known detection/interpolation status; appropriate split; licensing for the intended use; a bounded acquisition size; and a conventional baseline. Newer is not automatically more suitable. Publicly accessible is not synonymous with unrestricted redistribution or commercial use.

The bundled sports excerpts are intentionally too small to establish a general learned sports representation. Obtain full, permitted independent trials before training. Pin source revisions and hashes, then retain untouched raw files and a reproducible transformation log. Keep license notices with derivative subsets.

## 7. Convert an experiment into evidence, not a screenshot

Run `python course.py run --case r05 --output my_work/r05_attempt01`. The runner first executes R04 because this lab consumes its generated comparison. That dependency is explicit; saved reports from earlier downloads are not used as hidden inputs.

Review the original digit ablation beside the profile geometry diagnostics. Explain why the digital representation that performs well on digits has not been shown to work on soccer profiles. The task-specific feature spaces and observation processes differ.

Write an experiment card with: question, data/version/license, independent unit, inputs available at decision time, preprocessing, baseline, candidate, metrics, hyperparameter selection, failure criteria, compute budget, immutable outputs, and conclusion. Include an “unsupported conclusions” paragraph.

A completed run and a passed unit test establish different things. The run shows what happened for a particular protocol. The test can rule out a specific bug. Neither alone supplies a causal explanation or domain deployment validation.

## Independent work and mastery

Implement `identity_overlap`, `causal_mask`, and `paired_differences`. Give a constructed overlap example, a timestamp exactly at the decision cutoff, and a comparison where equal average accuracy hides different individual mistakes.

**Gate:** design one sports and one non-sports study using the same learning principle but appropriate different observation contracts. Specify a held-out evaluation that cannot be defeated by duplicated IDs, future-aware processing, or tuning on the reported test. Do not count a proposed study as executed.

**Completion of this extension:** demonstrate all five units independently, reproduce the numerical controls, audit one primary-paper claim, and defend a new experiment. The full-book audit and the existing advanced proof obligations remain separate. Kubernetes is an optional execution environment, not a prerequisite for understanding these lessons.


---

Source: `curriculum/APPLICATIONS.md`

# Apply one idea in another industry

Do not run every case before learning the foundations. Choose the observation type that matches your question, finish one baseline, then compare the topological or geometric extension. A new dataset is a new scientific context, not permission to reinterpret its units.

| Domain | Case / data card | Important observation distinction |
|---|---|---|
| Healthcare | [Image-summary classification](industry/lessons/wdbc.md) | Feature records are not raw clinical images or a deployment validation cohort. |
| Food chemistry | [Wine cultivars](industry/lessons/wine.md) | Cultivar label is not a taste or quality score. |
| Manufacturing | [Plant process measurements](industry/lessons/stackloss.md) | Twenty-one days are not a large independent manufacturing benchmark. |
| Business | [Firm-year panel](industry/lessons/grunfeld.md) | Firm identity and time both matter for splitting. |
| Environment | [Historical CO₂](industry/lessons/co2.md) | Missing weekly slots are not measured values. |
| Water | [Annual Nile measurements](industry/lessons/nile.md) | A change point alone does not establish a cause. |
| Marine climate | [Sea-surface temperatures](industry/lessons/elnino.md) | A scalar historical series is not a full atmospheric field. |
| Transportation | [Traveler choice sets](industry/lessons/modechoice.md) | Alternatives belong to the same traveler and must stay together. |
| Agriculture | [Seed geometry](applications_v7/seeds/lesson.md) | Feature-space topology is not a physical hole in a kernel. |
| Materials | [Concrete mixtures and uncertainty](applications_v7/concrete_slump/lesson.md) | Split calibration data from fitting and evaluation data. |
| Handwriting | [Representation comparison](lessons/11_lesson.md) | A now-exposed demonstration test set is not a new holdout. |
| Stereo vision | [Measured reconstruction](lessons/15_lesson.md) | Pixels, disparity and metric depth require explicit conventions. |
| Solar activity | [Temporal analysis](sessions/19_session.md) | Later confirmation is not live detection at onset. |
| Material response | [Copper measurements](physics/lessons/21.md) | A measured response is not automatically a governing differential equation. |
| Basketball biomechanics | [SPL units and motion](sports_v8/lessons/S00.md) | Selected frames from one trial are not independent athlete outcomes. |
| Soccer profiles | [Profile topology](sports_v8/lessons/S03.md) | Aggregate profiles are not pitch trajectories. |
| Modern basketball metadata | [ACB readiness](sports_v9/lesson.md) | Ten sample games are not all covered season games or tracking frames. |

## Open data does not mean unlimited rights or complete coverage
Read the [retained data catalogue](docs/v7/DATA_CATALOG.md), [modern sports plans](docs/v8/SPORTS_DATASETS.md), [ACB data card](sports_v9/DATA_CARD.md), and [optional cross-industry plans](docs/v6/OPTIONAL_DATA.md). A plan is not an acquired dataset. The exact filenames are also reachable through the reader's all-materials library.

For video, wearables, motion capture, medical or industrial systems, define the task before selecting the newest source. Preserve participant identity for grouping, but do not use identifiers as predictive features without a justified task. Respect dataset-specific noncommercial and other restrictions before using any examples in a product.

The original small hand-derived controls remain essential: they distinguish a software defect from a surprising real-data result. Synthetic and manufactured examples are labeled and never counted as observed sources.


## Latest basketball source check

Read the [v9 sports update](docs/v9/SPORTS_UPDATE.md) for the verified ACB metadata boundary and the larger tracking acquisition plan.


[Exact square explorer](reference/square_explorer.html) · [Historical browser progress widget](site/progress.html). The historical widget uses separate local browser storage and is not synchronized with the evidence-backed CLI log.


## Representation-learning continuation (v11)

These five units reuse the established mathematical/data foundations instead of repeating a second core course. Read them in order after their stated prerequisites.

| Unit | Primary lesson | Experiment key |
|---|---|---|
| R01 | [Distributions, covariance, and whitening](representations/lessons/R01.md) | `r01` |
| R02 | [Characteristic functions, projections, and SIGReg](representations/lessons/R02.md) | `r02` |
| R03 | [Agreement, collapse, and SSL mechanisms](representations/lessons/R03.md) | `r03` |
| R04 | [Real-image training and independent evaluation](representations/lessons/R04.md) | `r04` |
| R05 | [Sports and cross-industry transfer](representations/lessons/R05.md) | `r05` |

Use the [terminology map](representations/TERMINOLOGY.md) for acronym lookup and the [source audit](representations/SOURCE_AUDIT.md) for supplied claims versus verified qualifications. The optional [Kubernetes lesson](docs/release/KUBERNETES.md) is deployment practice, not a prerequisite for topology.


---

Source: `curriculum/SITUATIONS.md`

# Which situation am I in?

This is a decision guide, not another lesson series. Each situation points to the canonical concept and tells you what evidence to obtain next.

## 1. I cannot understand the symbols
**Locate the gap:** distinguish a set from an array, a function from its output, and an equality from an assignment. Use the [notation primer](foundations/00_numbers_symbols_and_types.md), then [Stage 01](curriculum/stages/01.md). Translate one expression into a sentence before computing. Do not memorize an equation whose inputs you cannot identify.

## 2. I have a spreadsheet of features
**Ask:** what does one row represent, what units do its columns use, and which columns are labels or IDs? Start at [00](curriculum/stages/00.md), then [02](curriculum/stages/02.md). Fit any learned scaling on training data only. A length measured in metres is not commensurate with age or a category code just because both are numbers. Compare a simple baseline before a persistence representation.

## 3. My distance behaves strangely
Compute a three-point example. Does symmetry hold? Does the triangle inequality hold? Squared Euclidean distance may be useful in an objective, but it is not generally a metric. Check [02](curriculum/stages/02.md). Distinguish changing numerical scale from preserving topology, and record how thresholds transform with units.

## 4. I see a loop in a plot
A two-dimensional projection can hide or introduce apparent structure. Specify the ambient observation space, metric, complex, filtration and coefficient field before interpreting a diagram. Use [05–08](curriculum/stages/05.md). Calculate a square or triangle example first. A graph cycle that is filled by a 2-simplex is a boundary and does not contribute a nonzero H1 class.

## 5. My persistence result disagrees with a library
Check coefficient field, filtration convention, maximum simplex dimension, scale truncation, zero-length intervals and essential classes before changing code. Use [09](curriculum/stages/09.md) and `tests/test_optional_libraries.py`. Library absence is not agreement. A pipeline that computes H1 must include triangles that can kill 1-cycles.

## 6. My dataset is too large
Start with a documented subset and an exact control. A Rips construction can grow combinatorially; our educational implementation is intentionally small. Subsampling changes the analysis, so preserve the selection rule and rerun sensitivity checks. The [performance stage](curriculum/stages/18.md) distinguishes data movement, preprocessing, inference and latency. Do not assert that a GPU is the bottleneck before measuring it.

## 7. I have camera images and want metres
Work through [14](curriculum/stages/14.md), [15](curriculum/stages/15.md) and [17](curriculum/stages/17.md). Establish coordinate directions, calibration, scale, timing and visibility. Fit registration using one reference set and evaluate on other measurements. A predicted point cloud, a low reprojection residual, and a true held-out distance error answer different questions. A ground homography does not provide metric locations of airborne objects.

## 8. My tracking has missing or estimated observations
Do not relabel interpolated or extrapolated positions as directly observed. Separate physical elapsed time from frame index and a game clock. Use [19](curriculum/stages/19.md) and [sports S04](sports_v8/lessons/S04.md). For live decisions, disallow future frames; report stale-result age and visibility along with any event. Test hard negatives such as a hand passing near a ball without contact.

## 9. I want to predict an athlete's next result
Define the prediction cutoff and independent unit. Keep all data for a held-out athlete, trial or game together as required by the question. Whole-sequence features can leak future information into an earlier-time task. Use [sports S05](sports_v8/lessons/S05.md) and the [leakage laboratory](methods_v7/leakage/lesson.md). Do not turn 12 frames from one trial into 12 independent target outcomes.

## 10. I want to combine team totals
Determine the table grain before joining or summing. A player's team rows and season-total row are overlapping summaries. Preserve alias mappings. Rates need numerators and denominators, not a naive sum. Use the [ACB readiness lab](sports_v9/lesson.md), then test deliberately duplicated records and conflicting IDs.

## 11. A physics-constrained model gives implausible results
Check units, initial/boundary conditions, physical regime, identifiability, time-step size and numerical integration. A soft residual penalty is not a theorem, while one invariant does not establish all of physical validity. Use [21](curriculum/stages/21.md), [23–26](curriculum/stages/23.md), and [the source-claim map](docs/v9/CLAIMS_AND_LIMITS.md). Distinguish measured data from a manufactured example with a known analytic answer.

## 12. The total training loss decreases but a condition gets worse
Inspect each loss and its gradient; compute pairwise inner products before choosing gradient surgery. Opposing nonzero gradients cannot share a strict first-order descent direction. With several losses, sequential operations can change earlier alignments. Use [27](curriculum/stages/27.md). Repair an incorrect interface condition instead of expecting an optimizer to fix the model's mathematical specification.

## 13. My score improves slightly
Save individual paired predictions. Count successes gained and lost, not only the net change. Check the split, preprocessing and tuning history. Use [11–12](curriculum/stages/11.md) and the [paired-result session](sessions/12_session.md). An exposed test set is useful teaching data, not a fresh confirmatory holdout. A small improvement may not justify greater complexity.

## 14. I need uncertainty or deployment acceptance
Specify the population, independent unit, data-generating assumptions, and decision cost. Marginal coverage is not a guarantee for a particular person, mixture or future domain. Use the [concrete lesson](applications_v7/concrete_slump/lesson.md), [10](curriculum/stages/10.md), and [30](curriculum/stages/30.md). Validate on relevant independent measurements before operational use. The course's small examples do not certify clinical, safety-critical or professional sports deployment.

## 15. I cannot run the notebook
Use `python scripts/course.py doctor`, then run the stage's entry check. Read the first actual traceback. Missing dependency, changed input, predecessor failure and a mathematical assertion are different problems. `run --stage` rebuilds declared artifact dependencies in a fresh workspace. Use a new output directory rather than overwriting the evidence that explains the failure. A skipped optional library remains untested.

## 16. I have finished a stage but keep forgetting it
Do a changed problem with notes closed; explain a nonexample and an assumption. Record the exact misconception. Re-read only the relevant subsection, then repeat a different problem later. The progress log stores your declaration and evidence hash, not an independent certification of mastery.


---

Source: `industry/lessons/co2.md`

# Missingness, past-only windows and seasonal shape

**Prerequisite route:** Stages 00–03, 07–12 and 18–22. Beginners can inspect the data first and return to the advanced parts after the prerequisite stages.

**Central idea:** The time axis and the missingness mask are part of the dataset.

Start with the [shared beginner data primer](docs/v6/BEGINNER_DATA_PRIMER.md), then the [dataset card](industry/cards/co2.md). Open the [worked lab](industry/notebooks/co2.ipynb) only after predicting its first result.

## What you should be able to explain

By the end, identify the observation unit, separate a stored row from an independent example, justify the metric or representation, describe which data fit each transform, calculate the relevant baseline, and reject an unsupported domain claim. Software success and scientific interpretation are assessed separately.

## Work a small example first

Take a controlled weekly sequence [10,11,NaN,13,14,15]. Removing NaN makes 11 and 13 appear adjacent. A first-difference computed as if one week separates them is wrong. Keeping the calendar slots allows the window builder to reject unsupported examples rather than silently change their meaning. The notebook writes source indices so every forecast can be traced back to raw measurements.

A training-only local-shape transform subtracts a window's first value from each coordinate. It removes that window's level but retains short-term differences. It is an explicit representation choice, not a recovery of an invariant atmospheric state. A diagram that changes after detrending may be telling you about the preprocessing, not a discovered new physical phenomenon.

## Walk through the real-data experiment


## 1. A blank observation is not zero

The archive has 2,284 weekly date slots but only 2,225 measurements. Fifty-nine missing values remain missing. Dropping them and treating adjacent remaining rows as adjacent weeks would change the time axis. We create source-traceable windows and reject windows that cross a missing measurement or a time gap.

## 2. Define exactly what is being forecast

Each example uses twelve observed past weeks to predict one week ahead. During test evaluation later test predictions may use earlier **observed** test-period readings. This is rolling one-step prediction, not a free-running forecast of the entire future.

Our strict support split drops boundary windows instead of borrowing history across partitions; it is conservative and explicitly different from a less restrictive operational evaluation.

## 3. Inspect trend, gaps, and a delay-space cloud

A delay vector turns a time interval into a point. A loop may reflect seasonal repetition. It is not proof that the scalar series uniquely reconstructs the atmosphere's physical state. The point-cloud sample below is training-only; no test labels decide which diagram to show.

## 4. Diagnose an invalid shortcut

Why is interpolation using readings on both sides of a future gap unavailable for an online forecast? Why should overlapping windows not be treated as independent patients? How would changing the forecast horizon alter the information set?

Further model development needs a new locked protocol; the displayed test results are already exposed. These are historical observations, not a statement of today's atmospheric concentration.

## Save your evidence

Create `my_work/industries/co2.md` with your prediction, actual result, explanation, one failed assumption and one claim the evidence does not justify. Use the separate learner notebook only after you understand the worked code. No notebook execution automatically marks your learning complete.

## Independent conceptual questions

**co2.Q1.** Why does dropping missing rows distort a fixed weekly lag?

**co2.Q2.** What is the target index for length three, end index two, horizon two?

**co2.Q3.** How does observed-history one-step testing differ from free-running rollout?

**co2.Q4.** Why is a seasonal-looking loop not proof of a reconstructed atmospheric attractor?

## Independent code and delayed recall

Use [your learner notebook](industry/learner/co2.ipynb), then compare with the [worked answers](industry/answers/co2.ipynb). Do not use the answers as an input to your first attempt. After a delay, explain the observation unit, the main leakage trap, and a result this data cannot establish without reopening the lesson.

## Mastery evidence

Save `my_work/industries/co2.md` with a prediction, a hand calculation, one changed-code experiment, observed output and one limitation. Record the dataset hash and exact source rows you evaluated. To pass, all three coding tasks must run, the four conceptual answers must be correct, and the central leakage/interpretation error must be corrected. An independent delayed explanation—not a checkmark—is the retention evidence.


---

Source: `industry/lessons/elnino.md`

# Monthly climate records and delay representations

**Prerequisite route:** Stages 01–03, 07–12, 21–22 and 28. Beginners can inspect the data first and return to the advanced parts after the prerequisite stages.

**Central idea:** A calendar baseline makes the representation and evaluation more interpretable.

Start with the [shared beginner data primer](docs/v6/BEGINNER_DATA_PRIMER.md), then the [dataset card](industry/cards/elnino.md). Open the [worked lab](industry/notebooks/elnino.ipynb) only after predicting its first result.

## What you should be able to explain

By the end, identify the observation unit, separate a stored row from an independent example, justify the metric or representation, describe which data fit each transform, calculate the relevant baseline, and reject an unsupported domain claim. Software success and scientific interpretation are assessed separately.

## Work a small example first

Suppose the mean January temperature in the chosen training years is 24 degrees C. A January observation of 25.5 has an anomaly of +1.5 degrees relative to that baseline. This controlled arithmetic does not assert that all published climate anomaly products use our baseline. In the notebook the twelve training monthly means are calculated and saved explicitly.

The monthly long view is derived by a fixed column order; alphabetically sorting month names would scramble chronology. After reshaping, the window constructor uses an integer month index. A temperature in one regional record is not a spatial field. Operator training needs varying input functions or conditions with corresponding solution functions, so the optional field-simulation path is separate from this observed scalar time-series exercise.

## Walk through the real-data experiment


## 1. Reshape without changing time

The original rows contain years and twelve named month columns. We create a long table ordered January through December for each year. This adds no observations: 61 annual rows become 732 monthly values. The signal is regional mean SST in degrees Celsius, not an anomaly until we subtract a declared baseline.

## 2. Compare a seasonal forecast, persistence, and learned lags

The seasonal baseline predicts the training average for the target month. Persistence predicts the last observed temperature. Ridge predicts from twelve observed lags. Each makes a different assumption. All test windows remain inside the test period and predict one month ahead using observed history.

## 3. Visualize anomalies and training delay topology

Subtracting a seasonal mean is not harmless by default: the reference period is part of the definition. A baseline fit on all years would use future distribution information. We keep the training baseline fixed. A short delay cloud is an exploratory summary, not a recovered global climate manifold or a climate neural operator.

## 4. Distinguish one series from an operator dataset

An operator-learning study needs multiple input functions or conditions and corresponding solution fields, with function-level splits. This single regional series is not equivalent to many independent PDE trajectories. The core manufactured heat-operator examples and optional simulated field datasets serve a different role.

Independent task: explain how changing the climatology fit period can change the apparent anomalies without changing any original observations.

## Save your evidence

Create `my_work/industries/elnino.md` with your prediction, actual result, explanation, one failed assumption and one claim the evidence does not justify. Use the separate learner notebook only after you understand the worked code. No notebook execution automatically marks your learning complete.

## Independent conceptual questions

**elnino.Q1.** Why must the reference period accompany an anomaly value?

**elnino.Q2.** Why is alphabetical month ordering wrong?

**elnino.Q3.** Can the same 732 values become independent PDE solutions just by creating windows?

**elnino.Q4.** Why must we compare last value and monthly climatology before more complicated models?

## Independent code and delayed recall

Use [your learner notebook](industry/learner/elnino.ipynb), then compare with the [worked answers](industry/answers/elnino.ipynb). Do not use the answers as an input to your first attempt. After a delay, explain the observation unit, the main leakage trap, and a result this data cannot establish without reopening the lesson.

## Mastery evidence

Save `my_work/industries/elnino.md` with a prediction, a hand calculation, one changed-code experiment, observed output and one limitation. Record the dataset hash and exact source rows you evaluated. To pass, all three coding tasks must run, the four conceptual answers must be correct, and the central leakage/interpretation error must be corrected. An independent delayed explanation—not a checkmark—is the retention evidence.


---

Source: `industry/lessons/grunfeld.md`

# Firm panels, timestamps and prediction availability

**Prerequisite route:** Stages 00–03, 10–12, 19 and 21. Beginners can inspect the data first and return to the advanced parts after the prerequisite stages.

**Central idea:** Two records from the same company are not two independently sampled companies.

Start with the [shared beginner data primer](docs/v6/BEGINNER_DATA_PRIMER.md), then the [dataset card](industry/cards/grunfeld.md). Open the [worked lab](industry/notebooks/grunfeld.ipynb) only after predicting its first result.

## What you should be able to explain

By the end, identify the observation unit, separate a stored row from an independent example, justify the metric or representation, describe which data fit each transform, calculate the relevant baseline, and reject an unsupported domain claim. Software success and scientific interpretation are assessed separately.

## Work a small example first

Write two records for one imagined firm: year t has investment 100, year t+1 has investment 120. A last-investment baseline predicts 100 for the later record and incurs absolute error 20. That arithmetic says nothing about causality. A fitted coefficient using capital and value may capture association, firm scale or missing covariates.

Our panel shift happens within each firm. A shift on the entire concatenated table would accidentally use the last record of one company as the previous record for another. This is a silent data-engineering failure that can survive model training. Compare same-firm chronological evaluation with leaving entire firms out; the latter tests a different generalization question. Publication delays and later accounting revisions are not in this snapshot, so the availability assumption stays qualified.

## Walk through the real-data experiment


## 1. Respect the panel structure

A panel repeatedly observes the same entity. This table contains eleven firms, with annual records over twenty years. We create prior-year predictors within each firm. In particular, same-year year-end market value is not available at the beginning of that year.

This is an explicitly simplified availability assumption: the notebook does not contain publication-time or revision-vintage data.

## 2. Compare with doing almost nothing

The last observed investment value is a serious baseline. A pooled ridge model shares one relationship across firms; it does not imply that all firms have the same structural mechanism. Both MAE and RMSE retain the source monetary scale. We do not invent a million-dollar multiplier.

## 3. Look at errors by firm instead of hiding them in an average

A low pooled error can hide a poorly modeled firm. The following view is a descriptive breakdown of this exposed test set, not a basis for tuning firm-specific models against it. A new-firm claim would require a different, entity-disjoint evaluation.

## 4. Separate prediction from intervention

No fitted coefficient here is a causal effect of increasing a firm's equipment. The data contain selection, omitted variables, repeated firms, and historical accounting conventions.

Exercise: design two different tests—future years of known firms and years from previously unseen firms. Explain why these answer different questions, and why revised financial data complicate a genuine real-time historical simulation.

## Save your evidence

Create `my_work/industries/grunfeld.md` with your prediction, actual result, explanation, one failed assumption and one claim the evidence does not justify. Use the separate learner notebook only after you understand the worked code. No notebook execution automatically marks your learning complete.

## Independent conceptual questions

**grunfeld.Q1.** Why is a shift within firm necessary?

**grunfeld.Q2.** Why is same-year year-end value unavailable for a start-of-year forecast?

**grunfeld.Q3.** What does a known-firm future-year test not establish?

**grunfeld.Q4.** Does a capital coefficient identify the causal effect of buying equipment?

## Independent code and delayed recall

Use [your learner notebook](industry/learner/grunfeld.ipynb), then compare with the [worked answers](industry/answers/grunfeld.ipynb). Do not use the answers as an input to your first attempt. After a delay, explain the observation unit, the main leakage trap, and a result this data cannot establish without reopening the lesson.

## Mastery evidence

Save `my_work/industries/grunfeld.md` with a prediction, a hand calculation, one changed-code experiment, observed output and one limitation. Record the dataset hash and exact source rows you evaluated. To pass, all three coding tasks must run, the four conceptual answers must be correct, and the central leakage/interpretation error must be corrected. An independent delayed explanation—not a checkmark—is the retention evidence.


---

Source: `industry/lessons/modechoice.md`

# Choice sets, group splits and fair baselines

**Prerequisite route:** Stages 00–03, 07–12 and 19. Beginners can inspect the data first and return to the advanced parts after the prerequisite stages.

**Central idea:** The physical or decision-making unit must survive reshaping and splitting.

Start with the [shared beginner data primer](docs/v6/BEGINNER_DATA_PRIMER.md), then the [dataset card](industry/cards/modechoice.md). Open the [worked lab](industry/notebooks/modechoice.ipynb) only after predicting its first result.

## What you should be able to explain

By the end, identify the observation unit, separate a stored row from an independent example, justify the metric or representation, describe which data fit each transform, calculate the relevant baseline, and reject an unsupported domain claim. Software success and scientific interpretation are assessed separately.

## Work a small example first

With 210 travelers and four alternatives each, the array has 840 alternative records. A person-level prediction requires selecting one of the four modes once for each traveler. A split after pivoting gives one independent choice set per row. A split before pivoting could put part of a person's choice set into the fitting data and another part into the test data.

Cheapest offered mode is a concrete baseline, not an assumption that price alone determines behavior. Waiting time, travel time, income and unobserved preferences can matter. Our classifier does not estimate an intervention effect from changing a ticket price. The source sampled choices disproportionately; a probability distribution in this sample is not a population market-share forecast.

## Walk through the real-data experiment


## 1. Reconstruct the choice set

Each traveler has four alternatives. Randomly splitting the 840 rows could put the same traveler into training and test. Instead, pivot to 210 person-level examples. Include offered waiting times, prices, in-vehicle times and income. Exclude the target and party size whose availability is tied to the chosen mode. We also exclude generalized cost because it is constructed from other cost/time terms.

## 2. Establish person-level baselines

This simple multinomial classifier treats each traveler's thirteen offered attributes as predictors. It is not the same model as a conditional-logit utility model. We compare it with the training-majority mode and the cheapest offered mode. All return exactly one choice per traveler.

## 3. Inspect sample geometry without inventing market shares

The study deliberately oversamples some modes. Prediction fractions are not population transport shares, and learned probabilities are not automatically population-calibrated. A topology diagram summarizes offered attributes in the chosen standardized metric; it does not recover the real road network.

## 4. Transfer the grouping lesson

In sports, several shots can belong to one athlete; in healthcare, several images can belong to one patient; in manufacturing, many overlapping windows can come from one run. Choose the independent unit before creating a split.

Explain why a predicted change under a modified ticket price is not a validated causal effect. What sampling weights, policy experiment, or external evidence would be needed?

## Save your evidence

Create `my_work/industries/modechoice.md` with your prediction, actual result, explanation, one failed assumption and one claim the evidence does not justify. Use the separate learner notebook only after you understand the worked code. No notebook execution automatically marks your learning complete.

## Independent conceptual questions

**modechoice.Q1.** Why do 840 records not imply 840 independent decisions?

**modechoice.Q2.** Why exclude `choice` and the potentially post-choice `psize` from features?

**modechoice.Q3.** How can probabilities sum to one and still be uncalibrated for a population?

**modechoice.Q4.** What is analogous to traveler grouping in sports and healthcare?

## Independent code and delayed recall

Use [your learner notebook](industry/learner/modechoice.ipynb), then compare with the [worked answers](industry/answers/modechoice.ipynb). Do not use the answers as an input to your first attempt. After a delay, explain the observation unit, the main leakage trap, and a result this data cannot establish without reopening the lesson.

## Mastery evidence

Save `my_work/industries/modechoice.md` with a prediction, a hand calculation, one changed-code experiment, observed output and one limitation. Record the dataset hash and exact source rows you evaluated. To pass, all three coding tasks must run, the four conceptual answers must be correct, and the central leakage/interpretation error must be corrected. An independent delayed explanation—not a checkmark—is the retention evidence.


---

Source: `industry/lessons/nile.md`

# Retrospective change and forward evaluation

**Prerequisite route:** Stages 02, 07–12, 19 and 21. Beginners can inspect the data first and return to the advanced parts after the prerequisite stages.

**Central idea:** A detected change is a descriptive result until its cause is independently established.

Start with the [shared beginner data primer](docs/v6/BEGINNER_DATA_PRIMER.md), then the [dataset card](industry/cards/nile.md). Open the [worked lab](industry/notebooks/nile.ipynb) only after predicting its first result.

## What you should be able to explain

By the end, identify the observation unit, separate a stored row from an independent example, justify the metric or representation, describe which data fit each transform, calculate the relevant baseline, and reject an unsupported domain claim. Software success and scientific interpretation are assessed separately.

## Work a small example first

For a controlled signal of eight zeros followed by eight ones, the split before the first one yields two constant segments and zero within-segment squared error. The unit test checks that exact result. A real river series has nonzero noise and dependence. Searching many cut points makes the chosen one look better by construction; the winner is not itself a significance test.

The model uses annual total volume, not instantaneous water speed or discharge. To convert volume to average rate you would need an explicit duration and consistent units. Even then you would not know subannual peaks or extreme-event timing. Such missing resolution matters for operational infrastructure decisions; it cannot be repaired by using a more expressive neural architecture.

## Walk through the real-data experiment


## 1. Define volume and chronology

The measurements are annual river volumes, in units of 100 million cubic metres. A volume is not a flow rate in cubic metres per second. There are one hundred years, not one hundred independent river systems. First partition years, then construct windows inside each partition.

## 2. Find a descriptive change using training years only

We fit two constant means and choose the split with smallest within-segment squared error. The selected split is retrospective within the training period. A low error does not explain the cause, prove a change is significant, or justify moving a dam. Many candidate splits were inspected; ordinary one-test reasoning would ignore that search.

## 3. Keep a forward prediction question separate

The change-point fit is not automatically a forecasting model. Here we independently compare last value, a fixed training mean, and a ridge model of five past annual readings. No causality or physical conservation law is enforced by any of them.

## 4. Identify what would be required for physics

A hydrological conservation model needs more than this scalar annual series: specify inflows, outflows, storage, rainfall, spatial boundaries and uncertainty. The manufactured PDE examples in the core course have these assumptions by construction; this observational series does not magically inherit them.

Transfer exercise: write one descriptive claim supported by the plot and one causal claim that it cannot support.

## Save your evidence

Create `my_work/industries/nile.md` with your prediction, actual result, explanation, one failed assumption and one claim the evidence does not justify. Use the separate learner notebook only after you understand the worked code. No notebook execution automatically marks your learning complete.

## Independent conceptual questions

**nile.Q1.** Why is the two-mean search retrospective?

**nile.Q2.** How does annual volume differ from instantaneous discharge?

**nile.Q3.** Why must the change point be selected without reading the future evaluation years?

**nile.Q4.** Which missing quantities prevent this one series from specifying a full hydrology PDE?

## Independent code and delayed recall

Use [your learner notebook](industry/learner/nile.ipynb), then compare with the [worked answers](industry/answers/nile.ipynb). Do not use the answers as an input to your first attempt. After a delay, explain the observation unit, the main leakage trap, and a result this data cannot establish without reopening the lesson.

## Mastery evidence

Save `my_work/industries/nile.md` with a prediction, a hand calculation, one changed-code experiment, observed output and one limitation. Record the dataset hash and exact source rows you evaluated. To pass, all three coding tasks must run, the four conceptual answers must be correct, and the central leakage/interpretation error must be corrected. An independent delayed explanation—not a checkmark—is the retention evidence.


---

Source: `industry/lessons/stackloss.md`

# Small-sample process monitoring

**Prerequisite route:** Stages 01–02, 10–12, 21 and 26–27. Beginners can inspect the data first and return to the advanced parts after the prerequisite stages.

**Central idea:** A small observational table is useful for learning model fragility, not certifying a reactor.

Start with the [shared beginner data primer](docs/v6/BEGINNER_DATA_PRIMER.md), then the [dataset card](industry/cards/stackloss.md). Open the [worked lab](industry/notebooks/stackloss.ipynb) only after predicting its first result.

## What you should be able to explain

By the end, identify the observation unit, separate a stored row from an independent example, justify the metric or representation, describe which data fit each transform, calculate the relevant baseline, and reject an unsupported domain claim. Software success and scientific interpretation are assessed separately.

## Work a small example first

Calculate an ordinary mean and one residual before running Ridge. If a source-scale observation is 20 and a prediction is 15, the signed residual observed minus predicted is 5; its absolute error is 5. Do not convert it to kilograms or a flow rate without a documented unit relationship. When a label uses an encoded percentage, keep the encoding explicit in plots.

The source row order is preserved for a simple train/validation/test demonstration. Missing timestamps prevent claiming a faithfully reconstructed future operating shift. The leave-one-training-row-out exercise asks how much individual observations influence a prediction. It does not increase the number of independent experiments. A large neural network might memorize these rows; that is not evidence of an identifiable physical state or safe control behavior.

## Walk through the real-data experiment


## 1. Read the encoded variables

There are only twenty-one plant records. Exact dates and instrument metadata are absent. We preserve source row order, but do not call it a verified future-production timeline. Stack loss uses the documented encoded response scale; other ambiguous units are not invented. We hold out rows to demonstrate the procedure, not certify a plant-control system.

## 2. Investigate how fragile the fitted coefficients are

Leave out one **training** row, refit both scaling and model on the remaining training rows, then predict that omitted row. This is a sensitivity exercise, not an additional independent test set. A large change caused by a single row matters when the whole training set has fourteen observations.

## 3. Compare geometry with process meaning

Build a small training point-cloud diagram. The distances join observations with similar standardized process values. The diagram does not enforce a mass-balance law. A scalar residual model is not a reconstructed reactor, and correlation cannot determine whether changing a control knob causes the predicted change.

## 4. Define a responsible next experiment

Specify the missing timestamps, calibration units, actuator limits, safe excitation protocol, and independently recorded future runs before proposing a physics-informed model. Do not pretend that the eight new datasets supply the boundary conditions for every PDE in the course.

Transfer questions: why might a neural network fit these rows and still be useless? Which quantities would a defensible conservation-law experiment need to measure?

## Save your evidence

Create `my_work/industries/stackloss.md` with your prediction, actual result, explanation, one failed assumption and one claim the evidence does not justify. Use the separate learner notebook only after you understand the worked code. No notebook execution automatically marks your learning complete.

## Independent conceptual questions

**stackloss.Q1.** Why must the holdout be described as source-order rather than a verified operational-time split?

**stackloss.Q2.** What changes when scaling is refit in each leave-one-out training fold?

**stackloss.Q3.** Why can a PINN with a wrong boundary condition still produce low training error?

**stackloss.Q4.** List four observations needed for an independently testable plant conservation model.

## Independent code and delayed recall

Use [your learner notebook](industry/learner/stackloss.ipynb), then compare with the [worked answers](industry/answers/stackloss.ipynb). Do not use the answers as an input to your first attempt. After a delay, explain the observation unit, the main leakage trap, and a result this data cannot establish without reopening the lesson.

## Mastery evidence

Save `my_work/industries/stackloss.md` with a prediction, a hand calculation, one changed-code experiment, observed output and one limitation. Record the dataset hash and exact source rows you evaluated. To pass, all three coding tasks must run, the four conceptual answers must be correct, and the central leakage/interpretation error must be corrected. An independent delayed explanation—not a checkmark—is the retention evidence.


---

Source: `industry/lessons/wdbc.md`

# Cell-image measurements and honest classification

**Prerequisite route:** Stages 00–03 and 07–12. Beginners can inspect the data first and return to the advanced parts after the prerequisite stages.

**Central idea:** A medical-sounding name does not turn a teaching classifier into a medical device.

Start with the [shared beginner data primer](docs/v6/BEGINNER_DATA_PRIMER.md), then the [dataset card](industry/cards/wdbc.md). Open the [worked lab](industry/notebooks/wdbc.ipynb) only after predicting its first result.

## What you should be able to explain

By the end, identify the observation unit, separate a stored row from an independent example, justify the metric or representation, describe which data fit each transform, calculate the relevant baseline, and reject an unsupported domain claim. Software success and scientific interpretation are assessed separately.

## Work a small example first

For a hand calculation, consider a controlled confusion matrix with 90 benign and 10 malignant examples. A rule calling everything benign gets 90 correct, but malignant recall is zero. Balanced accuracy is (1 + 0)/2 = 0.5. This is an invented arithmetic control, not a result measured on this dataset. Compare it with the real confusion matrix produced by the notebook. Explicitly say which is which.

The original measured features describe variation among cell nuclei. Our standardized point cloud compares image summaries; we never reconstruct actual three-dimensional cells. Computing homology after projecting to two coordinates answers a question about that projection. It can merge or separate structures that differ in the original feature space. Test a controlled projection before interpreting a real plot.

## Walk through the real-data experiment


## 1. Define the independent example before fitting

Each row summarizes nuclei in a digitized fine-needle-aspirate image. These are not raw images. The sklearn snapshot lacks the original identifiers, so we cannot verify a patient-disjoint or hospital-disjoint test. We map **malignant to 1** explicitly. No threshold or model in this lesson is a clinical recommendation.

Predict: which columns would leak the answer or identify a row rather than measure the specimen?

## 2. Establish a fixed, explainable baseline

A logistic model maps a linear score to a number between zero and one. That number is not automatically calibrated for a new hospital. We fix C=1 before viewing validation or test results. Accuracy can hide unequal class performance, so we also report balanced accuracy, a confusion matrix, and ROC AUC. All preprocessing parameters come from training rows.

## 3. Ask a topological question at the correct level

Now study the geometry of a fixed small training cohort. A persistence diagram belongs to this point cloud and its metric; it is not a separate diagnostic test for each row. A loop can reflect sampling, correlated features or preprocessing. Selecting the most dramatic diagram after inspecting labels would be exploratory selection, not an independent discovery.

## 4. Stop before an unsupported conclusion

**Answer independently:** (a) Why does a row-disjoint test not establish patient independence here? (b) Why does zero training error not prove a clinically usable system? (c) What additional identifiers and validation cohorts would be required?

Do not improve the reported test score by repeatedly trying features. Any further search needs a newly protected evaluation. The source card records the original source and reuse conditions.

## Save your evidence

Create `my_work/industries/wdbc.md` with your prediction, actual result, explanation, one failed assumption and one claim the evidence does not justify. Use the separate learner notebook only after you understand the worked code. No notebook execution automatically marks your learning complete.

## Independent conceptual questions

**wdbc.Q1.** Explain why `label == 0` means positive malignancy in this loader but is not a universal label convention.

**wdbc.Q2.** Draw a confusion matrix for an always-benign classifier and calculate both ordinary and balanced accuracy.

**wdbc.Q3.** Identify the absent identifiers that prevent verifying a hospital-level or patient-level holdout.

**wdbc.Q4.** Explain why a cohort persistence diagram is not one diagnosis per row.

## Independent code and delayed recall

Use [your learner notebook](industry/learner/wdbc.ipynb), then compare with the [worked answers](industry/answers/wdbc.ipynb). Do not use the answers as an input to your first attempt. After a delay, explain the observation unit, the main leakage trap, and a result this data cannot establish without reopening the lesson.

## Mastery evidence

Save `my_work/industries/wdbc.md` with a prediction, a hand calculation, one changed-code experiment, observed output and one limitation. Record the dataset hash and exact source rows you evaluated. To pass, all three coding tasks must run, the four conceptual answers must be correct, and the central leakage/interpretation error must be corrected. An independent delayed explanation—not a checkmark—is the retention evidence.


---

Source: `industry/lessons/wine.md`

# Chemistry, scale and out-of-sample topological descriptors

**Prerequisite route:** Stages 01–02 and 06–12. Beginners can inspect the data first and return to the advanced parts after the prerequisite stages.

**Central idea:** A good topological experiment must make a descriptor available for a genuinely new query.

Start with the [shared beginner data primer](docs/v6/BEGINNER_DATA_PRIMER.md), then the [dataset card](industry/cards/wine.md). Open the [worked lab](industry/notebooks/wine.ipynb) only after predicting its first result.

## What you should be able to explain

By the end, identify the observation unit, separate a stored row from an independent example, justify the metric or representation, describe which data fit each transform, calculate the relevant baseline, and reject an unsupported domain claim. Software success and scientific interpretation are assessed separately.

## Work a small example first

Use a hand-checkable geometry before the real chemistry: points at (0,0), (1,0), (1,1), (0,1). Under the edge-distance Rips convention, the perimeter loop is born at 1 and filled when diagonal edges and triangles enter at square-root two. The full small filtration—not a graph without triangles—is required. Multiply all coordinates by two and check the interval scales by two.

Now connect that test to the chemistry. The same idea applies in thirteen standardized coordinates; no two-dimensional picture is required for computation. Each local query complex contains the query and eight fixed-training neighbors. Changes in the reference cloud or standardization alter the question. Reserving reference rows keeps the supervised fitting query from including itself as a training landmark. It costs fitting data, so the raw-feature comparison uses that same reduced fitting set.

## Walk through the real-data experiment


## 1. Distinguish measurement, cultivar and quality

The target identifies three cultivars, not consumer quality or safety. A change from grams to milligrams can alter raw Euclidean distances. Standardization is therefore an explicit modeling choice, fitted on training data only.

Our comparison gives every model the **same supervised fitting rows**. A separate subset of training rows is reserved as a fixed reference cloud.

## 2. Define a descriptor that can be applied to an unseen row

For one query, choose its eight nearest training reference points. Form the nine-point Rips complex through dimension two. Summarize finite H0 merge lengths and H1 lifetimes. The reference set is frozen; test observations never become reference points.

The six numbers are engineered local summaries. They are not a magical recovery of the topology of one vector. Small complete complexes keep the computation inspectable.

## 3. Compare raw, topological, and combined representations

C=1, eight neighbors and thirty anchors are fixed teaching choices—not the outcome of a hidden test-set search. We show validation and test scores separately. A win here would be a result for this one protocol, not evidence that topology is generally superior.

## 4. Check a property, not just a score

Multiplying all standardized coordinates by two should multiply Rips birth/death distances by two. Counts need not be reinterpreted as physical units. The assertion below tests the descriptor contract independently of cultivar prediction. Then explain why arbitrary feature-wise scaling is a different operation.

## Save your evidence

Create `my_work/industries/wine.md` with your prediction, actual result, explanation, one failed assumption and one claim the evidence does not justify. Use the separate learner notebook only after you understand the worked code. No notebook execution automatically marks your learning complete.

## Independent conceptual questions

**wine.Q1.** Why is cultivar not an ordinal quality target?

**wine.Q2.** Why are reference rows excluded from supervised fitting rows in this comparison?

**wine.Q3.** Which six descriptor entries should change under uniform scale multiplication?

**wine.Q4.** What new evidence is needed before saying topology improves wine analysis generally?

## Independent code and delayed recall

Use [your learner notebook](industry/learner/wine.ipynb), then compare with the [worked answers](industry/answers/wine.ipynb). Do not use the answers as an input to your first attempt. After a delay, explain the observation unit, the main leakage trap, and a result this data cannot establish without reopening the lesson.

## Mastery evidence

Save `my_work/industries/wine.md` with a prediction, a hand calculation, one changed-code experiment, observed output and one limitation. Record the dataset hash and exact source rows you evaluated. To pass, all three coding tasks must run, the four conceptual answers must be correct, and the central leakage/interpretation error must be corrected. An independent delayed explanation—not a checkmark—is the retention evidence.


---

Source: `applications_v7/seeds/lesson.md`

# Agriculture case — What does “shape” mean in a table?

## Start without subject knowledge

A wheat kernel is an individual object. A measurement turns one property of that object into a number. A row collects measurements for one kernel; a column repeats a particular measurement across kernels. A class label names a category, not an amount. Subtracting class 1 from class 3 does not define a meaningful physical difference.

The included UCI Seeds snapshot has 210 rows, seven geometric measurements and three integer class labels, with 70 rows per label. UCI describes X-ray-derived measurements of Kama, Rosa and Canadian kernels. We retain the source integers rather than guess the integer-to-name mapping. The original radiographs are not included. These are observed extracted features, not simulated points and not a segmentation benchmark. [Provider and DOI](https://archive.ics.uci.edu/dataset/236/seeds).

**Learning objective:** distinguish a measurement, a constructed geometric feature, a metric-dependent descriptor, and a topological invariant. Then perform a small classification experiment without confusing its score with agricultural validation.

## A formula you can derive

For area A and perimeter P, define compactness C = 4πA/P². A circle of radius r has A = πr² and P = 2πr. Substitution gives C = 1. Under uniform scaling by s, area becomes s²A and perimeter becomes sP, so C does not change. Under a general stretch, it usually changes. Thus scale invariance is not invariance under every homeomorphism.

For example a rectangle with side lengths 2 and 1 has C = 4π(2)/6² = 2π/9, about 0.698. Stretch one side to 4; the new C is 4π(4)/10² = 4π/25, about 0.503. Both filled rectangles are homeomorphic to a disk. Their different compactness values did not discover different topology. This is an original worked calculation, not a new empirical finding.

The source already includes a compactness column. Recomputing it from the rounded area and perimeter is a consistency check, not permission to replace the provider's values. Small differences can result from rounding. The notebook reports the discrepancy. The inspected repository metadata does not specify physical length/area units, so we do not rename these columns millimetres or square millimetres. The dimensionless relation assumes internally consistent units.

## Why preprocessing changes the question

Euclidean distance adds squared coordinate differences. A column with a much larger numerical scale can dominate it. Our baseline standardizes each feature using the training mean and population standard deviation. That defines a particular geometry; it does not discover the uniquely correct geometry of wheat. A constant training column gets scale one, which avoids division by zero without creating variation.

Fit preprocessing on training observations only. Applying those fixed parameters to a held-out row is different from recalculating them using the held-out collection. The latter lets the test distribution influence the analysis before evaluation.

## The explicit experiment

We declare a stratified 126/42/42 training/validation/test split with fixed seed 17. Stratification preserves the class proportions in this demonstration. It does not supply missing farm or batch identities. Two logistic-regression pipelines use identical rows and fixed C=1: all seven features, and six features without compactness. A training-majority predictor is also shown. No hyperparameter is selected using validation or test results. Validation is reported as a diagnostic; the test partition is exposed after the prescribed experiment and must not become an unlimited tuning set.

The experiment asks whether these recorded features can distinguish the integer classes in this collection. It cannot establish future-farm performance, disease detection, crop yield, or field prevalence. The source table lacks acquisition dates and field/batch identifiers needed for those evaluation designs.

## Return after learning persistence

A small, declared subset of 24 training rows is standardized with the same training scaler and used to build a Vietoris–Rips filtration through triangles. Pairwise distances determine when edges enter; three mutually connected vertices supply a triangle. The notebook calculates H0 and H1 persistence. These are properties of this sampled, standardized seven-dimensional feature cloud, not holes in a physical grain. The subset uses fixed row identities; no class outcome is used to select an attractive diagram. Its row IDs and intervals are saved.

This persistence calculation is descriptive. It is not added secretly to the classifier and is not credited with any classification improvement. The earlier Wine case teaches a fixed-reference predictive descriptor when you are ready to study that separate formulation.

## Read the result correctly

Accuracy is correct predictions divided by test rows. A confusion matrix preserves which classes were confused. Report the denominator, not only a percentage. Balanced classes in this designed collection do not show natural prevalence. Two different models can tie on accuracy but misclassify different rows. Inspect the saved predictions before making a claim about improvement.

## Your independent work

Implement four small functions in `learner.ipynb`. Then explain the rectangle example without looking. Change only the chosen persistence subset after clearly labeling that new experiment exploratory; predict whether its diagram must remain identical. It need not: sample selection changes the complex. Do not mistake a sensitivity result for evidence that the original source table is wrong.

To pass, identify the observation unit; calculate compactness; justify the split and scaler; explain the meaning and limitations of the diagram; and describe a missing data field needed for an actual farm deployment study.

[Data card](data/v7/seeds/metadata.json) · [Worked lab](applications_v7/seeds/lab.ipynb) · [Your coding exercises](applications_v7/seeds/learner.ipynb) · [Reference answers](applications_v7/seeds/answers.ipynb) · [Questions and answers](applications_v7/seeds/questions.md)


---

Source: `applications_v7/concrete_slump/lesson.md`

# Materials case — A prediction needs an error range and a meaning

## Begin with the observation

A mixture is specified by quantities of ingredients. A laboratory test measures its responses. This source records 103 concrete-mixture tests with seven ingredient quantities and three outputs. Ingredients are given in kilograms in one cubic metre of concrete; slump and flow are centimetres; compressive strength is MPa at 28 days. This is the **Concrete Slump Test** dataset, not the separate 1,030-row concrete-strength dataset. [Provider and DOI](https://archive.ics.uci.edu/dataset/182/concrete+slump+test).

Our task is to predict the 28-day strength from the seven ingredients. The source row ID is an identifier, not an ingredient. Slump and flow are measured responses; they are excluded from the chosen pre-measurement prediction task. Including a column because it improves a score is not a substitute for establishing that it would be available at decision time.

## What a baseline means

A constant training-mean predictor ignores ingredients. It answers: how well can we do using only the typical training response? A ridge regression predicts an intercept plus a weighted sum of standardized ingredient quantities. Its penalty discourages very large fitted coefficients. Our fixed regularization value is 10, chosen for this teaching protocol before results are shown, not reported as optimal.

Suppose measured strengths are 20, 30 and 40, while a model predicts 22, 25 and 43. Absolute errors are 2, 5 and 3 MPa; their mean is 10/3 MPa. Squared-error metrics punish the error of five more strongly, but they answer a different question. We report MAE and RMSE with the target unit. Neither metric is a certification that a structure can safely use the material.

## Why training, calibration and testing are different

The lab uses a fixed random ordering: 52 training rows fit the scaler and model, 25 calibration rows set the error radius, and 26 test rows assess the fixed procedure. The model is not refitted after calibration. We do not reuse calibration rows for tuning the model or choosing the score. Test outcomes are used only for the final reported diagnostics.

The source describes 78 initial and 25 later observations, but the table does not supply authenticated dates or batch IDs. We therefore label the random mixture-level split as an educational protocol, not a proven temporal, new-batch or exchangeable deployment design. Randomly shuffling a dataset does not create independence that the collection process lacked.

## Derive the calibration radius by ranks

For the fitted predictor f, each calibration error is s_i = |y_i - f(x_i)|. At nominal error rate α, use the one-based rank

k = ceil((n_cal + 1)(1 - α)).

Sort calibration errors and take the k-th value. If k exceeds n_cal, use an infinite radius rather than inventing an unsupported finite extreme quantile. For n_cal=25 and α=0.1, k=24. Python's zero-based index is therefore 23. We select an order statistic directly; interpolating between values is not the same rule.

For a hand example with nine sorted errors 1,2,…,9 and α=0.2, k=ceil(10×0.8)=8. A prediction of 30 receives [22,38]. At α=0.1 the radius is nine. Requesting 99% nominal coverage with only nine calibration points needs rank ten and yields an uninformative infinite interval under this conservative construction. This illustrates a sample-size limitation, not a software failure.

Under exchangeability of calibration and future scores for a predictor fixed independently of them, the rank argument gives finite-sample **marginal** coverage. It does not say every recipe, subgroup or realized test set has exactly the nominal coverage. Distribution shift and dependent batches require additional reasoning. [Primary tutorial, including proof and limitations](https://arxiv.org/abs/2107.07511). This package adds the worked arithmetic and a real-data implementation; it does not reproduce that tutorial's experiments.

## Test usefulness as well as coverage

A radius of a million MPa would cover these observed outcomes but be useless. Report interval width alongside empirical coverage. Inspect errors for individual held-out mixtures, but label any subgroup discovered after looking at them as exploratory. Our symmetric intervals may have negative lower bounds; those are retained and discussed rather than silently clipped. Known physical constraints can justify a different set construction, but that choice must be stated before interpreting its coverage.

The notebook draws intervals centered on the fixed test predictions. The x-axis orders points by predicted strength, not time. Sorting for a plot is not a chronological analysis. It saves row IDs, predictions, bounds, coverage flags, calibration scores, rank and radius so you can verify the whole calculation.

## What you may conclude

You may report this model's errors and this interval procedure's empirical coverage on these declared rows. You may not infer engineering fitness, plant-wide safety, causal ingredient effects, or future-batch coverage from this example. A learned coefficient is not a controlled experimental intervention.

To pass, calculate an order statistic by hand, distinguish calibration from model fitting, trace one interval to its source row, explain marginal versus conditional coverage, and identify the batch information that an independent industrial study would need.

[Data card](data/v7/concrete_slump/metadata.json) · [Worked lab](applications_v7/concrete_slump/lab.ipynb) · [Your coding exercises](applications_v7/concrete_slump/learner.ipynb) · [Reference answers](applications_v7/concrete_slump/answers.ipynb) · [Questions and answers](applications_v7/concrete_slump/questions.md)


---

Source: `methods_v7/claims/lesson.md`

# Methods lab — Read a scientific claim, then test exactly what it says

## Four kinds of statement

A source can motivate an idea without proving it. Keep four labels separate: **source claim**, **mathematical statement with assumptions**, **original worked calculation**, and **measured experiment**. This lesson uses the supplied posts about symplectic structure, projection and PINN gradient conflicts as prompts. The source audit records their scope. We do not rewrite the posts as if their authors had supplied our qualifications.

The symplectic post asserts exact energy conservation across arbitrary rollout steps and describes one algebraic correction as restricting updates to a physical constraint manifold. The gradient-conflict post reports Norm-PCGrad advantages on its selected benchmarks. The HNN/LNN post links formulations through the Legendre transform. The manifold post describes local charts and smooth transitions. These are the supplied sources' positions; the calculations below are original educational checks, not reproductions of their empirical studies.

## Continuous dynamics and discrete updates are not the same object

For canonical coordinates z=(q,p), let J=[[0,1],[-1,0]] and dynamics z_dot=J grad H. For differentiable, time-independent H and an exact solution, the chain rule gives dH/dt = grad(H)^T J grad(H)=0 because J is skew-symmetric. Explicit time dependence or external dissipative forces change the claim. A floating-point integrator is a discrete map approximating a trajectory; it needs its own analysis.

Take H=(q²+p²)/2, nondimensional unit-oscillator variables. Kick then drift:

p_new = p - h q; q_new = q + h p_new.

At (q,p)=(1,0), h=0.2 gives p_new=-0.2 and q_new=0.96. Energy changes from 0.5 to (0.96²+0.2²)/2=0.4808. The map A=[[1-h²,h],[-h,1]] nevertheless satisfies A^T J A=J. Thus being symplectic does not imply exact conservation of this H at every step. The lab checks both identities separately and plots a longer trajectory, without calling nondimensional values joules or seconds.

## A single linearized correction can leave a residual

For C(x)=x^T x-1, the desired set is the unit sphere. Its Jacobian is 2x^T. The minimum-norm linearized correction is x_new=x-((x^T x-1)/(2x^T x))x when x is nonzero. At x=(2,0), it gives (1.25,0). The new constraint residual is 1.25²-1=0.5625, not zero. It has solved the first-order approximation, not the original nonlinear equation exactly.

Iteration can reduce the residual; radial normalization x/||x|| is exact for this particular sphere away from zero. Neither fact makes one formula an exact universal projection for every constraint. At zero the Jacobian is rank deficient. The reference function raises a clear error instead of inventing a direction. At arbitrary constraints, rank, convergence region, metric and desired conservation properties must be examined independently.

## Conflicting objectives do not always admit simultaneous improvement

For two losses with gradients g1=(1,0) and g2=(-1,0), their inner product is -1. A small update -ηd decreases both to first order only if g1·d>0 and g2·d>0. These conditions contradict each other. No gradient-surgery algorithm can produce a direction satisfying both strict inequalities in this example. An optimizer may choose a compromise or stall; it does not remove mathematical incompatibility.

The supplied Norm-PCGrad preprint's reported improvements are benchmark-specific. Our small example is not a performance comparison between PCGrad, Norm-PCGrad and ConFIG. The existing Stage 27 covers their operations and interface-condition issues. [Primary preprint](https://arxiv.org/abs/2609.14841).

## Turn the lesson into a claim ledger

For each future paper, save its exact source/version, the proposed guarantee, assumptions, the implemented object, the test, and its scope. Distinguish a model's learned vector field from the numerical solver and the hardware implementation. Timing one matrix multiplication does not establish end-to-end latency; matching a drawing does not establish camera calibration. Those topics are developed in the retained geometry stages.

The lab also loads observed Seeds measurements to compare two homeomorphic rectangle controls and the source's compactness feature. This is a real-data bridge, not evidence that wheat obeys Hamiltonian dynamics. Use observed data when the scientific question fits; use an exact manufactured counterexample when falsifying a universal mathematical claim.

To pass, derive each counterexample on paper, run it, explain the variable and unit conventions, and rewrite your own conclusion so it says no more than the calculation supports. A numerical test supports a calculation; it is not a substitute for a general proof.

[Claim audit](docs/v7/SOURCE_AUDIT.md) · [Worked lab](methods_v7/claims/lab.ipynb) · [Learner coding](methods_v7/claims/learner.ipynb) · [Reference answers](methods_v7/claims/answers.ipynb) · [Questions](methods_v7/claims/questions.md)


---

Source: `methods_v7/leakage/lesson.md`

# Methods lab — Two different rows can contain the same evidence

## What is the object of evaluation?

An array has rows, but the scientific unit might be a person, a physical object, a manufacturing batch, a camera session, or a time interval. A splitter that keeps row numbers apart has not necessarily kept independent units apart. This lab makes that distinction visible without inventing a new observed dataset.

We begin with the 210 observed Seeds feature vectors. Then we deliberately make three exact software copies of each row. There are now 630 array rows but still only 210 source kernels. These copies are a **manufactured leakage stress test**. They are not additional measurements, repeatability trials, new kernels, or a larger agricultural study.

The repeated source ID is the unit key. Generated copy IDs distinguish software rows. Saving both makes it possible to ask two questions independently: are array indices shared, and are source kernels shared?

## Why a nearest-neighbor method exposes the problem

A one-nearest-neighbor classifier assigns the label of the closest training feature vector. If an exact copy of a test row exists in training, its distance is zero. It can look excellent without transferring to a new kernel. We compare a random row split with a split that assigns all copies of each original kernel together.

Both experiments fit standardization only on their own training data. This controls one kind of leakage while intentionally varying the other. All feature columns, labels, copies and fixed random seeds are recorded. The difference is descriptive: this small constructed stress test does not estimate the numerical inflation in every real dataset.

## A hand example

Suppose rows 0 and 1 describe kernel A and rows 2 and 3 describe kernel B. Training on rows [0,2] and testing on [1,3] shares no row indices. It shares both kernels. The row audit passes, but the unit audit fails. A valid new-kernel split might train on [0,1] and test on [2,3], although two kernels would be far too few for a useful real evaluation.

The audit returns both results instead of guessing which one matters. You must provide an appropriate unit key. Unique random IDs assigned to every copied row would conceal the problem; identifiers are part of the scientific design, not merely software formatting.

## Distance depends on units

The lab also multiplies one numerical feature by 1,000. That simulates a change of numerical representation; because the source units are not independently specified, we do not label it a real mm-to-m conversion. Raw Euclidean distances generally change. A training-standardized representation should agree after a positive column-wise rescaling if its scaler is consistently refitted on the same training rows. We test this arithmetic identity separately from any claim that standardization is scientifically appropriate.

Do not transfer the identity to arbitrary nonlinear transforms, feature removal, imputation, or changing reference samples. Nor does equal standardized data imply that a model is fair across missing demographic groups.

## Connect back to images, time and physics

A medical scan produces many image patches; a random patch split may share the patient. A video produces adjacent windows; the windows may share frames and events. A numerical PDE solution produces many spatial samples; testing on different points from the same solution is not necessarily testing a new initial condition. These are proposed analogies. This lab uses Seeds copies only; it does not claim to have evaluated patients, basketball clips, or PDE generalization.

The retained course includes complete-choice-set and time-support checks. Return to those after this exact example. Group splitting and chronological splitting address different threats; neither word is a universal guarantee against leakage.

## Repair the experiment, not the narrative

When an audit fails, first define the intended future query. Is it a new kernel, new plant, new site, or another reading of a familiar device? Then choose the split, transformations and metric to match it. Do not merely delete inconvenient test rows until the score improves. Save the reason and the exclusions, and retain a final evaluation set appropriate to the revised question.

Your assessment is to demonstrate the four-row example, write the two overlap checks, interpret the manufactured-copy result, and propose the missing group key for a domain you care about. A passing test proves this audit implementation detected these overlaps, not that an unseen collection is independent.

[Worked lab](methods_v7/leakage/lab.ipynb) · [Learner coding](methods_v7/leakage/learner.ipynb) · [Reference answers](methods_v7/leakage/answers.ipynb) · [Questions](methods_v7/leakage/questions.md)


---

Source: `sports_v8/lessons/S00.md`

# S00 — Begin with one observation, not a model

## Your destination
By the end, you can open a sports record, explain every selected field, convert
its units, and identify what it cannot tell you. No topology vocabulary is needed
at the start. Read core Stage 00 for arrays and Stage 01 for functions when needed.

## First picture in words
Imagine pausing a free-throw video. A processing system estimates the centre of
the ball and several body landmarks. Each landmark has three numbers. The first
number is not “how good the shot was”; it is a coordinate along one chosen axis.
Changing the origin changes coordinates without necessarily changing distances.

An **observation** is one recorded item. A **feature** is a value we calculate or
select to describe an item. A **label** is the outcome or annotation we intend to
explain. A **group** identifies related items, such as all frames of one shot or
all shots from one person. These are different roles, even when all are stored
in one JSON file. JSON means nested named values and lists; a CSV is a table.

Our selected SPL records come from one trial, T0001, participant P0001, session
2025-12-18. They are twelve deliberately selected frames, not twelve independent
athletes and not the complete 458-trial session. The provider's free-throw README
is dated March 2026 and lists this session at 60 frames per second. The collection
date and documentation date are different facts. See the [SPL card](sports_v8/cards/spl.md).

The second excerpt contains twelve football physical-profile rows. Player 2858
appears in three positions. “Twelve rows” therefore does not mean “twelve people.”
The first twelve source rows are a convenience excerpt, not a random sample of
a league. See the [SkillCorner card](sports_v8/cards/skillcorner.md).

## Numbers become quantities only after units and frames are known
A vector is an ordered list. For example, `(x,y,z)` specifies three coordinates.
The SPL position values are in feet. Their origin is the court centre. The
outcome's `landing_x` and `landing_y` use a different hoop-local system and are
in inches. `entry_angle` is in degrees. Converting units does not by itself
transform between those two origins.

Use the international-foot conversion:

```
metres = feet × 0.3048
metres = inches × 0.0254
```

Thus ten feet is 3.048 metres, and twelve inches is 0.3048 metres. A coordinate
reported as 18.8 feet is 5.73024 metres in the same frame. To change the origin,
we would also need the appropriate translation, and perhaps a rotation. Unknown
camera geometry cannot be supplied by multiplying a column.

The free-throw result `made` applies to the shot, not each frame. Putting the
same result on many frames can be a useful storage operation, but it creates no
new independent outcomes. The landing location and final entry angle are not
available before the ball reaches the hoop; they must not become pre-release
predictor inputs merely because they share a file with the pose.

## Your first code
Run the worked notebook `sports_v8/notebooks/S00.ipynb`. It loads local snapshots,
not the network. The following is the essential pattern:

```python
from pathlib import Path
from shape_lab.sports_v8 import load_sports, to_metres
spl, profiles = load_sports(Path.cwd())  # run from the project root
first = spl['records'][0]
ball_m = to_metres(first['ball'], spl['xyz_unit'])
print(first['frame'], ball_m)
print(len(profiles), profiles['player_id'].nunique())
```

`first['ball']` gets the value named `ball`. The function returns an array of
three coordinates. `.nunique()` counts distinct identifiers, not table rows.
The notebook prints the result before calculating anything more ambitious.
Predict which count will be smaller before running it.

## The first accuracy check
Convert metres back to feet and compare with the input. This checks arithmetic,
not whether the camera measurement is correct. Check the local file hash. This
checks whether our local file changed, not whether a transcription matches the
provider. These are separate levels of evidence.

Because direct downloads failed in the build environment, the two sports
excerpts were transcribed from selected official numeric text. Source URLs,
Git blob hashes and selection rules are included. An optional local verifier
compares full original bytes and selected values; it was not executed remotely
here. The observed-source status must never be changed to “independently verified
measurement” by passing a local checksum test.

## What to learn quickly, and what to revisit deeply
For the first pass, learn observation, feature, label, group, coordinate frame,
unit, provenance and subset. For the deep pass, write a data contract: permitted
units, required columns, identity keys, valid time order, missing-value policy,
and a source revision. A contract makes an assumption executable. It does not
prove that all assumptions are correct.

## Exercises — stop before the answers
1. Twelve frames from one shot all have result `made`. How many shot outcomes
are represented? Could you estimate prediction accuracy for unseen shooters?
2. Convert a two-foot wrist displacement and a two-inch hoop offset to metres.
Explain why their equal numeric input does not imply equal distance.
3. The football table has repeated player IDs. Propose a key that distinguishes
rows while retaining the player ID needed to keep a person in one partition.
4. Why do neither a hash match nor a unit round trip validate markerless geometry?

## Worked answers
1. One shot outcome. No unseen-shooter evaluation is possible from one shooter
and one selected trial; more frames cannot fix that design limitation.
2. 0.6096 m and 0.0508 m. The first is twelve times the second. They also refer to
different frames and quantities; conversion alone does not align the hoop frame.
3. A candidate is player, team, season and position, with the source row retained
for audit. Verify uniqueness in the full release before assuming it. Split by
player rather than the finer row key for an unseen-player question.
4. A hash addresses file identity. A round trip addresses reversible arithmetic.
Measurement accuracy needs independent references and a declared error metric.

## Mastery gate and delayed recall
Explain the two records without opening a model notebook. Independently solve
the three coding exercises. Tomorrow, explain why collection date, release date
and analysis date cannot substitute for one another. Record one limitation in
your own words in `my_work/S00.md`; do not mark mastery solely from running code.


---

Source: `sports_v8/lessons/S01.md`

# S01 — Position, angle, and motion are different objects

## Your destination
Calculate an unsigned landmark angle and a time-averaged velocity, state their
units, and refuse to bridge unobserved gaps without an explicit policy. Connect
this to core Stages 02–03 on distances and maps, and Stage 14 on coordinate frames.

## Start with a displacement
If a ball moves from `(1,2,3)` to `(1.1,2,3)` metres, its displacement is the second
vector minus the first: `(0.1,0,0)` metres. Its travelled path might be longer if
it moved along a curve. The norm, `sqrt(dx²+dy²+dz²)`, is straight-line separation.
An estimated average velocity divides displacement by elapsed time. Its norm is
the magnitude of the average velocity, not necessarily average speed along an
unknown curved path.

With frame IDs 110 and 115 at 60 Hz, elapsed time is `(115-110)/60 = 1/12` second.
It is not `1/60` merely because these records are adjacent in our small table.
Our excerpt is nonuniformly sampled. This is a useful built-in failure case:
assigning `np.arange(len(records))/60` would invent a different clock.

The notebook uses the declared sampling rate and original frame IDs. It keeps
the raw source `time` separately. Values such as frame 115/time 1916 are consistent
with truncated milliseconds, but our main calculations do not require that
interpretation. A nominal sample clock is still not hardware exposure timing.

## A joint angle from three landmarks
Take shoulder A, elbow B, and wrist C. The two rays meeting at the elbow are
`u=A-B` and `v=C-B`. Their unsigned angle is

```
cos(theta) = dot(u,v) / (norm(u) * norm(v))
theta_degrees = arccos(cos(theta)) * 180/pi
```

For A=(1,0,0), B=(0,0,0), C=(0,1,0), the dot product is zero and the angle is
90 degrees. For A=(-1,0,0), B=(0,0,0), C=(1,0,0), it is 180 degrees. Translate
all three points by the same vector: the subtraction cancels that translation.
Scale them uniformly by a positive factor: numerator and denominator both gain
the square of that factor. The angle does not change.

This angle is NOT automatically elbow flexion under a clinical anatomical
coordinate convention. Such a convention may define zero at extension and
requires anatomical axes, sign conventions and validation. We call our number
“unsigned shoulder–elbow–wrist angle.” Precise naming prevents overclaiming.

Coincident shoulder and elbow points give a zero-length ray. There is no defined
angle to recover, so the code raises an error rather than assigning zero degrees.
Floating-point division may produce 1.0000000000000002; clipping the cosine to
[-1,1] handles roundoff, not missing landmarks or incorrect identities.

## Run the observed excerpt
The lab converts all four coordinate arrays to metres, calculates the landmark
angles, and prints accepted and rejected velocity intervals. With a strict
one-frame-gap rule, only our adjacent frames 0 and 1 pass. Relaxing the rule to
five frames admits the selected 110–140 intervals. That is an analysis policy;
it does not transform five-frame averages into measured 60 Hz derivatives.

```python
velocity, accepted = interval_velocities(frames, ball_m, fps=60,
                                         max_gap_frames=5)
```

A rejected row is NaN, accompanied by `accepted=False`. Plot accepted points
without connecting across rejected gaps. A smooth connecting line is otherwise
a surprisingly persuasive way to hide unavailable evidence.

## A controlled mistake that you should try
Recompute with the wrong clock of one frame between every record. Compare the
magnitude of the velocities. Then restore the correct clock. Do this only on a
copy labeled “incorrect timing control.” Save both settings so a future reader
cannot mistake the intentionally wrong result for the final analysis.

A short apparent hand–ball distance is not a contact sensor. Pose and ball
estimates can be wrong, the wrist is not the contact patch, and visibility varies.
One must not label our nearest frame as a verified release. There is no independent
per-frame release annotation bundled in this excerpt.

## Go deeper when needed
A derivative is a limit of displacement divided by smaller time intervals.
Finite differences estimate it under assumptions. Differentiating noise can
magnify its influence: independent coordinate noise of standard deviation sigma
makes a two-point velocity error scale like `sqrt(2)*sigma/dt` in a scalar
idealization. This is a derivation for a stated noise model, not an error estimate
for SPL. We have not measured SPL's sigma. Filtering creates another estimator,
with choices about delay, boundaries and future information; S04 investigates that.

## Exercises
1. A 0.2 m displacement occurs over frames 20 to 24 at 40 Hz. Calculate the
average-velocity magnitude for a straight displacement along one axis.
2. Why can a landmark angle stay unchanged after a camera-frame rotation?
3. What should happen when an input ray has length zero?
4. Can a 240 Hz camera specification justify a 240 Hz ball trajectory after
frames were dropped, duplicated or synthesized?

## Worked answers
1. Elapsed time is 4/40=0.1 s; the magnitude is 2 m/s. This does not reveal curved
path length between observations.
2. Orthogonal rotations preserve dot products and norms. They therefore preserve
the ratio defining the angle. Arbitrary projection into an image need not.
3. Mark it undefined or stop explicitly. A fabricated zero would be a false
anatomical statement, not a harmless numerical default.
4. No. Audit actual timestamps, observed versus derived frames, gaps and identity.
A device mode is not proof of end-to-end effective temporal resolution.

## Mastery gate
Derive the angle, calculate one time interval by hand, explain every rejected
interval, and distinguish velocity, speed, displacement and path length. Delayed
recall: explain how higher fps can make unfiltered differentiation noisier even
though it offers finer time sampling.


---

Source: `sports_v8/lessons/S02.md`

# S02 — A flight model is a hypothesis to test

## Your destination
Fit a transparent vertical-motion model, compare fitting residuals with later
points, and explain why a plausible parabola does not validate a reconstruction.
Core Stage 21 introduces rates; Stages 23–26 distinguish physical equations,
integration schemes and learned models. We deliberately begin with least squares.

## Derive the model before training anything
Assume vertical acceleration is constant and equals -g, with upward positive.
Integrating once gives `v(t)=v0-g*t`; integrating again gives
`z(t)=z0+v0*t-g*t²/2`. Three parameters appear if g is unknown; two if g is fixed.
Set time zero at the first fitting observation to improve numerical conditioning.
The parameter v0 is velocity at this chosen reference time, not necessarily release
velocity. A change in origin of time changes its interpretation.

For z0=2 m, v0=4 m/s, g=9.81 m/s² and t=0.2 s, height is
`2 + 0.8 - 0.1962 = 2.6038 m`. The value 9.81 is our conventional illustrative
near-Earth assumption; it is not a measured acceleration of this athlete's ball.

Write the free fit as `z = a + b*u + c*u²`. Each row of the design matrix is
`[1,u,u²]`. Least squares selects coefficients minimizing the sum of squared
height residuals. Then `g_fit=-2*c`. The fitted curvature can absorb tracking
error, time error, unmodelled forces, collisions or a bad window. Calling it an
estimate of physical gravity without qualification would hide these alternatives.

## The explicit observed-data window
We select frames 110,115,120,125,130 for fitting. We examine 135 and 140 as later
points of the same shot. These choices are documented, visible demonstration
choices—not a preregistered independent athlete experiment. The provider warns
that the ball can be noisy near entry to and exit from the capture volume.

The calculation compares three transparent alternatives:

1. Constant height at the last fitting observation.
2. Fixed-gravity parabola with fitted height and velocity.
3. Free quadratic with fitted curvature as well.

The free fit can improve fit error simply because it has more flexibility. The
later-point error is informative but only concerns two selected values in one
trial. It does not establish population performance, a release detector, or a
measurement-system calibration.

The notebook saves coefficients, fitting row IDs, evaluation row IDs, residuals,
and height predictions. It also evaluates sensitivity to a wrong sampling rate.
These outputs are more useful than one smooth curve with no experiment record.

## Timing and unit counterexamples
If all times are multiplied by c while positions stay unchanged, the same
quadratic path can be fitted with velocity divided by c and acceleration divided
by c². Low residuals alone cannot identify the true clock scale. Likewise, using
feet as if they were metres scales all coefficients by approximately 3.28.
A model may fit the wrong physical quantities almost perfectly.

When source values leave the capture volume, do not extend the model across a
catch, bounce or uncertain tracking segment and call it one uninterrupted flight.
We intentionally keep frames 180 and 210 as visible examples of the broader
record, but do not include them in our short fitting window.

## How this connects to HNNs, PINNs and world models
A Hamiltonian neural network represents a structured vector field, and a PINN
penalizes differential-equation residuals. Neither method supplies missing
measurement metadata. A model trained on markerless estimates learns through
those estimates and their selection process. It needs conventional baselines,
independent trials and a justified observation-noise model.

The supplied HNN/LNN learning source frames the sequence as data, learned
physical structure, derived dynamics and prediction. We retain that pathway in
the earlier course. This lab adds an original adequacy check; it does not claim
to reproduce the source's networks or validate their application to free throws.

## Hands-on sequence
First run the manufactured exact trajectory: its known coefficients should be
recovered to numerical precision. Next run the selected observed points. Then
change the fitting window, clock and model class one at a time. Keep a table
with the changed assumption, fitted coefficients, later errors and explanation.
Never modify the saved source excerpt to make the fit improve.

## Exercises
1. Why are at least three distinct time values necessary for an unconstrained
quadratic fit? What does having exactly three points fail to test?
2. A wrong clock doubles every elapsed time. What happens to fitted g?
3. Why is a two-point continuation check different from an unseen-athlete test?
4. What additional evidence would support an actual release-speed claim?

## Worked answers
1. Three coefficients require three independent design columns. Exactly three
points can interpolate a quadratic with zero residual, leaving no redundancy to
examine lack of fit. More points do not automatically make the assumptions true.
2. The fitted coefficient becomes g/4, while the geometric parabola can still fit.
3. The same athlete, session, shot and measurement system are shared. A broader
claim needs independent trials and grouping that matches the intended use.
4. Independently annotated release timing, validated coordinates and timebase,
appropriate post-release observations, uncertainty, and held-out physical checks.
A named parameter in a polynomial is not that evidence.

## Mastery gate
Explain the columns of the design matrix, every parameter's units, the time
origin and the meaning of each residual. Delayed recall: give an example where
excellent fit error is compatible with incorrect metres or seconds.


---

Source: `sports_v8/lessons/S03.md`

# S03 — Shape of a player profile is not shape on a pitch

## Your destination
Build a tiny point cloud from real football profile measurements, calculate its
persistent homology, and state precisely what the points and distances mean.
Read core Stages 06–09 for the full hand calculation and reduction algorithm.
The lab can be viewed earlier; its algebra is not a prerequisite for opening a table.

## Decide what one point represents
A point need not be a physical location. Here one point is a published
player/team/season/position profile. Its selected coordinates are distance-related
summary features. Our 12 rows represent 8 player IDs. The provider filters the
season aggregates to performances above 60 minutes. These are therefore selected
summaries, not every minute played by every athlete.

The README calls the aggregates player-season data. Direct inspection shows
repeated IDs across positions in this excerpt; we retain the finer observed row
grain rather than silently collapsing the records. Exact averaging and weighting
should be checked against the full provider definitions before using these numbers
as season totals. The notebook never treats `total_distance_full_all` as a sum
across the entire season. `count_match` is not a sample weight by default.

For our descriptive cloud, select `running_distance_full_all`,
`hsr_distance_full_all`, and `sprint_distance_full_all`. These quantities summarize
different speed regimes; the official glossary defines the thresholds and the
distance categories. They are not x,y,z positions. A coordinate-frame rotation
of a pitch is therefore not the same thing as mixing these feature columns.

## Why scaling changes a question
Euclidean distance computes the square root of the sum of squared coordinate
differences. A feature with a larger numerical range can dominate that sum.
For a training-reference standardization, set

```
standardized_feature = (value - fitting_mean) / fitting_standard_deviation
```

A deviation of one then means one fitting-set standard deviation for that column.
This is a deliberate new metric, not a neutral improvement to all questions.
Changing metres to centimetres uniformly across all distance columns scales every
Rips birth and death. Standardizing each column separately changes relative weights
and can change which features appear. The lab reports both choices.

The full twelve-row profile cloud is an explicitly exploratory calculation. A
separate small group partition is used only to demonstrate training-only fitting
of preprocessing. No sports prediction accuracy is estimated on this excerpt.

## Rips complexes in the smallest useful example
For four corners of a unit square, edges appear at distance one. The four
perimeter edges form a loop. At sqrt(2), both diagonals and the filled triangles
appear. Thus its H1 interval is `[1,sqrt(2))` under our maximum-edge convention.
The function `cloud_diagrams` reuses the course's F2 boundary reduction and builds
through triangles so H1 classes can die. A graph-only clique omission would give
a different mathematical object.

The notebook first verifies this square, then uses the real profile cloud. A
long-lived profile feature is a property of the selected observations and metric.
It is not a tactical formation, a physical void, or evidence that a coach intended
a particular shape. The rows are not simultaneous positions from a match.

## Order and invariance
Permuting rows changes names in the implementation but not the distance-based
barcode. A rigid transform of a Euclidean coordinate cloud preserves distances.
A uniform positive scale factor multiplies barcode coordinates by that factor.
These are exact mathematical controls; arbitrary feature standardization is not
one of those invariances.

For a moving squad, one cloud per timestamp loses temporal identity unless you
also preserve track IDs and time. A path traversed forward and backward has the
same unparameterized point set. Persistence alone cannot distinguish those motion
directions. A state representation that includes time or velocity changes the
metric and requires a justified scale between its components.

## Bridge to actual tracking
The optional SkillCorner XY adapter accepts provider frame records and respects
`is_detected`. Its tests use manufactured schema examples, not a downloaded match.
The full tracking file encountered during this build was a Git LFS pointer to a
roughly 97 MB object. A pointer is metadata, not the object. Current body-pose data
are larger still. Acquisition and independent validation are explicit next steps.

For actual tracking, write down observed/extrapolated policy, identity scope,
pitch dimensions, attack direction, missing-player rules and the timestamp.
Compare detected-only clouds with all-provider clouds as a missingness sensitivity
analysis. Neither policy automatically yields a complete ground-truth team.

## Exercises
1. Why can a “hole” in three distance-summary features not be drawn as a hole
between football players on the field?
2. What does changing all metres to centimetres do to a Rips barcode?
3. What breaks when scaling means are fitted using future test observations?
4. Why can a forward and a backward movement have identical point-cloud persistence?

## Worked answers
1. The axes describe athlete profiles, not simultaneous field positions. Their
units, observation grain and generating process differ.
2. All finite birth/death coordinates multiply by 100 if the same distance rule
is used. The numerical units change; the combinatorial sequence is reparameterized.
3. The representation gains information from the evaluation set. The result no
longer measures the complete previously fixed training procedure on unseen input.
4. An unordered point set discards order. Direction is information that must be
represented and tested separately, not recovered from a barcode by interpretation.

## Mastery gate
Derive the square interval, identify the exact selected feature columns and
scaling policy, explain repeated IDs and reject one tempting unsupported claim.
Delayed recall: construct two sequences with the same point set and different order.


---

Source: `sports_v8/lessons/S04.md`

# S04 — Time, missingness and uncertainty change the evidence

## Your destination
Separate an observed value from a derived estimate, avoid future information in
a live calculation, and test a mathematically justified perturbation bound without
pretending to know the measurement system's true error distribution. Connect this
to core Stages 10, 15 and 18–19.

## An observation is not a complete continuous trajectory
The sample contains gaps. Between two recorded points, many continuous paths are
possible. Linear interpolation chooses a straight segment; a last-value hold
chooses a constant segment. Both are estimators. Drawing either densely does not
increase the number of independent observed frames.

For a live query at time q, a past-only hold selects the last sample with
`t_i <= q`. It rejects the result when `q-t_i` exceeds a declared age threshold.
For observations `(0,10), (1,20), (2,30)` and q=1.5, the hold returns 20, while
linear interpolation between 1 and 2 returns 25. The interpolation uses the
sample at time 2, which has not yet arrived at time 1.5. It may be appropriate
for offline reconstruction, but not for that live decision.

The notebook retains source-row indices for every held value. An unavailable
answer has index -1 and a NaN value. It does not silently borrow a later point.
The worked S04 lab also illustrates a short stale-age threshold on the sparse
basketball excerpt. Some queries legitimately have no answer.

## Where the timestamp belongs
Capture time, estimated scene time, arrival time, model completion time and screen
display time are different. A source at nominal scene time 1.0 may arrive at 1.2.
Our simple hold assumes values are available at their recorded source time; a
real system must add availability/arrival times. Record that assumption rather
than claiming the teaching function is a production streaming service.

A fixed camera frame rate cannot correct an identity swap. Likewise, smoothing
coordinates cannot show that an occluded hand touched a ball. For an interaction
hypothesis, retain IDs, visibility, time bounds, supporting frames, and whether
the event was observed or inferred. The previously supplied interaction source
motivates this separation; our exercises do not reproduce its event detector.

## A perturbation experiment with a known assumption
Take the finite point cloud X and create Y by adding small artificial offsets.
Let `delta=max_i ||X_i-Y_i||`. By two triangle inequalities,

```
abs(||X_i-X_j|| - ||Y_i-Y_j||) <= ||X_i-Y_i||+||X_j-Y_j|| <= 2*delta.
```

Every Rips simplex's filtration value is the maximum of its edge lengths. With
the same labeled vertices, those values therefore differ by at most 2*delta.
For these finite filtrations, the corresponding persistence-diagram stability
bound is consistent with that perturbation. The notebook compares finite H1
bars using the existing exact small-diagram bottleneck function and checks the
bound numerically. The general stability theorem is taught in core Stage 10.

Our artificial offsets have a seeded generator and a stated scale. They are not
estimated SPL camera noise, confidence intervals for biomechanics, or a measure
of unseen-athlete accuracy. A sensitivity analysis says how an analysis responds
to a specified perturbation; measurement validation needs independent truth.

## A stability bound is not a usefulness guarantee
If the metric encodes the wrong question, a stable result can still be irrelevant.
If all coordinates are biased by an unrecognized scale factor, a repeatable
algorithm can report repeatable but wrong physical distances. If an occluded
player disappears from a cloud, its vertex set changes; the simple matched-point
argument above is no longer a complete justification. Do not reuse the formula
without checking its assumptions.

Current SkillCorner documentation distinguishes detected and extrapolated XY,
and describes a predicted pose-error radius. Those values are outputs of a
provider model. They are not guaranteed simultaneous coverage for every joint in
a frame, nor a substitute for checking coverage on a suitable held-out dataset.
The full pose data are listed in the catalogue but not bundled or evaluated here.

## Exercises
1. With observations at 0 and 2 seconds, can an interpolation at 1 second be
used in a decision made at 1 second? State an exception and its meaning.
2. Every matched point moves by at most 0.01 m. What edge-distance change bound
follows? Does it prove a selected sports event occurred?
3. Why must a reported nearest-neighbour hold include source time or source row?
4. A smooth trajectory fills fifty missing frames. How many new observations
were measured by that filling operation?

## Worked answers
1. Not when the time-2 sample is unavailable. In offline retrospective analysis
it can be used, explicitly labeled as future-assisted reconstruction.
2. At most 0.02 m under the specified Euclidean matched-point assumptions. It
bounds a mathematical representation's change, not contact, intent or outcome.
3. To audit age, availability, repeated use and whether the decision used future
information. Values without provenance can appear newer than their evidence.
4. Zero. It creates fifty derived values. An uncertainty-aware smoother may be
useful, but the provenance and validation requirements remain.

## Mastery gate
Explain source versus query time, identify unavailable estimates, derive the
2*delta edge bound, and state where that derivation stops applying. Delayed recall:
why does a low bottleneck distance not automatically imply a good sports predictor?


---

Source: `sports_v8/lessons/S05.md`

# S05 — Design the evaluation before building the predictor

## Your destination
Distinguish unseen frames, shots, sessions, athletes and venues; keep preprocessing
inside training; and propose a valid full-data experiment without manufacturing
accuracy from our tiny excerpts. This applies equally to patients, machines,
companies and households in the retained industry cases.

## The prediction question determines the split
“Will the next frame look similar?” and “Will this work on a new athlete?” are
different questions. A random frame split can place neighbouring moments of the
same shot in training and testing. A random shot split may still share the same
athlete. A player-level split tests one kind of transfer but can share the venue,
measurement hardware and session conditions. No split removes every form of
shared structure; describe the population to which the result pertains.

For a pre-release free-throw prediction, specify the decision cutoff and permitted
inputs first. Final outcome, hoop landing location and final entry angle are
labels or future information. A retrospectively detected release time may itself
use later frames. Calling all features “pre-release” by their array position does
not establish availability. If using post-release evidence, rename the task.

The SPL documentation lists stable athlete IDs across sessions. Therefore
P0001 in two sessions must remain the same group for an unseen-athlete evaluation.
With the full five-participant recent session, leave-one-athlete-out evaluation
has only five athlete test groups; hundreds of frames do not increase that group
count. Hyperparameter tuning and any calibration need a separate training-only
or nested procedure, and uncertainty should reflect the real grouping.

## A concrete group exercise on actual profile IDs
The twelve football profile rows contain eight unique IDs. In the worked notebook
we assign player IDs [211,218,2759,2858] to a training-reference group, [4322,4792]
to a validation-reference group, and [5468,5521] to a test-reference group. This is
an explicit demonstration of index construction, NOT a performance benchmark.

The partition function requires nonempty, disjoint sets that cover all observed
IDs. Repeated position rows travel with their player. It rejects an overlap
rather than resolving it silently. Then standardization fits means and standard
deviations on training rows only. A repeated player's additional position can
change that player's weight in fitting; document that rather than equating rows
with equally weighted independent athletes.

Compare the training-only means with means calculated on all rows. They usually
differ. The latter could leak evaluation information even though it never looks
at a label. The leakage operation is a deliberately labeled control, not a
recommended preprocessing shortcut.

## Do not train on the demonstration excerpt just to print accuracy
The basketball excerpt supplies one outcome and one athlete. The football subset
is biased by source ordering and is very small. These data are excellent for
schema inspection, hand calculations, invariance checks and execution. They
cannot answer the independent sports performance questions we actually care
about. The notebook consequently prints split counts and preprocessing diagnostics,
not an inflated classifier score.

## A full-data protocol you can execute later
After acquiring a suitable release and accepting its actual terms, freeze a
manifest of athlete/session/trial IDs and source hashes. Pick a prediction time
and outcome. Start with an intercept or class-frequency baseline, then a small
model using conventional kinematic features. Fit all feature transformations
using training data. Choose parameters using validation data only. Compare
conventional features, topology alone and their combination on identical test
units and cutoffs. Preserve sample-level predictions, not just aggregate scores.

For classification, report an appropriate discrimination measure and probability
quality, class counts, coverage, and group-specific errors where supported. For
regression, compare absolute/squared errors against a meaningful constant or
persistence baseline. For events, use event matching, timing error and false
alarms rather than only frame accuracy. Larger valid effects are not guaranteed;
a negative result is a successful learning outcome when the design is sound.

Do not repeatedly tune against the same test set after reading its errors. An
exposed demonstration partition is not a new independent holdout in the next
version of a notebook. Maintain a fresh experimental question or fresh test units.

## Rights and participants are part of the protocol
SPL excerpts and derivatives are noncommercial/share-alike. SkillCorner has a
repository MIT license, retained with its selected excerpt. Video resources may
have separate terms for data, code and weights. The current OpenBiomechanics data
license has additional restrictions; its MIT code license does not override them.
These are recorded source terms, not permission from this course to use data in
commercial World Model Sports products. No scraped private athlete information or
new identity inference is needed for this learning path.

## Exercises
1. A player has twenty trials; fifteen train and five test. What transfer can
this design not establish?
2. Why can label-free PCA or standardization still create leakage?
3. Which fields of the SPL trial must be excluded from a pre-release predictor?
4. Does accepting a code repository's MIT license automatically license its
videos, third-party weights and noncommercial movement data?

## Worked answers
1. It does not establish unseen-player performance. It may evaluate within-player
trial transfer if all other availability and grouping conditions are appropriate.
2. Evaluation observations influence the learned representation. Fit it inside
the training partition or each training fold, not once before splitting.
3. At minimum final result, hoop landing values and final entry angle; also exclude
any future-assisted feature or annotation unavailable by the chosen cutoff.
4. No. Check each artifact's terms and provenance independently. Keep restrictions
attached to copied data and derived products as required.

## Mastery gate
Write a protocol with observation grain, decision time, allowed inputs, grouping,
three partitions, baseline, metric and uncertainty unit. Delayed recall: explain
why even a perfectly disjoint split can answer the wrong scientific question.


---

Source: `sports_v8/lessons/S06.md`

# S06 — From worked examples to an independent sports study

## Your destination
Choose an appropriate current sports dataset, explain its observation model,
acquire only a bounded slice after reviewing rights, and complete a defensible
study. “Modern” describes methods and releases; it does not make every dataset
suitable or more accurate. The registry was checked on 2026-09-21 and is not an
exhaustive claim about every release in the world.

## Four questions before downloading
**What is measured?** Video pixels, marker trajectories, markerless estimates,
provider-derived events and simulator states are different evidence. A rendered
depth map has exact simulator geometry but does not measure a real athlete.

**What is the independent unit?** A player, trial, session, match, camera pair or
venue may matter. Multi-view images of the same event must not be split across
partitions as though they were unrelated photographs.

**What do I want to infer?** A track ID, on-ground player position, airborne ball
height, movement class, release event and injury risk require different labels.
A dataset with pose labels but no outcomes cannot test an outcome classifier.

**What is actually licensed?** A freely reachable URL is not a general commercial
license. Verify code, data, model weights, derivative conditions, participant
consent and the intended application. Keep separate storage for restricted data.

## A bounded selection route
For interpretable basketball biomechanics, start with the recent SPL release and
its documentation. For 3x3 video identity and tracking, examine TrackID3x3. For
wearable/video alignment, inspect BasketHAR's 2026 paper and hosting. For multiview
mobile capture, MUVS is relevant; for user-generated multi-object tracking, UVY is
a different dataset with a different purpose. For soccer, SkillCorner separates
season aggregates, XY tracks and pose, while SoccerTrack v2 and SoccerNet GSR
support specific annotated reconstruction tasks. For baseball, consult current
OpenBiomechanics documentation rather than an old pre-July-2026 clone recipe.

The full catalogue explains access, dates, units, limitations, baseline, split
and output for each. Only the two small sports excerpts have been bundled and
executed here. No downloaded videos, full tracks, wearables or baseball datasets
are implied by a catalogue entry. BASKET-Multiview is deliberately marked synthetic.

## Your minimum viable independent experiment
Pick ONE question. For example: “Do topological descriptors of movement windows
add information to conventional features for this specific available label?”
Start with enough independent trials/people to design a real evaluation; our
single basketball trial is not that experiment.

Create a protocol with the input contract, target, cutoff, groups, preprocessing,
baseline, proposed descriptor, and acceptance criteria. Do not define success as
“topology must win.” Define success as a reproducible, appropriately evaluated
answer with documented limitations. Set aside independently grouped test data
before inspecting its outcomes. Store exact source revisions and exclusions.

First reproduce a simple baseline. Inspect a few raw observations against their
metadata and labels. Next implement one descriptor and test exact controls.
Finally compare on identical test units. Report the result, computational cost,
coverage and the conditions under which it fails. Changing one component at a
time makes the comparison interpretable; adding every modern architecture at once
makes it harder to learn why the result occurred.

## A full deliverable, not just a notebook
Your independent folder should contain: a protocol written before evaluation;
a data manifest and dictionary; acquisition instructions; environment versions;
source-level split assignments; tests; a notebook with outputs; prediction or
reconstruction files; a short interpretation; and a list of open questions.
Private raw video need not be copied into the report. Use consent and access
controls appropriate to the people and setting.

When learning with this chat, bring the protocol, failing test or one bounded
result table—not thousands of unrelated logs. We can review the definition,
calculation, implementation and interpretation separately. The evidence record
should distinguish “read”, “solved with help”, “independently demonstrated” and
“retained after a delay”. A green program run is not a passing oral explanation.

## Capstone review rubric
State all units and frames. Explain where every label comes from. Demonstrate a
known-answer mathematical test and one deliberately failing case. Show that
preprocessing and parameter selection do not inspect held-out outcomes. Explain
whether the claimed accuracy is relative to human labels, provider estimates,
independent physical measurements or simulator truth. Report rejected/missing
samples as well as accepted ones. Check rights before proposing a deployment.

For a geometry study, use fit references and different validation references;
check scale and timing, not only reprojection. For an event study, count false
releases and timing errors on independently labeled clips, including near-contact
negatives. For a dynamic model, compare long-rollout state and phase error with
energy and constraints separately. These requirements connect the earlier source
posts to an auditable experiment without adopting their claims uncritically.

## Exercises
1. Name one modern dataset suitable for mobile multiview data and one suited to
wearable alignment. Why are their annotations not interchangeable?
2. Why should a simulated basketball dataset remain useful but separate from
measured calibration evidence?
3. A full source download has a different Git hash from the record. What happens?
4. What makes a course complete for its agreed scope without claiming all
mathematics or all possible applications have been exhausted?

## Worked answers
1. MUVS and BasketHAR respectively. Camera selection/synchronized viewpoints and
activity-related multimodal signals support different targets and evaluations;
verify actual release labels before designing the study.
2. Known simulator geometry enables exact checks and controlled variations, but
rendering/domain assumptions do not validate real camera or athlete measurements.
3. The verifier stops. Inspect whether the upstream revision changed or the bytes
are incorrect; create a new audited manifest only after reviewing the difference.
4. Demonstrated competence on the agreed concepts, independent work, retained
understanding and explicit remaining proof/book/application obligations. More
files alone do not establish that outcome.

## Delayed recall and completion
Without notes, explain why the newest dataset need not be the right first dataset.
Write a one-page independent protocol and defend two ways your result could be
wrong. The final core-book audit and specialized proofs remain visible in the
retained course. Finish this path by demonstrating understanding, not by resetting
your progress when a new archive version arrives.


---

Source: `sports_v9/lesson.md`

# ACB readiness lab — what a modern sports dataset actually contains

## Begin with the question, not the algorithm
Imagine you receive three folders: game metadata, tracking frames and season aggregates. They describe the same competition, but they do not contain the same observations. A row in a match catalog is one game. A tracking line is one frame. A player-team-season row summarizes many events. Treating all of these as interchangeable can create double counting and misleading evaluation before a neural network is involved.

This lab adds the complete **ten-game metadata catalog** from SkillCorner's ACB 2025–2026 sample release. It is real provider metadata. It does not include those games' tracking streams or event files. The older course's SPL and soccer excerpts remain separate, with their existing acquisition limitations.

## Exact source evidence
The official GitHub connector returned the complete JSON plus blob ID `6db83d7fa75a699270630c02efc330ce8a8d2e2b`. The included UTF-8 bytes were reconstructed from that text and match the Git blob hash exactly. This closes the transcription-integrity check for this specific file. It is not an independent second retrieval, nor verification of the historical game scores against another organization.

See [the data card](sports_v9/DATA_CARD.md) for source and license information. The loader checks both the Git blob ID and the local SHA-256 before parsing.

## 1. Learn an observation unit
The match with ID 114243 has a final home score of 83 and away score of 68. Its final margin is 83 − 68 = 15 points. That is an observed outcome recorded by the provider, not an input that would have been available before tip-off.

The catalog has ten rows, not 293 games, not 327 games and not millions of independent frames. The broader provider documentation describes 293 covered games in the season aggregates and ten sample games with raw files. A sample catalog does not become a full-season dataset because the season label is shared.

**Your check:** count distinct game IDs, seasons, and teams separately. Say which count answers your question. A team can appear in more than one game without creating a duplicate game.

## 2. Time has a role
The metadata's scheduled tip-off is an aware UTC timestamp. It is not a tracking-frame timestamp. A future frame time is not interchangeable with a countdown game clock, which can stop at whistles. Keep scheduled time, elapsed video time, frame index and period/game clock in different fields.

We sort the ten games chronologically and assign six to fitting, two to validation, and two to testing. This demonstrates a game-level split. It does not establish unseen-team evaluation because teams may recur. There are too few selected games for a credible general sports benchmark; do not use a fitted accuracy number to conceal that limitation.

**Hand calculation:** 6 + 2 + 2 = 10. Intersection of any two game-ID sets must be empty. Changing row order must not change the assignment.

## 3. Avoid counting a traded player twice
The provider documents both team rows and a `team_name = total` row for some players. Suppose an invented example has 10 attempts on team A, 5 on team B, and 15 in its total row. Adding all three yields 30; choosing only team rows yields 15. The example is deliberately constructed and is not a claim about any real athlete.

The sum operation applies to additive counts. Do not sum shooting percentages, speeds or per-game averages as if they were counts. To combine a rate, first identify its numerator, denominator and coverage.

A provider alias table may map multiple IDs to a canonical athlete. We resolve explicit mappings and reject cycles. We do not merge athletes merely because their names look similar.

## 4. Tracking is not automatically physical ground truth
The current primer states that player z coordinates are fixed at zero, whereas ball z is positive. Therefore this product does not independently measure player jump height. Detector flags and uncertainty-like fields need their documented meanings; a model's error estimate is not independent calibration truth.

Do not infer airborne metric position from a ground homography. To validate camera geometry, use the earlier camera and holdout lessons. To evaluate motion, obtain the actual tracking payload, determine units and timing, preserve missingness and estimated observations, and compare with independent labels or measurements.

## 5. Source claims versus our experiments
The supplied learning posts discuss manifolds, mechanics and architectural structure. This lab does not validate their broad claims by counting games. It teaches the data contract needed before attempting those applications. The [claims map](docs/v9/CLAIMS_AND_LIMITS.md) points to the specific existing calculations that test narrower mathematical statements.

## Independent work
**A1.** Write a function that counts unique games without treating each opponent as a new observation.

**A2.** Recreate the chronological game assignment. Explain which predictions could be legitimately evaluated and which population remains untested.

**A3.** Implement an alias-chain resolver. Give an example where two mappings form a cycle and explain why the loader should stop.

**A4.** Implement the additive team-row total. Explain why this function must not be reused to sum percentages.

**A5.** Write a pre-acquisition protocol for the full tracking files: required source revision, rights review, bounded download size, compressed-file integrity, IDs, coordinate frame, units, clocks, missingness, split unit, baseline and independent acceptance measurement.

Attempt [the learner notebook](sports_v9/practice/acb_readiness.ipynb) before opening [the reference answers](sports_v9/solutions/acb_readiness.ipynb).

## Completion gate
You can distinguish games, frames, athletes, events and aggregates; keep outcomes out of earlier-time inputs; show a split without shared games; and identify a question that this metadata cannot answer. Passing the code checks is evidence of implementation, not mastery or basketball-model validity.


---

Source: `docs/v9/CLAIMS_AND_LIMITS.md`

# Source statements, mathematical tests and remaining limits

The supplied posts remain attributed source material. This edition does not silently turn promotional statements into proven facts. The author-written lessons are explanatory additions; the numerical reports document actual course experiments, not full-paper reproductions.

| Supplied concept | Source framing | Canonical treatment | What this does not establish |
|---|---|---|---|
| PINN/PIKAN failures | Conflicting residual, boundary and interface gradients; Norm-PCGrad benchmark claims | [Stage 27](physics/lessons/27.md), gradient examples and interface controls | Full 2D/3D benchmark reproduction, universal conflict-free descent or measured negligible overhead. |
| Symplectic structure | Post claims exact arbitrary-step energy conservation and eliminated drift | [Stage 24](physics/lessons/24.md), separate symplectic, energy and state errors | That preserving one geometric property preserves every physical quantity. |
| Manifold projection | Post describes one algebraic correction as returning to the physical manifold | [Stage 25](physics/lessons/25.md), nonlinear residual and iteration checks | One Newton-like correction being exact for a general nonlinear constraint. |
| HNNs and LNNs | Different mechanics formulations related through the Legendre transform | [Stage 23](physics/lessons/23.md), regularity assumptions and restricted teaching networks | A general LNN benchmark or physical validity outside the modeled regime. |
| Charts and flows | Local coordinates, smooth transitions and local diffeomorphisms | [13](lessons/13_lesson.md) and [22](physics/lessons/22.md), explicit map/inverse tests | A camera image being an invertible chart of an entire 3D scene. |
| VGGT and successors | Learned geometry proposed from RGB input | [16](lessons/16_lesson.md), architecture and output contracts | Trained VGGT inference, metrically calibrated output, or independently validated fast sports motion. |
| ROS2/point-cloud speed | Source reports throughput and conversion improvements | [18](lessons/18_lesson.md), CPU profiling and timing boundaries | Reproduction of the post's GPU hardware or latency benchmark. |
| Human–object interactions | Prototype combines pose, tracks and temporal reasoning | [19](lessons/19_lesson.md), timing and negative controls | Proximity proving contact, or independent basketball event precision/recall. |

## A concrete distinction
For a unit-mass oscillator with H=(q²+p²)/2, a kick-then-drift symplectic Euler step from (1,0) with h=0.2 gives p=-0.2 and q=0.96. Its energy is (0.96²+0.2²)/2=0.4808, not 0.5. This is our worked counterexample to a general arbitrary-step exact-energy assertion, not a quotation from the supplied post.

The existing mathematical treatment and source audit are preserved in [the v5 audit](docs/v5/SOURCE_AUDIT.md), [geometry source references](docs/SOURCES_V3.md), and [v8 sports audit](docs/v8/SOURCE_AUDIT.md). Source links are dated; mutable websites can change after review.

## Verification boundaries
A hash verifies identity of bytes relative to the stated expected value. It does not verify the scientific truth of measurements. A notebook run verifies that those code cells executed under the recorded environment. A mathematical theorem requires its hypotheses and proof, not merely many passing numeric checks. An optional acquisition plan is not a downloaded payload.

The original book's complete text has not been inspected. [The book audit](docs/BOOK_TOC_AUDIT_V2.md) remains open. Major theorems and advanced directions are explicitly identified in [proof deepening](docs/DEEPENING_PROOFS.md). Do not mark them complete from file counts.


---

Source: `docs/v9/DEDUPLICATION.md`

# Consolidation: one source, one required route

## What changed
The previous archive contained seven cumulative `COMPLETE_COURSE_V2` through `V8` Markdown exports plus `COURSE_GUIDE.md`. Later volumes embedded earlier volumes and inherited several competing start instructions. These eight files are now short compatibility pointers. A single current `COMPLETE_COURSE.md` exports each selected source once. The canonical home is `START_HERE.html`.

`curriculum/catalog.json` owns the 31 stage IDs, prerequisite order, primary lesson, primary worked notebook, independent assignment, reference answers and optional repair resources. The primary lessons are all unique paths. Old explanations remain available as optional clarification or retrieval practice, not additional mandatory introductory reading.

## What was not thrown away
Original source lessons, workbooks, exercises, solutions, data cards, notebooks and data have been retained. A paragraph audit compares whitespace-normalized blocks from the retired exports against retained Markdown. Compilation-only passages not matched there are preserved once, with the old filenames and hashes, in `reference/compilation_history_v9.json`. This is a mechanical preservation audit, not a claim that all mathematical statements in historical text are correct.

The reader builds one HTML page per source, rather than recreating the same lesson separately under many release versions. Resolvable old rendered paths become lightweight aliases to those pages. Pages without an unambiguous source remain available to avoid silently deleting a unique interactive exercise. Counts and mappings are in `reports/v9/reader_build.json`.

## What “no double information” means here
There is one required lesson per core stage, one named worked notebook, a separate independent attempt, and an answer reference. Repeating a definition in an optional primer, revisiting an idea during delayed recall, and applying it to another dataset are intentional learning activities. We do not claim zero semantic repetition across every historical source, problem statement, or answer.

The combined reading volume is an optional export of canonical sources, not an extra book that must also be completed. Code remains in inspectable modules and notebooks; notebooks importing those modules are not duplicate implementations.

## Which instructions win
Use `docs/v9/FIRST_SESSION.md` for current setup and `docs/v9/VERIFICATION.md` for current evidence. Older verification reports are historical records. Older CLI scripts remain compatibility tools; `scripts/course.py` is the main entry point. Existing progress files keep their original filenames to preserve continuity.


## Measured consolidation

Eight overlapping cumulative Markdown exports were retired, with 388 unmatched compilation-only passages retained in the historical record. 1321 older generated HTML pages are lightweight compatibility aliases. The exact required route contains 31 unique primary lesson paths. The original interactive square explorer and historical browser progress widget remain available rather than being replaced by prose.


---

Source: `docs/release/KUBERNETES.md`

# Kubernetes without making it a prerequisite for mathematics

## What this route is for

Start locally with uv. Use Docker to package the environment. Use Kubernetes only when you want to learn how a scheduler runs the same image as a bounded job and preserves its results. A cluster does not make a theorem correct, remove data leakage, or improve a model by itself.

The supplied deployment is a **single-user, disposable kind-cluster teaching example**, not a production service. It has no public ingress, shared notebook tenancy, billing integration, GPU scheduling, autoscaling, or authentication gateway. Never deploy it to a production context just to follow a lesson.

**Validation levels are separate:** JSON parsing; project policy tests; Kubernetes server-side schema/admission checks; scheduling/PVC binding; actual test and notebook completion; and browser access. This build can execute the first two only. Docker, kubectl, and kind are absent in the build environment. Run the live verifier below to establish the remaining levels on your machine.

## Vocabulary from zero

An **image** is a packaged filesystem plus metadata, not a running machine. A **container** is a process using that image. A **Pod** is Kubernetes' scheduling unit for one or more tightly related containers. A **Job** runs work intended to finish; a **Deployment** maintains a desired number of continuously running Pods. A **Service** supplies stable routing to matching Pods. A **namespace** scopes names; it is not a complete security boundary by itself.

A **PVC** requests persistent storage. Here it retains experiment output across Pod termination. **ReadWriteOnce** concerns attachment on one node; it does not mean exactly one Pod may access the volume. Our reader and job share one claim and are intended for a single-node kind cluster. Multi-node placement, concurrent writers, storage topology, backups, and multi-user ownership require a separate design.

The **context** identifies a cluster/user/namespace combination in your kubeconfig. Always specify the intended context. The provided live verifier rejects context names not starting with `kind-`, requires an absent dedicated namespace, and makes no deletion calls. A name prefix is an accident-prevention guard, not cryptographic proof that a cluster is safe: inspect the server you selected.

## Included resources

`deploy/kubernetes/resources.json` is JSON, which Kubernetes accepts as a manifest format. It contains a Namespace, a 4 GiB PVC, a reader Deployment, a ClusterIP Service, and a Job. `tools/k8s_verify.py` renders a copy with your chosen image, profile, and namespace, then optionally validates/applies it against a live server.

All containers run as UID/GID 1000 with privilege escalation disabled, dropped Linux capabilities, RuntimeDefault seccomp, no mounted service-account token, and a read-only root filesystem. `/tmp` is a bounded scratch volume. `/work` is the persistent result volume. The reader mounts it read-only and never serves it. CPU/memory requests and limits are specified.

The Job does not retry automatically (`backoffLimit: 0`, `restartPolicy: Never`). Its output directory contains the Pod UID, avoiding a retry silently overwriting a previous run. It runs the selected-profile tests and Stage 00, and writes `acceptance.json` with both return codes. A Job timeout or eviction is a failure to investigate, not a license to lower the test bar.

The reader serves only course material. Private paths and directory listings are denied. It is still a development server, not an authenticated public application. The Service is ClusterIP; access it through an explicitly local port-forward. Namespace policy labels are set to Restricted. No network isolation guarantee is made: no NetworkPolicy is bundled, and actual enforcement would depend on the cluster networking implementation.

## Step 1 — Complete the native setup first

From the course directory, install the supported Python/uv prerequisites using the official guides linked below, then:

```bash
python3 tools/bootstrap.py --profile core
uv run --no-sync python course.py check 0
uv run --no-sync python course.py run --stage 0 --output my_work/native_acceptance01
```

The bootstrap must produce a genuine `uv.lock`. Inspect and commit that lock after successful dependency resolution. The observed-version constraints and saved Linux outputs are not a substitute for a resolved dependency graph. An explicit reuse-installed diagnostic environment is not a clean installation.

Use `physics` for the representation training and neural-physics units. Use `full` only when you also need Ripser and GUDHI comparisons and intend to require no skips.

## Step 2 — Build and verify the same image

With a working Docker engine:

```bash
python3 tools/docker_verify.py --profile core --output my_work/docker_acceptance01
```

This executes an actual build/test/Stage-00 sequence. The Compose image tag is `listening-to-shape:11`. Record the image ID after build:

```bash
docker image inspect listening-to-shape:11 --format '{{.Id}}'
```

The tag is convenient for a local lesson but is mutable. For a shared registry, use the resolved image digest and preserve it in the experiment protocol. No digest is invented in this package.

## Step 3 — Use a new, disposable local cluster

Install **kind** and **kubectl** using their official platform instructions. The checked kind quickstart documents v0.33.0; the CI example pins that release, not an unqualified latest download. On a Mac with Homebrew, the quickstart also documents `brew install kind`. Verify `kind version`, `kubectl version --client`, and `docker info` before proceeding.

The following commands explicitly create a local cluster and load the image. They are not run automatically by the Python verifier:

```bash
kind create cluster --name shape-learning
kind load docker-image listening-to-shape:11 --name shape-learning
kubectl --context kind-shape-learning cluster-info
```

Check the displayed endpoint. The default single-node kind storage provisioner is expected for this lesson; a cluster without a default dynamic storage class will leave the PVC Pending. Do not solve that by mounting arbitrary host system directories.

## Step 4 — Inspect before applying

Static checks do not contact a cluster:

```bash
uv run --no-sync python tools/k8s_verify.py \
  --static --namespace shape-lesson01 --profile core \
  --output my_work/k8s_static01
```

Read the rendered `resources.json` and `verification.json`. `static_only` means exactly that. To request live namespace creation, server-side dry-run, apply, rollout, test execution, and log collection:

```bash
uv run --no-sync python tools/k8s_verify.py \
  --context kind-shape-learning --namespace shape-lesson01 \
  --image listening-to-shape:11 --profile core --apply \
  --output my_work/k8s_live01
```

Use a namespace and local evidence directory that do not exist. The script first creates only the Namespace, then checks all resources through server-side dry-run. Even if that later check fails, the new namespace remains for inspection. No existing namespace or PVC is overwritten or deleted by the verifier.

An exit code of 2 means a prerequisite/guard blocked completion. Exit code 1 means a requested check failed. `cluster_verified: true` is only written after the Job completed, both program return codes were zero, and the reader rollout succeeded. It does not claim that all notebooks, GPUs, CNI policies, or production requirements were tested.

## Step 5 — Open the reader and preserve results

```bash
kubectl --context kind-shape-learning -n shape-lesson01 \
  port-forward --address 127.0.0.1 service/course-reader 8000:8000
```

Open `http://127.0.0.1:8000/START_HERE.html`. Stop the port-forward with Ctrl+C. It does not delete results.

In another terminal, inspect the recorded Job output directory in `my_work/k8s_live01/verification.json`. Export its files from the reader Pod, whose `/work` mount sees the retained PVC read-only. For example, first obtain the Pod name, then copy `/work` into a new local folder:

```bash
kubectl --context kind-shape-learning -n shape-lesson01 get pods -l app=course-reader
kubectl --context kind-shape-learning -n shape-lesson01 cp POD_NAME:/work my_work/k8s_export01
```

Replace `POD_NAME` with the actual name; `kubectl cp` requires `tar` inside the image. If unavailable, use a reviewed file-export method rather than exposing the volume publicly. Confirm the exported `acceptance.json`, test XML/log, execution manifest, and notebooks before considering cleanup.

Deleting the namespace deletes its PVC object and may delete the storage according to the provisioner's reclaim policy. Deleting a disposable kind cluster can destroy all its local storage. Cleanup is intentionally manual and not part of the acceptance script.

## Diagnose the first failing layer

| Symptom | Inspect | Do not assume |
|---|---|---|
| `uv.lock` missing | bootstrap logs and package-index/DNS access | A constraints file is a lock |
| `ImagePullBackOff` | image tag/digest, kind image load, platform, registry credentials | Python code has run |
| PVC Pending | default StorageClass, volume events, binding mode | Reapplying fixes storage |
| Pod Pending | requests, node capacity, scheduling events | The model is slow |
| Permission denied | UID/GID, fsGroup, mount path, storage-driver behavior | Running privileged is necessary |
| OOMKilled | limit, actual peak memory, notebook parallelism | A model correctness failure is the cause |
| Job Failed | full logs, return codes, saved partial evidence | A green reader means experiments passed |
| Reader ready but browser blocked | local port-forward, port conflict, browser/network policy | Kubernetes completed navigation testing |
| Re-run refuses a folder | previous evidence and new output name | Existing results should be overwritten |

## Sources
- Kubernetes Jobs: https://kubernetes.io/docs/concepts/workloads/controllers/job/
- Security contexts: https://kubernetes.io/docs/tasks/configure-pod-container/security-context/
- Persistent volumes: https://kubernetes.io/docs/concepts/storage/persistent-volumes/
- kind quickstart: https://kind.sigs.k8s.io/docs/user/quick-start/
- kubectl installation: https://kubernetes.io/docs/tasks/tools/
- uv Docker integration: https://docs.astral.sh/uv/guides/integration/docker/

All commands here describe a proposed local deployment path. Consult the current `VERIFICATION.md` for which portions actually ran in the delivered build.
