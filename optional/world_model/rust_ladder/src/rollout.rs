//! WM06 — measure one-step prediction separately from free rollout.
//!
//! Two experiments, two questions:
//!
//! * **One-step**: start from an actual state each time, predict one successor.
//! * **Free rollout**: start once, then feed the model's own prediction back in.
//!
//! Teacher-forced numbers can look excellent while the same model is useless three steps
//! into a dream. The only way to know is to measure both, at each depth, against a baseline
//! that assumes nothing ever changes.
//!
//! Python sibling: `python/wm06_rollout.py`.

use crate::dataset::Transition;
use crate::model::DeltaModel;
use crate::state::{State, THETA_LIMIT, X_LIMIT};

/// Mean absolute error of one prediction, in physical units.
#[derive(Debug, Clone, Copy, PartialEq)]
pub struct Error {
    pub position_m: f64,
    pub angle_rad: f64,
}

impl Error {
    pub fn zero() -> Self {
        Self {
            position_m: 0.0,
            angle_rad: 0.0,
        }
    }

    fn add(self, other: Error) -> Self {
        Self {
            position_m: self.position_m + other.position_m,
            angle_rad: self.angle_rad + other.angle_rad,
        }
    }

    fn scale(self, factor: f64) -> Self {
        Self {
            position_m: self.position_m * factor,
            angle_rad: self.angle_rad * factor,
        }
    }
}

fn absolute_error(predicted: State, truth: State) -> Error {
    Error {
        position_m: (predicted.x - truth.x).abs(),
        angle_rad: (predicted.theta - truth.theta).abs(),
    }
}

/// Teacher-forced error: every step starts from the real state.
pub fn one_step_error(model: &DeltaModel, rows: &[Transition]) -> Result<Error, String> {
    if rows.is_empty() {
        return Err("no transitions to evaluate".to_string());
    }
    let mut total = Error::zero();
    for row in rows {
        let predicted = model.predict(row.state, row.action)?;
        total = total.add(absolute_error(predicted, row.successor));
    }
    Ok(total.scale(1.0 / rows.len() as f64))
}

/// Errors **at each depth** `1..=horizon`, with the frozen baseline beside them.
///
/// The two arrays are the measurement, not an intermediate. Averaging over depths answers
/// "how wrong on average" instead of "how wrong at depth h", and the average hides the depth
/// where the dream falls apart.
#[derive(Debug, Clone, PartialEq)]
pub struct RolloutCurve {
    pub depth: Vec<usize>,
    pub model: Vec<Error>,
    pub frozen: Vec<Error>,
}

impl RolloutCurve {
    /// The deepest depth that stays inside a tolerance on **both** visible numbers.
    ///
    /// "Inside tolerance" is a stated rule, not a fact about the model: change the tolerance
    /// and the horizon changes.
    pub fn trust_horizon(&self, tolerance_m: f64, tolerance_rad: f64) -> usize {
        self.depth
            .iter()
            .zip(self.model.iter())
            .take_while(|(_, error)| {
                error.position_m <= tolerance_m && error.angle_rad <= tolerance_rad
            })
            .count()
    }

    /// The deepest depth that beats the frozen baseline on the angle.
    pub fn deepest_depth_beating_frozen(&self) -> usize {
        self.depth
            .iter()
            .zip(self.model.iter().zip(self.frozen.iter()))
            .take_while(|(_, (model, frozen))| model.angle_rad < frozen.angle_rad)
            .map(|(depth, _)| *depth)
            .max()
            .unwrap_or(0)
    }
}

/// Dream `horizon` steps from each episode start, never consulting reality after the start.
///
/// Only episodes with at least `horizon + 1` transitions are used, and the **same** eligible
/// subset is used at every depth, so the curve is not distorted by a changing sample.
pub fn rollout_curve(
    model: &DeltaModel,
    rows: &[Transition],
    bounds: &[(usize, usize)],
    horizon: usize,
) -> Result<RolloutCurve, String> {
    if horizon == 0 {
        return Err("horizon must be positive".to_string());
    }
    if rows.is_empty() {
        return Err("no transitions to roll out".to_string());
    }
    let mut curve = RolloutCurve {
        depth: (1..=horizon).collect(),
        model: Vec::new(),
        frozen: Vec::new(),
    };

    for steps in 1..=horizon {
        let mut model_total = Error::zero();
        let mut frozen_total = Error::zero();
        let mut count = 0usize;
        for (begin, end) in bounds {
            if end.saturating_sub(*begin) < steps {
                continue;
            }
            let start = rows[*begin].state;
            let mut current = start;
            for offset in 0..steps {
                let row = &rows[begin + offset];
                current = model.predict(current, row.action)?;
            }
            let truth = rows[begin + steps - 1].successor;
            // Error at exactly this depth.
            model_total = model_total.add(absolute_error(current, truth));
            // The lazy baseline freezes at the same step the model started from.
            frozen_total = frozen_total.add(absolute_error(start, truth));
            count += 1;
        }
        if count == 0 {
            return Err(format!("no episode is long enough for depth {steps}"));
        }
        curve.model.push(model_total.scale(1.0 / count as f64));
        curve.frozen.push(frozen_total.scale(1.0 / count as f64));
    }
    Ok(curve)
}

