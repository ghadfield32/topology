# Install once; keep your current learning progress

This is the combined native16 edition built from the available v14 archive, not from an unverified v15 link. It preserves the Python course and the Poux addition. It adds `native/` and `native_course.py`; it does not require restarting Stage 00. Geoff's current learning position is Stage 01.

## 1. What each tool does

**Python/uv** supply the existing course environment and the comparison driver. **Go** compiles the native Go program. **rustup** installs Rust toolchains; **Cargo** resolves/builds/tests Rust crates. **Docker** packages a program and its runtime files into an image. **Kubernetes** schedules an image and manages work and storage. A successful native run does not prove a container or cluster ran.

Go and Rust do their own computation and data decoding. The Python driver invokes the binaries and checks outputs. It does not secretly implement their models for them. The independent Python reference checks use NumPy/Pillow, the original Python topology implementation, and PyTorch as separate checks.

## 2. Preserve your working repository

Extract the full ZIP beside your current repository. Create a review branch in your existing repo; inspect `git status` before copying anything. Do not unzip over the repository blindly. Preserve `.git/`, your real `uv.lock`, `my_work/`, edited learner notebooks, active progress logs, `.local-bin/`, `.uv-cache/`, `.uv-python/`, local setup notes, and existing PVCs.

The intended additive paths are `native/`, `native_course.py`, `START_NATIVE.html`, `docs/v16/`, and `tests/test_native_v16.py`. The top-level `polyglot.py` compatibility entry redirects old `run/list/verify` requests to the new native workspace. Keep the prior Go/Rust companion sources for comparison but treat them as historical, not the required execution route. Poux remains under `curriculum/extensions/poux_spatial_ai/`.

No new Python dependencies are required by the native CLI itself. Data comparison needs the existing NumPy/Pillow course environment, and `--science` additionally needs PyTorch. The archive does not invent a Python lockfile; preserve and validate the one already resolved in your repo. `uv run --no-sync` deliberately uses your prepared environment without silently changing dependency resolution.

## 3. Native toolchains

This delivery actually executed **Go 1.23.2** and **Rust/Cargo 1.90.0**, on Linux x86_64. These are tested reference versions, not a claim to be the newest or suitable for exposed production services. Use current security-maintained tools for production after running the acceptance matrix.

Install Go through https://go.dev/doc/install and Rust through https://rustup.rs/ . On Windows, the standard MSVC Rust target also needs Microsoft's C++ linker/build tools when not already installed. Do not assume Python/uv installed a C++ linker. On macOS, install the platform command-line developer tools if the linker is missing.

For the tested Rust compiler:
```
rustup toolchain install 1.90.0 --profile minimal
```
`native/rust/rust-toolchain.toml` selects it in that workspace. The source requires Rust >=1.83, but this delivery certifies 1.90.0 only. Rust dependencies have a genuine Cargo.lock and **36 vendored source crates**, including their license files. After compiler installation, `cargo test --offline --locked` does not need crates.io for those crates. Vendored dependencies do not include the Rust compiler, system linker or Docker base images.

Go uses only the standard library. There is no fake or unnecessary go.sum. `go.mod` is still the module/version contract.

## 4. Windows PowerShell: first native acceptance

From the course root:
```powershell
$env:PYTHONUTF8 = '1'
# Preserve these settings when using your existing local uv installation:
$env:UV_CACHE_DIR = Join-Path $PWD.Path '.uv-cache'
$env:UV_PYTHON_INSTALL_DIR = Join-Path $PWD.Path '.uv-python'

go version
rustc --version
cargo --version
uv run --no-sync python native_course.py doctor
uv run --no-sync python native_course.py build --lang all --output my_work/native_build01
uv run --no-sync python native_course.py test --lang all --output my_work/native_tests01
uv run --no-sync python native_course.py compare --lab stage01 --output my_work/native_stage01_01
```

Open `my_work/native_stage01_01/index.html`, `execution.json` and the two `stage01.json` files. Each result records what it consumed and what it computed. No stage is marked assessed.

## 5. macOS/Linux

Use the same `python native_course.py ...` commands through your existing uv environment. Do not copy a Windows `.venv` to macOS or Linux. The native code has no required CUDA path, so the mathematical labs do not need an RTX card. This delivery did not execute macOS or Windows native acceptance; run it on your machine rather than interpreting cross-platform source as a cross-platform test result.

## 6. Entire native inventory and data checks

```
uv run --no-sync python native_course.py list
uv run --no-sync python native_course.py data list
uv run --no-sync python native_course.py data verify --lang all --output my_work/native_data01
uv run --no-sync python native_course.py verify --science --output my_work/native_acceptance01
```

`verify --science` runs both native test suites, every native unit, decoded-source comparisons, valid/invalid parser fixtures, and selected independent NumPy/Python/PyTorch checks. It does not replay all 133 original notebooks. Its result states that scope explicitly.

`--require-original-parity` intentionally refuses a full-original equivalence claim while the coverage ledger contains gaps. Do not remove that check just to make a screen green.

## 7. Run a binary without a Python launcher

From `native/go`:
```
go test -count=1 ./...
go run ./cmd/shape-go --repo ../.. --lab stage01
```
From `native/rust`:
```
cargo test --offline --locked
cargo run --offline --locked --release --bin shape-rust -- --repo ../.. --lab stage01
```

Run Cargo from its workspace so it discovers `.cargo/config.toml`. Merely passing a manifest path from an unrelated directory does not necessarily discover that workspace's Cargo configuration. Both native CLIs also support `--decode RELATIVE_FILE`, `--list`, and `--output NEW_DIRECTORY`.

## 8. Typical failures

| Failure | What to inspect; do not hide it |
|---|---|
| `cargo`/`rustc` missing | Toolchain installation and PATH; a Rust source file is not a compiled program. |
| C++ linker unavailable | Windows build-tools installation; not a math error. |
| Offline crate not found | Run from `native/rust`; preserve vendor and its config. Never delete the lock to force resolution. |
| Python package missing | Use the existing course environment; native compilation is separate from NumPy/PyTorch audit dependencies. |
| Output directory exists | Choose a new attempt name. Do not erase earlier evidence automatically. |
| Dataset hash mismatch | Stop and inspect the changed source. Do not simply rewrite the expected hash. |
| Native mismatch | Compare input IDs, units, dtype, algorithm, parameter choices, tolerances and intermediates. |
| Model does worse than baseline | Preserve the result and investigate the protocol; a bad model score is not a compiler failure. |

## 9. First real learning session

```
uv run --no-sync python native_course.py show stage01
uv run --no-sync python native_course.py prepare --lab stage01 --output my_work/stage01_native_practice01
```

Read the primary Python lesson once. Make the hand prediction. The private workspace contains editable native source and three independent challenges, not an automatically graded completion. Follow its START.md. A copied reference solution is guided practice, not independent mastery.

After Stage 01, try `poux_bridge`: count-weighted means from selected basketball observations. Then continue to Stage 02. Do not perform a full environment reinstall for each lesson.
