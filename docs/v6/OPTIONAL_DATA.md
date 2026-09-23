# Optional expansion datasets: acquisition gates, not completed experiments

Reviewed 20 September 2026. These are selected learning extensions, not a universal ranking of the “best” data. Selection favors a clear owner, documented observations, useful group/time structure, meaningful baselines and a manageable route from the bundled examples. A larger download is not automatically a better first lesson.

**None of the ten entries below was downloaded or executed for v6.** Downloading from Python in the build environment failed, so the required labs instead use genuine offline exports already distributed with installed scientific packages. Public documentation was checked separately. No credentials, remote writes, model weights or sports records are included here.

Eight candidates are general public research data sources; the two sports entries have noncommercial or additional restrictions and are deliberately not labeled unrestricted open data. The Well's selected data-file license remains an acquisition gate.

## Safe acquisition workflow

Choose one case only. Visit its official source, read the license and data dictionary, choose the exact version, and download into a separate directory outside the existing snapshots. Record acquisition date, original URL, DOI/revision and bytes hash. Preserve the untouched download. Verify row or trajectory counts, fields, units, sample rates, missing codes and subject/session identifiers before creating a training table.

Write the question and information cutoff first. Partition groups or timelines before producing overlapping windows. Fit scaling/imputation/landmarks only on allowed training evidence. Build a tiny baseline before a neural or topological model. Save a predeclared protocol, split table, predictions and limitations. A failed download or unknown unit is a visible stop, not an invitation to manufacture a substitute.

Provider download pages are linked below. For UCI datasets, the official page has an archive and a Python `ucimlrepo` example. That convenience retrieves records; it does not choose a valid evaluation split for you. For PhysioNet use the named version and supplied checksums. For The Well specify a dataset AND split: its documentation says omitting them requests the entire collection.

## Wine Quality — food process measurements

**Status:** Not downloaded, not bundled, not executed. **Kind:** observed.

