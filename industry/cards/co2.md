# Dataset card: co2

## Identity and evidence

**Title:** Missingness, past-only windows and seasonal shape

**Sector:** environment. **Kind:** observed historical data. **Canonical snapshot:** 2284 rows.

**Source attribution:** [Keeling and Whorf (2004), atmospheric CO2 series, CDIAC; historical statsmodels snapshot.](https://www.statsmodels.org/stable/datasets/generated/co2.html)

**Reuse basis:** [Public domain (dataset distributor statement)](https://www.statsmodels.org/stable/datasets/generated/co2.html). 

**Acquisition:** offline export from installed package distribution; no invented records, using statsmodels 0.14.6. Primary documentation reviewed 2026-09-20. The current online documentation may describe a newer package release; the files and hashes here identify the actual distribution used.

**Observation unit:** One weekly date slot, possibly missing a CO2 observation.

**Limitations:** 2284 slots, 2225 observed values and 59 missing. Snapshot covers 1958–2001, not current CO2.

## Files and provenance

[Normalized CSV](../../data/industries/co2/data.csv) · [Original package-distribution CSV](../../data/industries/co2/source_distribution.csv) · [Machine-readable metadata](../../data/industries/co2/metadata.json)

Normalized SHA-256: `b67fef114ef5c027ad8b5e0aeae76525f218184df64bbf289a7d299a13c14277`

Original distribution SHA-256: `16695fa2786e53414e5a6b54767a3fdf5de99cfbc68617f69d1362d92776a92f`

Changes: Preserved loaded values and row order; added zero-based row_id. Calendar fields cast to integers; CO2 datetime index exported as ISO date. Missing CO2 observations remain blank, never zero.

Missing values by column: `{"co2": 59}`. An empty object means none are present, not that real-world measurement uncertainty is zero.

## Complete column dictionary

| Column | Role | Units / encoding | Meaning |
|---|---|---|---|
| `row_id` | metadata | source scale; see data card (not guessed) | row id |
| `date` | metadata | ISO date | Weekly calendar slot from the loaded index; no intraday timestamp asserted. |
| `co2` | response_or_signal | ppmv | Atmospheric CO2 concentration; blanks are missing. |

## Evaluation and approved learning use

Read the [case lesson](../lessons/co2.md) before the [worked notebook](../notebooks/co2.ipynb). The notebook persists its split, source identifiers, fitted transforms where applicable, predictions and metrics under `reports/v6/industries/co2/`. Its test partition is already exposed in the reference outputs. New tuning requires a new protocol.

The data are suitable for the stated teaching calculation, not certified clinical decisions, trading, process control, dam operations, operational climate forecasting or transport interventions. Scale, age and missing metadata limit claims independently of prediction accuracy.

## Rebuild without inventing records

Normal lessons read the bundled CSV. To intentionally recreate the snapshots install the recorded distributions using the optional `data-rebuild` extra, then run `python scripts/prepare_industry_data.py --replace`. This explicitly overwrites snapshots and requires rerunning every verification. The raw distribution copy allows comparison before and after normalization. No web download is represented as having succeeded.
