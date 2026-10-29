//! Integration tests for the ownership and mutation contracts.
//!
//! These call the library exactly as a downstream user would: through the public path.

use rust_practice::{
    append_feature, dependent_feature_kernel, max_abs_row_product, rank, rank_with_feature,
    translate_in_place, translated, InputError,
};

const TOL: f64 = 1e-12;

fn iris_like() -> Vec<[f64; 4]> {
    vec![
        [5.1, 3.5, 1.4, 0.2],
        [4.9, 3.0, 1.4, 0.2],
        [4.7, 3.2, 1.3, 0.2],
        [5.0, 3.6, 1.4, 0.2],
    ]
}

fn as_rows(rows: &[[f64; 4]]) -> Vec<Vec<f64>> {
    rows.iter().map(|r| r.to_vec()).collect()
}

#[test]
fn append_borrows_the_input_and_returns_owned_rows() {
    let rows = iris_like();
    let before = rows.clone();
    let out = append_feature(&rows, 2.0, -3.0).expect("valid input");

    // The caller's data is readable and unchanged after the call.
    assert_eq!(rows, before);
    assert_eq!(out.len(), rows.len());
    for (source, produced) in rows.iter().zip(&out) {
        assert_eq!(&produced[..4], source);
        let expected = 2.0 * source[0] - 3.0 * source[1];
        assert!((produced[4] - expected).abs() < TOL);
    }
}

#[test]
fn appended_column_is_a_kernel_vector_with_zero_row_products() {
    let rows = iris_like();
    let (a, b) = (2.0, -3.0);
    let widened = append_feature(&rows, a, b).expect("valid input");
    let kernel = dependent_feature_kernel(a, b).expect("valid coefficients");
    assert_eq!(kernel, [-2.0, 3.0, 0.0, 0.0, 1.0]);

    let worst = max_abs_row_product(&widened, &kernel).expect("finite products");
    assert!(worst < 1e-12, "dependent feature must vanish, got {worst}");
}

#[test]
fn rejection_reports_the_row_and_column_and_produces_no_output() {
    let mut rows = iris_like();
    rows[2][1] = f64::NAN;
    match append_feature(&rows, 1.0, 0.0) {
        Err(InputError::NonFinite { row, column }) => {
            assert_eq!((row, column), (2, 1));
        }
        other => panic!("expected a typed nonfinite rejection, got {other:?}"),
    }
}

#[test]
fn overflow_at_a_late_row_is_still_rejected_before_any_output() {
    let mut rows = iris_like();
    rows[3][0] = f64::MAX;
    // row 3 would be 2*MAX + 0, which is infinite even though rows 0..2 are fine.
    match append_feature(&rows, 2.0, 0.0) {
        Err(InputError::Overflow { row, column }) => {
            assert_eq!(row, 3);
            assert_eq!(column, rust_practice::INPUT_COLUMNS);
        }
        other => panic!("expected a typed overflow rejection, got {other:?}"),
    }
}

#[test]
fn degenerate_coefficients_are_rejected_rather_than_silently_accepted() {
    let rows = iris_like();
    assert_eq!(
        append_feature(&rows, 0.0, 0.0),
        Err(InputError::ZeroCoefficients)
    );
    assert_eq!(
        append_feature(&rows, f64::INFINITY, 1.0),
        Err(InputError::NonFiniteParameter { name: "a" })
    );
    assert_eq!(append_feature(&[], 1.0, 1.0), Err(InputError::EmptyInput));
}