[Official source](https://archive.ics.uci.edu/dataset/186/wine+quality) · DOI `10.24432/C56S3T`. Source review: 2026-09-20.

**Why it fits:** Metrics, class imbalance, ordinal targets, persistent descriptors and distribution shift.

**Scope and format:** Two separate red/white tables; validate their downloaded row counts, delimiter and duplicate patterns before use. 11 physicochemical predictors; sensory quality is an ordered score. This is NOT the bundled 178-row Wine cultivar dataset.

**Units and conventions:** Use the provider variable table; do not turn an ordinal score into a calibrated physical quantity.

**Proposed protocol (course design, not a published result):** Predict the ordinal score or a predeclared threshold. Begin with a constant and a simple regression/classification baseline. Group identical feature records before splitting, retain wine type, and test a red-to-white domain shift separately. Do not fit preprocessing on the held-out type.

**License/access gate:** CC BY 4.0

## Concrete Compressive Strength — construction

**Status:** Not downloaded, not bundled, not executed. **Kind:** observed.

[Official source](https://archive.ics.uci.edu/dataset/165/concrete+compressive+strength) · DOI `10.24432/C5PK67`. Source review: 2026-09-20.

**Why it fits:** Units, nonlinear response surfaces, grouped evaluation, inverse ambiguity.

**Scope and format:** 1,030 observations in the provider description; verify the workbook after acquisition. Eight inputs: seven mix/ingredient quantities and age; output is compressive strength.

**Units and conventions:** Ingredients are reported in kg per cubic metre; age in days; strength in MPa.

**Proposed protocol (course design, not a published result):** Compare a mean predictor, ridge and a nonlinear baseline. Keep repeated mix formulations together when evaluating new formulations; investigate age extrapolation separately. Positivity and dimensional consistency are useful checks, not a proof that a chosen mechanistic law is correct.

**License/access gate:** CC BY 4.0

## Airfoil Self-Noise — aerospace and acoustic engineering

**Status:** Not downloaded, not bundled, not executed. **Kind:** observed.

[Official source](https://archive.ics.uci.edu/dataset/291/airfoil+self+noise) · DOI `10.24432/C5VW2C`. Source review: 2026-09-20.

**Why it fits:** Heterogeneous units, sampling geometry, operating-regime holdouts, residual diagnosis.

**Scope and format:** Provider description: 1,503 measured observations. Frequency, angle of attack, chord length, free-stream velocity and suction-side displacement thickness; scaled sound-pressure output.

**Units and conventions:** Hz, degrees, metres, metres per second, metres, and dB respectively; confirm conventions from the actual distribution. Treat angle as a measured value, not an automatic binary flag.

**Proposed protocol (course design, not a published result):** Group repeated operating configurations before evaluating unseen configurations. Start with mean/ridge and inspect residuals across frequency. A point table has no full pressure field, mesh or time derivative: it cannot by itself supervise an acoustic PDE residual.

**License/access gate:** CC BY 4.0

## Bike Sharing — urban mobility and service demand

**Status:** Not downloaded, not bundled, not executed. **Kind:** observed.

[Official source](https://archive.ics.uci.edu/dataset/275/bike+sharing+dataset) · DOI `10.24432/C5W894`. Source review: 2026-09-20.

**Why it fits:** Time windows, seasonal baselines, target leakage, availability time.

**Scope and format:** Hourly and daily files spanning 2011–2012. Provider page row totals and commonly distributed hourly totals differ; actual file counts are an acquisition gate. Calendar, weather and demand fields. Count is the total of casual and registered users.

**Units and conventions:** Demand counts; weather fields include normalized quantities, so preserve the exact published normalization constants and units.

**Proposed protocol (course design, not a published result):** Use contiguous time blocks. Remove casual and registered counts when predicting total: they directly determine the answer. Compare last-day/last-week seasonality with a learned model. Weather observed during the target hour is not automatically a feature available before it.

**License/access gate:** CC BY 4.0

## Appliances Energy Prediction — buildings and energy

**Status:** Not downloaded, not bundled, not executed. **Kind:** observed.

[Official source](https://archive.ics.uci.edu/dataset/374/appliances+energy+prediction) · DOI `10.24432/C5VC8G`. Source review: 2026-09-20.

**Why it fits:** Signals, missingness, seasonal controls, negative controls and temporal dependence.

**Scope and format:** Provider: 19,735 observations at 10-minute resolution over approximately 4.5 months. One Belgian building: appliance energy, light energy, room conditions and nearby weather; rv1/rv2 are random variables.

**Units and conventions:** Appliance energy in Wh, not instantaneous W. Room temperatures in Celsius and relative humidity in percent; retain the provider units for each remaining field.

**Proposed protocol (course design, not a published result):** Partition whole time blocks before lagging. Remove rv1/rv2 from the meaningful baseline and use them only as a deliberate negative control. Compare previous value and daily seasonal forecast. A single building cannot establish unseen-building accuracy.

**License/access gate:** CC BY 4.0

## Human Activity Recognition — wearables and movement

**Status:** Not downloaded, not bundled, not executed. **Kind:** observed.

[Official source](https://archive.ics.uci.edu/dataset/240/human+activity+recognition+using+smartphones) · DOI `10.24432/C54S4K`. Source review: 2026-09-20.

**Why it fits:** Group splits, overlapping signals, delay coordinates and sensor transformations.

**Scope and format:** Provider: 30 volunteers, six activities, 10,299 windows and 561 derived features; archive about 58.2 MB. 50-Hz accelerometer/gyroscope signals and derived features; 128-sample (2.56-second) windows overlap by 50%.

**Units and conventions:** Use source README conversions and distinguish total versus body acceleration; gyroscope angular-rate conventions must be retained.

**Proposed protocol (course design, not a published result):** Honor the supplied subject-disjoint train/test partition. Make validation subject-disjoint within training. Do not randomly split overlapping windows. Compare simple features before delay-cloud topology. Test missing sensors as a separate stress experiment.

**License/access gate:** CC BY 4.0

## PTB-XL 1.0.3 — clinical waveforms

**Status:** Not downloaded, not bundled, not executed. **Kind:** observed.

[Official source](https://physionet.org/content/ptb-xl/1.0.3/) · DOI `10.13026/kfzx-aw45`. Source review: 2026-09-20.

**Why it fits:** Waveforms, sampling, metadata, multilabel metrics, group-level uncertainty.

**Scope and format:** Version 1.0.3: 21,799 ten-second ECGs from 18,869 patients; about 3 GB uncompressed / 1.7 GB ZIP. Twelve leads at 100 and 500 Hz with patient metadata and clinical statement labels. This is multilabel data, not a single interchangeable diagnosis.

**Units and conventions:** Source acquisition resolution is 1 microvolt per least-significant bit; WFDB decoding determines the returned physical units. Do not multiply twice.

**Proposed protocol (course design, not a published result):** Use suggested folds 1–8 for training, 9 validation and 10 test. Retain patient grouping. Decode WFDB gain/baseline rather than assuming raw integers are millivolts. First run waveform/label/lead checks, then conventional and topology-feature baselines. Treat age/date de-identification rules explicitly.

**License/access gate:** CC BY 4.0

## The Well — physical simulation operators

**Status:** Not downloaded, not bundled, not executed. **Kind:** numerical simulation, not measured observations.

[Official source](https://polymathic-ai.org/the_well/). Source review: 2026-09-20.

**Why it fits:** Neural operators, trajectory splits, spatial fields, boundary conditions and conservation.

**Scope and format:** Original overview describes 15 TB across 16 datasets; current navigation has additional entries. Individual sets range from GB to TB. Select one named dataset and split, never download all by default. HDF5 trajectories with coordinates, scalar/vector/tensor fields and boundary metadata; use the official data-format documentation.

**Units and conventions:** Dataset-specific physical or nondimensional units; record coordinates, time spacing and normalization for the selected case.

**Proposed protocol (course design, not a published result):** Begin with one small trajectory and its documented grid. Respect provided train/validation/test trajectories (not random frames). Compare persistence of the state, a simple spectral/finite-difference baseline and a small operator. Assess rollout error, constraints and resolution change separately.

**License/access gate:** Dataset-specific data license must be checked before acquisition. The software license does not establish rights for every data file.

## SPL Open Data — basketball biomechanics (restricted research track)

**Status:** Not downloaded, not bundled, not executed. **Kind:** observed markerless motion-capture output; not automatically raw physical ground truth.

[Official source](https://github.com/Sport-Performance-Lab/SPL-Open-Data). Source review: 2026-09-20.

**Why it fits:** Biomechanics, rotations, time alignment, causal windows, subject/session holdouts.

**Scope and format:** Official README updated March 2026: five participants, 583 free-throw trials, two sessions. Do not substitute counts from a different competition or old subset. Action-specific README, participant metadata and per-trial JSON. Check the exact trial revision for landmarks, coordinate system, units and sampling.

**Units and conventions:** Must be read from the selected action README and actual trial. No unit conversion is assumed in this package.

**Proposed protocol (course design, not a published result):** Check timestamps and coordinate units before deriving velocities. Separate participants or sessions according to the question. Predict from pre-release information only when claiming a live forecast. Preserve capture confidence and evaluate against independent outcome/reference definitions.

**License/access gate:** CC BY-NC-SA 4.0. Noncommercial and ShareAlike conditions; review intended use separately before commercial work.

## OpenBiomechanics — baseball (restricted research track)

**Status:** Not downloaded, not bundled, not executed. **Kind:** observed processed motion/force data, with module-specific acquisition.

[Official source](https://github.com/drivelineresearch/openbiomechanics/blob/main/LICENSE-DATA.md). Source review: 2026-09-20.

**Why it fits:** Signals, geometry, alignment, evidence provenance and license-aware reproducibility.

**Scope and format:** Select a named module, release and small trial. Current release sizes/counts were not independently downloaded here. C3D, processed signal archives, metadata and point-of-interest tables; module README defines markers, coordinates and signs.

**Units and conventions:** Module-specific: read the actual definitions for position, angles, forces, moments and time.

**Proposed protocol (course design, not a published result):** Keep athlete/session groups intact; align events without using future outcomes as input. Verify sensor rates, frames, units and filtering. Explain that prediction from a movement dataset is not validated injury-risk assessment. Employees/contractors or other covered associations must check the additional restriction.

**License/access gate:** CC BY-NC-SA 4.0 plus an explicit professional-organization exclusion. Data/docs restrictions differ from MIT code licensing. Obtain any necessary written permission before use.

## Further documentation

[The Well data format](https://polymathic-ai.org/the_well/data_format/) · [The Well dataset overview](https://polymathic-ai.org/the_well/datasets_overview/) · [Creative Commons BY 4.0](https://creativecommons.org/licenses/by/4.0/) · [Creative Commons BY-NC-SA 4.0](https://creativecommons.org/licenses/by-nc-sa/4.0/).

The source posts from earlier versions remain attributed in [the v5 audit](../v5/SOURCE_AUDIT.md). In particular, PINN gradient surgery, symplectic integration and manifold projections still require their stated assumptions. Adding an industrial table does not reproduce an operator benchmark or validate physical conservation.
