# Reproducing the current addition

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
