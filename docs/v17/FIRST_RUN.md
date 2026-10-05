# Start here: one curriculum, real projects

Open `LEARN_TOPOLOGY.html`. It is the new primary navigation page. The old reader and every original source remain available; they are not additional mandatory reading.

## The first decision: keep your current environment

Your installed topology repository and genuine uv.lock already work according to your local evidence. This ZIP is not a command to delete them. Extract it beside the current repo. Follow MIGRATION.md and use a review branch. Keep `my_work/`, progress logs, edited learner files, Windows fixes, the local workbook generator, lockfiles and existing PVCs.

For learning on your Windows computer, use VS Code. Your existing Windows environment remains usable for the core. For the new C/C++/GPU engineering projects, the supplied source recommends WSL2/Linux as the unified tool environment. Do not copy a Windows `.venv` into WSL. Create the Linux environment with the resolver and existing lock in a separate Linux checkout after your intended changes are committed.

On Linux tools, prefer a Linux-side project directory such as `~/projects/topology` rather than treating `/mnt/c/...` as the primary build directory. The referenced Microsoft guidance explains filesystem locality. Do not move/delete the only copy of your work as an optimization.

## Readiness is not acceptance

From the project root:
```
uv run --no-sync python learn.py doctor
uv run --no-sync python learn.py list
```
This prints available commands; it does not install anything or call a missing dependency a pass. The tested environment is described in VERIFICATION.md. C/C++ need a compiler, linker and CMake; Go needs its toolchain; Rust needs the compiler and linker even though its base source dependencies are vendored; TypeScript uses tsc and Node; PyTorch is needed for the optional profiler/binding-header fallback.

Keep ordinary dependency installation separate from lesson execution. Use the existing bootstrap when creating a new Python environment. This release adds no mandatory Python dependency to the old manifest and fabricates no Python, npm, or PyO3 lockfile. Source Rust validators have real resolver-produced locks. TypeScript compilation used the installed tsc5.8.3; package-lock generation on a connected machine remains your deliberate setup step.

## Your next topology session: Stage01, not a restart

```
uv run --no-sync python learn.py session --lab stage01 --output my_work/learning_stage01_01
```
Read the resulting START.md. It links to the existing lesson and creates private Python and native Go/Rust practice copies. Use a NEW output directory for each attempt. In those private subdirectories, compile your edited code as instructed; running the root reference command would otherwise test the reference, not your changes.

Run the mathematical references separately:
```
uv run --no-sync python course.py run --stage 1 --output my_work/stage01_python_reference01
uv run --no-sync python native_course.py compare --lab stage01 --output my_work/stage01_native_reference01
```
The original Python and native16 protocol scopes differ in some later labs. Compare the coverage ledger before comparing scores. Do not present protocols with different models/splits as language benchmarks.

## Your first engineering project

```
uv run --no-sync python learn.py project --unit sys01 --output my_work/c_reader01
uv run --no-sync python learn.py check-project --workspace my_work/c_reader01 --output my_work/c_reader01/attempt01
```
The second command compiles files under `my_work/c_reader01/project/`, not reference source. Predict the 588-byte size of the 12-observation binary (12-byte header plus12×48), then locate every field. Make a private wrong change, see a failure, fix it, and explain why it failed.

The same interface accepts sys00 through sys09. Missing optional dependencies return status `blocked` and exit3. A compiler/test error in available project code is `failed`, not a missing-dependency excuse. Project success is scoped to the declared checks, not every topic in the source lesson.

## One connected real-data result

After the tested C/C++/Rust/TypeScript toolchains are available:
```
uv run --no-sync python learn.py demo --output my_work/integrated_demo01
```
Open its index.html. The output contains the derived binary, source hash, C/Rust reader summaries, Python-fit/C++ predictions, SQL queries, JSON contract, local viewer, and limitations. The viewer reads a file chosen locally; it never uploads data. It shows 3D positions using a labeled orthographic projection. It is not a recovered full scene.

## Optional notebook interfaces

`learning/workbooks/index.html` has57×3 reference interfaces and10 project interfaces. Open them in VS Code/Jupyter. The kernel is explicitly Python; Go/Rust cells invoke compiled native programs rather than interpreting native syntax. Python cells launch the original scientific notebook through its runner, not simply inspect old native output.

```
uv run --no-sync python learn.py workbooks --check
uv run --no-sync jupyter lab
```
Do not edit these generated files directly. Edit `systems/tools/generate_workbooks.py`, regenerate, and review the diff. Your local `workbooks/polyglot/` generator from the earlier transcript is not overwritten.

## Daily loop

Explain the idea. Predict one result. Implement in a real project. Break an assumption intentionally in an isolated exercise. Apply the concept to the registered real data. Then record what surprised you, what failed, why, the Python comparison, and an unsupported conclusion. Templates do not grade your reasoning.

All-language verification and a full workbook sweep are occasional release checks, not prerequisites for every lesson. Native Python is enough to begin topology; Kubernetes comes after one correct bounded project.

## Reproduce the new project matrix

```
uv run --no-sync python learn.py verify-projects --output my_work/projects_acceptance01
```
This prepares and builds the actual ten private project copies, records each outcome, and returns exit3 when optional dependencies block a requested unit. That is not an all-pass. Use `--units sys01 sys02` for a deliberately scoped two-project check.

To execute the generated language interfaces after a substantive runner/environment change:
```
uv run --no-sync python systems/tools/sweep_workbooks.py --output my_work/workbook_acceptance01
```
This is a reference sweep, not learner assessment or proof that all original/native protocols are identical. Fresh notebook kernels are shut down explicitly after every attempt, including failures.
