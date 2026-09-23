# Conceptual answer criteria: elnino

Attempt the questions in the lesson first. These criteria do not automatically assess your work.

## elnino.Q1

Why must the reference period accompany an anomaly value?

**Reasoning:** Subtracting a different fitted baseline changes the anomaly without changing the original measurement.

## elnino.Q2

Why is alphabetical month ordering wrong?

**Reasoning:** Calendar order is a semantic property, not the alphabetic order of names.

## elnino.Q3

Can the same 732 values become independent PDE solutions just by creating windows?

**Reasoning:** No; overlapping transformations do not create independent simulation initial conditions or solution fields.

## elnino.Q4

Why must we compare last value and monthly climatology before more complicated models?

**Reasoning:** They encode strong simple persistence/seasonality structure; complexity alone is not evidence of useful prediction.

## Delayed recall: attempt after a gap

### elnino.R1

What is one observation here, and when is a row not an independent example?

**Answer criteria:** One year with twelve monthly regional mean temperatures; the derived long view has one month per row.

### elnino.R2

How do you prevent climatology from seeing future observations?

**Answer criteria:** Fit all twelve monthly means using training years only, then apply them unchanged. Keep sequence order and account for whole-window support at the split.

### elnino.R3

State one unsupported conclusion and the additional evidence needed.

**Answer criteria:** 61 years, 1950–2010, 732 monthly observations. Not an operational forecast or a simulated PDE field. Name an independent evaluation appropriate to the claim; explain what the existing data do not contain.

