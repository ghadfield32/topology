# Dataset card: nile

## Identity and evidence

**Title:** Retrospective change and forward evaluation

**Sector:** water_infrastructure. **Kind:** observed historical data. **Canonical snapshot:** 100 rows.

**Source attribution:** [Cobb (1978), The Problem of the Nile; statsmodels distribution.](https://www.statsmodels.org/stable/datasets/generated/nile.html)

**Reuse basis:** [Public domain (dataset distributor statement)](https://www.statsmodels.org/stable/datasets/generated/nile.html). 

**Acquisition:** offline export from installed package distribution; no invented records, using statsmodels 0.14.6. Primary documentation reviewed 2026-09-20. The current online documentation may describe a newer package release; the files and hashes here identify the actual distribution used.

**Observation unit:** One annual river-volume observation, not an instantaneous discharge-rate sample.

**Limitations:** 100 annual observations, 1871–1970. A detected change is not proof of its physical cause.

## Files and provenance

[Normalized CSV](../../data/industries/nile/data.csv) · [Original package-distribution CSV](../../data/industries/nile/source_distribution.csv) · [Machine-readable metadata](../../data/industries/nile/metadata.json)

Normalized SHA-256: `fa4813b7d95f16c78ca32a909e2de1979ed99959352e29850bcaab1dd8eab982`

Original distribution SHA-256: `88e97bea7249e5832a85e41aec6ce4b8f7b1b14aae930c8363da7f193286b598`

Changes: Preserved loaded values and row order; added zero-based row_id. Calendar fields cast to integers; CO2 datetime index exported as ISO date. Missing CO2 observations remain blank, never zero.

Missing values by column: `{}`. An empty object means none are present, not that real-world measurement uncertainty is zero.

## Complete column dictionary

| Column | Role | Units / encoding | Meaning |
|---|---|---|---|
| `row_id` | metadata | source scale; see data card (not guessed) | row id |
| `year` | metadata | calendar year | 1871–1970. |
| `volume` | response_or_signal | 10^8 m^3 per annual observation | Annual recorded volume; do not label as cubic metres per second. |

## Evaluation and approved learning use

Read the [case lesson](../lessons/nile.md) before the [worked notebook](../notebooks/nile.ipynb). The notebook persists its split, source identifiers, fitted transforms where applicable, predictions and metrics under `reports/v6/industries/nile/`. Its test partition is already exposed in the reference outputs. New tuning requires a new protocol.

The data are suitable for the stated teaching calculation, not certified clinical decisions, trading, process control, dam operations, operational climate forecasting or transport interventions. Scale, age and missing metadata limit claims independently of prediction accuracy.

## Rebuild without inventing records

Normal lessons read the bundled CSV. To intentionally recreate the snapshots install the recorded distributions using the optional `data-rebuild` extra, then run `python scripts/prepare_industry_data.py --replace`. This explicitly overwrites snapshots and requires rerunning every verification. The raw distribution copy allows comparison before and after normalization. No web download is represented as having succeeded.
