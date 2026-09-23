# Dataset card: grunfeld

## Identity and evidence

**Title:** Firm panels, timestamps and prediction availability

**Sector:** business. **Kind:** observed historical data. **Canonical snapshot:** 220 rows.

**Source attribution:** [Grunfeld; 11-firm reconstruction documented by Kleiber and Zeileis (2008); statsmodels distribution.](https://www.statsmodels.org/stable/datasets/generated/grunfeld.html)

**Reuse basis:** [Public domain (dataset distributor statement)](https://www.statsmodels.org/stable/datasets/generated/grunfeld.html). 

**Acquisition:** offline export from installed package distribution; no invented records, using statsmodels 0.14.6. Primary documentation reviewed 2026-09-20. The current online documentation may describe a newer package release; the files and hashes here identify the actual distribution used.

**Observation unit:** One firm-year record. A repeated firm is not a new independent company.

**Limitations:** 220 rows; 11 firms, 1935–1954. Historical data, not investment advice or current-market evidence.

## Files and provenance

[Normalized CSV](../../data/industries/grunfeld/data.csv) · [Original package-distribution CSV](../../data/industries/grunfeld/source_distribution.csv) · [Machine-readable metadata](../../data/industries/grunfeld/metadata.json)

Normalized SHA-256: `69c2ae99098dbc3735e5a10d1855341ea3db6160b1c9890cc33236dca9914df6`

Original distribution SHA-256: `6f6ca138e645eeee6ff3e54fe5b9b498f7ddb5c484237d2a8489c524b3c94098`

Changes: Preserved loaded values and row order; added zero-based row_id. Calendar fields cast to integers; CO2 datetime index exported as ISO date. Missing CO2 observations remain blank, never zero.

Missing values by column: `{}`. An empty object means none are present, not that real-world measurement uncertainty is zero.

## Complete column dictionary

| Column | Role | Units / encoding | Meaning |
|---|---|---|---|
| `row_id` | metadata | source scale; see data card (not guessed) | row id |
| `invest` | response_or_signal | 1947-dollar source scale | Gross investment; no additional millions multiplier is assumed. |
| `value` | feature | 1947-dollar source scale | Year-end market value; not available at the beginning of that same year. |
| `capital` | feature | 1947-dollar source scale | Stock of plant and equipment. |
| `firm` | metadata | category | Company identity; eleven labels. |
| `year` | metadata | calendar year | 1935–1954. |

## Evaluation and approved learning use

Read the [case lesson](../lessons/grunfeld.md) before the [worked notebook](../notebooks/grunfeld.ipynb). The notebook persists its split, source identifiers, fitted transforms where applicable, predictions and metrics under `reports/v6/industries/grunfeld/`. Its test partition is already exposed in the reference outputs. New tuning requires a new protocol.

The data are suitable for the stated teaching calculation, not certified clinical decisions, trading, process control, dam operations, operational climate forecasting or transport interventions. Scale, age and missing metadata limit claims independently of prediction accuracy.

## Rebuild without inventing records

Normal lessons read the bundled CSV. To intentionally recreate the snapshots install the recorded distributions using the optional `data-rebuild` extra, then run `python scripts/prepare_industry_data.py --replace`. This explicitly overwrites snapshots and requires rerunning every verification. The raw distribution copy allows comparison before and after normalization. No web download is represented as having succeeded.
