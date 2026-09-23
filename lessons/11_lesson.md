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
