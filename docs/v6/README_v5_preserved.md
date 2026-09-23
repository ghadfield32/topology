# Listening to Shape Learning System — v5

A complete combined, original learning companion: **31 stages**, from first mathematical ideas to topology, persistent homology, geometry, and introductory scientific machine learning. The actual book text is not included or audited.

**Extract everything and open `START_HERE.html`.** Start with [the first-session and migration guide](../v5/START.md). New learners begin at Stage 00. Continuing learners keep their evidence and migrate their old record; do not restart merely because the version changed.

The original 21 stages are preserved. Stages 21–30 add carefully qualified lessons on dynamical equations, smooth flows, HNNs/LNNs, symplectic methods, constraints, PINNs, conflicting gradients, neural operators and differentiable simulation. The [coverage matrix](../v5/COVERAGE.md) distinguishes actual implementation from conceptual coverage and full-paper reproduction. The [source audit](../v5/SOURCE_AUDIT.md) distinguishes the supplied posts from added mathematics and primary research.

## Install and run

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -e ".[notebooks,test,reader,physics]"
python -m pytest -q -ra
python -m jupyterlab
```

Windows instructions, optional-dependency limits and commands to reproduce the notebooks are in the first-session guide. Reading and saved outputs need no installation. Initial Python dependencies require network access or cached packages; the five observed data sources are bundled. New neural labs run on CPU and train only small manufactured problems, not empirical sports or clinical systems.

```bash
python scripts/study_v5.py next
python scripts/study_v5.py stage 0
python scripts/study_v5.py verify-evidence
python scripts/learn.py status
python scripts/learn.py handoff
```

The default record is `progress/learning_log_v5.json`, with all 31 stages unassessed. Use `--log` with the migrated filename to resume your earlier attempts. Migration never overwrites an existing destination or fabricates achievements. Browser-local checkboxes are separate.

## Evidence and limits

See [verification](../v5/VERIFICATION.md) for actual test, notebook, browser and archive checks. Synthetic controls, analytic ground truth, observed measurements, trained models and learner mastery are distinct evidence categories. Full PINN/PIKAN benchmark reproduction, general constrained mechanics, trained VGGT inference and independent physical holdouts are not claimed.

Original files, historical verification reports, and the v4 instructions remain available. The current entry point, verification and migration guide take precedence over historical version labels. The old v4 README is retained at `docs/V4_README_PRESERVED.md`.
