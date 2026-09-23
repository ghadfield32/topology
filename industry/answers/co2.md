# Conceptual answer criteria: co2

Attempt the questions in the lesson first. These criteria do not automatically assess your work.

## co2.Q1

Why does dropping missing rows distort a fixed weekly lag?

**Reasoning:** Adjacent remaining rows may no longer be seven days apart.

## co2.Q2

What is the target index for length three, end index two, horizon two?

**Reasoning:** Four; only positions zero through two are predictors.

## co2.Q3

How does observed-history one-step testing differ from free-running rollout?

**Reasoning:** Observed-history uses actual prior readings as they arrive; free running feeds predictions back and compounds errors.

## co2.Q4

Why is a seasonal-looking loop not proof of a reconstructed atmospheric attractor?

**Reasoning:** The embedding, sampling, noise, forcing and mathematical recovery assumptions need independent justification.

## Delayed recall: attempt after a gap

### co2.R1

What is one observation here, and when is a row not an independent example?

**Answer criteria:** One weekly date slot, possibly missing a CO2 observation.

### co2.R2

What observations can one forecast window depend on?

**Answer criteria:** Only past finite measurements at the expected weekly spacing. In this strict protocol the full input-to-target support belongs to one raw time block; never interpolate across a held-out boundary silently.

### co2.R3

State one unsupported conclusion and the additional evidence needed.

**Answer criteria:** 2284 slots, 2225 observed values and 59 missing. Snapshot covers 1958–2001, not current CO2. Name an independent evaluation appropriate to the claim; explain what the existing data do not contain.

