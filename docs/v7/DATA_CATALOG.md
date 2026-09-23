# The complete v7 dataset catalogue

## Included observations versus manufactured controls

The combined package retains all 13 earlier observed sources and adds two full small UCI numeric tables. There are now **15 included observed sources**, used in ten industry cases plus the original stages. Two additional methods labs create controlled copies or analytic counterexamples; they are not additional observed datasets.

The 13 earlier sources were retained, and their reference notebooks were re-executed in this build. Their historical acquisition records and license statements remain in their original cards. This version does not claim to have independently re-acquired every earlier dataset from its provider. The new official UCI metadata and numeric endpoints were inspected separately.

| Domain | Included source | Unit of observation and useful lesson |
|---|---|---|
| Botanical measurements | Iris, 150 rows | One flower measurement record; data shape, distances and basic representations. |
| Handwriting | Digits, 1,797 8×8 images | One image, not a known independent writer; pixels, topology and representation comparisons. |
| Computer vision | Calibrated Middlebury stereo pair with reference disparity | Matched images/pixels with stated calibration; reference-derived geometry and uncertainty. |
| Historical solar activity | Annual sunspot snapshot, 309 years | One annual value; delay coordinates and temporal availability. |
| Materials metrology | NIST Hahn1 thermal-expansion excerpt, 56 observations | One selected measurement from a larger source; units, inverse questions and limitations. |
| Healthcare | WDBC, 569 records | Extracted image measurements, not source scans or clinical validation. |
| Food chemistry | Wine, 178 records | One wine sample, three cultivars; chemical geometry and TDA features. |
| Manufacturing | Stackloss, 21 records | One historical operating-day observation; tiny-sample regression. |
| Business/econometrics | Grunfeld, 220 firm-years | Repeated firms; lagging and temporal panel evaluation. |
| Environment | CO2, 2,284 weekly slots | Includes 59 missing values; not 2,284 observed readings. |
| Water infrastructure | Nile, 100 annual records | Annual volume convention, not instantaneous discharge. |
| Marine climate | Niño 1+2, 61 wide yearly rows | Twelve monthly values per row; calendar and anomaly handling. |
| Transportation | Mode Choice, 840 alternatives for 210 travelers | Four alternatives form one choice set; grouped evaluation. |
| Agriculture — new | Seeds, 210 kernels | Seven X-ray-extracted geometric measurements; geometric feature versus topology. |
| Construction materials — new | Concrete Slump Test, 103 mixtures | Seven ingredient quantities and three measured responses; prediction intervals. |

Do not add these row counts and call the sum a number of independent people or experiments. The rows represent different entities, time aggregation and repeated units. Historical snapshots also do not become contemporary monitoring data because a notebook was rerun today.

## New agriculture source: Seeds

[UCI record](https://archive.ics.uci.edu/dataset/236/seeds) · DOI **10.24432/C5H30K**. Citation: Charytanowicz, Niewczas, Kulczycki, Kowalski and Lukasik (2010), *Seeds*, UCI Machine Learning Repository. UCI lists CC BY 4.0. The dataset contains 70 kernels from each of three varieties and seven extracted measurements: area, perimeter, compactness, kernel length, width, asymmetry and groove length. Integer targets are retained as 1,2,3; the numeric-to-named-variety mapping is not independently verified here.

The inspected metadata does not specify physical area/length units or a full asymmetry definition. Those gaps remain explicit. Compactness is given by 4πA/P²; it is a derived geometric feature, not a topological invariant. The original X-ray images, farm identities and acquisition dates are not in the supplied table.

Files: `data/v7/seeds/source_numeric.txt`, `table.csv` and `metadata.json`. The normalized table adds a 1-based `source_id`; it excludes that ID and the label from model features. No rows are deliberately dropped. The lab saves a stratified 126/42/42 split and descriptive persistence for a fixed training subset. It does not claim new-farm validation or a predictive TDA improvement.

## New construction source: Concrete Slump Test

[UCI record](https://archive.ics.uci.edu/dataset/182/concrete+slump+test) · DOI **10.24432/C5FG7D**. Citation: Yeh (2007), *Concrete Slump Test*, UCI Machine Learning Repository. UCI lists CC BY 4.0. Inputs are cement, slag, fly ash, water, superplasticizer, coarse aggregate and fine aggregate, recorded as kg in one cubic metre. Responses are slump and flow in cm and 28-day compressive strength in MPa.

This is the 103-record Slump Test source, not the separate 1,030-record compressive-strength source. UCI describes 78 initially collected and 25 later records, but authenticated dates and batch identities are not supplied. The demonstration predicts strength using ingredients only and does not infer a verified chronological split from row IDs.

Files: `data/v7/concrete_slump/source_numeric.csv`, `table.csv` and `metadata.json`. The provider row IDs are preserved. The fixed protocol assigns 52 rows to fitting, 25 to error calibration and 26 to testing. Its interval result is an empirical teaching experiment, not engineering certification or a per-recipe safety guarantee.

## Acquisition transparency and reproducibility

The container could not download provider files directly because network/DNS access failed. All numeric records of the two new tables were instead **transcribed from complete official plaintext retrieved through the web tool**, with whitespace/column naming normalized. No rows or values were intentionally changed. This route is explicitly recorded rather than called a byte-identical source download. Row counts, shapes, class counts, endpoints, finite values and local integrity are checked; those checks alone cannot rule out every transcription error.

Local SHA-256 values identify the bundled source-text representations and normalized CSV files. A separate canonical numeric fingerprint preserves decimal values and row/column order while ignoring whitespace and equivalent decimal notation. It does not include column names, so schema semantics must be checked separately. Neither fingerprint is an independently obtained provider checksum.

For an independently connected environment, the opt-in verifier retrieves the exact official numeric endpoint, compares ordered canonical numeric values, fails clearly on mismatch, and never overwrites your files:

```bash
python scripts/verify_v7_remote.py seeds
python scripts/verify_v7_remote.py concrete_slump
```

That remote comparison was **not executed in this build**. It is a reproducible outstanding check, not a green badge.

## Attribution and reuse

Both new sources are attributed to their UCI creators and linked to [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/). Normalization and generated IDs are disclosed. Existing data licenses remain source-specific; the course code license does not override them. The full lesson sources and raw social-media pages were not redistributed as textbooks or scraped personal-profile records.

## Larger next steps are still optional

The [retained optional acquisition guide](../v6/OPTIONAL_DATA.md) covers Wine Quality, Concrete Compressive Strength, Airfoil Self-Noise, Bike Sharing, Appliances Energy Prediction, smartphone activity recognition, PTB-XL, The Well, SPL Open Data and OpenBiomechanics. Those ten collections are not newly acquired or executed here. Some are simulation sources; some have noncommercial or domain-specific restrictions. Check the exact data/weight license and evaluation identities before use.

For all earlier schemas, units, hashes and license details, use the [v6 catalogue and cards](../v6/DATA_CATALOG.md), [original data description](../../data/README.md), [stereo card](../../data/stereo/README.md), [time-series card](../../data/time_series/README.md), and [v5 scientific-ML source audit](../v5/SOURCE_AUDIT.md). Undefined fields remain undefined; neither unit conversion nor a physics model is guessed from a convenient column name.
