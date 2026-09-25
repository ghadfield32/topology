# Verification of this small addition

Executed 25 September 2026 on Linux, Python 3.13.5. This is **not** a revalidation of the whole 133-notebook course or of the user’s local Docker/Kubernetes installation.

## Completed checks

- All 37 tutorial labels and URLs were compared programmatically with the six explicit lists in the supplied article. Counts are **7, 7, 8, 2, 4, 9** with no repeated tutorial URL.
- The existing `curriculum/START.md` content is retained byte-for-byte before the additive optional-link block. `curriculum/catalog.json`, all 31 primary lessons, source data, lock/dependencies, runtime/deployment files and learner progress are not changed.
- The 20 isolated bridge tests first failed because the implementation was absent, then all passed after implementation. They cover unequal batches, empty streams/chunks, generator input, translation/order behavior, numeric validity, unit validation, source hash mismatch, safe output location, overwrite refusal and unchanged source data.
- The bridge ran against the existing SPL excerpt from the v12 course archive. The data hash matches the manifest also inspected in the GitHub repository. Its three controlled numerical checks passed.
- The observed sample centroid was approximately **[4.0312118934, -7.6953969094, 2.7657245696] metres**. With chunk sizes **1 and 11**, incorrectly averaging chunk means equally displaced it by **1.1224149165 metres**. The weighted result matched the whole-stream result to floating-point tolerance.

The sports file is a previously selected numeric transcription, not a newly acquired full source. These are summary calculations over 12 nonuniformly selected observations from one trial. They are not a time average, a measured release point, independent athlete validation or a static-scene reconstruction.

## Repeat the checks

From the repository root in the existing environment:

```powershell
uv run --no-sync python curriculum/extensions/poux_spatial_ai/test_bridge.py
uv run --no-sync python curriculum/extensions/poux_spatial_ai/bridge.py --repo . --output my_work/poux_bridge01
```

Use a different new output folder for each repeat. Results include the source hash, original acquisition caveat, code hash, runtime, controlled checks and unsupported conclusions. The tests use clearly labeled synthetic fixtures; the script run uses the already bundled observed-source excerpt.

## Not claimed

No new LAS/LAZ/E57 file, model, full article, paid course or book chapter was acquired. No PointNet training, COLMAP/Meshroom run, semantic pipeline, Poisson/marching-cubes run, large-memory benchmark or viewer deployment is included. Those remain plans with explicit gates. No full-course test pass, external-library agreement, browser test, Windows/macOS test, clean uv resolution, Docker build, Kubernetes Job or human mastery assessment is claimed for this addition.

A source hash checks continuity, not physical truth. A finite unit test checks its assertions, not every possible input. The project’s established installation and previous evidence remain distinct from this scoped extension.
