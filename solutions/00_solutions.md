# Stage 00 — Worked solutions

Read after an independent attempt. These answer this course’s original exercises, not graded exercises from an external course.

## 00.1

**Question:** Explain observation, feature, label, and dataset using one handwriting image.

**Worked answer:** An observation is one 8×8 image. Its 64 pixel intensities can be features. The written digit 0–9 is its label. The dataset is the collection of such images and labels. A pixel can instead become an observation in a different, explicitly chosen analysis.

## 00.2

**Question:** What do the two numbers in an array shape mean? What does X[:, 0] select?

**Worked answer:** For a matrix the first number counts rows and the second counts columns. The colon selects every row; zero selects the first column. A 150×4 matrix is not a four-image dataset.

## 00.3

**Question:** Predict whether `3 == 3` and `3 == 4` are true; explain why assignment is different.

**Worked answer:** The comparisons evaluate to True and False. `a = 3` changes the variable binding and does not ask a yes/no question. `a == 3` tests the current value.

## 00.4

**Question:** Why do we run an exact synthetic example before a real-data experiment?

**Worked answer:** An exact example provides an expected answer independent of the program. Real data exercise the method but usually do not reveal the true topology directly. Neither alone provides every kind of validation.

## 00.5

**Question:** What does a passed software test establish, and what does it not establish?

**Worked answer:** It establishes that a specified check passed on the tested inputs in the executed environment. It does not certify all possible inputs, statistical significance, scientific usefulness, or the learner’s understanding.

## 00.6

**Question:** Find the digits split sizes in data/manifest.json and explain why they are not the original UCI split.

**Worked answer:** There are 1,077 training, 360 validation, and 360 test images. All are from scikit-learn’s 1,797-image snapshot, which corresponds to the original UCI test set. This new split is per image; it cannot establish separation by writer.

## Delayed retrieval

In several days, change one number or assumption in two exercises and solve them without reading this file. Explain how the answer changes and why. Record the new questions and your reasoning in the learner ledger.
