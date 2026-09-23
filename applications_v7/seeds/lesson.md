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

[Data card](../../data/v7/seeds/metadata.json) · [Worked lab](lab.ipynb) · [Your coding exercises](learner.ipynb) · [Reference answers](answers.ipynb) · [Questions and answers](questions.md)
