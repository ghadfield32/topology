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
