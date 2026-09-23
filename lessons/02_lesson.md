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
