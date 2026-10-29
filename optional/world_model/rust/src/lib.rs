//! Dependency-free Rust companion to `optional/world_model/python`.
//!
//! Python is the full reference: it trains a small GRU world model with PyTorch and
//! reports physical-unit errors. This crate reproduces the parts of the same method
//! that are exactly checkable without a network library, so a learner can read the
//! algorithm as arithmetic and ownership instead of as tensor calls:
//!
//! * [`cartpole`] — the same four-number physics, with `terminated` and `truncated`
//!   kept apart, and a two-number visible observation.
//! * [`goals`] — the two goal functions and the averaging bug, over plain vectors.
//! * [`linear_model`] — a one-step *delta* predictor fitted by least squares. It is
//!   deliberately not a GRU: the point is that predicting the change is what makes
//!   error growth measurable, not that a small linear map is a world model.
//! * [`persistence`] — an independent F2 persistence reduction over the same
//!   filtration, so the Python H0/H1 counts are checked rather than trusted.
//! * [`topology`] — reads the committed fixture and reports counts and persistence.
//!
//! No crates are used, so `cargo test --offline --locked` works with no vendor
//! directory and no network access.

pub mod cartpole;
pub mod goals;
pub mod linear_model;
pub mod persistence;
pub mod topology;
