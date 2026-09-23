from pathlib import Path
import json
R=Path(__file__).resolve().parents[1]
def write(name,s):(R/'docs/v7'/name).write_text(s.strip()+'\n')
write('START.md',r'''# Start here — one continuing course, not another restart

## Your first session, with no assumed background

Extract the ZIP completely into a new folder. Open `START_HERE.html`. Choose Stage 00 and read its new entry guide. It defines observation, feature, label and table dimensions. Predict the shape of the selected data table on paper, then inspect the saved lab or run the tiny entry check. No software installation is required to read the offline lessons and saved outputs.

There are 31 core stages, ten industry cases, and two new methods laboratories. Do not start all of them simultaneously. The original stages contain the full subject progression. The new entry guides help you begin each stage; they do not replace the deeper lesson, workbook, independent practice or proof obligations. Industry cases are parallel applications, not ten new prerequisites.

A useful first answer is five sentences: what one row represents; which fields are predictors; what output you predict; what actually happened; and one conclusion the output does not justify. Save it as `my_work/00_first_session.md`. Reading the supplied answer does not mark this as independent mastery.

## Read, calculate, run, transfer, revisit

First establish the meaning of each symbol and observation. Then calculate the smallest case manually. Run the reference and investigate disagreements. Change one assumption, predicting the effect first. Implement the learner functions without copying. Finally answer a new question and return later for recall. When a prerequisite is missing, use the relevant primer rather than restarting the entire course.

The new uncertainty primer assumes no statistical background and defines training, calibration, testing, coverage and leakage. The original primers cover notation, Python, proofs, linear algebra, calculus, measurement uncertainty and dynamics. Their assignments are linked from the original stage pages.

## Setup for running code on Mac or Linux

In the extracted `listening_to_shape_lab` folder:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -e ".[notebooks,test,reader]"
python scripts/course_v7.py check 0
python scripts/course_v7.py verify-new-data
python -m jupyterlab
```

To run the full inherited physics neural laboratories, also install `python -m pip install -e ".[physics]"`. To run all tests use `python -m pytest -q -ra`. The delivered verification environment includes CPU PyTorch; a local environment without it will not have the same optional-check coverage. Initial installation needs internet or a package cache. The required data snapshots are bundled. The new cases run on CPU and require no GPU or model weights.

The exact tested Python version and library versions are in the current verification report. The retained dependency pins are not a promise that every future operating system or Python release supports every pinned package.

On Windows PowerShell, create the environment with `py -m venv .venv`. Use `.\.venv\Scripts\Activate.ps1` to activate it. If activation is restricted, invoke `.\.venv\Scripts\python.exe` directly; no execution-policy change is required. Replace only the initial environment-creation command with `py`.

## Find the right lesson and notebook

```bash
python scripts/course_v7.py stage 0
python scripts/course_v7.py case seeds
python scripts/course_v7.py check all
```

The first command prints the entry and full-stage paths. Open `notebooks/00_lab.ipynb` for the original first worked lab and `practice/learner/00_practice.ipynb` for its independent exercises. For the new agriculture case open `applications_v7/seeds/lab.ipynb`, then `applications_v7/seeds/learner.ipynb`. Materials is under `applications_v7/concrete_slump/`; the two methods labs are under `methods_v7/`.

Learner notebooks deliberately raise `NotImplementedError` until you write your answer. Reference notebooks are separate and executed. A failed learner exercise is not a broken reference package. Do not edit the checks merely to obtain green output.

## Preserve your work from v6 or earlier

Keep the old folder until migration is checked. Preserve `my_work/`, `progress/learning_log_v5.json` and `progress/industry_log_v6.json`, plus any evidence files stored elsewhere. Retain the same relative paths when a log points to them. Do not replace a used log with the empty one shipped in the new ZIP.

Version 7 retains 31 core stages and the original eight-case log unchanged. The two new cases and two methods labs have response templates and a separate unassessed checklist in `progress/v7_extension_checklist.json`; this checklist does not silently merge with old logs. It is manually editable, not an automatic grader. A source hash verifies unchanged bytes, not whether your proof is correct.

The existing commands remain valid:

```bash
python scripts/study_v5.py next
python scripts/study_v5.py verify-evidence
python scripts/learn.py handoff
python scripts/industry.py status
python scripts/industry.py verify-evidence
```

These tools calculate review dates when requested; they create no background notifications. Browser-local progress, where present in historical readers, is a separate record and is not automatically synchronized.

## Bring an answer back to this chat

State the stage/case ID, your prediction, the calculation you attempted, the actual code/output, and one point of uncertainty. Ask for a hint before opening the full answer. After correction, solve an unfamiliar variant. Preserve your wrong turn as useful evidence of what changed in your understanding.

The actual book text has not been audited. The source posts are not complete technical specifications. The course is an original learning system for the defined introductory and applied scope, not a guarantee of professional competence in every domain. The coverage map identifies what is implemented, demonstrated, source-reviewed, or still requires independent work.
''')
write('UNCERTAINTY_PRIMER.md',r'''# Evidence and uncertainty from zero

## A number needs an object, a unit, and a moment of availability

“30” could be a class code, a time in seconds, a strength in MPa or a row number. Before writing a model, say what it measures. A prediction-time feature must actually be available when the prediction is requested. The result of a laboratory test cannot quietly become an input to a model advertised as making a prediction before that test.

A label is not always a physical quantity. The Seeds integers 1, 2 and 3 are categories. Their ordering is not a measured distance. The Concrete Slump strength output is a physical response in MPa, so an error of 3 MPa has a unit; a classification error does not use the same measure.

## Mean, error, and a simple baseline

The mean of 20, 30 and 40 is 30. A constant predictor trained on those three outcomes predicts 30 for every future case. Its usefulness is not sophistication; it establishes what a method must improve upon. Fit it on the training outcomes, not all outcomes.

If predictions are 22, 25 and 43 for true values 20, 30 and 40, residuals y-prediction are -2, 5 and -3. Absolute errors are 2, 5 and 3. Mean absolute error is 10/3. Root mean squared error is sqrt((4+25+9)/3), about 3.559. Both keep the target's unit, but RMSE places greater emphasis on larger errors. Calculate them directly before importing a metric function.

A low average can hide a severe tail. Keep per-observation errors and report the denominator. For classification, 38 correct predictions out of 42 gives about 90.48%; the remaining four errors still need interpretation. Accuracy does not encode asymmetric costs or unknown population prevalence.

## Fitting and evaluation are different operations

Training chooses model parameters. Validation can choose hyperparameters or compare alternatives. Calibration, in the interval example, uses a fixed model's additional error observations to choose a radius. Testing evaluates the fixed procedure. Using the same outcomes repeatedly for all of those tasks can make a result look better than it generalizes.

A preprocessing mean is a fitted parameter. A selected persistence-image grid can also be fitted. A diagram threshold chosen after examining the final test labels is a selection decision. Write every such choice into the protocol. Use fixed choices for the small demonstration; use nested or otherwise appropriately separated selection when a real project requires tuning.

## Rank is not an interpolated quantile

Sort nine calibration errors [1,2,3,4,5,6,7,8,9]. At nominal error rate .2, the split-conformal order is ceil((9+1)×.8)=8, so choose error eight. This example defines an order statistic directly. A software quantile routine has a convention; interpolating between neighbors does not necessarily implement the intended rank.

A 99% nominal level would require rank ten, beyond the available nine errors. Our conservative construction returns infinity. It is deliberately uninformative rather than quietly reporting an unjustified finite endpoint. The function uses a decimal alpha contract to avoid an accidental ceiling jump caused only by binary floating-point representation.

## Where the coverage guarantee comes from

For a predictor fixed independently of calibration/test observations, assume their scores are exchangeable. Imagine sorting n calibration scores and one future score together. With no ties, the future score has a symmetric rank among n+1 positions. Choosing k=ceil((n+1)(1-alpha)) covers at least k/(n+1) of those ranks; conservative tie handling retains the lower-bound guarantee. This is a probability averaged over the sampling of calibration and future observations. It does not force every finite test set or every particular recipe to attain that fraction.

This is an original compact derivation and implementation guide for the split-conformal rank rule. The primary reference is Angelopoulos and Bates, [A Gentle Introduction to Conformal Prediction](https://arxiv.org/abs/2107.07511), particularly the coverage discussion and proof appendix. More advanced procedures for time dependence, group-specific guarantees or distribution shift require their own assumptions and constructions; the simple rule does not automatically solve those settings.

Randomly permuting rows is not proof of exchangeability. Hidden batches, families, patients, seasons or repeated experiments may remain dependent or shifted. In the concrete table, authenticated batch/time identities are absent. The interval lab demonstrates the method and its empirical result, not a guaranteed industrial recipe policy.

## Marginal, conditional and empirical are different words

Marginal coverage averages over a specified sampling process. Conditional coverage would condition on a feature value or subgroup; the simple marginal statement does not give all such guarantees. Empirical coverage is the fraction inside intervals in a particular finite sample. A test set of 26 has coarse steps of 1/26, about 3.85 percentage points. Observing 25/26 is not the same claim as a precisely known 96.15% future coverage probability.

Interval width measures how informative the set is. An infinite interval covers all finite outcomes but says almost nothing. Even a statistically valid procedure may be too broad for a useful decision. Describe both coverage and width, then seek domain-specific validation rather than certifying safety from this notebook.

## Correct rows can still leak information

Make two software copies of each of two kernels, giving rows A1,A2,B1,B2. Training on A1,B1 and testing on A2,B2 shares no row indices but shares both source kernels. An exact-copy nearest neighbor can look excellent without handling a new object. The manufactured-copy lab preserves source IDs so the problem is visible.

The appropriate group depends on the future question: kernel, plant, farm, patient, camera session or PDE initial condition. Grouping by source row cannot establish an unseen-farm evaluation when farm identities are absent. Time windows also have support intervals; overlapping inputs or future-derived labels can cross a nominal split.

## Keep four evidence levels visible

A source claim is what a post or paper asserts. A mathematical conclusion follows from a specified argument and assumptions. A computed result describes the implementation and experiment actually run. A deployment conclusion requires additional evidence about the intended environment and consequences. Do not replace any one with another.

Finish by explaining one example from each level. Then show how a result could be repeatable, numerically stable and still interpreted incorrectly. The methods case on source claims provides worked counterexamples rather than asking you to memorize a warning.
''')
write('DATA_CATALOG.md',r'''# The complete v7 dataset catalogue

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
''')
write('SOURCE_AUDIT.md',r'''# Source audit — preserve claims, label extensions

## Basis of the course

The original learning source proposes: understand the idea, state it precisely, calculate by hand, implement, test and explain limitations. The 31 retained stages and 31 new entry guides continue that organization. The book’s table of contents, not its complete text, supplied the initial scope. No chapter is marked as independently audited against unavailable full text.

The supplied social-media posts and prior WMS integration note are retained as conceptual prompts through the existing source ledgers. We do not redistribute unrelated profile and messaging text. The additional calculations below are original educational extensions requested by the user, not text silently substituted for the source authors' arguments.

| Supplied source | What it asserts or proposes | This course's separate treatment |
|---|---|---|
| PINN/PIKAN gradient-conflict post (supplied lines 65–81) | Composite residual, boundary and interface objectives can conflict; Norm-PCGrad improves the authors' benchmarks. | Preserve benchmark scope; retain Stage 27; add the exact opposite-gradient example, which is not a benchmark reproduction. |
| Invariant-manifold/symplectic post (lines 67–84) | Symplectic structure is presented as ensuring exact energy over arbitrary steps; one algebraic correction is presented as constraining updates to the manifold; major throughput claims are made. | Attribute those claims; separately calculate the oscillator's energy change and a nonzero sphere residual. No GPU/HPC benchmark or climate validation is claimed. |
| HNN/LNN comparison (lines 65–90) | Learn mechanics through Hamiltonian or Lagrangian structure and a Legendre connection. | Retain definitions and add explicit momentum/velocity arithmetic and regularity requirements. The trained LNN remains a restricted teaching model. |
| Smooth-manifold/chart post (lines 67–100) | Local coordinates, smooth transitions and vector-field-generated local diffeomorphisms. | Retain its local framing; teach explicit chart round trips and finite-time flow domains. Numerical steps are not assumed to inherit exact-flow invertibility. |
| WMS geometry/engineering/events note | Geometry proposals need metric registration and holdouts; profiling and temporal evidence matter. | Keep the existing modules and boundaries. Current v7 work changes the learning package, not WMS production code or automations. |

## External research checked for the new addition

UCI Seeds and Concrete Slump metadata and their complete numeric endpoints were inspected. Both source cards specify the units provided, missing metadata, observation counts, licenses and DOI. Source transfer into the container used declared numeric transcription, not a claimed byte-identical download. See the data catalogue for the outstanding remote numeric comparison.

The primary conformal reference is [Angelopoulos and Bates, A Gentle Introduction to Conformal Prediction](https://arxiv.org/abs/2107.07511). The new lab uses a direct finite-sample order statistic and an explicit infinite-radius case. Its guarantee requires a predictor fixed independently of exchangeable calibration/test scores. Marginal coverage is not guaranteed conditional coverage for every recipe. The article's empirical studies are not reproduced here.

The gradient-conflict paper [Tackling Failure Modes of PINNs and PIKANs Using Conflict-Free Gradients](https://arxiv.org/abs/2609.14841) remains a primary reading supporting attribution of the supplied post's research claims. The new opposite-gradient calculation does not establish that Norm-PCGrad wins or loses on its experimental benchmarks.

For formal topology, the retained course uses the [ETH 2026 TDA course](https://ti.inf.ethz.ch/ew/courses/TDA26/index.html), Tinarrage, Morris and the linked deeper references. The entry guides are short original worked examples; they do not replace the formal proofs or claim author endorsement.

## How to state a result honestly

“Source-reported” means an author made the claim in the identified source. “Analytically derived” means the shown argument establishes it under its explicit assumptions. “Executed” means the recorded implementation ran in this environment and produced the retained outputs. “Independently validated” would require appropriate separate evidence; ordinary regression tests and source hashes do not alone establish it.

The v7 data experiments use observed kernel/mixture records; duplicate rows, rectangles, oscillator trajectories, attention arithmetic and sphere corrections are manufactured or analytic controls. They remain labeled that way. A plausible plot is not a proof of causality, calibrated scale, structural safety or domain transfer.
''')
write('COVERAGE.md',r'''# Coverage, depth and completion

## Three subject tracks, one foundation

Stages 00–12 cover the agreed introductory topology/persistence scope. Stages 13–20 connect it to geometric reasoning and evidence-based computer vision. Stages 21–30 introduce dynamics and scientific machine learning. Each retained stage keeps its complete learning section, independent code, questions and proof obligations. The new entry guides provide a smaller starting example for each, with 31 runnable checks.

Ten included industry cases support transfer: healthcare, food chemistry, manufacturing, business panels, environmental monitoring, hydrology, marine climate, transportation, agriculture and construction materials. The two new methods labs teach leakage and source-claim evaluation. They are not mislabeled as new observed industries.

## What the new parts actually implement

| Addition | Implemented and run | Boundary |
|---|---|---|
| Seeds | Source checks, compactness consistency, fixed train/validation/test classifiers, descriptive Rips persistence on 24 training rows | No source images, farm split, causal crop inference or predictive TDA comparison in this new lab |
| Concrete Slump | Fixed ridge and mean baselines, separate error calibration, corrected order statistic, test intervals and saved row-level results | Exchangeability is not established by random permutation; no structural certification |
| Leakage | Manufactured exact copies of observed kernels, row/unit overlap audit, fixed 1-NN comparison, scale-change arithmetic | No additional observed kernels; no claim to estimate all leakage effects |
| Claims/evidence | Symplectic-versus-energy arithmetic, nonlinear correction residual, opposite gradients, observed compactness bridge | Not a reproduction of paper benchmarks or a physical climate model |
| Entry guides | 31 distinct hand-worked examples and runnable checks with misconception repairs | Not a substitute for the original stage exercises or full proofs |

## What “deep enough” requires

For elementary definitions and results, you should explain them, construct examples and nonexamples, and reproduce the assigned proofs and hand calculations. For algorithms, inspect intermediate state and pass exact controls before using real-data outputs. For major theorems, state hypotheses and proof strategy, then follow the explicit deeper-proof assignments where required. For applications, defend observation units, inputs, transformations, split, baselines and limits.

A suggested assessment convention is 85% on ordinary questions, with every critical misconception repaired. This is a course convention, not accreditation. Independently demonstrate a result and repeat it after a delay. “Read,” “ran,” “solved with help,” and “solved independently” remain different statuses.

## Remaining obligations stay visible

The actual book text has not been reconciled chapter by chapter. Ripser/GUDHI comparisons require the optional libraries and remain skipped in this build. Trained VGGT inference, current GPU/hardware benchmarks, real sports-event precision/recall, full-paper reproductions and independent physical/clinical validation are not supplied by these teaching notebooks. Broader topics such as spectral sequences, general multiparameter persistence, full manifold classification and arbitrary scientific-model deployment are not represented as exhausted by this course.

The existing [scientific-ML coverage map](../v5/COVERAGE.md) distinguishes trained examples from conceptual or operation-only demonstrations; the [v6 map](../v6/COVERAGE.md) documents older industry boundaries. Earlier reports are historical; consult the current verification report for this delivery's executed checks.

## Finishing a unit instead of downloading another version

Choose the next unassessed stage. Produce a prediction, a hand calculation, a traceable execution and an explanation of one failure mode. Apply the concept in one additional suitable dataset, not every dataset at once. Complete the independent questions, receive feedback, and revisit after a delay. The evidence file, not a software-generated green badge, is what supports continuation.
''')
write('REPRODUCE.md',r'''# Reproducing the current addition

Run commands from the extracted project root. New data are already included; do not rerun the source-normalization builder over modified learner data. `verify-new-data` validates local hashes and schema without downloading or rewriting anything.

```bash
python scripts/course_v7.py verify-new-data
python scripts/course_v7.py check all
python -m pytest -q -ra
python scripts/execute_new_v7.py
```

`execute_new_v7.py` clears and reruns only the eight new reference notebooks, preserving the learner assignments. It writes `reports/v7/new_notebook_execution.json` and regenerates new experiment reports. To rerun all 99 inherited references, use `python scripts/reexecute_inherited_v7.py`. That command can take substantially longer because it includes the existing small neural-training examples; no speed guarantee is implied.

Changing an experiment creates a new result. Keep the delivered archive immutable as a reference and make changes in a working copy. Do not update a manifest merely to disguise a changed source. Save a new protocol, split and environment for a new experiment; do not call a reused teaching test partition unseen evidence.

To regenerate the offline reader after successful notebook execution, use `python scripts/build_reader_v7.py`. It refuses notebook error outputs. This updates the reader, not the learner's mastery. `python scripts/check_release_v7.py` checks stage counts, links and execution records and writes the current structural audit. Generated audit files are not substitutes for independent scientific validation.
''')
# New-source attribution separate from the inherited code license.
for name in ['seeds','concrete_slump']:
 meta=json.loads((R/f'data/v7/{name}/metadata.json').read_text())
 (R/f'data/v7/{name}/ATTRIBUTION.md').write_text(f"# Attribution and provenance: {name}\n\n{meta['citation']}\n\nDOI: {meta['doi']}\n\nProvider: {meta['url']}\n\nLicense listed by UCI: CC BY 4.0 — https://creativecommons.org/licenses/by/4.0/\n\n{meta['acquisition']}\n\nThe normalized CSV changes formatting/column names; the Seeds file adds a generated source ID. Metadata records schema, source numeric digest and local file hashes. No images, labels beyond the source codes, or inferred units were added. Retain attribution and disclose modifications when redistributing. The course code license does not override the source license.\n")