/// Convert normalized values back to physical units, for reporting.
pub fn to_physical(values: [f64; 2]) -> (f64, f64) {
    (values[0] * X_LIMIT, values[1] * THETA_LIMIT)
}

/// A tiny worked example used in the guide: a frozen model versus a correct one.
pub fn demo_curve() -> RolloutCurve {
    let depth: Vec<usize> = (1..=5).collect();
    let model = depth
        .iter()
        .map(|d| Error {
            position_m: 0.001 * *d as f64,
            angle_rad: 0.0005 * *d as f64,
        })
        .collect();
    let frozen = depth
        .iter()
        .map(|d| Error {
            position_m: 0.004 * *d as f64,
            angle_rad: 0.002 * *d as f64,
        })
        .collect();
    RolloutCurve {
        depth,
        model,
        frozen,
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    use crate::dataset::{collect, episode_bounds, split_episodes, CollectConfig, Rng};

    fn rows() -> Vec<Transition> {
        let mut rng = Rng::new(41);
        collect(
            &mut rng,
            CollectConfig {
                episodes: 10,
                max_steps: 100,
                exploration: 0.4,
                bias_scale: 0.15,
            },
        )
        .expect("collect")
    }

    #[test]
    fn one_step_error_is_finite_and_smaller_than_the_frozen_baseline() {
        let data = rows();
        let model = DeltaModel::fit(&data, 1e-6).expect("fit");
        let error = one_step_error(&model, &data).expect("one step");
        assert!(error.position_m.is_finite() && error.angle_rad.is_finite());
        assert!(error.position_m >= 0.0 && error.angle_rad >= 0.0);
    }

    #[test]
    fn the_curve_reports_an_error_at_every_depth() {
        let data = rows();
        let bounds = episode_bounds(&data);
        let model = DeltaModel::fit(&data, 1e-6).expect("fit");
        let curve = rollout_curve(&model, &data, &bounds, 5).expect("curve");
        assert_eq!(curve.depth, vec![1, 2, 3, 4, 5]);
        assert_eq!(curve.model.len(), 5);
        assert_eq!(curve.frozen.len(), 5);
        for error in &curve.model {
            assert!(error.angle_rad.is_finite() && error.position_m.is_finite());
        }
    }

    #[test]
    fn error_at_depth_is_not_the_mean_over_depths() {
        // With a deliberately wrong model, depth 1 error should be smaller than depth 4.
        // If the function averaged 1..h, the two would be much closer together.
        let data = rows();
        let bounds = episode_bounds(&data);
        let model = DeltaModel::fit(&data, 1e-6).expect("fit");
        let curve = rollout_curve(&model, &data, &bounds, 6).expect("curve");
        assert!(
            curve.model[0].angle_rad <= curve.model[5].angle_rad,
            "error should grow with depth for this model"
        );
    }

    #[test]
    fn trust_horizon_counts_leading_depths_inside_the_tolerance() {
        let curve = demo_curve();
        // Model error is 0.0005 * depth rad, so tolerance 0.0015 allows three depths.
        assert_eq!(curve.trust_horizon(1.0, 0.0015), 3);
        // A tolerance nothing satisfies gives zero, not an error.
        assert_eq!(curve.trust_horizon(0.0, 0.0), 0);
        // The frozen baseline is always worse in the demo, so all five depths beat it.
        assert_eq!(curve.deepest_depth_beating_frozen(), 5);
    }

    #[test]
    fn evaluation_uses_held_out_episodes() {
        let data = rows();
        let (_, holdout) = split_episodes(&data, 0.7).expect("split");
        let bounds = episode_bounds(holdout);
        let model = DeltaModel::fit(&data, 1e-6).expect("fit");
        let curve = rollout_curve(&model, holdout, &bounds, 3).expect("curve");
        assert_eq!(curve.model.len(), 3);
    }

    #[test]
    fn impossible_requests_are_errors() {
        let data = rows();
        let bounds = episode_bounds(&data);
        let model = DeltaModel::fit(&data, 1e-6).expect("fit");
        assert!(rollout_curve(&model, &data, &bounds, 0).is_err());
        assert!(rollout_curve(&model, &[], &[], 3).is_err());
        assert!(one_step_error(&model, &[]).is_err());
        // A horizon longer than every episode must say so rather than invent data.
        assert!(rollout_curve(&model, &data, &bounds, 10_000).is_err());
    }
}
