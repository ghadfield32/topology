# An experiment is more than a notebook output

## One reusable experiment contract

Before running a case, write down the question, the independent observation unit, the quantities and units, which information exists at prediction time, the fitting/evaluation split, the baseline, the metric, and one outcome that would make you reject the proposed method.

After running it, preserve its code/input identity, actual interpreter, environment, parameters, outputs, errors, and limitations. The runner records much of the computational identity automatically. It cannot decide whether your physical assumption is justified or whether your proof is valid.

## What the runner saves

```text
my_work/your_attempt/
  execution.json
  executed/
    ...freshly executed reference notebooks...
  artifacts/
    reports/
    physics/reports/
    industry/reports/
```

`execution.json` contains the ordered prerequisite closure; a SHA-256 map of protected inputs; the Python and package inventory; each notebook's status, actual kernel record, source hash, timing and cell counts; and whether protected source inputs changed.

The first executed code cell is a small environment probe. It checks that the kernel is using the interpreter requested by the runner and that course code was imported from the isolated copied input tree. That is intentionally stronger than trusting the notebook's generic `python3` kernel label.

The runner creates new kernels but shares one temporary input workspace for that run's declared data/report dependencies. It does not claim each notebook runs in a totally separate filesystem. A failed predecessor blocks its dependents. Historical outputs are excluded from the initial workspace.

## How to read failure statuses

**Passed:** the notebook's supplied code completed, its provenance check passed, and no error outputs remained.

**Failed:** execution or a provenance check failed. Inspect the saved notebook and error record.

**Blocked:** a required predecessor failed, so the dependent notebook was not executed. A missing optional model/data source is not automatically replaced by a synthetic dataset unless that notebook explicitly teaches a synthetic control.

**Not assessed:** your learning status remains unchanged. Reference execution does not solve your independent exercises on your behalf.

## First experiment report template

Create `my_work/<topic>/REPORT.md` with these headings:

1. Question and hypothesis.
2. One observation and the independent evaluation group.
3. Dataset provenance, selection, units and missingness.
4. Representation, metric, coordinate/scale convention and model assumptions.
5. Baseline, split and information cutoff.
6. Prediction before execution.
7. Exact command and run-manifest path.
8. Observed metrics and failure cases.
9. Interpretation and a conclusion the evidence does not support.
10. The next independently testable experiment.

Do not write causal, medical, biomechanical or commercial conclusions merely because a data column has a familiar name. The data card determines what is observed; the model determines what is inferred; a separate study determines which applications are validated.

## Comparing representations

For a table, compare ordinary features with topological summaries and their combination using a matched evaluation design. For a time series, preserve chronology and feature availability. For movement, split by the relevant athlete/session/trial group rather than by nearly identical frames. For geometry, fit registration on one set of references and evaluate on different ones. For physical learning, separate data error, residual error, numerical error and invariant error.

These are not interchangeable criteria. A small PDE residual is not automatically accurate recovery of an unknown coefficient. A long persistence interval is not automatically scientific meaning. A correct round trip through your own projection/unprojection functions is a consistency test, not an independent calibration measurement.

## CPU and GPU interpretation

The supplied demonstrations are intentionally bounded CPU experiments. Their measured runtime belongs to the recorded host. It is not an RTX 4090 benchmark. GPU synchronization, transfer time, compilation, precision and end-to-end latency require their own experiments before comparing performance. The earlier geometry and physics lessons develop these distinctions without claiming that the full external architectures were reproduced.

## When to deepen the mathematics

Complete the elementary proof obligations in the primary course. For interval decomposition, stability, nerve results and other major theorems, read the designated primary mathematical source, state hypotheses accurately, and complete the deeper assignments where requested. The actual forthcoming book audit remains separate. This code package does not imply that every theorem or every branch of topology has been covered in full.

## Current v12 private practice

All 25 keys from `python course.py cases` support `python course.py practice KEY --output my_work/KEY_practice01`. This creates a separate editable learner notebook and answer file even when references are read-only. `python course.py acceptance --profile physics --references all --jobs 1 --output my_work/all01` verifies a fresh complete replay and its detailed evidence. It does not assess the learner.
