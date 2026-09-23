# Start once, learn in order, preserve your evidence

Version 12 • beginner-first repository edition • 22 September 2026

## What this folder is

This is a course project, not a plugin for your production application. A **repository** is the version-controlled folder containing the project. A **terminal** accepts commands. An **environment** supplies Python and installed packages. A **notebook** combines explanations, code cells, and saved outputs. A **test** checks a specific expectation; it does not assess your understanding. An **experiment** specifies observations, assumptions, methods, and measurements before interpreting a result.

Start by extracting the entire archive. Do not run files while they are still inside the ZIP. Open `START_HERE.html` for the offline reader. Lessons and saved outputs need no installation. External videos, papers, optional datasets, and weights require separate access. The publisher's complete book is not included.

Keep one required reading path: Stage → primary lesson → prediction → worked lab → independent assignment → explanation. Open a primer only to repair a gap. The combined reading export is another view of the same material, not an additional assignment.

## Choose your execution path

| Path | Use it for | What it does not prove |
|---|---|---|
| Read only | Learn vocabulary and inspect saved experiments now | That code ran on your computer |
| Native uv | First experiments and ordinary daily learning | That Docker or Kubernetes works |
| Docker | Rebuild a container environment and isolate its filesystem | That a cluster schedules the image |
| Local Kubernetes | Learn admission, Pods, Jobs, storage, and service access | That a production cluster or every platform is supported |

Start native. Kubernetes is optional infrastructure practice, not a prerequisite for learning sets, homology, or self-supervision. The supplied deployment workflow accepts a separately chosen disposable local kind context; never aim it at a work or production cluster.

## Before running commands

Copy the complete folder, including dotfiles, into a new dedicated repository or an isolated subdirectory such as `learning/listening-to-shape`. Do not replace another project's `pyproject.toml`, `uv.lock`, Dockerfile, CI workflow, or agent instructions. See [Git import](GIT_IMPORT.md).

The teaching runtime is Python 3.13.5. uv 0.10.0 was available in the build environment; it is a tested tool version, not a claim to be the newest. Install uv through its official instructions: https://docs.astral.sh/uv/getting-started/installation/ . Then open a terminal in the folder containing `course.py`.

On macOS/Linux, `pwd` prints that folder and `ls` lists its files. On PowerShell, use `Get-Location` and `Get-ChildItem`. Do not include the prompt characters shown by your terminal when copying commands.

## Create your own genuine environment

```bash
uv python install 3.13.5
uv run --no-project --python 3.13.5 python tools/bootstrap.py --profile physics
```

`--no-project` prevents the bootstrap launcher from first trying to install the whole project automatically. The script then performs the actual project resolution and synchronization explicitly. It fails rather than replacing the requested setup with an unrelated installed environment.

Profiles:

| Profile | Includes | Use |
|---|---|---|
| `core` | Numeric libraries, notebooks, reader, tests | Topology and most small industry/sports cases |
| `physics` | Core plus CPU-oriented PyTorch dependency selection | All supplied worked references, including neural physics and representations |
| `full` | Physics plus Ripser and GUDHI | Independent topology-library checks; no skipped checks accepted |

The bootstrap creates `uv.lock` using uv's resolver when absent, or checks an existing lock. It then synchronizes with `--locked`. Review and commit a successfully resolved lock. **No lock was generated in this build environment because package-index access failed.** Installed-version observations and direct pins are evidence about the tested host, not a substitute for a real resolved lock or a fresh installation. After you change requirements, explicitly resolve, inspect the diff, synchronize, and rerun acceptance.

A setup attempt saves `setup.json` and command logs in a new `my_work/setup-*` folder. A command timeout or failure is not a pass. A supplied `--reuse-installed` option is for an explicitly labeled offline diagnostic only; do not use it to certify a clean install. An inherited diagnostic `.venv` must not later be relabeled independent. Keep the old workspace and use a new extraction rather than deleting work automatically.

## One command collects first-session evidence

```bash
uv run --no-sync python course.py doctor --profile physics
uv run --no-sync python course.py acceptance --profile physics --references first --output my_work/acceptance01
```

`doctor` checks declared direct versions as well as package presence. It is not a full resolver, vulnerability scan, or deployment test. `--no-sync` runs the already-prepared environment without silently resolving again.