#[test]
fn failed_translation_leaves_every_point_untouched() {
    let mut points = vec![[0.0, 1.0, 2.0], [3.0, 4.0, 5.0], [6.0, 7.0, 8.0]];
    let before = points.clone();

    // Row 2 is fine, row 0 would overflow; the later failure must not leave row 2 moved.
    let mut attempted = before.clone();
    attempted[0][0] = f64::MAX;
    let snapshot = attempted.clone();
    let result = translate_in_place(&mut attempted, [f64::MAX, 0.0, 0.0]);
    assert!(matches!(result, Err(InputError::Overflow { row: 0, .. })));
    assert_eq!(attempted, snapshot);

    // A successful call does change the caller's data.
    translate_in_place(&mut points, [1.0, -1.0, 0.5]).expect("finite offset");
    assert_eq!(points[0], [1.0, 0.0, 2.5]);
    assert_ne!(points, before);
}

#[test]
fn preserving_form_leaves_the_source_row_table_alone() {
    let points = vec![[0.0, 0.0, 0.0], [1.0, 1.0, 1.0]];
    let moved = translated(&points, [2.0, 0.0, 0.0]).expect("finite offset");
    assert_eq!(points, vec![[0.0, 0.0, 0.0], [1.0, 1.0, 1.0]]);
    assert_eq!(moved, vec![[2.0, 0.0, 0.0], [3.0, 1.0, 1.0]]);
}

#[test]
fn translation_rejects_a_nonfinite_offset_without_touching_data() {
    let mut points = vec![[0.0, 0.0, 0.0]];
    let before = points.clone();
    let result = translate_in_place(&mut points, [0.0, f64::NAN, 0.0]);
    assert!(matches!(
        result,
        Err(InputError::NonFiniteParameter { name: "offset[1]" })
    ));
    assert_eq!(points, before);
}

#[test]
fn rank_reports_the_tolerance_it_used() {
    // Three rows, exactly rank 2 over the reals.
    let rows = vec![
        vec![1.0, 0.0, 0.0],
        vec![0.0, 1.0, 0.0],
        vec![1.0, 1.0, 0.0],
    ];
    assert_eq!(rank(&rows, 1e-12).expect("valid"), 2);
    assert_eq!(
        rank(&rows, 0.0),
        Err(InputError::InvalidTolerance { tolerance: 0.0 })
    );
    assert!(matches!(
        rank(&rows, -1.0),
        Err(InputError::InvalidTolerance { .. })
    ));
}

#[test]
fn a_dependent_feature_cannot_increase_rank() {
    let rows = as_rows(&iris_like());
    let (before, after) = rank_with_feature(&rows, 2.0, -3.0, 1e-12).expect("valid");
    assert_eq!(before, after, "a dependent column must not add rank");
}

#[test]
fn a_feature_inside_the_span_never_increases_rank() {
    let rows = vec![
        vec![1.0, 0.0, 0.0],
        vec![0.0, 1.0, 0.0],
        vec![0.0, 0.0, 0.0],
    ];
    let (before, after) = rank_with_feature(&rows, 1.0, 1.0, 1e-12).expect("valid");
    assert_eq!(before, 2);
    // x0 + x1 is a combination of the existing columns for these rows, so rank stays 2.
    assert_eq!(after, 2, "the added column is still inside the span here");

    let taller = vec![vec![1.0, 0.0], vec![0.0, 1.0]];
    let (b2, a2) = rank_with_feature(&taller, 1.0, 0.0, 1e-12).expect("valid");
    assert_eq!((b2, a2), (2, 2));
}

#[test]
fn a_narrower_row_table_is_rejected_before_the_feature_is_computed() {
    let rows = vec![vec![1.0], vec![2.0]];
    assert_eq!(
        rank_with_feature(&rows, 1.0, 1.0, 1e-12),
        Err(InputError::DimensionMismatch {
            expected: 2,
            found: 1
        })
    );
}

#[test]
fn ragged_input_is_a_typed_error_not_a_panic() {
    // A fixed-width array cannot be ragged, so the Vec-based entry point carries the check.
    let ragged = vec![vec![1.0, 2.0], vec![1.0]];
    assert_eq!(
        rank(&ragged, 1e-12),
        Err(InputError::RaggedRow {
            row: 1,
            expected: 2,
            found: 1
        })
    );
}
