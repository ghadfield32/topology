//! WM05 — fit a transition model from data.
//!
//! The model is a linear map on five features. That is deliberately small: the point is to
//! see that `predict` uses **fitted coefficients** and never calls the simulator. If you
//! delete `simulator::step` from the program after collection, prediction must still work.
//!
//! Five features: normalized cart position, normalized pole angle, a two-entry action
//! one-hot, and a bias. Two outputs: the normalized change in each visible number.
//!
//! Python sibling: `python/wm05_model.py` (same features, same ridge, same solve).

use crate::action::Action;
use crate::dataset::Transition;
use crate::state::{State, THETA_LIMIT, X_LIMIT};

/// Number of features in the design matrix.
pub const FEATURES: usize = 5;
/// Number of predicted outputs.
pub const OUTPUTS: usize = 2;

/// Build the feature row for one state/action pair.
pub fn features(state: State, action: Action) -> [f64; FEATURES] {
    let normalized = state.normalized();
    let mut row = [0.0; FEATURES];
    row[0] = normalized[0];
    row[1] = normalized[1];
    row[2] = if action == Action::Right { 1.0 } else { 0.0 };
    row[3] = if action == Action::Left { 1.0 } else { 0.0 };
    row[4] = 1.0;
    row
}

/// A fitted linear delta model. It owns its coefficients and borrows nothing.
#[derive(Debug, Clone, PartialEq)]
pub struct DeltaModel {
    /// `coefficients[output][feature]`.
    pub coefficients: [[f64; FEATURES]; OUTPUTS],
    /// The ridge term that was used. Zero would be singular for some datasets.
    pub ridge: f64,
    /// How many transitions the fit saw.
    pub samples: usize,
}

impl DeltaModel {
    /// Fit by ridge-regularized normal equations.
    ///
    /// `training` is **borrowed**: the fit reads the transitions and returns a new model
    /// that owns only its coefficients, so the caller keeps its data.
    pub fn fit(training: &[Transition], ridge: f64) -> Result<Self, String> {
        if training.is_empty() {
            return Err("no transitions to fit".to_string());
        }
        if !ridge.is_finite() || ridge < 0.0 {
            return Err("ridge must be finite and nonnegative".to_string());
        }

        // Accumulate the 5x5 Gram matrix and the two right-hand sides.
        let mut gram = [[0.0f64; FEATURES]; FEATURES];
        let mut rhs = [[0.0f64; FEATURES]; OUTPUTS];
        for row in training {
            let x = features(row.state, row.action);
            for (i, left) in x.iter().enumerate() {
                for (j, right) in x.iter().enumerate() {
                    gram[i][j] += left * right;
                }
            }
            let target = row.visible_delta();
            for (output, column) in rhs.iter_mut().enumerate() {
                for (i, value) in column.iter_mut().enumerate() {
                    *value += x[i] * target[output];
                }
            }
        }
        for (i, row) in gram.iter_mut().enumerate() {
            row[i] += ridge;
        }

        let mut coefficients = [[0.0f64; FEATURES]; OUTPUTS];
        for output in 0..OUTPUTS {
            coefficients[output] = solve(&gram, &rhs[output])?;
        }
        Ok(Self {
            coefficients,
            ridge,
            samples: training.len(),
        })
    }

    /// Predict the next state. This is the only place dynamics live after fitting.
    pub fn predict(&self, state: State, action: Action) -> Result<State, String> {
        let x = features(state, action);
        let now = state.normalized();
        let mut next_visible = [0.0f64; 2];
        for output in 0..OUTPUTS {
            let delta: f64 = self.coefficients[output]
                .iter()
                .zip(x.iter())
                .map(|(coefficient, feature)| coefficient * feature)
                .sum();
            next_visible[output] = now[output] + delta;
        }
        // Only the two visible numbers move. The velocities are not observable to this
        // model, so it does not invent them; it reports the state it would observe.
        let (x_position, theta) = State::from_normalized(next_visible);
        State::new(x_position, state.v, theta, state.omega)
    }

    /// A copy of the coefficients, for checking that planning did not mutate them.
    pub fn weights(&self) -> Vec<f64> {
        self.coefficients.iter().flatten().copied().collect()
    }
}

