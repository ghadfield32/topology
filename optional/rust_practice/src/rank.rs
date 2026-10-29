//! A tolerance-explicit rank, and the rank consequence of a dependent feature.
//!
//! Rank here means the numerical rank of a row table over the reals, computed by Gaussian
//! elimination with partial pivoting. The tolerance is a *choice*: it decides which pivot is
//! treated as zero. Reporting a rank without its tolerance is an incomplete result.

use crate::error::InputError;

/// Numerical rank of `rows`, treating a pivot with `|value| <= tolerance` as zero.
///
/// Rows are interpreted as observations and columns as features; the rank is the same
/// either way, but the caller should say which is which.
///
/// # Examples
///
/// ```
/// use rust_practice::rank;
///
/// let rows = vec![
///     vec![1.0, 0.0, 0.0],
///     vec![0.0, 1.0, 0.0],
///     vec![1.0, 1.0, 0.0],
/// ];
/// // The third row is the sum of the first two, so the rank is 2, not 3.
/// assert_eq!(rank(&rows, 1e-12)?, 2);
/// # Ok::<(), rust_practice::InputError>(())
/// ```
pub fn rank(rows: &[Vec<f64>], tolerance: f64) -> Result<usize, InputError> {
    if rows.is_empty() {
        return Err(InputError::EmptyInput);
    }
    if !tolerance.is_finite() || tolerance <= 0.0 {
        return Err(InputError::InvalidTolerance { tolerance });
    }
    let columns = rows[0].len();
    for (row, cells) in rows.iter().enumerate() {
        if cells.len() != columns {
            return Err(InputError::RaggedRow {
                row,
                expected: columns,
                found: cells.len(),
            });
        }
        for (column, value) in cells.iter().enumerate() {
            if !value.is_finite() {
                return Err(InputError::NonFinite { row, column });
            }
        }
    }

    // Elimination works on an owned copy: the borrowed input stays inspectable, and a
    // caller who passes a large table pays for one deliberate copy rather than hidden
    // aliasing.
    let mut work: Vec<Vec<f64>> = rows.to_vec();
    let mut pivot_row = 0;
    for column in 0..columns {
        let best = (pivot_row..work.len())
            .max_by(|&l, &r| {
                work[l][column]
                    .abs()
                    .partial_cmp(&work[r][column].abs())
                    .expect("values are finite")
            })
            .expect("pivot range is non-empty");
        if work[best][column].abs() <= tolerance {
            continue;
        }
        work.swap(pivot_row, best);
        let pivot = work[pivot_row][column];
        for row in (pivot_row + 1)..work.len() {
            let factor = work[row][column] / pivot;
            if factor == 0.0 {
                continue;
            }
            // `pivot_row < row`, so split_at_mut gives one shared pivot row and one
            // exclusive target row without an extra allocation or an index loop.
            let (above, target) = work.split_at_mut(row);
            let source = &above[pivot_row][column..columns];
            for (value, pivot_value) in target[0][column..columns].iter_mut().zip(source) {
                *value -= factor * pivot_value;
            }
        }
        pivot_row += 1;
        if pivot_row == work.len() {
            break;
        }
    }
    Ok(pivot_row)
}

/// Rank of `rows` after appending the column `a * x0 + b * x1`.
///
/// The added column is a linear combination of two existing columns, so the widened matrix
/// has the same rank as the original. This function exists so the claim is measured on real
/// data rather than asserted; it returns both ranks instead of hiding one of them.
pub fn rank_with_feature(
    rows: &[Vec<f64>],
    a: f64,
    b: f64,
    tolerance: f64,
) -> Result<(usize, usize), InputError> {
    if !a.is_finite() {
        return Err(InputError::NonFiniteParameter { name: "a" });
    }
    if !b.is_finite() {
        return Err(InputError::NonFiniteParameter { name: "b" });
    }
    if a == 0.0 && b == 0.0 {
        return Err(InputError::ZeroCoefficients);
    }
    if rows.is_empty() {
        return Err(InputError::EmptyInput);
    }
    let width = rows[0].len();
    if width < 2 {
        return Err(InputError::DimensionMismatch {
            expected: 2,
            found: width,
        });
    }

    let before = rank(rows, tolerance)?;
    let mut widened = Vec::with_capacity(rows.len());
    for (row, cells) in rows.iter().enumerate() {
        if cells.len() != width {
            return Err(InputError::RaggedRow {
                row,
                expected: width,
                found: cells.len(),
            });
        }
        let added = a * cells[0] + b * cells[1];
        if !added.is_finite() {
            return Err(InputError::Overflow { row, column: width });
        }
        let mut next = Vec::with_capacity(width + 1);
        next.extend_from_slice(cells);
        next.push(added);
        widened.push(next);
    }
    let after = rank(&widened, tolerance)?;
    Ok((before, after))
}
