//! A mutating function with a documented all-or-nothing contract.
//!
//! Compare the two signatures:
//!
//! * [`translate_in_place`] takes `&mut` — exclusive access, so the caller cannot read the
//!   points while the call runs.
//! * [`translated`] takes `&` and returns an owned copy.
//!
//! Choosing between them is an API decision, not a style preference.

use crate::error::InputError;

/// Translate every point by `offset`, changing the caller's data.
///
/// # Errors
///
/// Returns [`InputError::EmptyInput`] for no points, [`InputError::NonFiniteParameter`] for a
/// non-finite offset, [`InputError::NonFinite`] for a rejected input coordinate, and
/// [`InputError::Overflow`] if a proposed coordinate would not be finite.
///
/// # Contract
///
/// On error the input is **unchanged**. Every coordinate is validated and every proposed
/// value is computed first; the write happens only after the whole batch is known to be
/// valid. A caller who needs the partially updated data is out of luck by design — that is
/// the decision this function documents.
///
/// # Examples
///
/// ```
/// use rust_practice::{translate_in_place, InputError};
///
/// let mut points = [[0.0, 0.0, 0.0], [f64::MAX, 0.0, 0.0]];
/// let original = points;
///
/// // Row 0 would succeed, row 1 overflows: the call fails and nothing moves.
/// let result = translate_in_place(&mut points, [f64::MAX, 0.0, 0.0]);
/// assert!(matches!(result, Err(InputError::Overflow { row: 1, .. })));
/// assert_eq!(points, original);
///
/// translate_in_place(&mut points, [1.0, 2.0, 3.0])?;
/// assert_eq!(points[0], [1.0, 2.0, 3.0]);
/// # Ok::<(), InputError>(())
/// ```
pub fn translate_in_place(points: &mut [[f64; 3]], offset: [f64; 3]) -> Result<(), InputError> {
    if points.is_empty() {
        return Err(InputError::EmptyInput);
    }
    for (axis, value) in offset.iter().enumerate() {
        if !value.is_finite() {
            return Err(InputError::NonFiniteParameter {
                name: match axis {
                    0 => "offset[0]",
                    1 => "offset[1]",
                    _ => "offset[2]",
                },
            });
        }
    }

    let mut proposed = Vec::with_capacity(points.len());
    for (row, point) in points.iter().enumerate() {
        for (column, value) in point.iter().enumerate() {
            if !value.is_finite() {
                return Err(InputError::NonFinite { row, column });
            }
        }
        let mut next = *point;
        for axis in 0..3 {
            next[axis] = point[axis] + offset[axis];
            if !next[axis].is_finite() {
                return Err(InputError::Overflow { row, column: axis });
            }
        }
        proposed.push(next);
    }

    for (point, next) in points.iter_mut().zip(proposed) {
        *point = next;
    }
    Ok(())
}

/// Translate every point by `offset` without touching the caller's data.
///
/// The preserving form allocates once. It returns a new vector, so callers that must keep
/// both versions do not need to remember to clone first.
pub fn translated(points: &[[f64; 3]], offset: [f64; 3]) -> Result<Vec<[f64; 3]>, InputError> {
    let mut owned = points.to_vec();
    translate_in_place(&mut owned, offset)?;
    Ok(owned)
}
