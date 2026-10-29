//! # Optional Rust practice
//!
//! An additive crate for ownership, API contracts and typed errors. It sits beside the
//! course; it is **not a second curriculum** and owns no stage order or lab catalogue.
//!
//! What the module layout is meant to make visible:
//!
//! * [`mod@error`] — a rejected record is data the caller must handle, not a panic.
//! * [`mod@table`] — borrow to inspect, own to produce; the whole table is validated before
//!   any output row exists.
//! * [`mod@translate`] — a mutating function whose on-error behaviour is documented and tested.
//! * [`mod@rank`] — a numerical rank that always reports its tolerance.
//!
//! The worked reference is not the assignment. See `EXERCISES.md` for the independent
//! change, which stays `not_assessed` until the learner demonstrates it.
#![forbid(unsafe_code)]

pub mod error;
pub mod rank;
pub mod table;
pub mod translate;

pub use error::InputError;
pub use rank::{rank, rank_with_feature};
pub use table::{append_feature, dependent_feature_kernel, max_abs_row_product, INPUT_COLUMNS};
pub use translate::{translate_in_place, translated};
