# A small, inspectable pipeline for your own CSV

Use this after stages 06–10. It is an exploratory teaching tool, not a replacement for a production library, large-data engine, or a valid scientific study design. The bundled data are sufficient to complete the course; your private data never need to leave your machine.

## Reproduce a real-data example first

From the course directory:

```bash
python scripts/explore_csv.py data/raw/iris.csv \
  --columns sepal_length_cm sepal_width_cm petal_length_cm petal_width_cm \
  --source-note "Bundled corrected Iris snapshot; exploratory teaching example" \
  --units "centimetres" --points 20 --out reports/my_iris_experiment
```

The output folder must not already exist; use a new name for a new run. The command writes an inspectable JSON report and a finite H1 persistence-diagram image. Labels and identifiers are excluded because you name only measurement columns. The report records source hash, columns, row-selection indices, seed, scale convention, and the Rips/homology contract. There is no prediction target or claim of test performance.

## Substitute your data deliberately

Create a numeric CSV with one clearly defined observation per row. Decide what a row means BEFORE plotting: a person, event, image embedding, or motion window are different designs. Pass only the columns justified by your metric. Include a source note and units. Missing/nonfinite/nonnumeric selected values are rejected, not silently imputed. The cap of 24 observations prevents accidental combinatorial growth in this educational algorithm; the report tells you that it is a subset, not the whole population.

`--scale standard` standardizes the selected exploratory sample and records its fitted means/scales. It changes the metric. It is not a training/evaluation pipeline, and must not be reused as one without a separate train-fitted protocol. Constant columns are rejected under standard scaling. Duplicate feature vectors can create zero-distance observations, which are reported; this is a pseudometric on distinct row IDs rather than evidence that the rows are identical entities.

## Interpretation checklist

Describe the units, selected observations, feature meanings, normalization, scale, coefficient field, maximum homology degree and simplex degree. Identify the finite bars and terminal unpaired classes correctly. Change one reasonable representation choice and compare; a sensitive result is useful evidence, not something to hide. A detected loop is a feature of this metric/filtration on this sample, not automatically a causal process or an independently significant discovery.

## Sports and CV transfer remains a separate experiment

For movement windows, write down timestamp availability and grouping by subject/session before constructing embeddings. Calibration error, projection, joint-angle conventions and missing detections may change geometry before topology sees the data. Hold out the correct independent groups and compare conventional kinematic/image features before adding descriptors. No sports dataset, calibration system or WMS production integration was executed in this release.

Use `docs/CAPSTONE_PROTOCOL.md` for the evaluation contract. Known demonstration test labels in this archive are not an untouched holdout for future tuning.
