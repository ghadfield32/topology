# Listening to Shape Learning System — v4

Open **START_HERE.html** after extracting the whole archive. Begin with [the first-session guide](START_V4.md). This is an original beginner-first learning companion, not the book text or an author-endorsed course.

The 21-stage topology and geometry sequence is preserved. Each stage links its lesson, workbook, new guided session, original lab, consolidation experiment, independent coding notebook, worked answers and mastery criteria. Six foundation primers support the notation and Python. The package contains four real datasets alongside explicitly identified exact and synthetic controls.

The new [coverage map](COVERAGE_V4.md) specifies 84 outcomes. The [evidence map](EVIDENCE_MAP_V4.md) says what each data example establishes and what it does not. See [verification](VERIFICATION_V4.md) for executed tests and outstanding limitations; [changes](V4_CHANGELOG.md) for preservation details.

## Install and run

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -e ".[notebooks,test,reader]"
python scripts/study.py doctor
python -m pytest -q -ra
python -m jupyterlab
```

Windows commands and troubleshooting are in the first-session guide. The build was executed on Linux/Python 3.13.5, not on Mac or Windows. Dependency installation needs internet or local cached wheels; required datasets do not. GPU inference is optional and is not a shipped verification claim.

```bash
python scripts/study.py stage 0
python scripts/study.py next
python scripts/study.py verify-evidence
python scripts/learn.py handoff
```

Preserve your answer files and existing `progress/learning_log_v3.json`. Its format intentionally remains unchanged. Neither notebook execution nor this package upgrade creates learner achievements. Run independent exercises, retain evidence and repair gaps rather than repeatedly restarting the course.

## Structure

`lessons/`, `workbooks/`, `sessions/`: explanations at different depths.

`notebooks/`, `consolidation/`, `practice/answers/`: executed references.

`practice/learner/`, `practice/transfer_v4.json`, `curriculum/response_templates/`: independent work and templates.

`src/shape_lab/`, `tests/`, `scripts/`: inspectable educational implementations, tests and local tools.

`data/`, `reports/`, `docs/`: provenance, results, sources and assessment boundaries.

The full-book audit, larger proof-reading obligations, unavailable optional comparisons, trained-model validation, physical holdouts and independent application remain explicit. Successful reference code is not learner mastery or production certification.
