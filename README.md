# Listening to Shape — repository edition v12

A beginner-first course from topology to geometry, dynamics and representation learning. **One primary route:** 31 core stages, 5 representation units, 25 named cases, 133 worked references and 56 independent learner notebooks. Industry and sports sources retain their own provenance and terms.

**This checkout:** [local setup, verification, and learning route](docs/LOCAL_SETUP.md).

**Read:** extract everything and open `START_HERE.html`. **Start:** [first-run guide](docs/release/FIRST_RUN.md). **Evidence:** [verification](docs/release/VERIFICATION.md). **Import:** [Git guide](docs/release/GIT_IMPORT.md). **Repository assistant:** [copy/paste handoff](docs/release/AGENT_HANDOFF.md).

## Native setup

Install uv through its official instructions, then run from this folder:

```bash
uv python install 3.13.5
uv run --no-project --python 3.13.5 python tools/bootstrap.py --profile physics
uv run --no-sync python course.py acceptance --profile physics --references first --output my_work/acceptance01
uv run --no-sync python course.py stage 0
uv run --no-sync python course.py practice 0 --output my_work/practice00_attempt01
uv run --no-sync jupyter lab
```

Normal setup must resolve/check a genuine `uv.lock` and synchronize it. A clean install was blocked in the build environment, so no fabricated lock is supplied. Review and commit your successful resolver output. Core omits PyTorch; physics supports all references; full additionally requires Ripser/GUDHI with no skipped checks.

## Run a lesson or application

```bash
uv run --no-sync python course.py run --stage 0 --output my_work/stage00_attempt01
uv run --no-sync python course.py cases
uv run --no-sync python course.py run --case wine --output my_work/wine01
uv run --no-sync python course.py practice s00 --output my_work/sports_practice01
uv run --no-sync python course.py acceptance --profile physics --references all --jobs 1 --output my_work/course01
```

A run directory must be new. Experiments copy clean source inputs, not old report caches; notebooks use fresh kernels with interpreter/source checks. Reference source can be read-only. Private answers and progress are not automatically graded or published.

## Container and cluster practice

Follow [Docker](docs/release/DOCKER.md) then [Kubernetes](docs/release/KUBERNETES.md). Static configuration/policy tests are not image builds or live cluster execution. This host lacked those runtimes. Live application requires an explicitly selected disposable context and new namespace; no automatic cluster/namespace/PVC deletion occurs.

## What changed in v12

All 25 case practice routes are now registered. Direct dependency version mismatches block readiness. Acceptance checks child JUnit totals and exact reference identities, not just exit codes. Read-only source copying is made writable only in the disposable workspace. Kubernetes denies unsafe/mixed objects; its reader no longer mounts private result storage. Docker lab references are read-only with separately writable learner work. Serial execution is the default after a recorded parallel kernel startup failure. Read the exact current evidence and remaining limits before presenting results.

Use each lesson once, repair only the missing prerequisite, attempt your own solution, then return for delayed recall. A test pass is not a proof of mastery, clinical or sports validity, complete-book coverage, or universal physical fidelity. See [source coverage](docs/release/SOURCE_COVERAGE.md) and [license/attribution](LICENSE.md).
