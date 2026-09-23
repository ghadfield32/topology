"""Build source-linked course navigation and the optional data expansion catalogue."""
from pathlib import Path
import json
R=Path(__file__).resolve().parents[1]
D=R/'docs/v6'
options=[
 dict(id='wine_quality',name='Wine Quality — food process measurements',url='https://archive.ics.uci.edu/dataset/186/wine+quality',doi='10.24432/C56S3T',license='CC BY 4.0',kind='observed',size='Two separate red/white tables; validate their downloaded row counts, delimiter and duplicate patterns before use.',schema='11 physicochemical predictors; sensory quality is an ordered score. This is NOT the bundled 178-row Wine cultivar dataset.',protocol='Predict the ordinal score or a predeclared threshold. Begin with a constant and a simple regression/classification baseline. Group identical feature records before splitting, retain wine type, and test a red-to-white domain shift separately. Do not fit preprocessing on the held-out type.',concepts='Metrics, class imbalance, ordinal targets, persistent descriptors and distribution shift.',units='Use the provider variable table; do not turn an ordinal score into a calibrated physical quantity.'),
 dict(id='concrete',name='Concrete Compressive Strength — construction',url='https://archive.ics.uci.edu/dataset/165/concrete+compressive+strength',doi='10.24432/C5PK67',license='CC BY 4.0',kind='observed',size='1,030 observations in the provider description; verify the workbook after acquisition.',schema='Eight inputs: seven mix/ingredient quantities and age; output is compressive strength.',protocol='Compare a mean predictor, ridge and a nonlinear baseline. Keep repeated mix formulations together when evaluating new formulations; investigate age extrapolation separately. Positivity and dimensional consistency are useful checks, not a proof that a chosen mechanistic law is correct.',concepts='Units, nonlinear response surfaces, grouped evaluation, inverse ambiguity.',units='Ingredients are reported in kg per cubic metre; age in days; strength in MPa.'),
 dict(id='airfoil',name='Airfoil Self-Noise — aerospace and acoustic engineering',url='https://archive.ics.uci.edu/dataset/291/airfoil+self+noise',doi='10.24432/C5VW2C',license='CC BY 4.0',kind='observed',size='Provider description: 1,503 measured observations.',schema='Frequency, angle of attack, chord length, free-stream velocity and suction-side displacement thickness; scaled sound-pressure output.',protocol='Group repeated operating configurations before evaluating unseen configurations. Start with mean/ridge and inspect residuals across frequency. A point table has no full pressure field, mesh or time derivative: it cannot by itself supervise an acoustic PDE residual.',concepts='Heterogeneous units, sampling geometry, operating-regime holdouts, residual diagnosis.',units='Hz, degrees, metres, metres per second, metres, and dB respectively; confirm conventions from the actual distribution. Treat angle as a measured value, not an automatic binary flag.'),
 dict(id='bike',name='Bike Sharing — urban mobility and service demand',url='https://archive.ics.uci.edu/dataset/275/bike+sharing+dataset',doi='10.24432/C5W894',license='CC BY 4.0',kind='observed',size='Hourly and daily files spanning 2011–2012. Provider page row totals and commonly distributed hourly totals differ; actual file counts are an acquisition gate.',schema='Calendar, weather and demand fields. Count is the total of casual and registered users.',protocol='Use contiguous time blocks. Remove casual and registered counts when predicting total: they directly determine the answer. Compare last-day/last-week seasonality with a learned model. Weather observed during the target hour is not automatically a feature available before it.',concepts='Time windows, seasonal baselines, target leakage, availability time.',units='Demand counts; weather fields include normalized quantities, so preserve the exact published normalization constants and units.'),
 dict(id='appliances',name='Appliances Energy Prediction — buildings and energy',url='https://archive.ics.uci.edu/dataset/374/appliances+energy+prediction',doi='10.24432/C5VC8G',license='CC BY 4.0',kind='observed',size='Provider: 19,735 observations at 10-minute resolution over approximately 4.5 months.',schema='One Belgian building: appliance energy, light energy, room conditions and nearby weather; rv1/rv2 are random variables.',protocol='Partition whole time blocks before lagging. Remove rv1/rv2 from the meaningful baseline and use them only as a deliberate negative control. Compare previous value and daily seasonal forecast. A single building cannot establish unseen-building accuracy.',concepts='Signals, missingness, seasonal controls, negative controls and temporal dependence.',units='Appliance energy in Wh, not instantaneous W. Room temperatures in Celsius and relative humidity in percent; retain the provider units for each remaining field.'),
 dict(id='har',name='Human Activity Recognition — wearables and movement',url='https://archive.ics.uci.edu/dataset/240/human+activity+recognition+using+smartphones',doi='10.24432/C54S4K',license='CC BY 4.0',kind='observed',size='Provider: 30 volunteers, six activities, 10,299 windows and 561 derived features; archive about 58.2 MB.',schema='50-Hz accelerometer/gyroscope signals and derived features; 128-sample (2.56-second) windows overlap by 50%.',protocol='Honor the supplied subject-disjoint train/test partition. Make validation subject-disjoint within training. Do not randomly split overlapping windows. Compare simple features before delay-cloud topology. Test missing sensors as a separate stress experiment.',concepts='Group splits, overlapping signals, delay coordinates and sensor transformations.',units='Use source README conversions and distinguish total versus body acceleration; gyroscope angular-rate conventions must be retained.'),
 dict(id='ptbxl',name='PTB-XL 1.0.3 — clinical waveforms',url='https://physionet.org/content/ptb-xl/1.0.3/',doi='10.13026/kfzx-aw45',license='CC BY 4.0',kind='observed',size='Version 1.0.3: 21,799 ten-second ECGs from 18,869 patients; about 3 GB uncompressed / 1.7 GB ZIP.',schema='Twelve leads at 100 and 500 Hz with patient metadata and clinical statement labels. This is multilabel data, not a single interchangeable diagnosis.',protocol='Use suggested folds 1–8 for training, 9 validation and 10 test. Retain patient grouping. Decode WFDB gain/baseline rather than assuming raw integers are millivolts. First run waveform/label/lead checks, then conventional and topology-feature baselines. Treat age/date de-identification rules explicitly.',concepts='Waveforms, sampling, metadata, multilabel metrics, group-level uncertainty.',units='Source acquisition resolution is 1 microvolt per least-significant bit; WFDB decoding determines the returned physical units. Do not multiply twice.'),
 dict(id='well',name='The Well — physical simulation operators',url='https://polymathic-ai.org/the_well/',doi=None,license='Dataset-specific data license must be checked before acquisition. The software license does not establish rights for every data file.',kind='numerical simulation, not measured observations',size='Original overview describes 15 TB across 16 datasets; current navigation has additional entries. Individual sets range from GB to TB. Select one named dataset and split, never download all by default.',schema='HDF5 trajectories with coordinates, scalar/vector/tensor fields and boundary metadata; use the official data-format documentation.',protocol='Begin with one small trajectory and its documented grid. Respect provided train/validation/test trajectories (not random frames). Compare persistence of the state, a simple spectral/finite-difference baseline and a small operator. Assess rollout error, constraints and resolution change separately.',concepts='Neural operators, trajectory splits, spatial fields, boundary conditions and conservation.',units='Dataset-specific physical or nondimensional units; record coordinates, time spacing and normalization for the selected case.'),
 dict(id='spl',name='SPL Open Data — basketball biomechanics (restricted research track)',url='https://github.com/Sport-Performance-Lab/SPL-Open-Data',doi=None,license='CC BY-NC-SA 4.0. Noncommercial and ShareAlike conditions; review intended use separately before commercial work.',kind='observed markerless motion-capture output; not automatically raw physical ground truth',size='Official README updated March 2026: five participants, 583 free-throw trials, two sessions. Do not substitute counts from a different competition or old subset.',schema='Action-specific README, participant metadata and per-trial JSON. Check the exact trial revision for landmarks, coordinate system, units and sampling.',protocol='Check timestamps and coordinate units before deriving velocities. Separate participants or sessions according to the question. Predict from pre-release information only when claiming a live forecast. Preserve capture confidence and evaluate against independent outcome/reference definitions.',concepts='Biomechanics, rotations, time alignment, causal windows, subject/session holdouts.',units='Must be read from the selected action README and actual trial. No unit conversion is assumed in this package.'),
 dict(id='openbiomechanics',name='OpenBiomechanics — baseball (restricted research track)',url='https://github.com/drivelineresearch/openbiomechanics/blob/main/LICENSE-DATA.md',doi=None,license='CC BY-NC-SA 4.0 plus an explicit professional-organization exclusion. Data/docs restrictions differ from MIT code licensing. Obtain any necessary written permission before use.',kind='observed processed motion/force data, with module-specific acquisition',size='Select a named module, release and small trial. Current release sizes/counts were not independently downloaded here.',schema='C3D, processed signal archives, metadata and point-of-interest tables; module README defines markers, coordinates and signs.',protocol='Keep athlete/session groups intact; align events without using future outcomes as input. Verify sensor rates, frames, units and filtering. Explain that prediction from a movement dataset is not validated injury-risk assessment. Employees/contractors or other covered associations must check the additional restriction.',concepts='Signals, geometry, alignment, evidence provenance and license-aware reproducibility.',units='Module-specific: read the actual definitions for position, angles, forces, moments and time.'),
]
for x in options:x.update(status='Not downloaded, not bundled, not executed',source_review_date='2026-09-20')
(R/'optional/industry_datasets_v6.json').write_text(json.dumps(options,indent=2)+'\n')
text='''# Optional expansion datasets: acquisition gates, not completed experiments

Reviewed 20 September 2026. These are selected learning extensions, not a universal ranking of the “best” data. Selection favors a clear owner, documented observations, useful group/time structure, meaningful baselines and a manageable route from the bundled examples. A larger download is not automatically a better first lesson.

**None of the ten entries below was downloaded or executed for v6.** Downloading from Python in the build environment failed, so the required labs instead use genuine offline exports already distributed with installed scientific packages. Public documentation was checked separately. No credentials, remote writes, model weights or sports records are included here.

Eight candidates are general public research data sources; the two sports entries have noncommercial or additional restrictions and are deliberately not labeled unrestricted open data. The Well's selected data-file license remains an acquisition gate.

## Safe acquisition workflow

Choose one case only. Visit its official source, read the license and data dictionary, choose the exact version, and download into a separate directory outside the existing snapshots. Record acquisition date, original URL, DOI/revision and bytes hash. Preserve the untouched download. Verify row or trajectory counts, fields, units, sample rates, missing codes and subject/session identifiers before creating a training table.

Write the question and information cutoff first. Partition groups or timelines before producing overlapping windows. Fit scaling/imputation/landmarks only on allowed training evidence. Build a tiny baseline before a neural or topological model. Save a predeclared protocol, split table, predictions and limitations. A failed download or unknown unit is a visible stop, not an invitation to manufacture a substitute.

Provider download pages are linked below. For UCI datasets, the official page has an archive and a Python `ucimlrepo` example. That convenience retrieves records; it does not choose a valid evaluation split for you. For PhysioNet use the named version and supplied checksums. For The Well specify a dataset AND split: its documentation says omitting them requests the entire collection.

'''
for o in options:
    text+=f'''## {o['name']}

**Status:** {o['status']}. **Kind:** {o['kind']}.

[Official source]({o['url']}){(' · DOI `'+o['doi']+'`') if o['doi'] else ''}. Source review: {o['source_review_date']}.

**Why it fits:** {o['concepts']}

**Scope and format:** {o['size']} {o['schema']}

**Units and conventions:** {o['units']}

**Proposed protocol (course design, not a published result):** {o['protocol']}

**License/access gate:** {o['license']}

'''
text+='''## Further documentation

[The Well data format](https://polymathic-ai.org/the_well/data_format/) · [The Well dataset overview](https://polymathic-ai.org/the_well/datasets_overview/) · [Creative Commons BY 4.0](https://creativecommons.org/licenses/by/4.0/) · [Creative Commons BY-NC-SA 4.0](https://creativecommons.org/licenses/by-nc-sa/4.0/).

The source posts from earlier versions remain attributed in [the v5 audit](../v5/SOURCE_AUDIT.md). In particular, PINN gradient surgery, symplectic integration and manifold projections still require their stated assumptions. Adding an industrial table does not reproduce an operator benchmark or validate physical conservation.
'''
(D/'OPTIONAL_DATA.md').write_text(text)
cat=json.loads((R/'data/industries/catalog.json').read_text())['datasets']
intro='''# Dataset catalogue: what is actually in the ZIP

## Two levels, with different evidence

**Included and executed:** eight new compact observed snapshots from scikit-learn 1.8.0 and statsmodels 0.14.6. They add eight worked cases to the five observed sources already in v5. The eight new normalized tables contain **4,273 rows in their source-specific formats**; those rows are not 4,273 independent, comparable people or events. One traveler contributes four alternatives and one El Niño row contains twelve monthly values. The five older sources are Iris, handwritten digits, measured stereo, historical sunspots and the NIST thermal-expansion excerpt; their original cards remain in the course.

**Selected but not acquired:** [ten next-step datasets](OPTIONAL_DATA.md), including larger waveforms, wearable motion, energy, construction, aerodynamics, physics simulations and restricted sports research sources. Their descriptions are source-checked; their experiments are proposed, not run.

## Why compact historical sources are useful first

They run offline on CPU, are small enough to inspect, and expose different mistakes: label mapping in healthcare, descriptor design in chemistry, tiny samples in manufacturing, lagged panels in business, gaps in atmospheric measurements, physical units in hydrology, calendar seasonality in marine data, and repeated people in transport. They do not substitute for contemporary multi-site production validation. No dataset here is claimed to be universally “best.”

'''
intro+='| Included case | Snapshot rows | Real-world unit | Provenance and license |\n|---|---:|---|---|\n'
for m in cat:
    intro+=f'| [{m["id"]}](../../industry/cards/{m["id"]}.md) | {m["rows"]:,} | {m["observation_unit"]} | [{m["provider"]} {m["provider_version"]}]({m["source_url"]}); {m["license"]} |\n'
