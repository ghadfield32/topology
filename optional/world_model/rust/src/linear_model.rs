//! A one-step *delta* predictor fitted with explicit linear algebra.
//!
//! This is not the Python model. Python trains a GRU with PyTorch; this crate fits a
//! linear map with a hand-written solve so that the *mechanics* of the method are
//! visible: features in, **change** out, then free rollout to see the error grow.
//!
//! Why the same idea still applies here: the two decisions that matter in the article
//! are not architectural. Predict the change rather than the position, and put both
//! numbers on one scale. A linear map makes both decisions impossible to hide behind a
//! deep network, which is exactly why it is a useful second implementation.
//!
//! Honest boundary: without memory this model cannot be correct, because the visible
//! observation omits the velocities. Its rollout error growth is therefore a *lower*
//! bound on what a recurrent model can achieve, not a reproduction of it.

use crate::cartpole::{Visible, THETA_LIMIT, X_LIMIT};

/// The five features: two visible numbers, a two-entry action one-hot, and a bias.
pub const FEATURES: usize = 5;

pub fn feature_vector(visible: Visible, action: u8) -> Result<[f64; FEATURES], String> {
    if action > 1 {
        return Err(format!("action must be 0 or 1, got {action}"));
    }
    let normal = visible.normalized();
    let mut values = [0.0; FEATURES];
    values[0] = normal[0];
    values[1] = normal[1];
    values[2] = if action == 1 { 1.0 } else { 0.0 };
    values[3] = if action == 0 { 1.0 } else { 0.0 };
    values[4] = 1.0;
    Ok(values)
}

/// A fitted linear delta model. Two coefficient rows, one per output dimension.
#[derive(Debug, Clone)]
pub struct DeltaModel {
    pub coefficients: [[f64; FEATURES]; 2],
    pub ridge: f64,
    pub samples: usize,
}

impl DeltaModel {
    /// Predict the next visible observation from the current one and one action.
    ///
    /// The output is written as `current + delta`, in normalized units, which is the
    /// same arithmetic as `WorldModel::step` in Python.
    pub fn predict(&self, visible: Visible, action: u8) -> Result<Visible, String> {
        let features = feature_vector(visible, action)?;
        let normal = visible.normalized();
        let mut next = [0.0; 2];
        for (row, coefficient) in self.coefficients.iter().enumerate() {
            let delta: f64 = coefficient
                .iter()
                .zip(features.iter())
                .map(|(c, f)| c * f)
                .sum();
            next[row] = normal[row] + delta;
        }
        Ok(Visible::from_normalized(next))
    }

    /// Free rollout: the output becomes the next input and reality is not consulted.
    pub fn free_rollout(&self, start: Visible, actions: &[u8]) -> Result<Vec<Visible>, String> {
        let mut current = start;
        let mut out = Vec::with_capacity(actions.len());
        for action in actions {
            current = self.predict(current, *action)?;
            out.push(current);
        }
        Ok(out)
    }
}

/// Fit by ridge-regularized normal equations with partial pivoting.
///
/// `ridge` is stated rather than tuned: it keeps the 5x5 system invertible when a
/// collection happens to contain only one action. It is not a claim about
/// generalization.
pub fn fit_delta_model(
    samples: &[(Visible, u8, Visible)],
    ridge: f64,
) -> Result<DeltaModel, String> {
    if samples.is_empty() {
        return Err("no samples to fit".to_string());
    }
    if !ridge.is_finite() || ridge < 0.0 {
        return Err("ridge must be finite and nonnegative".to_string());
    }
    let mut gram = [[0.0f64; FEATURES]; FEATURES];
    let mut rhs = [[0.0f64; FEATURES]; 2];
    for (visible, action, next) in samples {
        let features = feature_vector(*visible, *action)?;
        for (i, row) in gram.iter_mut().enumerate() {
            for (j, cell) in row.iter_mut().enumerate() {
                *cell += features[i] * features[j];
            }
        }
        let target = target_delta(*visible, *next);
        for (row, values) in rhs.iter_mut().enumerate() {
            for (i, cell) in values.iter_mut().enumerate() {
                *cell += features[i] * target[row];
            }
        }
    }
    for (i, row) in gram.iter_mut().enumerate() {
        row[i] += ridge;
    }

    let mut coefficients = [[0.0f64; FEATURES]; 2];
    for row in 0..2 {
        let solved = solve_symmetric(&gram, &rhs[row])?;
        coefficients[row] = solved;
    }
    Ok(DeltaModel {
        coefficients,
        ridge,
        samples: samples.len(),
    })
}

/// The learning target: how much the visible observation changes, in normalized units.
pub fn target_delta(visible: Visible, next: Visible) -> [f64; 2] {
    [
        (next.cart_position - visible.cart_position) / X_LIMIT,
        (next.pole_angle - visible.pole_angle) / THETA_LIMIT,
    ]
}

