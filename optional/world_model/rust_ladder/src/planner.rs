//! WM07 — plan by imagining, without refitting the model.
//!
//! A goal is a **function over a dreamed future**, chosen at run time. It is not a field in
//! the model, not a weight, and not something training decides. That is the payload of the
//! whole exercise: physics is indifferent to your goals, so the goal is a separate object
//! you can change on a Tuesday.
//!
//! The planner **borrows** the model. Only the random generator is mutated, and a
//! `&mut` on the generator is what stops it being used from two places at once.
//!
//! Python sibling: `python/wm07_planner.py`.

use crate::action::Action;
use crate::dataset::Rng;
use crate::model::DeltaModel;
use crate::state::{State, THETA_LIMIT, X_LIMIT};

/// What the planner is asked to achieve. Changing this changes nothing in the model.
#[derive(Debug, Clone, Copy, PartialEq)]
pub enum Goal {
    /// Stay upright for as many dreamed steps as possible.
    Balance,
    /// End the dream near `target` metres, still upright.
    Park(f64),
}

impl Goal {
    pub fn name(self) -> String {
        match self {
            Goal::Balance => "balance".to_string(),
            Goal::Park(target) => format!("park({target:.3} m)"),
        }
    }
}

/// One dreamed future.
#[derive(Debug, Clone, PartialEq)]
pub struct Dream {
    pub states: Vec<State>,
    pub failed_at: Option<usize>,
}

impl Dream {
    /// How many steps the dream survives before a failure is detected.
    pub fn alive_steps(&self) -> usize {
        self.failed_at.unwrap_or(self.states.len())
    }

    /// The state at the last reachable step.
    ///
    /// A failed dream cannot "come back alive": every step after `failed_at` is unreachable,
    /// so scoring uses the last step *before* the failure. Returning the final element
    /// regardless is how a doomed plan gets scored as if it had succeeded.
    pub fn last_reachable(&self) -> State {
        let reachable = self.alive_steps();
        if reachable == 0 {
            // The very first dreamed step failed. Report the initial state.
            self.states.first().copied().unwrap_or_else(State::upright)
        } else {
            self.states[reachable - 1]
        }
    }
}

/// Score a dream under a goal. Larger is better, and the units are stated per goal.
///
/// Every term is in **physical units**: metres for position, radians divided by the failure
/// angle for uprightness. Mixing a normalized 1.0 with a metric target is a silent unit bug,
/// because normalized 1.0 is 2.4 metres.
pub fn score(goal: Goal, dream: &Dream) -> f64 {
    let alive_fraction = dream.alive_steps() as f64 / dream.states.len().max(1) as f64;
    match goal {
        Goal::Balance => {
            let upright = dream
                .states
                .iter()
                .take(dream.alive_steps())
                .map(|state| state.theta.abs() / THETA_LIMIT)
                .sum::<f64>()
                / dream.alive_steps().max(1) as f64;
            alive_fraction - upright
        }
        Goal::Park(target) => {
            // Scored by where the dream *ends*, not by its average distance. The only
            // manoeuvre that moves a cart-pole right begins by pushing left, so an average
            // score rejects the correct plan and reports it as a bad model.
            let distance_m = (dream.last_reachable().x - target).abs();
            let upright = dream.last_reachable().theta.abs() / THETA_LIMIT;
            alive_fraction - distance_m - 0.5 * upright
        }
    }
}

/// A plan: the action sequence that scored best, and its score.
#[derive(Debug, Clone, PartialEq)]
pub struct Plan {
    pub actions: Vec<Action>,
    pub score: f64,
    pub candidates: usize,
}

/// Dream one candidate from a real state, using only the fitted model.
pub fn dream(model: &DeltaModel, start: State, actions: &[Action]) -> Result<Dream, String> {
    if actions.is_empty() {
        return Err("a dream needs at least one action".to_string());
    }
    let mut states = Vec::with_capacity(actions.len());
    let mut current = start;
    let mut failed_at = None;
    for action in actions {
        current = model.predict(current, *action)?;
        if current.failed() {
            failed_at = Some(states.len());
            states.push(current);
            break;
        }
        states.push(current);
    }
    Ok(Dream { states, failed_at })
}

/// Invent candidates, dream them, score them, return the best plan.
///
/// `sequences` random plans of length `horizon` are sampled. That is a real limit: with 200
/// samples, a 3-step plan space (8 options) is covered thoroughly and a 15-step space
/// (`2^15`) is not. How accurate the model is and how well the search covers the space are
/// two different ceilings.
pub fn plan(
    model: &DeltaModel,
    start: State,
    goal: Goal,
    horizon: usize,
    sequences: usize,
    rng: &mut Rng,
) -> Result<Plan, String> {
    if horizon == 0 || sequences == 0 {
        return Err("horizon and sequences must be positive".to_string());
    }
    let mut best: Option<Plan> = None;
    for _ in 0..sequences {
        let actions: Vec<Action> = (0..horizon)
            .map(|_| Action::from_index(rng.below(2) as usize))
            .collect::<Result<_, _>>()?;
        let dreamt = dream(model, start, &actions)?;
        let value = score(goal, &dreamt);
        if best.as_ref().map(|plan| value > plan.score).unwrap_or(true) {
            best = Some(Plan {
                actions,
                score: value,
                candidates: sequences,
            });
        }
    }
    best.ok_or_else(|| "no candidate was evaluated".to_string())
}

