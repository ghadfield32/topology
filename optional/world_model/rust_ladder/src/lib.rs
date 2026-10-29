//! WM01–WM09: a beginner ladder from `Hello, world!` to a working world model.
//!
//! This crate sits beside [`super`](../README.md) deliberately. The sibling crate
//! (`optional/world_model/rust/`) is the *reference* companion: it reproduces the article's
//! method with an independent persistence reduction and a least-squares delta model. This
//! crate is the *learning* ladder: one idea per module, small enough to type by hand, in
//! the order a person actually builds such a project.
//!
//! | Module | Rung | Rust you practise | Modelling idea |
//! |---|---|---|---|
//! | [`state`] | WM01 | structs, fields, `f64` | represent a state |
//! | [`action`] | WM02 | enums, `match` | represent a choice |
//! | [`simulator`] | WM03 | methods, `Result`, `?` | calculate and validate a step |
//! | [`dataset`] | WM04 | vectors, loops, records | keep episodes and successors |
//! | [`model`] | WM05 | borrowed slices, fits | learn from data |
//! | [`rollout`] | WM06 | evaluation loops | one step versus free rollout |
//! | [`planner`] | WM07 | borrowing, goals | act without refitting |
//! | [`shape`] | WM08 | graphs, projections | describe geometry, not dynamics |
//! | [`experiment`] | WM09 | files, CLI, output dirs | save a repeatable run |
//!
//! Every module has a Python sibling in `python/` with the same name and the same numbers,
//! so the comparison is about the *languages*, not about two different experiments.
//!
//! **The complete state is used here.** The article hides the velocities and needs a GRU to
//! infer them; that is the right second step, not the first. Nothing in this crate is a
//! reproduction of the article's scores.

pub mod action;
pub mod dataset;
pub mod experiment;
pub mod model;
pub mod planner;
pub mod rollout;
pub mod shape;
pub mod simulator;
pub mod state;
