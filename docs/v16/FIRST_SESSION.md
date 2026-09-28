# Continue at Stage 01: Python, Go and Rust

You have already completed Stage 00. Keep your existing repository, environment, true uv.lock, private answers and Kubernetes PVCs. Extract this archive into a new folder and review `native/guides/SETUP.md` before copying changes.

## One session, not three courses

Read `lessons/01_lesson.md` once. Derive real versus F2 rank and the null vector of the Iris matrix augmented by `2*x0-3*x1`. Write what you predict before execution. Use the Python reference for its full explanation; then compare Go and Rust. Inspect the different ownership/aliasing/error choices. Finally change one assumption and explain the result.

From your course root, using the already-installed environment:
```powershell
$env:PYTHONUTF8 = '1'
uv run --no-sync python native_course.py doctor
uv run --no-sync python native_course.py compare --lab stage01 --output my_work/native_stage01_01
uv run --no-sync python native_course.py prepare --lab stage01 --output my_work/native_practice01
```
Open the comparison's `index.html` and the practice directory's `START.md`. It contains editable worked Go and Rust source plus three independent challenges. A reference copy is guided practice until you make and explain an independent change.

To verify all registered data and native work:
```powershell
uv run --no-sync python native_course.py verify --science --output my_work/native_acceptance01
```
Go and Rust must be installed. Rust dependencies are vendored, but the compiler and system linker are not. Setup instructions explain the actual workspace and Cargo configuration.

## What to write in answer.md

Define the input and observation unit. Show the hand calculation. Explain which matrix is copied and which storage can alias. Record the source and output hashes. Compare numeric results with declared tolerances. Change a pivot or feature definition and predict the effect. State one conclusion the observations do not support. Record what needed help, then attempt a changed example after a delay.

## Next exercise

Run `poux_bridge` in both languages. Derive the count-weighted mean and explain why equal weighting of unequal batches is wrong. Explain why a mean of selected nonuniform basketball frames is neither a release location nor a time average. Then continue to Stage 02; do not reset your learning record.
