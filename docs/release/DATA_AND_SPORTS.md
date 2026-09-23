# Data, industries and sports: one current index

## How to choose a dataset

Choose a source because its observation type, measurement definitions, rights, sample structure and reference information suit the question. Newer is not automatically better for teaching fundamentals; a small well-documented table is often more inspectable than a large opaque video collection. This release adds implementation reliability rather than another unverified payload.

The course retains observed examples in biological measurements, handwritten images, calibrated stereo, astronomy, materials, clinical image-summary measurements, food chemistry, manufacturing, business panels, atmosphere, water, marine climate, travel choice, agriculture and concrete. Constructed shapes, copied-row leakage controls, oscillator/PDE examples and model predictions remain labeled separately from observed data.

## Canonical detailed cards

- [Cross-industry catalogue and field definitions](../v7/DATA_CATALOG.md)
- [Earlier provenance and selected snapshots](../v6/DATA_CATALOG.md)
- [Modern sports dataset selection guide](../v8/SPORTS_DATASETS.md)
- [Current ACB metadata case](../../sports_v9/lesson.md)
- [Sports excerpt data cards](../../sports_v8/README.md)
- [Optional larger datasets](../v6/OPTIONAL_DATA.md)

The original source dates and verification limitations in those documents remain historical evidence. This v12 packaging work does not silently relabel every optional source as freshly acquired or executed.

## What is runnable now

Use `python course.py cases` for the named experiments. The registry links each command to the actual existing notebook, lesson, observation status and scope; it does not create a second copy of the lesson. Default runs do not download data.

| Route | Observations and teaching use | Important limit |
|---|---|---|
| `wdbc` | Image-derived measurements and classification | Not raw pathology images or clinical validation. |
| `wine` | Chemical features and descriptor comparisons | Cultivars, not wine quality; small exposed teaching split. |
| `stackloss` | Plant measurements and regression | Tiny historical sample and source-specific units. |
| `grunfeld` | Firm-year observations | Repeated firms and chronological information matter. |
| `co2`, `elnino`, `nile` | Historical environmental time series | Missingness, calendar construction and prediction horizon are explicit. |
| `modechoice` | Complete traveler choice sets | Alternative rows are not independent travelers. |
| `seeds`, `concrete_slump` | Agricultural geometry and material response | Source-text transcriptions retain pending upstream byte-comparison limits. |
| `leakage`, `claims` | Deliberately constructed failure controls | Not newly collected observations or provider benchmark reproductions. |
| `s00`–`s06` | Selected SPL trial frames and SkillCorner soccer profile excerpts | Sparse selections; not full athlete/session generalization. |
| `acb` | Ten ACB 2025–26 game metadata records | No full tracking/events/season aggregates analyzed by this case. |

## Sports reference check — September 22, 2026

The official SkillCorner basketball repository still describes ten sample games from ACB 2025–26, tracking at 25 frames per second, and separate offensive aggregates over 293 games. Those are source descriptions, not payloads newly loaded in this release. Official source: https://github.com/SkillCorner/opendata-basketball . Review its PRIMER, data dictionary, known issues and license before acquiring or interpreting the larger data.

Do not infer metric player jump height from an XY tracking product, recompute season aggregates from a ten-game sample, combine total rows with component team rows, or split alias identifiers as if they were distinct athletes. The existing ACB lesson teaches the metadata/identity boundary and preserves its provider-hash record.

SPL's included free-throw material is a selected excerpt, with feet for scene positions and different units for hoop-local quantities. Its noncommercial/share-alike data terms are separate from course-code terms. Optional modern multiview, wearable, tracking and baseball sources stay optional acquisition plans until their actual artifacts, rights and identity checks are satisfied. In particular, OpenBiomechanics restrictions must be checked before commercial/team use.

## What to record when replacing an excerpt with full data

Record the provider URL and version/revision, exact acquisition timestamp, license/access agreement, full byte hash, schema, units, frame and clock conventions, participant/session/game IDs, inclusion rules, missingness and detection flags. Keep raw bytes immutable; place derived subsets in a separate directory and record the derivation. Add a schema test, a source hash test and a group/time split test before changing a model.

A checksum proves agreement with the bytes you hashed. It does not establish that a provider's measurements are physically correct. A provider-hash match is a stronger source-identity check than hashing a local transcription alone, but still not independent ground truth.

## Data rights and public Git

Start with a private study repository when usage rights are unclear. Do not upload optional licensed videos or weights into Git automatically. The delivered permission for original course code does not override the separate data cards or upstream terms. See [the publication review](GIT_IMPORT.md) and [the package attribution record](../../LICENSE.md).
