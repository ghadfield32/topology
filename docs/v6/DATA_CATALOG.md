# Dataset catalogue: what is actually in the ZIP

## Two levels, with different evidence

**Included and executed:** eight new compact observed snapshots from scikit-learn 1.8.0 and statsmodels 0.14.6. They add eight worked cases to the five observed sources already in v5. The eight new normalized tables contain **4,273 rows in their source-specific formats**; those rows are not 4,273 independent, comparable people or events. One traveler contributes four alternatives and one El Niño row contains twelve monthly values. The five older sources are Iris, handwritten digits, measured stereo, historical sunspots and the NIST thermal-expansion excerpt; their original cards remain in the course.

**Selected but not acquired:** [ten next-step datasets](OPTIONAL_DATA.md), including larger waveforms, wearable motion, energy, construction, aerodynamics, physics simulations and restricted sports research sources. Their descriptions are source-checked; their experiments are proposed, not run.

## Why compact historical sources are useful first

They run offline on CPU, are small enough to inspect, and expose different mistakes: label mapping in healthcare, descriptor design in chemistry, tiny samples in manufacturing, lagged panels in business, gaps in atmospheric measurements, physical units in hydrology, calendar seasonality in marine data, and repeated people in transport. They do not substitute for contemporary multi-site production validation. No dataset here is claimed to be universally “best.”

| Included case | Snapshot rows | Real-world unit | Provenance and license |
|---|---:|---|---|
| [wdbc](../../industry/cards/wdbc.md) | 569 | One digitized fine-needle-aspirate image summary. The scikit-learn snapshot does not retain original IDs. | [sklearn 1.8.0](https://archive.ics.uci.edu/dataset/17/breast+cancer+wisconsin+diagnostic); CC BY 4.0 |
| [wine](../../industry/cards/wine.md) | 178 | One wine sample; cultivar is a category, not a quality score. | [sklearn 1.8.0](https://archive.ics.uci.edu/dataset/109/wine); CC BY 4.0 |
| [stackloss](../../industry/cards/stackloss.md) | 21 | One operating-day measurement in the historical plant table; original timestamps are unavailable. | [statsmodels 0.14.6](https://www.statsmodels.org/stable/datasets/generated/stackloss.html); Public domain (dataset distributor statement) |
| [grunfeld](../../industry/cards/grunfeld.md) | 220 | One firm-year record. A repeated firm is not a new independent company. | [statsmodels 0.14.6](https://www.statsmodels.org/stable/datasets/generated/grunfeld.html); Public domain (dataset distributor statement) |
| [co2](../../industry/cards/co2.md) | 2,284 | One weekly date slot, possibly missing a CO2 observation. | [statsmodels 0.14.6](https://www.statsmodels.org/stable/datasets/generated/co2.html); Public domain (dataset distributor statement) |
| [nile](../../industry/cards/nile.md) | 100 | One annual river-volume observation, not an instantaneous discharge-rate sample. | [statsmodels 0.14.6](https://www.statsmodels.org/stable/datasets/generated/nile.html); Public domain (dataset distributor statement) |
| [elnino](../../industry/cards/elnino.md) | 61 | One year with twelve monthly regional mean temperatures; the derived long view has one month per row. | [statsmodels 0.14.6](https://www.statsmodels.org/stable/datasets/generated/elnino.html); Public domain (dataset distributor statement) |
| [modechoice](../../industry/cards/modechoice.md) | 840 | One alternative offered to one traveler. Four rows form one choice set. | [statsmodels 0.14.6](https://www.statsmodels.org/stable/datasets/generated/modechoice.html); Public domain (dataset distributor statement) |

## What each card and folder provides

Each card gives the owner, DOI where available, citation, acquisition route, license, normalized and distribution-file hashes, observation unit, a field-by-field schema, label mapping, stated units and explicit unknowns. Missing counts and transformations are recorded. `data/industries/<case>/source_distribution.csv` preserves the package-distributed data file, not an assertion that it is the original instrument export. `data.csv` is the documented teaching table. `metadata.json` and `catalog.json` state exactly which version supplied it.

Every case saves its split, protocol, predictions, measures and figures under `reports/v6/industries/<case>/`. A label does not make a data point independent, and a source DOI does not prove an experiment was correctly evaluated. Use the saved row identifiers to trace a result back to its input.

## Deliberate exclusions and distinctions

The statsmodels **copper-market** dataset has reuse restrictions in its source documentation and was not added. This does not remove the different NIST copper thermal-expansion measurements already in v5. OpenBiomechanics and SPL Open Data are optional restricted-research routes, not silently redistributed commercial-use data. Clinical examples are educational analyses, not diagnosis tools.

The 178-row Wine dataset is cultivar classification; the separate Wine Quality dataset has sensory scores. CO₂ has 2,284 weekly slots but only 2,225 nonmissing measurements. El Niño is a historical Niño 1+2 temperature table, not a general ocean state. Grunfeld is a reconstructed historical panel, not a current investment recommendation. Nothing in these scalar tables supplies the missing camera frames or PDE fields needed for a different task.
