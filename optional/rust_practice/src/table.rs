//! The row-table contract: borrow to inspect, own to produce.
//!
//! `append_feature` is the worked reference for the central practice question. Read its
//! signature before its body:
//!
//! * the input is `&[[f64; 4]]` because the function only inspects it;
//! * the output is `Vec<[f64; 5]>` because the caller cannot supply storage for rows that
//!   do not exist yet;
//! * the caller keeps its data on every path, including the failing ones.

use crate::error::InputError;

/// Number of observed columns in an input row.
pub const INPUT_COLUMNS: usize = 4;

/// Add the column `a * x0 + b * x1` to every row.
///
/// # Errors
///
/// Returns [`InputError::EmptyInput`] for no rows, [`InputError::NonFiniteParameter`] if
/// `a` or `b` is not finite, [`InputError::ZeroCoefficients`] if both are zero,
/// [`InputError::NonFinite`] for a rejected input cell, and [`InputError::Overflow`] if a
/// proposed value would be infinite.
///
/// The whole table is validated before any output row is built, so a rejection after an
/// earlier row was processed still returns `Err` and produces no partial `Vec`.
///
/// # Examples
///
/// ```
/// use rust_practice::{append_feature, InputError};
///
/// let rows = [[1.0, 2.0, 3.0, 4.0], [5.0, 6.0, 7.0, 8.0]];
/// let widened = append_feature(&rows, 2.0, -1.0)?;
///
/// // The caller still owns the original table.
/// assert_eq!(rows[0], [1.0, 2.0, 3.0, 4.0]);
/// assert_eq!(widened[0], [1.0, 2.0, 3.0, 4.0, 2.0 * 1.0 - 1.0 * 2.0]);
///
/// // A degenerate feature is rejected rather than silently added as a constant column.
/// assert_eq!(append_feature(&rows, 0.0, 0.0), Err(InputError::ZeroCoefficients));
/// # Ok::<(), InputError>(())
/// ```
pub fn append_feature(rows: &[[f64; 4]], a: f64, b: f64) -> Result<Vec<[f64; 5]>, InputError> {
    if rows.is_empty() {
        return Err(InputError::EmptyInput);
    }
    if !a.is_finite() {
        return Err(InputError::NonFiniteParameter { name: "a" });
    }
    if !b.is_finite() {
        return Err(InputError::NonFiniteParameter { name: "b" });
    }
    if a == 0.0 && b == 0.0 {
        return Err(InputError::ZeroCoefficients);
    }

    // Validation pass: nothing is produced until every cell and every proposed value is
    // known to be finite.
    let mut proposed = Vec::with_capacity(rows.len());
    for (row, cells) in rows.iter().enumerate() {
        for (column, value) in cells.iter().enumerate() {
            if !value.is_finite() {
                return Err(InputError::NonFinite { row, column });
            }
        }
        let added = a * cells[0] + b * cells[1];
        if !added.is_finite() {
            return Err(InputError::Overflow {
                row,
                column: INPUT_COLUMNS,
            });
        }
        proposed.push(added);
    }

    // Construction pass: only now is the owned output allocated row by row.
    let mut out = Vec::with_capacity(rows.len());
    for (cells, added) in rows.iter().zip(proposed) {
        out.push([cells[0], cells[1], cells[2], cells[3], added]);
    }
    Ok(out)
}

/// The five coefficients `v` satisfying `A v = 0` when the fifth column is `a*x0 + b*x1`.
///
/// Because the added column is an exact linear combination of the first two, the widened
/// matrix cannot gain rank. The kernel vector makes that statement testable.
pub fn dependent_feature_kernel(a: f64, b: f64) -> Result<[f64; 5], InputError> {
    if !a.is_finite() {
        return Err(InputError::NonFiniteParameter { name: "a" });
    }
    if !b.is_finite() {
        return Err(InputError::NonFiniteParameter { name: "b" });
    }
    if a == 0.0 && b == 0.0 {
        return Err(InputError::ZeroCoefficients);
    }
    Ok([-a, -b, 0.0, 0.0, 1.0])
}

/// Largest absolute entry of `rows * v`, used to check a claimed kernel vector.
pub fn max_abs_row_product<R: AsRef<[f64]>>(rows: &[R], v: &[f64]) -> Result<f64, InputError> {
    if rows.is_empty() {
        return Err(InputError::EmptyInput);
    }
    let width = rows[0].as_ref().len();
    if v.len() != width {
        return Err(InputError::DimensionMismatch {
            expected: width,
            found: v.len(),
        });
    }
    let mut worst = 0.0_f64;
    for (row, cells) in rows.iter().enumerate() {
        let cells = cells.as_ref();
        if cells.len() != width {
            return Err(InputError::RaggedRow {
                row,
                expected: width,
                found: cells.len(),
            });
        }
        let mut total = 0.0;
        for (column, value) in cells.iter().enumerate() {
            if !value.is_finite() {
                return Err(InputError::NonFinite { row, column });
            }
            total += value * v[column];
        }
        worst = worst.max(total.abs());
    }
    Ok(worst)
}
