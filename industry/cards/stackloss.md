# Dataset card: stackloss

## Identity and evidence

**Title:** Small-sample process monitoring

**Sector:** manufacturing. **Kind:** observed historical data. **Canonical snapshot:** 21 rows.

**Source attribution:** [Brownlee (1965), Statistical Theory and Methodology in Science and Engineering; statsmodels distribution.](https://www.statsmodels.org/stable/datasets/generated/stackloss.html)

**Reuse basis:** [Public domain (dataset distributor statement)](https://www.statsmodels.org/stable/datasets/generated/stackloss.html). 

**Acquisition:** offline export from installed package distribution; no invented records, using statsmodels 0.14.6. Primary documentation reviewed 2026-09-20. The current online documentation may describe a newer package release; the files and hashes here identify the actual distribution used.

**Observation unit:** One operating-day measurement in the historical plant table; original timestamps are unavailable.

**Limitations:** 21 records. Cannot support a broad plant-deployment claim or certify a mechanistic model.

## Files and provenance

[Normalized CSV](../../data/industries/stackloss/data.csv) · [Original package-distribution CSV](../../data/industries/stackloss/source_distribution.csv) · [Machine-readable metadata](../../data/industries/stackloss/metadata.json)

Normalized SHA-256: `6c1de720cdef48f9b5193459e4b584295f9b7fa2c042e70e1e65bbccbe362d60`

Original distribution SHA-256: `7395953d62eec7abab783ae9603ff82f091d04a4689780e455c239f0f5509f64`

Changes: Preserved loaded values and row order; added zero-based row_id. Calendar fields cast to integers; CO2 datetime index exported as ISO date. Missing CO2 observations remain blank, never zero.

Missing values by column: `{}`. An empty object means none are present, not that real-world measurement uncertainty is zero.

## Complete column dictionary

| Column | Role | Units / encoding | Meaning |
|---|---|---|---|
| `row_id` | metadata | source scale; see data card (not guessed) | row id |
| `STACKLOSS` | response_or_signal | 10 × percent | Ammonia escaping the absorption column on the source encoded scale. |
| `AIRFLOW` | feature | source process-rate scale | Rate of plant operation; do not invent a flow unit. |
| `WATERTEMP` | feature | source temperature scale | Cooling-water temperature; no calibrated unit is asserted here. |
| `ACIDCONC` | feature | encoded concentration | Source wording of offset/scaling is ambiguous; preserve encoded values, do not invert the transform. |

## Evaluation and approved learning use

Read the [case lesson](../lessons/stackloss.md) before the [worked notebook](../notebooks/stackloss.ipynb). The notebook persists its split, source identifiers, fitted transforms where applicable, predictions and metrics under `reports/v6/industries/stackloss/`. Its test partition is already exposed in the reference outputs. New tuning requires a new protocol.

The data are suitable for the stated teaching calculation, not certified clinical decisions, trading, process control, dam operations, operational climate forecasting or transport interventions. Scale, age and missing metadata limit claims independently of prediction accuracy.

## Rebuild without inventing records

Normal lessons read the bundled CSV. To intentionally recreate the snapshots install the recorded distributions using the optional `data-rebuild` extra, then run `python scripts/prepare_industry_data.py --replace`. This explicitly overwrites snapshots and requires rerunning every verification. The raw distribution copy allows comparison before and after normalization. No web download is represented as having succeeded.
