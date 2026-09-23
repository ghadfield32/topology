# Conceptual answer criteria: wine

Attempt the questions in the lesson first. These criteria do not automatically assess your work.

## wine.Q1

Why is cultivar not an ordinal quality target?

**Reasoning:** The categories label origins/cultivars, not a numeric quality scale.

## wine.Q2

Why are reference rows excluded from supervised fitting rows in this comparison?

**Reasoning:** It avoids giving training queries a self-reference advantage absent for unseen queries; all models use the same supervised rows.

## wine.Q3

Which six descriptor entries should change under uniform scale multiplication?

**Reasoning:** H0 mean/std/max and H1 maximum/total lifetime scale; the H1 count stays unchanged away from numerical tolerance issues.

## wine.Q4

What new evidence is needed before saying topology improves wine analysis generally?

**Reasoning:** Independent data and a locked selection procedure, with uncertainty and suitable baselines; one exposed split is insufficient.

## Delayed recall: attempt after a gap

### wine.R1

What is one observation here, and when is a row not an independent example?

**Answer criteria:** One wine sample; cultivar is a category, not a quality score.

### wine.R2

How can a training query accidentally get an advantage in a local topology descriptor?

**Answer criteria:** Including the training query itself as a reference point creates an advantage absent for an unseen query. Reserve and freeze the reference set; compare models on identical fitting rows.

### wine.R3

State one unsupported conclusion and the additional evidence needed.

**Answer criteria:** 178 rows, 13 chemistry features, three cultivars. Different from Wine Quality (UCI 186). Name an independent evaluation appropriate to the claim; explain what the existing data do not contain.

