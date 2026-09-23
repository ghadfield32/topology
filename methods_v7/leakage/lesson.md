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

[Worked lab](lab.ipynb) · [Learner coding](learner.ipynb) · [Reference answers](answers.ipynb) · [Questions](questions.md)