intro+='''
## What each card and folder provides

Each card gives the owner, DOI where available, citation, acquisition route, license, normalized and distribution-file hashes, observation unit, a field-by-field schema, label mapping, stated units and explicit unknowns. Missing counts and transformations are recorded. `data/industries/<case>/source_distribution.csv` preserves the package-distributed data file, not an assertion that it is the original instrument export. `data.csv` is the documented teaching table. `metadata.json` and `catalog.json` state exactly which version supplied it.

Every case saves its split, protocol, predictions, measures and figures under `reports/v6/industries/<case>/`. A label does not make a data point independent, and a source DOI does not prove an experiment was correctly evaluated. Use the saved row identifiers to trace a result back to its input.

## Deliberate exclusions and distinctions

The statsmodels **copper-market** dataset has reuse restrictions in its source documentation and was not added. This does not remove the different NIST copper thermal-expansion measurements already in v5. OpenBiomechanics and SPL Open Data are optional restricted-research routes, not silently redistributed commercial-use data. Clinical examples are educational analyses, not diagnosis tools.

The 178-row Wine dataset is cultivar classification; the separate Wine Quality dataset has sensory scores. CO₂ has 2,284 weekly slots but only 2,225 nonmissing measurements. El Niño is a historical Niño 1+2 temperature table, not a general ocean state. Grunfeld is a reconstructed historical panel, not a current investment recommendation. Nothing in these scalar tables supplies the missing camera frames or PDE fields needed for a different task.
'''
(D/'DATA_CATALOG.md').write_text(intro)
(D/'SOURCE_AUDIT.md').write_text('''# Version 6 source and claim audit

Source review date: 20 September 2026. This is an expansion of the existing course, not a new reading of the actual book. The latest message supplied no additional text after “concepts:”; the previously provided posts remain represented in [the v5 source audit](../v5/SOURCE_AUDIT.md), not replaced with invented attachments.

## Evidence classes

**Supplied source claims:** The original posts discuss gradient conflicts in PINNs/PIKANs, Hamiltonian/Lagrangian learning, geometric constraints and smooth charts/flows. Their language, claimed outcomes and qualifications remain in the prior audit. User-supplied material is not treated as independent validation.

**Public source facts checked for v6:** UCI and statsmodels dataset pages, PhysioNet's named PTB-XL release, The Well documentation, SPL's official README and OpenBiomechanics' data license. The [dataset catalogue](DATA_CATALOG.md), [individual cards](../../industry/cards/wdbc.md), and [optional list](OPTIONAL_DATA.md) link the exact primary pages. The web pages were accessible; direct downloads from the build's Python environment were not.

**Actual bytes used:** Local distributions from scikit-learn 1.8.0 and statsmodels 0.14.6. CSV hashes, field counts, missingness, labels and derived splits were verified from these bytes. Current online documentation can describe a newer software version; the package never substitutes its version number for the installed source version.

**Course-designed experiments:** Choice of seed, small fixed model, split, topology descriptor, metric, and counterexample. These are original teaching protocols, not claimed reproductions of a source paper. All saved demonstrations expose their held-out partitions; further changes on those partitions are exploratory.

## Discrepancies and boundaries kept visible

- **CO₂ counts:** the exported data contain 2,284 weekly slots, including 59 missing values; the provider describes 2,225 observations. We retain the missing slots and reject windows crossing missing measurements. The source description and cited sampling reference need not refer to identical measurement procedures; this course does not resolve that ambiguity into a new instrument claim.
- **Modechoice shape:** the loaded distribution has nine data columns before our identifier, whereas the page's headline variable count is eight. The actual schema is listed; the repeated-alternative unit is not collapsed without documenting it.
- **Grunfeld units and availability:** the source uses a 1947-dollar scale without an established multiplier in this export. We do not label it millions of dollars. The source's year-end value is lagged before predicting the next year's investment; historical publication/revision dates are absent.
- **Small manufacturing table:** Stackloss describes 21 days but does not preserve calendar dates in this snapshot. A source-order holdout is explicitly not established forward-time forecasting. Ambiguous airflow and concentration conventions remain source-scale quantities.
- **Healthcare and wine units:** physical units absent from the provider descriptions are marked unknown. No millimetres or mass-concentration units are invented. Scikit-learn's benign/malignant encoding is stated before computing metrics.
- **Optional Bike Sharing counts:** provider summaries and commonly distributed archive counts are not assumed identical. The actual downloaded file must settle this in a future acquisition record.
- **SPL versions:** the current official repository summary and an external competition may describe different subsets. We use the repository's March 2026 summary only for its own catalogue entry, not as evidence that those trials are bundled or evaluated.
- **The Well licensing:** software license and individual simulation-data rights are separate. The selected file's data license remains an explicit acquisition gate. Its introductory 16-dataset count is not asserted to cover every currently listed dataset.

## Accuracy is a process, not a total guarantee

Hash checks detect changed bytes, not inaccurate sensors. Unit tests detect specified implementation failures, not all possible mistakes. A model can satisfy a numerical residual while the governing equation is wrong. A classifier can predict a label without revealing causal structure. A persistence feature can reflect preprocessing or sampling. The learner must state these distinctions in the stage and case assessments.

The required new cases include no neural operator or VGGT inference. Earlier manufactured neural examples remain separately labeled. A global data-cloud barcode is an exploratory cohort descriptor, not a patient-specific measurement, a physical cavity, or a proof of hidden topology.
''')
(D/'START.md').write_text('''# Start here: one course, eight optional industry cases

## Completely new to the subject

Extract the full ZIP into a new folder. Open `START_HERE.html`. Start at Stage 00; you need no coding environment to read lessons or inspect saved outputs. The existing primers explain notation and Python. The new [data primer](BEGINNER_DATA_PRIMER.md) explains observations, units, missing values, splits and elementary model measures.

After the first two stages, use only the **opening sections** of one industry case: [Wine](../../industry/lessons/wine.md) or [Stackloss](../../industry/lessons/stackloss.md) is a manageable first table. You do not need to understand the barcode cell yet. Return to that section after homology and persistence. You are learning one concept in two contexts, not eight new subjects simultaneously.

For every stage, the [31-stage transfer map](STAGE_MAP.md) identifies a concrete case, an exact small calculation, a run/check task and an unsupported conclusion. The ordinary course remains sequential; industry cases are optional parallel practice. Geometry keeps using genuine geometric controls and the included stereo observations rather than pretending a table is a camera dataset.

## Read, predict, calculate, run, explain

Read the lesson and small example. Predict an output in writing. Calculate an easy case by hand. Run the reference notebook and reconcile the result. Change exactly one assumption. Then implement the learner functions and attempt the conceptual questions without solutions. After a delay, answer the recall prompts. An honest “not yet” becomes a targeted prerequisite exercise, not a restart.

A useful first answer file is `my_work/00_first_session.md`: define a row and a column, predict an array's dimensions, report the result, and explain why a repeated row is not necessarily an independent observation. Use your own words.

## Python setup: Mac and Linux

From the extracted `listening_to_shape_lab` folder:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -e ".[notebooks,test,reader]"
python scripts/industry.py verify
python -m pytest -q -ra
python -m jupyterlab
```

The required new industry cases use NumPy, SciPy, pandas, matplotlib and scikit-learn on CPU. Install `python -m pip install -e ".[physics]"` when you reach the earlier physics neural examples (stages 21–30); without PyTorch, physics-specific checks may skip. All reference notebooks in the delivered build were executed with CPU PyTorch installed. Initial dependency installation needs internet or an existing package cache. No dataset download is needed for these cases.

On **Windows PowerShell**, create the environment with `py -m venv .venv` and activate with `.\\.venv\\Scripts\\Activate.ps1`. When activation is restricted, invoke `.\\.venv\\Scripts\\python.exe` directly for the remaining commands; no execution-policy change is required. Replace `python3` with `py` only at the initial creation step.

Open `notebooks/00_lab.ipynb` first. Industry notebooks live in `industry/notebooks/`; independent assignments are in `industry/learner/`; reference code and conceptual answers are in `industry/answers/`. Deliberate `NotImplementedError` functions in learner notebooks are exercises, not broken reference implementations.

## Preserve earlier learning

Do not extract over your only copy of earlier work. Copy `my_work/` and any other personal evidence files into the same relative paths in the new folder. Preserve **`progress/learning_log_v5.json`** unchanged: version 6 still has the same 31 core stages, so the schema and filename are intentionally retained. The old `study_v5.py` and `learn.py` commands remain valid. Do not replace a used log with the empty one supplied in this ZIP.

The eight cases have a separate new `progress/industry_log_v6.json`. It starts unassessed. In future upgrades preserve it alongside your core log. It is not a browser export and is not silently synchronized with browser storage. Recorded scores and independence declarations are yours; hashes verify evidence-file continuity, not correctness.

```bash
python scripts/study_v5.py next
python scripts/learn.py handoff
python scripts/industry.py list
python scripts/industry.py case wine
python scripts/industry.py status
python scripts/industry.py verify-evidence
python scripts/industry.py handoff
```

After making your own evidence file, record an attempt explicitly:

```bash
python scripts/industry.py record wine --kind practice --score 60 --evidence my_work/wine_attempt.md --note "Need to revisit training-only scaling"
```

Use `--kind assessment --independent --critical-clear` only when those statements are true. A score of at least 85 is a course convention, not accreditation. The tool's review dates are calculated on request; it creates no background notifications. `init` refuses to overwrite an existing log.

## Work with a tutor here

Bring your question, the stage/case ID, your prediction, your calculation, actual output and one uncertainty. Ask for a hint before the full solution. After correction, solve a related unfamiliar problem. Paste the handoff when starting another chat; it carries what you actually attempted rather than assuming completion from downloaded files.

## Reading depth and completion

Complete elementary arguments and hand calculations; for major theorems state assumptions and work the structured deeper-proof readings. Finish one independent case and explain its split, metric, failure cases and limits. All demonstrations' test data are exposed: a genuinely new experiment needs a fresh, appropriately separated evaluation. The actual book text has not been audited, and the course does not claim exhaustive coverage of every branch of topology, geometry or scientific machine learning.
''')
(D/'REPRODUCE.md').write_text('''# Reproduce and extend the industry work

## Replay the supplied demonstrations

Set up the environment as described in [Start](START.md). Run `python scripts/industry.py verify` before modifying data. Run `python scripts/run_industry_notebooks.py` to execute the eight worked case notebooks, or open one notebook and run from the top. The `verify_all_v6_notebooks.py` script executes all 99 reference notebooks sequentially; install the physics extra first. It overwrites saved reference outputs but not learner notebooks or progress. Preserve your own work and results before intentionally rerunning these scripts.

The exact reference notebook list and statuses are in `reports/v6/all_notebook_execution.json`. Code, data and protocol hashes are stored with each new worked case. Timing values describe this CPU/container run, not a guaranteed runtime or hardware benchmark. Floating-point results can vary across platforms; tests use appropriate tolerances where needed.

## Rebuild the bundled eight snapshots

This is optional and not needed to learn. Create a separate copy of the course, install `python -m pip install -e ".[data-rebuild]"`, and use `python scripts/prepare_industry_data.py`. By default it refuses existing output. The explicit `--replace` flag rebuilds normalized and distribution copies; use it only in the separate copy and review the hash changes. Scikit-learn 1.8.0 and statsmodels 0.14.6 are the exact sources used here. These are package-distributed snapshots, not fresh pulls from upstream instruments.

Do not edit `data.csv` and leave metadata hashes stale. A modified dataset is a new experiment. Give it a new location, source record, manifest and split. The loader rejects changed reference bytes instead of silently using them.

## What to save for an independent project

Keep the original bytes and license; record a data dictionary, unknown units, observational versus simulated status, acquisition date/version and source hash. State the prediction question and information cutoff. Save row/entity/trajectory identifiers, a split manifest, training-only preprocessing, baseline, fixed protocol, seed, predictions, metrics, environment and code revision/hash. Include a conclusion that the results do not justify.

For time-series work, assign raw time blocks before creating windows. For multiple rows per person or object, split the independent group before deriving features. For simulation operators, separate trajectories/initial conditions, not arbitrary grid cells. Declare whether any interpolation or smoothing uses future values. Use physically correct coordinates and boundaries before claiming PDE or geometric consistency.

## Tests are specifications

`tests/test_industry_v6.py` checks data integrity, missingness, groups, time support, scaling, exact topology examples and choice-table contracts. `tests/test_industry_exercises.py` checks the 24 reference activity solutions. `tests/test_industry_progress.py` checks evidence history and preservation. The tests do not establish clinical safety, economic causality, current climate accuracy or sports deployment validity.

Optional Ripser/GUDHI cross-checks remain a separate dependency group. Their skipped status is not an implicit pass. The original VGGT optional runner remains unexecuted on trained weights. Neither state changes merely because the eight new cases work.
''')
(D/'COVERAGE.md').write_text('''# Coverage: deepen the foundation without pretending to finish every field

## Retained core

All 31 core stage sections and the earlier eight primers remain. The topology course, geometric continuation and physics-learning path are unchanged in scope. The source discussions remain attributed in the v5 audit. The actual book is not reproduced or fully audited. See the original theorem-depth and book-coverage documents for obligations beyond worked introductory examples.

## New v6 layer

- One beginner data/statistics primer.
- Eight dataset cards with schemas, units/unknowns, provenance, licenses, hashes and transformations.
- Eight case lessons, eight executed worked notebooks, eight executed coding-solution notebooks and eight learner notebooks.
- Twenty-four coding exercises, 32 conceptual questions and 24 delayed-recall prompts; no prompt is counted again as a new question merely because it appears in a reader page.
- Thirty-one individual stage-transfer guides. These do not create 31 additional stages; they connect existing lessons to another context.
- Ten optional acquisition plans. They are not counted as downloaded or executed datasets.

## Totals after the extension

31 core stage sections; 8 parallel case sections; 9 primers; 99 executed reference notebooks; 39 learner notebooks; 143 coding exercises; 242 conceptual questions plus the existing 42 transfer questions; 117 delayed-recall prompts. These counts describe curriculum artifacts, not how much a person has mastered.

The eight new snapshots complement the five prior observed sources, for 13 distinct observed data sources across the combined package. Numerical controls and trained models on manufactured data remain separately labeled; the optional physics-simulation archive is not included in that count.

## What is implemented versus suggested

The eight new cases actually run fixed conventional baselines, inspect or use persistent-homology descriptors, and save results. Wine runs raw, topology-only and combined feature models against the same fitting rows. The other cases generally use topology for exploratory training-set geometry rather than claiming a topological predictive improvement. Each explicitly defines what an input point represents.

The optional sources have proposed acquisition and evaluation protocols only. No ECG, wearable, basketball, baseball, building-energy or large fluid-operator model was newly trained on those optional sources. Existing tiny manufactured HNN/LNN/PINN/operator examples remain teaching experiments, not reproductions of every cited paper.

## Limits that matter

No individual dataset represents an entire industry. Historical single-site and small-table examples are deliberately limited. Units cannot be inferred from column names alone. Label availability is not the same as real-time feature availability. Self-reported assessments can be wrong. Byte checks and successful notebooks cannot certify all scientific claims. A new independent project and delayed retention checks remain part of completing the agreed learning outcomes.
''')
# Copy old README, then provide one authoritative v6 start.
old=R/'README.md'
if not (D/'README_v5_preserved.md').exists():(D/'README_v5_preserved.md').write_text(old.read_text())
old.write_text('''# Listening to Shape Learning System v6

Open **START_HERE.html** after extracting the full ZIP. This version includes the entire 31-stage course plus eight parallel real-data industry cases. It is an original learning companion, not the actual book or an endorsed course.

[Start and preserve your work](docs/v6/START.md) · [Included data](docs/v6/DATA_CATALOG.md) · [31-stage transfer map](docs/v6/STAGE_MAP.md) · [Optional larger datasets](docs/v6/OPTIONAL_DATA.md) · [Coverage](docs/v6/COVERAGE.md) · [Verification](docs/v6/VERIFICATION.md).

Read without installing anything. To execute the new CPU industry cases, create an environment and install `python -m pip install -e ".[notebooks,test,reader]"`. Install the `physics` extra for all older neural examples. Then run `python scripts/industry.py verify`, `python -m pytest -q -ra`, and `python -m jupyterlab`. Full Mac/Linux/Windows instructions are in the start guide.

The core evidence file remains `progress/learning_log_v5.json` (same 31-stage schema). The new optional cases use `progress/industry_log_v6.json`. Preserve both and their evidence files during upgrades. Empty supplied logs do not replace your work.

All legacy guides and reports are retained as historical records. The authoritative current status is `docs/v6/VERIFICATION.md`; older version numbers refer to earlier snapshots, not extra unassessed work. Optional datasets are plans, not hidden downloads. See each dataset's own license rather than assuming the course's code license covers all data.
''')
p=R/'pyproject.toml';t=p.read_text().replace('version = "5.0.0"','version = "6.0.0"')
if 'data-rebuild' not in t:t=t.replace('[project.optional-dependencies]','[project.optional-dependencies]\ndata-rebuild = ["statsmodels==0.14.6"]')
p.write_text(t)
print('Wrote v6 documentation, optional catalogue and start files.')
