# CI acceptance and remaining reproducibility choices

The workflow has not run on GitHub during this build. Native jobs resolve/install and test on Linux, macOS, and Windows. The manually triggered full job runs all reference notebooks, Docker, and an ephemeral kind cluster. Every stage retains logs even after failures.

uv 0.10.0, Python 3.13.5, direct package dependencies, and kind v0.33.0 are explicit choices. Actions use maintained major-version tags; they are not immutable commit pins. The example kubectl setup requests the current stable channel and prints its resolved client version. Before treating this as a long-lived production pipeline, choose a client compatible with your cluster and pin the resolved version; pin reviewed Action commits, base-image digests, and the generated uv.lock too. Those choices require actual connected validation and are not fabricated here.

The Kubernetes job is for a disposable local cluster. No cleanup step deletes the PVC before evidence collection. Hosted-runner teardown still destroys ephemeral storage; important run artifacts must be copied/exported before teardown. Job program output, verification logs, and kind diagnostics are collected, but the script does not automatically archive every file on the PVC. For a complete evidence export, follow the Kubernetes guide's copy-out step before cleanup.

Do not copy this workflow over an existing repository workflow without reviewing its permissions, paths, matrix cost, and data licenses. A monorepo must adjust working-directory and artifact paths. Automatic remote publishing, registry pushes, and production deployments are intentionally absent.

## Current acceptance command

A native CI job may call `uv run --no-sync python course.py acceptance --profile core --references first --output my_work/ci-acceptance`. The manual full job should additionally require the full profile and run all references with `--jobs 1`. Upload child evidence even on failure. A workflow file is not a remotely executed CI run. Preserve its actual platform/client/server/lock/image identifiers when it runs.