/// The index of an action, kept for recording a decision.
pub fn action_index(action: Action) -> usize {
    action.index()
}

/// Normalize a state's visible numbers for reporting.
pub fn normalized_visible(state: State) -> [f64; 2] {
    [state.x / X_LIMIT, state.theta / THETA_LIMIT]
}

#[cfg(test)]
mod tests {
    use super::*;
    use crate::dataset::{collect, CollectConfig, Rng};
    use crate::model::DeltaModel;

    fn fitted() -> DeltaModel {
        let mut rng = Rng::new(51);
        let rows = collect(
            &mut rng,
            CollectConfig {
                episodes: 12,
                max_steps: 120,
                exploration: 0.4,
                bias_scale: 0.15,
            },
        )
        .expect("collect");
        DeltaModel::fit(&rows, 1e-6).expect("fit")
    }

    #[test]
    fn planning_does_not_mutate_the_fitted_weights() {
        let model = fitted();
        let before = model.weights();
        let mut rng = Rng::new(7);
        plan(&model, State::upright(), Goal::Balance, 4, 8, &mut rng).expect("plan");
        assert_eq!(
            model.weights(),
            before,
            "the planner borrowed the model, it did not train it"
        );
    }

    #[test]
    fn changing_the_goal_changes_the_decision_not_the_model() {
        let model = fitted();
        let before = model.weights();
        let mut balance_rng = Rng::new(9);
        let balance = plan(
            &model,
            State::upright(),
            Goal::Balance,
            5,
            32,
            &mut balance_rng,
        )
        .expect("plan");
        let mut park_rng = Rng::new(9);
        let park = plan(
            &model,
            State::upright(),
            Goal::Park(1.0),
            5,
            32,
            &mut park_rng,
        )
        .expect("plan");
        assert_eq!(model.weights(), before);
        // The scores live on different scales, so their names and goals must differ.
        assert_ne!(balance.score, park.score);
        assert_eq!(Goal::Balance.name(), "balance");
        assert!(Goal::Park(1.0).name().contains("1.000 m"));
    }

    #[test]
    fn a_failed_dream_cannot_come_back_alive() {
        // A dream that fails at step 2 must score using step 2, not a later success.
        let failed = Dream {
            states: vec![
                State::new(0.0, 0.0, 0.0, 0.0).expect("finite"),
                State::new(0.1, 0.0, 0.0, 0.0).expect("finite"),
                State::new(3.0, 0.0, 0.0, 0.0).expect("finite"), // off the rail
            ],
            failed_at: Some(2),
        };
        assert_eq!(failed.alive_steps(), 2);
        assert!((failed.last_reachable().x - 0.1).abs() < 1e-12);
    }

    #[test]
    fn parking_is_scored_by_the_final_distance_in_metres() {
        let near = Dream {
            states: vec![State::new(0.95, 0.0, 0.0, 0.0).expect("finite")],
            failed_at: None,
        };
        let far = Dream {
            states: vec![State::new(0.0, 0.0, 0.0, 0.0).expect("finite")],
            failed_at: None,
        };
        assert!(score(Goal::Park(1.0), &near) > score(Goal::Park(1.0), &far));
        // And the units are metres: 0.05 m away must beat 1.0 m away by about 0.95.
        let difference = score(Goal::Park(1.0), &near) - score(Goal::Park(1.0), &far);
        assert!(
            (difference - 0.95).abs() < 1e-9,
            "difference was {difference}"
        );
    }

    #[test]
    fn an_empty_dream_or_empty_plan_is_an_error() {
        let model = fitted();
        let mut rng = Rng::new(3);
        assert!(dream(&model, State::upright(), &[]).is_err());
        assert!(plan(&model, State::upright(), Goal::Balance, 0, 4, &mut rng).is_err());
        assert!(plan(&model, State::upright(), Goal::Balance, 3, 0, &mut rng).is_err());
    }

    #[test]
    fn the_plan_is_the_length_that_was_requested() {
        let model = fitted();
        let mut rng = Rng::new(11);
        let chosen = plan(&model, State::upright(), Goal::Balance, 6, 16, &mut rng).expect("plan");
        assert_eq!(chosen.actions.len(), 6);
        assert_eq!(chosen.candidates, 16);
    }
}
