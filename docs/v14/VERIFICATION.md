# v14 verification scope

This release extends the already-tested Python course with Poux spatial-AI material and Go/Rust companion labs.

## Executed in the archive build environment
- Python course suite: 810 passed, 2 skipped (Ripser and GUDHI unavailable).
- Poux bridge isolated tests: 20 passed.
- Go 1.23.2: workspace compiled; unit tests passed; all 57 companion labs executed successfully.
- Polyglot manifest tests: passed and confirm 31 stages + 25 cases + Poux bridge.

## Not executed in the archive build environment
- Rust compilation/tests: rustc/cargo were absent and DNS prevented toolchain installation.
- Polyglot Docker image builds/runs: Docker runtime was not available in this archive build environment.
- Polyglot Kubernetes Jobs: not applied to a cluster.
- Remote GitHub Actions workflow: configuration included but not executed here.

The existing Python Docker/Kubernetes material and its historical evidence remain in the package. Do not reinterpret historical evidence as proof that the newly added Go/Rust images ran.
