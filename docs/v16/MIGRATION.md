# Review-based migration; do not overwrite a working course

This archive contains the v14 baseline plus native16. Your existing Git repo may use v12 with local fixes. Do not replace its project files or reset its history merely to match a ZIP version label.

1. Extract the archive beside the repo. Inspect `git status` in the existing repo and create a review branch without discarding work.
2. Copy the additive paths `native/`, `native_course.py`, `START_NATIVE.html`, `docs/v16/`, and `tests/test_native_v16.py` to paths that do not already contain your work. The native workspaces are independent of the Python package version.
3. Review the compatibility replacement `polyglot.py`, optional `START_HERE.html` navigation link, ignore additions, and `.github/workflows/native-course-v16.yml` separately. Keep existing workflows and adjust paths in a monorepo.
4. Preserve the genuine `uv.lock`, `pyproject.toml`, local Windows fixes, `docs/LOCAL_SETUP.md`, `.local-bin`, all `my_work` and progress/evidence files. The archive does not include a new resolved Python lock.
5. Install the declared Go/Rust toolchains, run native unit tests, then Stage 01 and data verification. Run full native acceptance before broader adoption. Keep failures and successes in distinct output directories.
6. Review the diff before any commit/push. This delivery does not merge the existing Poux PR or replace your main branch.

`native/rust/vendor` contains dependency source with licenses; keep it and its matching Cargo.lock/config together. Do not commit build output or a compiler toolchain. Existing `polyglot/go` and `polyglot/rust` companions remain historical source in the full archive; use `native/` for the current execution path.

The isolated remote branch `learning/native-parity-v16` contains a compiler-provisioning workflow only. Its successful artifact enabled local Rust verification; it is not the full package, nor a reason to merge that branch as the completed course. New native source is supplied in this ZIP. The earlier remote core CI succeeded on three platforms, but that does not certify these new native files on those platforms.
