//! WM03 — calculate one simulator step, and say what went wrong.
//!
//! The equations are the standard CartPole ones. They are written out rather than hidden
//! behind a package because reading them is the point of this rung.
//!
//! Python sibling: `python/wm03_simulator.py`.

use crate::action::Action;
use crate::state::{State, DT, GRAVITY, HALF_LENGTH, MASS_CART, MASS_POLE};

/// Advance the state by one explicit-Euler step under `action`.
///
/// Returns `Result` rather than panicking: invalid input is a value the caller must handle,
/// so a bad call cannot take down a training loop halfway through a run.
///
/// A useful thing to check by hand first: from the upright state at rest, a right push gives
/// `x = 0`, `v = 0.1951`, `theta = 0`, `omega = -0.2927`. Position and angle are still zero
/// because this update advances them using the **old** velocities, which were zero. The
/// force changes the velocities for the *next* step. That is a property of Euler
/// integration, not a bug.
pub fn step(state: State, action: Action) -> Result<State, String> {
    let total_mass = MASS_CART + MASS_POLE;
    let (sin_theta, cos_theta) = state.theta.sin_cos();
    let force = action.force();

    // Standard CartPole equations of motion, one term at a time.
    let temp =
        (force + MASS_POLE * HALF_LENGTH * state.omega * state.omega * sin_theta) / total_mass;
    let angular_acceleration = (GRAVITY * sin_theta - cos_theta * temp)
        / (HALF_LENGTH * (4.0 / 3.0 - MASS_POLE * cos_theta * cos_theta / total_mass));
    let acceleration =
        temp - MASS_POLE * HALF_LENGTH * angular_acceleration * cos_theta / total_mass;

    let next = State {
        x: state.x + DT * state.v,
        v: state.v + DT * acceleration,
        theta: state.theta + DT * state.omega,
        omega: state.omega + DT * angular_acceleration,
    };

    // Guard the boundary between the computation and its caller. A non-finite result means
    // the arithmetic has already gone wrong; returning it would spread the damage silently.
    if !next.x.is_finite()
        || !next.v.is_finite()
        || !next.theta.is_finite()
        || !next.omega.is_finite()
    {
        return Err(format!("step produced a non-finite state from {state:?}"));
    }
    Ok(next)
}

/// One position update, with no acceleration.
///
/// This exists as a hand-checkable warm-up before the coupled equations: `1.0 + 0.4 * 0.02`
/// is `1.008`, and a learner should be able to say that before running anything.
pub fn advance_position(position: f64, velocity: f64, dt: f64) -> Result<f64, String> {
    if !position.is_finite() || !velocity.is_finite() || !dt.is_finite() {
        return Err("position, velocity and dt must be finite".to_string());
    }
    if dt <= 0.0 {
        return Err("dt must be positive".to_string());
    }
    Ok(position + velocity * dt)
}

#[cfg(test)]
mod tests {
    use super::*;
    use crate::state::State;

    #[test]
    fn hand_computed_position_update() {
        assert_eq!(advance_position(1.0, 0.4, 0.02).expect("finite"), 1.008);
    }

    #[test]
    fn a_bad_dt_is_an_error_not_a_panic() {
        assert!(advance_position(1.0, 0.4, 0.0).is_err());
        assert!(advance_position(1.0, 0.4, -0.02).is_err());
        assert!(advance_position(f64::NAN, 0.4, 0.02).is_err());
    }

    #[test]
    fn the_documented_hand_check_matches() {
        // These four numbers are quoted in the guide; asserting them keeps the guide and
        // the code from drifting apart.
        let next = step(State::upright(), Action::Right).expect("finite");
        assert!((next.x - 0.0).abs() < 1e-12);
        assert!((next.v - 0.195_121_951_2).abs() < 1e-9);
        assert!((next.theta - 0.0).abs() < 1e-12);
        assert!((next.omega - (-0.292_682_926_8)).abs() < 1e-9);
    }

    #[test]
    fn left_and_right_are_mirror_images_from_upright() {
        let right = step(State::upright(), Action::Right).expect("finite");
        let left = step(State::upright(), Action::Left).expect("finite");
        assert!((right.v + left.v).abs() < 1e-12);
        assert!((right.omega + left.omega).abs() < 1e-12);
    }

    #[test]
    fn position_advances_from_the_old_velocity() {
        // A state already moving should move this step, unlike the upright hand check.
        let moving = State::new(0.0, 1.0, 0.0, 0.0).expect("finite");
        let next = step(moving, Action::Left).expect("finite");
        assert!((next.x - DT * 1.0).abs() < 1e-15);
    }

    #[test]
    fn ten_thousand_steps_stay_finite() {
        let mut state = State::upright();
        for tick in 0..10_000 {
            state = step(
                state,
                if tick % 2 == 0 {
                    Action::Left
                } else {
                    Action::Right
                },
            )
            .expect("finite");
        }
        assert!(state.x.is_finite() && state.omega.is_finite());
    }
}
