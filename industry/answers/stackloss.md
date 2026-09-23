# Conceptual answer criteria: stackloss

Attempt the questions in the lesson first. These criteria do not automatically assess your work.

## stackloss.Q1

Why must the holdout be described as source-order rather than a verified operational-time split?

**Reasoning:** No original timestamps are provided to validate the presumed order.

## stackloss.Q2

What changes when scaling is refit in each leave-one-out training fold?

**Reasoning:** The omitted row no longer helps determine feature means/scales, so the experiment respects the held-out information boundary.

## stackloss.Q3

Why can a PINN with a wrong boundary condition still produce low training error?

**Reasoning:** A numerical training fit is not proof that its imposed equations and boundary conditions describe the real plant.

## stackloss.Q4

List four observations needed for an independently testable plant conservation model.

**Reasoning:** Examples include calibrated flow rates, concentrations, temperature units, storage changes, timestamps and actuator/operating conditions.

## Delayed recall: attempt after a gap

### stackloss.R1

What is one observation here, and when is a row not an independent example?

**Answer criteria:** One operating-day measurement in the historical plant table; original timestamps are unavailable.

### stackloss.R2

Why is source order not automatically a forward-time evaluation?

**Answer criteria:** Dates and their validated ordering are absent from the distribution. Call it a source-order holdout, not established temporal forecasting.

### stackloss.R3

State one unsupported conclusion and the additional evidence needed.

**Answer criteria:** 21 records. Cannot support a broad plant-deployment claim or certify a mechanistic model. Name an independent evaluation appropriate to the claim; explain what the existing data do not contain.

