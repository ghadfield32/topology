# macOS/Linux setup for Go and Rust companions

```bash
go version
cd polyglot/go && go test ./... && go run ./cmd/shape-go --repo ../.. --lab stage01 && cd ../..

rustc --version
cargo --version
cd polyglot/rust && cargo test && cargo run --bin shape-rust -- --repo ../.. --lab stage01 && cd ../..

uv run --no-sync python tools/polyglot_verify.py --require-rust --output my_work/polyglot_verify01.json
```

Install Go from go.dev and Rust with the official rustup installer if either toolchain is missing.