/// Gaussian elimination with partial pivoting on a small dense system.
fn solve_symmetric(
    matrix: &[[f64; FEATURES]; FEATURES],
    rhs: &[f64; FEATURES],
) -> Result<[f64; FEATURES], String> {
    let n = FEATURES;
    let mut a = *matrix;
    let mut b = *rhs;
    for column in 0..n {
        let mut pivot = column;
        for row in column + 1..n {
            if a[row][column].abs() > a[pivot][column].abs() {
                pivot = row;
            }
        }
        if a[pivot][column].abs() < 1e-12 {
            return Err(
                "singular normal equations; supply more data or a positive ridge".to_string(),
            );
        }
        a.swap(column, pivot);
        b.swap(column, pivot);
        let diagonal = a[column][column];
        for row in column + 1..n {
            let factor = a[row][column] / diagonal;
            if factor == 0.0 {
                continue;
            }
            for k in column..n {
                a[row][k] -= factor * a[column][k];
            }
            b[row] -= factor * b[column];
        }
    }
    let mut x = [0.0f64; FEATURES];
    for row in (0..n).rev() {
        let mut sum = b[row];
        for (k, value) in x.iter().enumerate().skip(row + 1) {
            sum -= a[row][k] * value;
        }
        x[row] = sum / a[row][row];
    }
    if x.iter().any(|value| !value.is_finite()) {
        return Err("non-finite coefficients; the fit is not usable".to_string());
    }
    Ok(x)
}

#[cfg(test)]
mod tests {
    use super::*;

    fn visible(cart: f64, angle: f64) -> Visible {
        Visible {
            cart_position: cart,
            pole_angle: angle,
        }
    }

    #[test]
    fn feature_vector_is_one_hot_and_bias() {
        let left = feature_vector(visible(1.0, 0.0), 0).expect("features");
        let right = feature_vector(visible(1.0, 0.0), 1).expect("features");
        assert_eq!(left[2], 0.0);
        assert_eq!(left[3], 1.0);
        assert_eq!(right[2], 1.0);
        assert_eq!(right[3], 0.0);
        assert_eq!(right[4], 1.0);
        assert!(feature_vector(visible(0.0, 0.0), 2).is_err());
    }

    #[test]
    fn delta_target_is_scaled_by_the_limits() {
        let delta = target_delta(visible(0.0, 0.0), visible(X_LIMIT, THETA_LIMIT));
        assert!((delta[0] - 1.0).abs() < 1e-15);
        assert!((delta[1] - 1.0).abs() < 1e-15);
    }

    #[test]
    fn a_noise_free_linear_process_is_recovered() {
        // The process moves the cart by 0.024 m and the angle by -0.02*THETA_LIMIT per
        // step, regardless of state or action. In normalized units that is a constant
        // delta of (+0.01, -0.02), which least squares must find exactly.
        let cart_step = 0.01 * X_LIMIT;
        let angle_step = -0.02 * THETA_LIMIT;
        let mut samples = Vec::new();
        for cart in [-1.0, -0.5, 0.0, 0.5, 1.0] {
            for angle in [-0.1, 0.0, 0.1] {
                for action in 0u8..2 {
                    let start = visible(cart, angle);
                    samples.push((start, action, visible(cart + cart_step, angle + angle_step)));
                }
            }
        }
        let model = fit_delta_model(&samples, 1e-9).expect("fit");
        let prediction = model.predict(visible(0.3, 0.05), 1).expect("predict");
        assert!((prediction.cart_position - (0.3 + cart_step)).abs() < 1e-6);
        assert!((prediction.pole_angle - (0.05 + angle_step)).abs() < 1e-6);
    }

    #[test]
    fn free_rollout_compounds_the_same_delta_forever() {
        let cart_step = 0.01 * X_LIMIT;
        let mut samples = Vec::new();
        for cart in [-1.0, 0.0, 1.0] {
            for action in 0u8..2 {
                let start = visible(cart, 0.0);
                samples.push((start, action, visible(cart + cart_step, 0.0)));
            }
        }
        let model = fit_delta_model(&samples, 1e-9).expect("fit");
        let path = model
            .free_rollout(visible(0.0, 0.0), &[1, 0, 1])
            .expect("rollout");
        assert_eq!(path.len(), 3);
        // Three identical deltas, because the model is linear: 3 * 0.024 m.
        assert!((path[2].cart_position - 3.0 * cart_step).abs() < 1e-6);
    }

    #[test]
    fn too_little_data_is_an_error_not_a_guess() {
        assert!(fit_delta_model(&[], 0.0).is_err());
        let single = [(visible(0.0, 0.0), 1u8, visible(0.0, 0.0))];
        assert!(
            fit_delta_model(&single, 0.0).is_err(),
            "singular without ridge"
        );
        assert!(
            fit_delta_model(&single, 1e-6).is_ok(),
            "ridge makes it solvable"
        );
    }

    #[test]
    fn missing_velocity_is_stated_not_hidden() {
        // Two states with identical visibility but different velocities get the same
        // prediction. That is the documented limitation, asserted as behaviour.
        let a = Visible {
            cart_position: 0.2,
            pole_angle: 0.05,
        };
        let model = DeltaModel {
            coefficients: [[0.0; FEATURES]; 2],
            ridge: 0.0,
            samples: 0,
        };
        assert_eq!(
            model.predict(a, 0).expect("predict"),
            model.predict(a, 1).expect("predict")
        );
    }
}
