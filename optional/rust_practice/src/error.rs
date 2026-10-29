//! Typed input errors, so a rejected record is a value the caller must handle.
//!
//! `Result` alone does not say whether the caller's data was changed. Every function in
//! this crate that can fail either takes its data by shared reference or documents that a
//! failure leaves the input untouched.

use std::fmt;

/// One rejected input, naming where it was rejected.
#[derive(Debug, Clone, PartialEq)]
pub enum InputError {
    /// No rows were supplied where at least one was required.
    EmptyInput,
    /// A row had a different length from the first row.
    RaggedRow {
        row: usize,
        expected: usize,
        found: usize,
    },
    /// A required dimension is missing or does not match the data.
    DimensionMismatch { expected: usize, found: usize },
    /// A finite number is required; `NaN` and the infinities are rejected.
    NonFinite { row: usize, column: usize },
    /// Both feature coefficients were zero, so the added column carries no information.
    ZeroCoefficients,
    /// A coefficient or offset itself was not a finite number.
    NonFiniteParameter { name: &'static str },
    /// A proposed value was not finite, so the operation was abandoned.
    Overflow { row: usize, column: usize },
    /// The rank tolerance was not strictly positive and finite.
    InvalidTolerance { tolerance: f64 },
}

impl fmt::Display for InputError {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        match self {
            InputError::EmptyInput => write!(f, "input is empty"),
            InputError::RaggedRow {
                row,
                expected,
                found,
            } => write!(
                f,
                "row {row} has {found} columns, expected {expected} from row 0"
            ),
            InputError::NonFinite { row, column } => {
                write!(f, "row {row} column {column} is not a finite number")
            }
            InputError::DimensionMismatch { expected, found } => {
                write!(f, "expected {expected} values, found {found}")
            }
            InputError::ZeroCoefficients => {
                write!(f, "both feature coefficients are zero")
            }
            InputError::NonFiniteParameter { name } => {
                write!(f, "parameter `{name}` is not a finite number")
            }
            InputError::Overflow { row, column } => write!(
                f,
                "the value proposed for row {row} column {column} is not finite; \
                 the input was left unchanged"
            ),
            InputError::InvalidTolerance { tolerance } => write!(
                f,
                "tolerance {tolerance} must be finite and strictly positive"
            ),
        }
    }
}

impl std::error::Error for InputError {}
