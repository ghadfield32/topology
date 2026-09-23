# Conceptual answer criteria: wdbc

Attempt the questions in the lesson first. These criteria do not automatically assess your work.

## wdbc.Q1

Explain why `label == 0` means positive malignancy in this loader but is not a universal label convention.

**Reasoning:** Read the explicit label map; our binary teaching target intentionally maps malignant to one.

## wdbc.Q2

Draw a confusion matrix for an always-benign classifier and calculate both ordinary and balanced accuracy.

**Reasoning:** Balanced accuracy averages the two recalls; ordinary accuracy weights classes by their sample counts.

## wdbc.Q3

Identify the absent identifiers that prevent verifying a hospital-level or patient-level holdout.

**Reasoning:** The snapshot lacks original patient and site identifiers, so a random row split cannot establish either separation.

## wdbc.Q4

Explain why a cohort persistence diagram is not one diagnosis per row.

**Reasoning:** The filtration is constructed from many observations and a selected metric; no individual clinical mechanism follows from it.

## Delayed recall: attempt after a gap

### wdbc.R1

What is one observation here, and when is a row not an independent example?

**Answer criteria:** One digitized fine-needle-aspirate image summary. The scikit-learn snapshot does not retain original IDs.

### wdbc.R2

What does a high score on this partition fail to establish?

**Answer criteria:** The original IDs/sites are absent. This image-summary split is not independent clinical or new-site validation.

### wdbc.R3

State one unsupported conclusion and the additional evidence needed.

**Answer criteria:** 569 rows; 30 features. Educational observational data, not clinical validation. Name an independent evaluation appropriate to the claim; explain what the existing data do not contain.

