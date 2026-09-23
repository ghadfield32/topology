# Local setup and learning route

This repository is the complete Listening to Shape v12 course imported at the
repository root. Start with [START_HERE.html](../START_HERE.html), then follow the
single 31-stage route through `course.py`. The five representation units and
the named industry and sports cases extend that route; they are not a second
required introduction.

Local integration changes from the supplied archive are limited to this guide
and its README link, Git/Docker ignores for downloaded tools and the ZIP,
`PYTHONUTF8` in CI, and a platform-independent path assertion in
`tests/test_repository_v10.py`. The teaching source, datasets, and lessons were
not edited.

## What was established here

On 23 September 2026, the 3,461 archive files were extracted into this
repository. All 3,454 paths in `MANIFEST.sha256` matched after extraction.
Python 3.13.5 was installed locally, and `tools/bootstrap.py` resolved a real
`uv.lock` and synchronized the `physics` and then `full` profile. The local
Windows first-reference acceptance passed in `my_work/acceptance04/`. Its
earlier failed or interrupted attempts remain in separate evidence folders.
The initial physics bootstrap records a fresh install in
`my_work/setup-20260923T195619945116Z/setup.json`.

Windows full-profile acceptance is recorded in `my_work/full_course01/` as a
failure because three POSIX or symlink tests skipped. Its 750 passing tests
had no assertion failures. The full Linux Docker image passed 753 tests with
zero skips and ran Stage 00; see `my_work/docker01/docker.json`. Static cluster
policy passed in `my_work/k8s_static01/`. Live acceptance passed in
`my_work/k8s_live01/verification.json` on the disposable
`kind-shape-learning` context in namespace `shape-study01`. The PVC is bound,
the Job completed, and the reader is ready. A port-forward returned HTTP 200
for the course home and Stage 00, and 403 for a private work path.
The completed Job's child reports and executed notebook were copied from the
PVC through a temporary read-only Pod into `my_work/k8s_export01/`; the copy
contains a passing `acceptance.json`, 753 zero-skip JUnit results, and Stage 00
with unchanged inputs. The temporary Pod was removed after export.
The strict complete replay in `my_work/docker-full-course01/` passed all 753
tests with zero skips and all 133 reference notebooks in fresh serial kernels;
its source inputs remained unchanged and evidence consistency passed.

`my_work/` is local evidence and learner work, ignored by Git. Do not erase it
to rerun a command; use a new output name. The cluster and its learner PVC are
retained. Export and check any work on that PVC before any deliberate cleanup.

## Daily native commands (PowerShell, from this directory)

```powershell
$env:PYTHONUTF8 = '1'
$env:UV_CACHE_DIR = Join-Path $PWD.Path '.uv-cache'
$env:UV_PYTHON_INSTALL_DIR = Join-Path $PWD.Path '.uv-python'
rtk uv run --no-sync python course.py doctor --profile full
rtk uv run --no-sync python course.py next
rtk uv run --no-sync python course.py stage 0
rtk uv run --no-sync python course.py check 0
```

`PYTHONUTF8` makes Windows text reads use UTF-8, as the lessons expect. The uv
settings keep downloaded tools and package caches in this workspace. Use
`tools/bootstrap.py --profile full` when rebuilding the environment; the
existing lock is checked and the environment is synced. Review the lock diff
after intentional dependency changes.

The private first exercises already exist in
`my_work/practice00_attempt01/` and `my_work/wine_practice01/`. Open their
`learner.ipynb` files and write your reasoning in the adjacent `answer.md`.
The observed wine reference was rerun in `my_work/wine_reference01/`. You can
start Jupyter with `rtk uv run --no-sync jupyter lab`. Keep reference outputs
separate from your own answers.

That wine replay used 178 measured samples. On its specified partition, the
raw-feature, topology-only, and combined accuracies were 0.889, 0.639, and
0.944 respectively. Reproduce the table, identify the held-out observation
unit and split, and explain why one exposed partition cannot establish that
the combined method wins on new collections. Cultivar is a category, not a
quality score.

For each stage, write the observation unit and expected result first. Make one
hand calculation, execute the worked example, solve the private assignment,
then explain a conclusion the evidence does not support. `course.py next`
reads your progress record; code execution does not mark understanding.

## Real-data route

After each relevant foundation, choose one case with a different observation
unit. The `course.py cases` command lists all 25 cases and labels observed
sources versus constructed controls. A compact cross-sector route is:

| Case | Sector and observation unit | Question to carry into the lesson |
| --- | --- | --- |
| `wine` | Food chemistry; one measured sample | Does a shape descriptor add value beyond ordinary features? |
| `wdbc` | Healthcare; one feature record | What population and validation are missing for a clinical claim? |
| `stackloss` | Manufacturing; one plant day | How sensitive is a result to only 21 days? |
| `grunfeld` | Business; one firm-year | How do firm and time dependence affect the split? |
| `co2` and `nile` | Environment and water; time-indexed measurements | Which apparent values are missing or uncertain, and what cannot establish cause? |
| `modechoice` | Transportation; alternatives grouped by traveler | How would row-wise splitting leak traveler information? |
| `seeds` and `concrete_slump` | Agriculture and materials; measured samples | What is feature-space geometry, and how is interval coverage checked? |
| `s00` through `s06` | Sports; selected observations and profiles | What is a frame, trial, athlete, or independent group? |
| `r01` through `r05` | Representation learning; measured data and labeled controls | What do covariance, projection scores, and frozen probes actually show? |

For a new reference attempt, run:

```powershell
rtk uv run --no-sync python course.py run --case wine --output my_work/wine_reference02
```

Use `practice wine` with another new output directory for an independent answer. Read each case's
data card and source terms before extending it. Selected sports excerpts do
not represent full tracking corpora; constructed controls are not observations.

## Kubernetes route and current cluster

Read [the Kubernetes lesson](release/KUBERNETES.md) alongside these steps.
The **context** chooses the cluster, the **namespace** isolates this exercise,
the reader **Deployment** stays available, and the acceptance **Job** ends with
a success or failure. Its **PVC** retains Job output beyond the Pod. The
**Service** has a stable internal address; port-forwarding gives temporary
local access without publishing it externally.

The local `kind` and matching Kubernetes 1.37 `kubectl` binaries are in
`.local-bin/`, which is ignored by Git. The downloaded `kubectl.exe` matched
its official SHA-256 file. To inspect the running exercise:

```powershell
$env:PATH = (Join-Path $PWD.Path '.local-bin') + ';' + $env:PATH
rtk kubectl config view --minify --context kind-shape-learning
rtk kubectl --context kind-shape-learning -n shape-study01 get pods,jobs,pvc,services
rtk kubectl --context kind-shape-learning -n shape-study01 logs job/course-acceptance
rtk kubectl --context kind-shape-learning -n shape-study01 port-forward service/course-reader 18000:8000
```

While port-forward runs, visit `http://127.0.0.1:18000/START_HERE.html`.
Stop forwarding with Ctrl+C. For another deployment exercise, first run
`tools/k8s_verify.py --static` with a new output folder. Live `--apply`
requires a newly chosen namespace on this disposable `kind-` context; the
existing `shape-study01` namespace is intentionally refused. The verifier does
not delete a namespace, cluster, or learner PVC.

## Evidence boundaries

The imported [release verification](release/VERIFICATION.md) describes tests
performed by the archive creator on Linux. The paths above record this
repository's Windows, Docker, and kind runs. A test pass establishes the
specified checks; it does not certify mastery, scientific validity for a new
population, or permission to redistribute a dataset. No learner stage has
been marked assessed here.
