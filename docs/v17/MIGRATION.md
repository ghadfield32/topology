# Integrate without discarding your work

This package is the supplied v16 course plus a new systems learning/navigation layer. It does not claim to contain unpublished files from your Windows checkout. The earlier log reports a local generator and171workbooks; the inspected remote did not expose that generator. New interfaces therefore live under `learning/workbooks/`, leaving your `workbooks/polyglot/` untouched.

1. Extract beside the existing repo. Inspect `git status --short --branch` and checkpoint intended local work on a review branch. Do not run reset/clean or force-unzip.
2. Preserve `.git`, real uv.lock, local setup docs, platform fixes, learner notebooks, progress, local tools and caches, downloaded data, and Kubernetes PVCs.
3. Add `systems/`, `learning/`, `learn.py`, `LEARN_TOPOLOGY.html`, `docs/v17/`, and the optional new workflow/devcontainer files only after reviewing collisions. The legacy v16 files are retained byte-for-byte in this archive; their historical version numbers are not new execution claims.
4. The old `course.py`, `native_course.py`, native protocol registry, data manifests and core catalogue remain execution authorities. The new front door delegates rather than copying their logic.
5. Preserve your real lock and run `uv lock --check`. A stale lock requires a reviewed resolver run, not copying a hand-written lock. Do not replace your production package/deployment files.
6. Test the new isolated suite, private source editing, Stage01 triad, and full-source result evidence. Then deliberately decide whether to run all171workbook interfaces and fullnativeacceptance.
7. Inspect `git diff --stat` before committing. Do not publish private answers, in-memory service captures, arbitrary absolute paths or derived noncommercial data without reviewing their rights.

## New source ownership

- `systems/catalog.json`: maps the supplied systems Stage0–9 to sys00–sys09; it does not redefine core stage order.
- `systems/lessons`: one primary systems explanation per source heading.
- `systems/c`, `cpp`, `go_service`, `rust_validator`, `pyo3`, `gpu`, `typescript`: real independent projects.
- `systems/python`: data contract, original Python calculations, verification and preparation.
- `systems/tools`: reproducible generation, workbook sweep, service probe.
- `learning`: navigation and generated interfaces. Generated reference workbooks are not learner submissions.
- `my_work`: all new private attempts, output artifacts and compiler products.

## Do not transplant environments

Windows binaries/venvs are not Linux toolchains. Recreate the environment in WSL rather than copying it. The course's native Rust sources use a vendored registry; copied private project configs point explicitly back to it. Recreate private copies after moving the entire parent course or update that path deliberately.

The default archive is a teaching repository, not an automatic production update. No remote commit, push, cluster apply, namespace removal or volume deletion is performed by opening it.

## Validate the extracted package before integration

```
python tools/verify_v17_archive.py
```
This checks the original extracted archive. It is not designed to declare your intentionally modified existing repo corrupt. Review legitimate local differences rather than replacing the manifest or erasing work to make that command green after a merge.
