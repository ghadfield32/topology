# Learning records and version history

The current default is `learning_log_v3.json` (stages 00–20). Use `python scripts/learn.py` to record evidence and [the v3 migration guide](../docs/LEARNING_SYSTEM_V3.md) to preserve an existing v2 log. All shipped logs start unassessed.

Legacy `learning_log_v2.json` and `learner_progress.json` are retained for compatibility and history, not synchronized with the current log. The old browser progress page is another separate store. Do not assume these files have been automatically merged.

The book-audit files remain unaudited against the actual full text. A completed introductory course does not silently update that status.
