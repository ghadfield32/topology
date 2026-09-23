# Verification evidence, not another lesson

`reference_execution.json` records the final fresh-workspace replay of every reference notebook. `saved_notebook_outputs_run.json` records the preceding successful run whose outputs were placed in the canonical notebooks; their teaching cells were verified unchanged. The runner adds one runtime probe per notebook. Delivered notebook bodies omit that probe to preserve the teaching sequence; the actual interpreter/import evidence remains in these manifests and notebook metadata.

`tests/` contains the full suite output and JUnit XML. `uv-diagnostic/` is an explicitly dependency-reusing installation check, not a fresh resolved installation. `docker/` records an unavailable engine, not a passed container. Other logs include regression tests failing before their fixes and passing afterwards. Timestamps, temporary paths and hardware timing are local evidence, not universal performance promises.

Read the current [verification report](../../docs/release/VERIFICATION.md), not an older versioned report, for the delivered release's scope.
