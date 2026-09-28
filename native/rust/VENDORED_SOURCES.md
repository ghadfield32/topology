# Vendored dependency sources

The 36 source crates in `vendor/` were resolved by Cargo from the pinned manifest on an isolated verification workflow and then used for a real `cargo test --offline --locked` and release build. Cargo.lock and `.cargo/config.toml` are part of that contract. Keep each crate's own license and metadata. These source crates are not the compiler or platform linker.

Do not patch read-only vendored sources silently. Use an explicit local patch/dependency change, document it, resolve the resulting lock and rerun acceptance. See the official Cargo documentation: https://doc.rust-lang.org/cargo/commands/cargo-vendor.html .
