# Dataset card: wine

## Identity and evidence

**Title:** Chemistry, scale and out-of-sample topological descriptors

**Sector:** food_chemistry. **Kind:** observed historical data. **Canonical snapshot:** 178 rows.

**Source attribution:** [Aeberhard and Forina (1992), Wine, UCI Machine Learning Repository.](https://archive.ics.uci.edu/dataset/109/wine)

**Reuse basis:** [CC BY 4.0](https://archive.ics.uci.edu/dataset/109/wine). The normalized snapshot is an adaptation of the distributed source. Attribution, source, license link and changes are recorded here; no endorsement is implied. 

**Acquisition:** offline export from installed package distribution; no invented records, using sklearn 1.8.0. Primary documentation reviewed 2026-09-20. The current online documentation may describe a newer package release; the files and hashes here identify the actual distribution used.

**Observation unit:** One wine sample; cultivar is a category, not a quality score.

**Limitations:** 178 rows, 13 chemistry features, three cultivars. Different from Wine Quality (UCI 186).

## Files and provenance

[Normalized CSV](../../data/industries/wine/data.csv) · [Original package-distribution CSV](../../data/industries/wine/source_distribution.csv) · [Machine-readable metadata](../../data/industries/wine/metadata.json)

Normalized SHA-256: `2f6d6d39c2ba1898b9d254feb78ae575383fac1f9ed735c9aaa9308293568aac`

Original distribution SHA-256: `10e8a802908b34f86e5da8ce962f3c806694bc98450a18f61851af59f324bede`

Changes: Preserved package data values and row order; added zero-based row_id. Normalized CSV serialization; replaced spaces/slashes in sklearn feature names. Provider label codes preserved and mapped explicitly; not original UCI IDs.

Missing values by column: `{}`. An empty object means none are present, not that real-world measurement uncertainty is zero.

## Complete column dictionary

| Column | Role | Units / encoding | Meaning |
|---|---|---|---|
| `row_id` | metadata | source scale; see data card (not guessed) | row id |
| `alcohol` | feature | source scale; see data card (not guessed) | Chemistry measurement: alcohol. Original source does not specify every unit. |
| `malic_acid` | feature | source scale; see data card (not guessed) | Chemistry measurement: malic acid. Original source does not specify every unit. |
| `ash` | feature | source scale; see data card (not guessed) | Chemistry measurement: ash. Original source does not specify every unit. |
| `alcalinity_of_ash` | feature | source scale; see data card (not guessed) | Chemistry measurement: alcalinity of ash. Original source does not specify every unit. |
| `magnesium` | feature | source scale; see data card (not guessed) | Chemistry measurement: magnesium. Original source does not specify every unit. |
| `total_phenols` | feature | source scale; see data card (not guessed) | Chemistry measurement: total phenols. Original source does not specify every unit. |
| `flavanoids` | feature | source scale; see data card (not guessed) | Chemistry measurement: flavanoids. Original source does not specify every unit. |
| `nonflavanoid_phenols` | feature | source scale; see data card (not guessed) | Chemistry measurement: nonflavanoid phenols. Original source does not specify every unit. |
| `proanthocyanins` | feature | source scale; see data card (not guessed) | Chemistry measurement: proanthocyanins. Original source does not specify every unit. |
| `color_intensity` | feature | source scale; see data card (not guessed) | Chemistry measurement: color intensity. Original source does not specify every unit. |
| `hue` | feature | source scale; see data card (not guessed) | Chemistry measurement: hue. Original source does not specify every unit. |
| `od280_od315_of_diluted_wines` | feature | source scale; see data card (not guessed) | Chemistry measurement: od280 od315 of diluted wines. Original source does not specify every unit. |
| `proline` | feature | source scale; see data card (not guessed) | Chemistry measurement: proline. Original source does not specify every unit. |
| `label` | response_or_signal | source scale; see data card (not guessed) | label |

Explicit loader label map: `{"0": "class_0", "1": "class_1", "2": "class_2"}`. These are not automatically the original provider codes.

## Evaluation and approved learning use

Read the [case lesson](../lessons/wine.md) before the [worked notebook](../notebooks/wine.ipynb). The notebook persists its split, source identifiers, fitted transforms where applicable, predictions and metrics under `reports/v6/industries/wine/`. Its test partition is already exposed in the reference outputs. New tuning requires a new protocol.

The data are suitable for the stated teaching calculation, not certified clinical decisions, trading, process control, dam operations, operational climate forecasting or transport interventions. Scale, age and missing metadata limit claims independently of prediction accuracy.

## Rebuild without inventing records

Normal lessons read the bundled CSV. To intentionally recreate the snapshots install the recorded distributions using the optional `data-rebuild` extra, then run `python scripts/prepare_industry_data.py --replace`. This explicitly overwrites snapshots and requires rerunning every verification. The raw distribution copy allows comparison before and after normalization. No web download is represented as having succeeded.
