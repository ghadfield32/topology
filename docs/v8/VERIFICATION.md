# v8 verification and interpretation limits

## Freshly executed in this build
The inherited v7 preflight returned 538 passed and 2 optional-library skips.
After the sports extension, the full suite returned **604 passed, 2 skipped,
zero failed**. The 66 new tests cover calculations, data contracts, invalid inputs,
source comparisons on fixtures, safe acquisition entry conditions, lessons,
notebook syntax and preservation of all 31 core stages.

**All 121 reference notebooks were rerun in fresh kernels**, including 107
retained notebooks and 14 new sports notebooks. Learner assignment notebooks
were excluded deliberately. The execution manifests list every path, status,
code-cell count, PNG count and elapsed time. The first sports run used a
non-interactive backend without embedded images; inline rendering was explicitly
activated and the new notebooks were rerun. No reference errors were retained.

Exact-control checks include length conversion, landmark angle invariance,
nonuniform frame timing, missing/gap withholding, exact quadratic recovery,
clock-scale ambiguity, Rips square bars, matched-cloud perturbations, player-group
splits and training-only preprocessing. These do not validate the underlying
sports measurement systems. They check the stated calculations and contracts.

## New observed-source example: fit does not prove physical correctness
Five selected SPL frames (110–130 in five-frame increments) fit the example;
135 and 140 are later values of the same selected shot. The fitted free-curvature
parameter is approximately 12.3739 m/s². It is not certified physical gravity.
Fitting RMSE is about 0.00925 m for the free quadratic and 0.01754 m for the
fixed-9.81 assumption. Later-point mean absolute errors are approximately:

| Model | Later-point MAE (m) |
|---|---:|
| Last fitted height | 0.0446231 |
| Fixed-gravity parabola | 0.0488125 |
| Free quadratic | 0.0446614 |

The free model fits better but does not outperform the simple constant-height
baseline on these two selected later points. The points are near the selected
arc's top, and the evaluation is small, same-shot and exposed. It is not an
athlete-generalization or independent measurement benchmark. Doubling the time
scale divides the fitted acceleration parameter by four while preserving fit.
Detailed settings and results are saved in `reports/v8/sports/S02.json`.

## Explicit non-completions
Ripser and GUDHI are unavailable and their two comparisons are skipped, not
passed. The full original sports files were not downloaded; selected numeric
excerpts were transcribed from official text. Local hash checks cannot establish
remote numeric equality. Optional source verifiers were checked on fixtures and
CLI rejection paths, not successful live downloads. Full videos, wearable records,
baseball data, SkillCorner tracks/pose and the ten-entry catalogue's full studies
were not executed. No predictive sports accuracy, trained VGGT, real-time camera
system, injury prediction or professional deployment is claimed.

The runtime is Linux/Python 3.13.5 with CPU libraries. Mac, Windows, CUDA and Apple
GPU execution were not tested. The optional readers' external source links depend
on network access. The actual book text remains unaudited. Mathematical identities,
program execution, reference-label accuracy and independent physical truth remain
different evidence levels.

## Delivery checks
Current release checks are recorded in `reports/v8/reader_links.json`,
`reports/v8/browser.json`, and the final archive check supplied beside the ZIP.
File-target checking is not a live external-link or fragment-ID audit. The final
archive receives path-safety, CRC and SHA256 checks and a fresh extracted-copy
test run. Earlier reports are retained as historical evidence, not asserted as
current file manifests. The new manual sports log starts with all seven items
unassessed and does not silently overwrite previous learner work.

## Reader verification actually performed
The current reader check examined 1,384 HTML files and 65,904 local file-link
targets, finding zero broken targets. Chromium rendered the desktop and mobile
pages; search filtering, answer reveal and an embedded executed figure passed.
The mobile home page had no horizontal overflow. The environment rejected
`file://` navigation with `ERR_BLOCKED_BY_ADMINISTRATOR`. Testing therefore
used a fresh page with document content and local CSS inlined. This demonstrates
rendering and the tested interactions, not successful file-to-file navigation.
Screenshot inspection found no clipped body text at the tested widths.

The optional authoring QA tools require the `qa` extra. `browser_check_v8.py`
uses the build environment's `/usr/bin/chromium`; that script's path is not a
cross-platform browser installer. These tools are not necessary for learning or
for opening the course in your normal browser. No font binaries are distributed.

## Review scope
Source, tests, documents and result claims received a same-session consistency
review. No independent human, external reviewer or independent agent review is
claimed. Historical verification files retain their original counts and dates;
this document and the v8 release manifest describe this build.

## Release-metadata regression found and corrected
The first suite after setting the release metadata to 8.0.0 exposed one inherited
assertion hard-coded to 7.0.0 (603 passed, 1 failed, 2 skipped). The assertion was
updated to require the declared module and package versions to equal 8.0.0;
it was not removed. The failing log is retained as `version_metadata_failure.txt`.
The final suite and extracted-copy check are the release acceptance evidence.