The acceptance command runs the chosen profile's tests and Stage 00 in a fresh workspace and kernel. It also renders/checks Kubernetes project policy **without contacting or applying to a cluster**. It validates the child test counts, exact notebook identities, profile, successful code execution, and unchanged source inputs. Read `my_work/acceptance01/index.html` and the adjacent JSON/log files. A native pass leaves Docker and Kubernetes runtime status as `not_run`.

A previously used output directory is refused. Use `acceptance02` for another attempt. Do not erase old evidence merely to make a rerun appear to be the first one.

## Your first learning session

```bash
uv run --no-sync python course.py stage 0
uv run --no-sync python course.py check 0
uv run --no-sync python course.py run --stage 0 --output my_work/stage00_attempt01
uv run --no-sync python course.py practice 0 --output my_work/practice00_attempt01
uv run --no-sync jupyter lab
```

Read the linked primary lesson. Before executing its smallest example, write what one row and one feature mean, the expected array shape, and the output you expect. Run the example. In Jupyter, open `my_work/practice00_attempt01/learner.ipynb`; put your explanation in the accompanying `answer.md`.

`NotImplementedError` in a learner function means **you have reached an assignment**. It is intentionally unfinished. Reference answers are separate. A `NotImplementedError` in a worked reference is a failure and should be reported.

A `.ipynb` notebook's `[ ]` means a cell has not executed, `[*]` means it is busy, and a number records its execution order. Restart the kernel and run from the top to avoid depending on hidden state. The course runner does that automatically for worked references and records the actual interpreter and copied source path.

## Continue without another restart

```bash
uv run --no-sync python course.py next
uv run --no-sync python course.py cases
uv run --no-sync python course.py run --case wine --output my_work/wine01
uv run --no-sync python course.py practice wine --output my_work/wine_practice01
uv run --no-sync python course.py run --case s00 --output my_work/sports01
uv run --no-sync python course.py practice r01 --output my_work/representation_practice01
```

All 31 stage and all 25 named case practice routes now resolve to existing learner notebooks. Answers are copied into separate workspaces; references remain unchanged. `next` reads the core learning record, not your shell history, so running a command does not mark a lesson as understood.

To replay the whole supplied set rather than one lesson:

```bash
uv run --no-sync python course.py acceptance --profile physics --references all --jobs 1 --output my_work/full_course01
```

Serial execution is the predictable default on laptops. `--jobs 2` is available after a serial pass when you deliberately measure performance. One parallel kernel-start failure was observed during the v12 audit; that failed record is retained. The runner does not hide it with a silent successful retry. Full profile requires both independent topology packages; it returns nonzero when those checks cannot run.

## How to read a result

`execution.json` lists each notebook, its success/failure, source hash, interpreter, source-code-cell count, and timing. `executed/` contains the actual rerun notebooks. `artifacts/` contains newly produced reports. `tests.json` and `junit.xml` report test counts. `acceptance.json` records the declared scope. A hash checks byte continuity, not measurement truth. A test pass checks its assertions, not every possible application.

Your answer should state: observation unit; method and assumptions; hand calculation; code/output; controlled change; conclusion; limitation; what required help. Revisit an unfamiliar variant after a delay. Mastery, notebook execution, source integrity, installation, and deployment are separate statuses.

## What to preserve before upgrading

Keep `my_work/`, your edited learner notebooks, existing progress logs, referenced evidence, and any real `uv.lock`. The older progress filenames are intentional compatibility interfaces. Copy rather than overwrite; reconcile conflicts. Blank tracked templates remain under `curriculum/response_templates/` and `progress/templates/`. Private answers and active logs are ignored by Git by default.

## Verification boundary for this delivery

See [the current verification report](VERIFICATION.md). Linux/native execution is distinct from clean uv sync, Docker image execution, Kubernetes admission/storage/Jobs, Mac/Windows, and GPU. No full sports tracking/video corpus or trained VGGT inference was newly executed. The retained datasets and terminology audits carry their original caveats. Complete-book reconciliation and independent proofs/capstones remain learning obligations.

Official setup reference: https://docs.astral.sh/uv/concepts/projects/sync/ .
