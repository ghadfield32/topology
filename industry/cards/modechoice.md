# Dataset card: modechoice

## Identity and evidence

**Title:** Choice sets, group splits and fair baselines

**Sector:** transportation. **Kind:** observed historical data. **Canonical snapshot:** 840 rows.

**Source attribution:** [Greene and Hensher, 1987 intercity mode-choice sample documented in Greene (1997/2011); statsmodels distribution.](https://www.statsmodels.org/stable/datasets/generated/modechoice.html)

**Reuse basis:** [Public domain (dataset distributor statement)](https://www.statsmodels.org/stable/datasets/generated/modechoice.html). 

**Acquisition:** offline export from installed package distribution; no invented records, using statsmodels 0.14.6. Primary documentation reviewed 2026-09-20. The current online documentation may describe a newer package release; the files and hashes here identify the actual distribution used.

**Observation unit:** One alternative offered to one traveler. Four rows form one choice set.

**Limitations:** 840 alternatives, 210 travelers. Choice-based sampling oversamples some modes; not population market shares.

## Files and provenance

[Normalized CSV](../../data/industries/modechoice/data.csv) · [Original package-distribution CSV](../../data/industries/modechoice/source_distribution.csv) · [Machine-readable metadata](../../data/industries/modechoice/metadata.json)

Normalized SHA-256: `be6deb2170ab4c0b4a09319308ec6098a07a1f9ef4418380cfc7bcc6331c3556`

Original distribution SHA-256: `d2d72c1db440f8ffce01f58ed39fc1145569ec1703970dac1636c154fc01fd8e`

Changes: Preserved loaded values and row order; added zero-based row_id. Calendar fields cast to integers; CO2 datetime index exported as ISO date. Missing CO2 observations remain blank, never zero.

Missing values by column: `{}`. An empty object means none are present, not that real-world measurement uncertainty is zero.

## Complete column dictionary

| Column | Role | Units / encoding | Meaning |
|---|---|---|---|
| `row_id` | metadata | source scale; see data card (not guessed) | row id |
| `individual` | metadata | ID | One traveler/choice-set identifier. |
| `mode` | metadata | category | 1 air; 2 train; 3 bus; 4 car. |
| `choice` | response_or_signal | binary | One selected alternative per choice set. |
| `ttme` | feature | minutes | Terminal waiting time, zero for car. |
| `invc` | feature | source dollars | In-vehicle monetary cost; not inflation-adjusted here. |
| `invt` | feature | minutes | In-vehicle travel time. |
| `gc` | feature | source dollars | Generalized cost combining cost and time; excluded to avoid double-counting. |
| `hinc` | feature | source thousands of dollars | Household income. |
| `psize` | feature | persons | Group size in the chosen mode; excluded because availability for prospective choice is uncertain. |

## Evaluation and approved learning use

Read the [case lesson](../lessons/modechoice.md) before the [worked notebook](../notebooks/modechoice.ipynb). The notebook persists its split, source identifiers, fitted transforms where applicable, predictions and metrics under `reports/v6/industries/modechoice/`. Its test partition is already exposed in the reference outputs. New tuning requires a new protocol.

The data are suitable for the stated teaching calculation, not certified clinical decisions, trading, process control, dam operations, operational climate forecasting or transport interventions. Scale, age and missing metadata limit claims independently of prediction accuracy.

## Rebuild without inventing records

Normal lessons read the bundled CSV. To intentionally recreate the snapshots install the recorded distributions using the optional `data-rebuild` extra, then run `python scripts/prepare_industry_data.py --replace`. This explicitly overwrites snapshots and requires rerunning every verification. The raw distribution copy allows comparison before and after normalization. No web download is represented as having succeeded.