/// Gaussian elimination with partial pivoting, on a small dense system.
///
/// Written out so the learner can read the algorithm instead of trusting a library. The
/// pivot threshold is explicit: `1e-12` is a statement about how close to singular is
/// "singular", and without it a rank-deficient system returns confident nonsense.
fn solve(
    matrix: &[[f64; FEATURES]; FEATURES],
    rhs: &[f64; FEATURES],
) -> Result<[f64; FEATURES], String> {
    let n = FEATURES;
    let mut a = *matrix;
    let mut b = *rhs;
    for column in 0..n {
        let mut pivot = column;
        for row in (column + 1)..n {
            if a[row][column].abs() > a[pivot][column].abs() {
                pivot = row;
            }
        }
        if a[pivot][column].abs() < 1e-12 {
            return Err(
                "normal equations are singular; collect more varied data or use ridge".to_string(),
            );
        }
        a.swap(column, pivot);
        b.swap(column, pivot);
        let diagonal = a[column][column];
        for row in (column + 1)..n {
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
    let mut solution = [0.0f64; FEATURES];
    for row in (0..n).rev() {
        let mut sum = b[row];
        for (k, value) in solution.iter().enumerate().skip(row + 1) {
            sum -= a[row][k] * value;
        }
        solution[row] = sum / a[row][row];
    }
    if solution.iter().any(|value| !value.is_finite()) {
        return Err("the fit produced non-finite coefficients".to_string());
    }
    Ok(solution)
}

/// Normalize a state's visible numbers, for a caller that needs the same scale.
pub fn normalized_limits() -> [f64; 2] {
    [X_LIMIT, THETA_LIMIT]
}

#[cfg(test)]
mod tests {
    use super::*;
    use crate::dataset::{collect, CollectConfig, Rng};
    use crate::state::{State, X_LIMIT};

    fn rows() -> Vec<Transition> {
        let mut rng = Rng::new(31);
        collect(
            &mut rng,
            CollectConfig {
                episodes: 8,
                max_steps: 80,
                exploration: 0.4,
                bias_scale: 0.15,
            },
        )
        .expect("collect")
    }

    #[test]
    fn feature_row_is_a_one_hot_plus_a_bias() {
        let state = State::new(1.2, 0.0, 0.0, 0.0).expect("finite");
        let left = features(state, Action::Left);
        let right = features(state, Action::Right);
        assert_eq!(left[2], 0.0);
        assert_eq!(left[3], 1.0);
        assert_eq!(right[2], 1.0);
        assert_eq!(right[3], 0.0);
        assert_eq!(left[4], 1.0);
        assert_eq!(right[4], 1.0);
        assert!((left[0] - 1.2 / X_LIMIT).abs() < 1e-15);
    }

    #[test]
    fn fitting_borrows_the_training_data() {
        let data = rows();
        let before = data.len();
        let model = DeltaModel::fit(&data, 1e-6).expect("fit");
        // The data is still usable afterwards: the fit borrowed it.
        assert_eq!(data.len(), before);
        assert_eq!(model.samples, before);
    }

    #[test]
    fn prediction_never_calls_the_simulator() {
        // A model fitted on a constant delta must reproduce that delta everywhere,
        // including at states the simulator would never produce.
        let mut synthetic = Vec::new();
        for state in [
            State::new(0.0, 0.0, 0.0, 0.0).expect("finite"),
            State::new(1.0, 0.0, 0.1, 0.0).expect("finite"),
            State::new(-1.0, 0.0, -0.1, 0.0).expect("finite"),
        ] {
            for action in Action::ALL {
                let successor =
                    State::new(state.x + 0.01 * X_LIMIT, state.v, state.theta, state.omega)
                        .expect("finite");
                synthetic.push(Transition {
                    episode: 0,
                    tick: 0,
                    state,
                    action,
                    successor,
                    terminated: false,
                    truncated: true,
                });
            }
        }
        let model = DeltaModel::fit(&synthetic, 1e-9).expect("fit");
        let probe = State::new(0.7, 5.0, 0.15, -3.0).expect("finite");
        let predicted = model.predict(probe, Action::Right).expect("predict");
        assert!((predicted.x - (0.7 + 0.01 * X_LIMIT)).abs() < 1e-9);
        // Velocities are reported unchanged, not invented.
        assert_eq!(predicted.v, probe.v);
        assert_eq!(predicted.omega, probe.omega);
    }

    #[test]
    fn the_fit_learns_real_dynamics_better_than_nothing() {
        let data = rows();
        let model = DeltaModel::fit(&data, 1e-6).expect("fit");
        let mut model_error = 0.0;
        let mut frozen_error = 0.0;
        for row in &data {
            let predicted = model.predict(row.state, row.action).expect("predict");
            model_error += (predicted.theta - row.successor.theta).abs();
            frozen_error += (row.state.theta - row.successor.theta).abs();
        }
        // Not a strong claim: only that fitting is doing something.
        assert!(
            model_error < frozen_error,
            "model {model_error} vs frozen {frozen_error}"
        );
    }

    #[test]
    fn bad_inputs_are_errors() {
        assert!(DeltaModel::fit(&[], 0.0).is_err());
        let data = rows();
        assert!(DeltaModel::fit(&data, -1.0).is_err());
        assert!(DeltaModel::fit(&data, f64::NAN).is_err());
    }

    #[test]
    fn weights_are_a_stable_copy() {
        let model = DeltaModel::fit(&rows(), 1e-6).expect("fit");
        let first = model.weights();
        let second = model.weights();
        assert_eq!(first, second);
        assert_eq!(first.len(), FEATURES * OUTPUTS);
    }
}
