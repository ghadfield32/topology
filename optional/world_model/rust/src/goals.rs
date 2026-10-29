//! Goal scoring: the part of the method that is *not* in the weights.
//!
//! The article's payload is that a trained world model plus a plain scoring function is a
//! planner, and editing the function changes the goal for free. Python implements both
//! goals with tensors. This module implements the same two functions over a plain `Vec`,
//! which makes the arithmetic — and the bug the article reports — visible.
//!
//! The bug is worth reproducing rather than describing: scoring a dream by its **average**
//! distance to the target rejects the only manoeuvre that works, because getting a
//! cart-pole to travel right requires pushing left first. The opening move of the correct
//! answer looks worse under an averaging score. Reproduce that here and the lesson stops
//! being a claim.

/// One imagined future: the visible states and the crash logits, one per dreamed step.
#[derive(Debug, Clone, PartialEq)]
pub struct Dream {
    pub visible: Vec<[f64; 2]>,
    pub termination_logits: Vec<f64>,
}

impl Dream {
    pub fn new(visible: Vec<[f64; 2]>, termination_logits: Vec<f64>) -> Result<Self, String> {
        if visible.is_empty() {
            return Err("a dream needs at least one step".to_string());
        }
        if visible.len() != termination_logits.len() {
            return Err(format!(
                "{} visible steps but {} logits",
                visible.len(),
                termination_logits.len()
            ));
        }
        if visible
            .iter()
            .any(|step| !step[0].is_finite() || !step[1].is_finite())
        {
            return Err("dream states must be finite".to_string());
        }
        if termination_logits
            .iter()
            .any(|value| value.is_finite().not())
        {
            return Err("dream logits must be finite".to_string());
        }
        Ok(Self {
            visible,
            termination_logits,
        })
    }

    /// Steps before the predicted crash. A logit above zero is "this step ends the game".
    pub fn alive(&self) -> Vec<bool> {
        self.termination_logits
            .iter()
            .map(|logit| *logit <= 0.0)
            .collect()
    }

    pub fn survives(&self) -> bool {
        self.alive().iter().all(|alive| *alive)
    }
}

trait Not {
    fn not(self) -> bool;
}

impl Not for bool {
    fn not(self) -> bool {
        !self
    }
}

/// Average of `values` over the steps that are still alive, or `None` if none are.
fn masked_mean(values: &[f64], alive: &[bool]) -> Option<f64> {
    let mut sum = 0.0;
    let mut count = 0usize;
    for (value, keep) in values.iter().zip(alive) {
        if *keep {
            sum += value;
            count += 1;
        }
    }
    (count > 0).then(|| sum / count as f64)
}

/// The value at the **last** surviving step. This is the corrected scoring rule.
fn terminal_value(values: &[f64], alive: &[bool]) -> Option<f64> {
    let last = alive.iter().rposition(|keep| *keep)?;
    Some(values[last])
}

/// Goal A: stay alive and upright. This is the goal a reward function used to encode.
pub fn score_balance(dream: &Dream) -> f64 {
    let alive = dream.alive();
    let survival = alive.iter().filter(|keep| **keep).count() as f64 / alive.len() as f64;
    let angles: Vec<f64> = dream.visible.iter().map(|step| step[1].abs()).collect();
    let upright = masked_mean(&angles, &alive).unwrap_or(0.0);
    survival - 4.0 * upright
}

/// Goal B, **corrected**: park at `target`, scored by where the dream ends up.
pub fn score_park(dream: &Dream, target: f64) -> f64 {
    let alive = dream.alive();
    let distances: Vec<f64> = dream
        .visible
        .iter()
        .map(|step| (step[0] - target).abs())
        .collect();
    let survival = alive.iter().filter(|keep| **keep).count() as f64 / alive.len() as f64;
    let off_target = terminal_value(&distances, &alive).unwrap_or(f64::INFINITY);
    let angles: Vec<f64> = dream.visible.iter().map(|step| step[1].abs()).collect();
    let upright = masked_mean(&angles, &alive).unwrap_or(0.0);
    survival - off_target - 0.5 * upright
}

/// Goal B, **as first written**: scored by the mean distance across the whole dream.
///
/// This function exists only to be compared against [`score_park`]. It is not a
/// worse-tuned version of the same idea; it encodes a different preference, and it is the
/// one the article initially shipped.
pub fn score_park_average(dream: &Dream, target: f64) -> f64 {
    let alive = dream.alive();
    let distances: Vec<f64> = dream
        .visible
        .iter()
        .map(|step| (step[0] - target).abs())
        .collect();
    let survival = alive.iter().filter(|keep| **keep).count() as f64 / alive.len() as f64;
    let off_target = masked_mean(&distances, &alive).unwrap_or(f64::INFINITY);
    let angles: Vec<f64> = dream.visible.iter().map(|step| step[1].abs()).collect();
    let upright = masked_mean(&angles, &alive).unwrap_or(0.0);
    survival - off_target - 0.5 * upright
}

/// A goal is a function, selected at runtime. Nothing here is stored in a weight.
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum Goal {
    Balance,
    Park,
    ParkAverage,
}

impl Goal {
    pub fn score(self, dream: &Dream, target: f64) -> f64 {
        match self {
            Goal::Balance => score_balance(dream),
            Goal::Park => score_park(dream, target),
            Goal::ParkAverage => score_park_average(dream, target),
        }
    }

