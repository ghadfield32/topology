# Reproduce and extend the industry work

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
