# Windows setup for Go and Rust companions

Run these from the course repository root in PowerShell.

## Go

Install Go 1.23+ using the official installer, then verify:

```powershell
go version
Push-Location polyglot/go
go test ./...
go run ./cmd/shape-go --repo ../.. --lab stage01
Pop-Location
```

## Rust

Install Rust through `rustup` from the official Rust site. Then:

```powershell
rustc --version
cargo --version
Push-Location polyglot/rust
cargo test
cargo run --bin shape-rust -- --repo ../.. --lab stage01
Pop-Location
```

The Rust crate has no third-party dependencies, so after the Rust toolchain itself is installed it does not need crates.io dependencies for these labs.

## Verify both

```powershell
uv run --no-sync python tools/polyglot_verify.py --require-rust --output my_work/polyglot_verify01.json
```

Do not call Rust "verified" until this command records a successful Cargo test on your machine or CI.