    pub fn name(self) -> &'static str {
        match self {
            Goal::Balance => "balance",
            Goal::Park => "park",
            Goal::ParkAverage => "park_average",
        }
    }
}

/// Pick the index of the best dream. Ties go to the earliest, which keeps runs repeatable.
pub fn best_plan(goal: Goal, dreams: &[Dream], target: f64) -> Result<usize, String> {
    if dreams.is_empty() {
        return Err("no candidate dreams".to_string());
    }
    let mut best = 0usize;
    let mut best_score = goal.score(&dreams[0], target);
    for (index, dream) in dreams.iter().enumerate().skip(1) {
        let score = goal.score(dream, target);
        if score > best_score {
            best = index;
            best_score = score;
        }
    }
    if !best_score.is_finite() {
        return Err("the best dream scored non-finite; check the goal's weights".to_string());
    }
    Ok(best)
}

#[cfg(test)]
mod tests {
    use super::*;

    /// Two dreams, both alive, targeting x = +1.0.
    ///
    /// `journey` does what the physics demands: push **left** first, then come back right
    /// and arrive. `hover` never moves. Over a short horizon the journey's early steps are
    /// further from the target than hovering is, so an averaging score prefers hovering —
    /// which is exactly the article's failure.
    fn journey_and_hover() -> (Dream, Dream) {
        let journey = Dream::new(
            vec![[0.0, 0.0], [-0.9, 0.0], [0.8, 0.0]],
            vec![-1.0, -1.0, -1.0],
        )
        .expect("dream");
        let hover = Dream::new(
            vec![[0.0, 0.0], [0.0, 0.0], [0.0, 0.0]],
            vec![-1.0, -1.0, -1.0],
        )
        .expect("dream");
        (journey, hover)
    }

    #[test]
    fn terminal_scoring_prefers_the_journey_that_arrives() {
        let (journey, hover) = journey_and_hover();
        assert!(score_park(&journey, 1.0) > score_park(&hover, 1.0));
    }

    #[test]
    fn average_scoring_rejects_the_journey_that_arrives() {
        // This is the article's bug, reproduced rather than described. The journey ends
        // 0.8 m closer to the target, yet its mean distance over the dream is worse.
        let (journey, hover) = journey_and_hover();
        let journey_average = score_park_average(&journey, 1.0);
        let hover_average = score_park_average(&hover, 1.0);
        assert!(
            journey_average < hover_average,
            "the averaging rule must prefer hovering: {journey_average} vs {hover_average}"
        );
        // And the terminal rule must rank them the other way round on the same dreams.
        assert!(score_park(&journey, 1.0) > score_park(&hover, 1.0));
    }

    #[test]
    fn the_two_park_goals_disagree_on_the_same_dreams() {
        let (journey, hover) = journey_and_hover();
        let dreams = [journey, hover];
        assert_eq!(best_plan(Goal::Park, &dreams, 1.0).expect("plan"), 0);
        assert_eq!(best_plan(Goal::ParkAverage, &dreams, 1.0).expect("plan"), 1);
    }

    #[test]
    fn balance_scores_a_surviving_upright_dream_above_a_falling_one() {
        let upright = Dream::new(vec![[0.0, 0.0], [0.0, 0.0]], vec![-2.0, -2.0]).expect("dream");
        let falling = Dream::new(vec![[0.0, 0.0], [0.0, 0.3]], vec![-2.0, 2.0]).expect("dream");
        assert!(score_balance(&upright) > score_balance(&falling));
    }

    #[test]
    fn a_crash_makes_the_terminal_distance_that_of_the_last_alive_step() {
        // The dream dies at step 2; its distance at step 3 must not be scored, because
        // that step never happened.
        let crashing = Dream::new(
            vec![[0.0, 0.0], [0.5, 0.0], [9.0, 0.0]],
            vec![-1.0, -1.0, 5.0],
        )
        .expect("dream");
        let alive = crashing.alive();
        assert_eq!(terminal_value(&[0.0, 0.5, 9.0], &alive), Some(0.5));
        assert!(!crashing.survives());
    }

    #[test]
    fn mismatched_lengths_and_non_finite_values_are_errors() {
        assert!(Dream::new(vec![[0.0, 0.0]], vec![-1.0, -1.0]).is_err());
        assert!(Dream::new(vec![], vec![]).is_err());
        assert!(Dream::new(vec![[f64::NAN, 0.0]], vec![-1.0]).is_err());
        assert!(Dream::new(vec![[0.0, 0.0]], vec![f64::NAN]).is_err());
    }

    #[test]
    fn an_empty_candidate_list_is_an_error_not_a_default_plan() {
        assert!(best_plan(Goal::Balance, &[], 1.0).is_err());
    }

    #[test]
    fn goal_selection_is_a_runtime_choice() {
        // The same dreams, three goals, chosen by name at run time.
        let (journey, hover) = journey_and_hover();
        let dreams = [journey, hover];
        let names: Vec<&str> = [Goal::Balance, Goal::Park, Goal::ParkAverage]
            .iter()
            .map(|goal| goal.name())
            .collect();
        assert_eq!(names, ["balance", "park", "park_average"]);
        assert!(best_plan(Goal::Balance, &dreams, 1.0).is_ok());
    }
}
