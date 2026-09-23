# Dataset card: elnino

## Identity and evidence

**Title:** Monthly climate records and delay representations

**Sector:** marine. **Kind:** observed historical data. **Canonical snapshot:** 61 rows.

**Source attribution:** [NOAA NWS ERSST.V3B, Niño 1+2; historical statsmodels distribution.](https://www.statsmodels.org/stable/datasets/generated/elnino.html)

**Reuse basis:** [Public domain (dataset distributor statement)](https://www.statsmodels.org/stable/datasets/generated/elnino.html). 

**Acquisition:** offline export from installed package distribution; no invented records, using statsmodels 0.14.6. Primary documentation reviewed 2026-09-20. The current online documentation may describe a newer package release; the files and hashes here identify the actual distribution used.

**Observation unit:** One year with twelve monthly regional mean temperatures; the derived long view has one month per row.

**Limitations:** 61 years, 1950–2010, 732 monthly observations. Not an operational forecast or a simulated PDE field.

## Files and provenance

[Normalized CSV](../../data/industries/elnino/data.csv) · [Original package-distribution CSV](../../data/industries/elnino/source_distribution.csv) · [Machine-readable metadata](../../data/industries/elnino/metadata.json)

Normalized SHA-256: `8c15911802ce2973931db0c3d822ae6abe961bfa6bd507cae5eb400beeee9af7`

Original distribution SHA-256: `b647be00e0fd264be9764e317e6b963f35030014ecca2b21b204521716e463ad`

Changes: Preserved loaded values and row order; added zero-based row_id. Calendar fields cast to integers; CO2 datetime index exported as ISO date. Missing CO2 observations remain blank, never zero.

Missing values by column: `{}`. An empty object means none are present, not that real-world measurement uncertainty is zero.

## Complete column dictionary

| Column | Role | Units / encoding | Meaning |
|---|---|---|---|
| `row_id` | metadata | source scale; see data card (not guessed) | row id |
| `YEAR` | metadata | source scale; see data card (not guessed) | YEAR |
| `JAN` | response_or_signal | degrees Celsius | Regional monthly mean sea-surface temperature for JAN. |
| `FEB` | response_or_signal | degrees Celsius | Regional monthly mean sea-surface temperature for FEB. |
| `MAR` | response_or_signal | degrees Celsius | Regional monthly mean sea-surface temperature for MAR. |
| `APR` | response_or_signal | degrees Celsius | Regional monthly mean sea-surface temperature for APR. |
| `MAY` | response_or_signal | degrees Celsius | Regional monthly mean sea-surface temperature for MAY. |
| `JUN` | response_or_signal | degrees Celsius | Regional monthly mean sea-surface temperature for JUN. |
| `JUL` | response_or_signal | degrees Celsius | Regional monthly mean sea-surface temperature for JUL. |
| `AUG` | response_or_signal | degrees Celsius | Regional monthly mean sea-surface temperature for AUG. |
| `SEP` | response_or_signal | degrees Celsius | Regional monthly mean sea-surface temperature for SEP. |
| `OCT` | response_or_signal | degrees Celsius | Regional monthly mean sea-surface temperature for OCT. |
| `NOV` | response_or_signal | degrees Celsius | Regional monthly mean sea-surface temperature for NOV. |
| `DEC` | response_or_signal | degrees Celsius | Regional monthly mean sea-surface temperature for DEC. |

## Evaluation and approved learning use

Read the [case lesson](../lessons/elnino.md) before the [worked notebook](../notebooks/elnino.ipynb). The notebook persists its split, source identifiers, fitted transforms where applicable, predictions and metrics under `reports/v6/industries/elnino/`. Its test partition is already exposed in the reference outputs. New tuning requires a new protocol.

The data are suitable for the stated teaching calculation, not certified clinical decisions, trading, process control, dam operations, operational climate forecasting or transport interventions. Scale, age and missing metadata limit claims independently of prediction accuracy.

## Rebuild without inventing records

Normal lessons read the bundled CSV. To intentionally recreate the snapshots install the recorded distributions using the optional `data-rebuild` extra, then run `python scripts/prepare_industry_data.py --replace`. This explicitly overwrites snapshots and requires rerunning every verification. The raw distribution copy allows comparison before and after normalization. No web download is represented as having succeeded.