# Preserve existing logs; a new manual checklist is explicitly separate.
p=R/'progress/v7_extension_checklist.json'
if not p.exists():p.write_text(json.dumps({'schema_version':1,'purpose':'Manual study checklist; no automatic grading or synchronization','sections':{x:{'status':'unassessed','evidence_files':[],'notes':''} for x in ['seeds','concrete_slump','leakage','claims']}},indent=2))
# Existing README is preserved once.
old=R/'docs/v7/README_v6_preserved.md'
if not old.exists():old.write_text((R/'README.md').read_text())
(R/'README.md').write_text('''# Listening to Shape Learning Lab — v7\n\nOpen **START_HERE.html** after fully extracting the ZIP. This is the complete retained course plus new beginner entry guides and cross-industry evidence laboratories.\n\n[First session, setup and migration](docs/v7/START.md) · [15 observed sources and their limits](docs/v7/DATA_CATALOG.md) · [Coverage](docs/v7/COVERAGE.md) · [Current verification](docs/v7/VERIFICATION.md) · [Source audit](docs/v7/SOURCE_AUDIT.md)\n\n31 core stages; 10 industry cases; 2 new methods laboratories. All saved reference outputs are demonstrations, not learner assessments. Deliberately incomplete functions occur only in separately labeled learner assignments.\n\n```bash\npython -m pip install -e ".[notebooks,test,reader]"\npython scripts/course_v7.py stage 0\npython scripts/course_v7.py check all\npython -m pytest -q -ra\npython -m jupyterlab\n```\n\nAdd the physics extra for the retained CPU neural examples: `python -m pip install -e ".[physics]"`. Installation needs network/cache; supplied data do not. Preserve my_work and existing progress logs when migrating. New material is an original extension to the supplied topic outline, not the full forthcoming book text, an author-endorsed course, or professional certification.\n''')
p=R/'pyproject.toml';s=p.read_text().replace('version = "6.0.0"','version = "7.0.0"');p.write_text(s)
print('Wrote current start, dataset, source, uncertainty, coverage and reproduction guides.')
