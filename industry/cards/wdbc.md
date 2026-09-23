# Dataset card: wdbc

## Identity and evidence

**Title:** Cell-image measurements and honest classification

**Sector:** healthcare. **Kind:** observed historical data. **Canonical snapshot:** 569 rows.

**Source attribution:** [Wolberg, Mangasarian, Street and Street (1993), Breast Cancer Wisconsin (Diagnostic), UCI.](https://archive.ics.uci.edu/dataset/17/breast+cancer+wisconsin+diagnostic)

**Reuse basis:** [CC BY 4.0](https://archive.ics.uci.edu/dataset/17/breast+cancer+wisconsin+diagnostic). The normalized snapshot is an adaptation of the distributed source. Attribution, source, license link and changes are recorded here; no endorsement is implied. 

**Acquisition:** offline export from installed package distribution; no invented records, using sklearn 1.8.0. Primary documentation reviewed 2026-09-20. The current online documentation may describe a newer package release; the files and hashes here identify the actual distribution used.

**Observation unit:** One digitized fine-needle-aspirate image summary. The scikit-learn snapshot does not retain original IDs.

**Limitations:** 569 rows; 30 features. Educational observational data, not clinical validation.

## Files and provenance

[Normalized CSV](../../data/industries/wdbc/data.csv) · [Original package-distribution CSV](../../data/industries/wdbc/source_distribution.csv) · [Machine-readable metadata](../../data/industries/wdbc/metadata.json)

Normalized SHA-256: `67a1bb2aa650da2ba7c76b5f64e1a180e00f50dcb0e91a2650be35d6251116dd`

Original distribution SHA-256: `fed3eb72d0575ef6192293f5093c6e801b1476b577d0386bf4455504522172ed`

Changes: Preserved package data values and row order; added zero-based row_id. Normalized CSV serialization; replaced spaces/slashes in sklearn feature names. Provider label codes preserved and mapped explicitly; not original UCI IDs.

Missing values by column: `{}`. An empty object means none are present, not that real-world measurement uncertainty is zero.

## Complete column dictionary

| Column | Role | Units / encoding | Meaning |
|---|---|---|---|
| `row_id` | metadata | source scale; see data card (not guessed) | row id |
| `mean_radius` | feature | source image/derived scale; physical calibration not specified in the cited summary | Image-derived nuclear mean radius; not a raw medical image. |
| `mean_texture` | feature | source image/derived scale; physical calibration not specified in the cited summary | Image-derived nuclear mean texture; not a raw medical image. |
| `mean_perimeter` | feature | source image/derived scale; physical calibration not specified in the cited summary | Image-derived nuclear mean perimeter; not a raw medical image. |
| `mean_area` | feature | source image/derived scale; physical calibration not specified in the cited summary | Image-derived nuclear mean area; not a raw medical image. |
| `mean_smoothness` | feature | source image/derived scale; physical calibration not specified in the cited summary | Image-derived nuclear mean smoothness; not a raw medical image. |
| `mean_compactness` | feature | source image/derived scale; physical calibration not specified in the cited summary | Image-derived nuclear mean compactness; not a raw medical image. |
| `mean_concavity` | feature | source image/derived scale; physical calibration not specified in the cited summary | Image-derived nuclear mean concavity; not a raw medical image. |
| `mean_concave_points` | feature | source image/derived scale; physical calibration not specified in the cited summary | Image-derived nuclear mean concave points; not a raw medical image. |
| `mean_symmetry` | feature | source image/derived scale; physical calibration not specified in the cited summary | Image-derived nuclear mean symmetry; not a raw medical image. |
| `mean_fractal_dimension` | feature | source image/derived scale; physical calibration not specified in the cited summary | Image-derived nuclear mean fractal dimension; not a raw medical image. |
| `radius_error` | feature | source image/derived scale; physical calibration not specified in the cited summary | Image-derived nuclear radius error; not a raw medical image. |
| `texture_error` | feature | source image/derived scale; physical calibration not specified in the cited summary | Image-derived nuclear texture error; not a raw medical image. |
| `perimeter_error` | feature | source image/derived scale; physical calibration not specified in the cited summary | Image-derived nuclear perimeter error; not a raw medical image. |
| `area_error` | feature | source image/derived scale; physical calibration not specified in the cited summary | Image-derived nuclear area error; not a raw medical image. |
| `smoothness_error` | feature | source image/derived scale; physical calibration not specified in the cited summary | Image-derived nuclear smoothness error; not a raw medical image. |
| `compactness_error` | feature | source image/derived scale; physical calibration not specified in the cited summary | Image-derived nuclear compactness error; not a raw medical image. |
| `concavity_error` | feature | source image/derived scale; physical calibration not specified in the cited summary | Image-derived nuclear concavity error; not a raw medical image. |
| `concave_points_error` | feature | source image/derived scale; physical calibration not specified in the cited summary | Image-derived nuclear concave points error; not a raw medical image. |
| `symmetry_error` | feature | source image/derived scale; physical calibration not specified in the cited summary | Image-derived nuclear symmetry error; not a raw medical image. |
| `fractal_dimension_error` | feature | source image/derived scale; physical calibration not specified in the cited summary | Image-derived nuclear fractal dimension error; not a raw medical image. |
| `worst_radius` | feature | source image/derived scale; physical calibration not specified in the cited summary | Image-derived nuclear worst radius; not a raw medical image. |
| `worst_texture` | feature | source image/derived scale; physical calibration not specified in the cited summary | Image-derived nuclear worst texture; not a raw medical image. |
| `worst_perimeter` | feature | source image/derived scale; physical calibration not specified in the cited summary | Image-derived nuclear worst perimeter; not a raw medical image. |
| `worst_area` | feature | source image/derived scale; physical calibration not specified in the cited summary | Image-derived nuclear worst area; not a raw medical image. |
| `worst_smoothness` | feature | source image/derived scale; physical calibration not specified in the cited summary | Image-derived nuclear worst smoothness; not a raw medical image. |
| `worst_compactness` | feature | source image/derived scale; physical calibration not specified in the cited summary | Image-derived nuclear worst compactness; not a raw medical image. |
| `worst_concavity` | feature | source image/derived scale; physical calibration not specified in the cited summary | Image-derived nuclear worst concavity; not a raw medical image. |
| `worst_concave_points` | feature | source image/derived scale; physical calibration not specified in the cited summary | Image-derived nuclear worst concave points; not a raw medical image. |
| `worst_symmetry` | feature | source image/derived scale; physical calibration not specified in the cited summary | Image-derived nuclear worst symmetry; not a raw medical image. |
| `worst_fractal_dimension` | feature | source image/derived scale; physical calibration not specified in the cited summary | Image-derived nuclear worst fractal dimension; not a raw medical image. |
| `label` | response_or_signal | source scale; see data card (not guessed) | label |

Explicit loader label map: `{"0": "malignant", "1": "benign"}`. These are not automatically the original provider codes.

## Evaluation and approved learning use

Read the [case lesson](../lessons/wdbc.md) before the [worked notebook](../notebooks/wdbc.ipynb). The notebook persists its split, source identifiers, fitted transforms where applicable, predictions and metrics under `reports/v6/industries/wdbc/`. Its test partition is already exposed in the reference outputs. New tuning requires a new protocol.

The data are suitable for the stated teaching calculation, not certified clinical decisions, trading, process control, dam operations, operational climate forecasting or transport interventions. Scale, age and missing metadata limit claims independently of prediction accuracy.

## Rebuild without inventing records

Normal lessons read the bundled CSV. To intentionally recreate the snapshots install the recorded distributions using the optional `data-rebuild` extra, then run `python scripts/prepare_industry_data.py --replace`. This explicitly overwrites snapshots and requires rerunning every verification. The raw distribution copy allows comparison before and after normalization. No web download is represented as having succeeded.
