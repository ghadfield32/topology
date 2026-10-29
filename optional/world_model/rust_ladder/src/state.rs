//! WM01 — represent the world with a `struct`.
//!
//! The whole CartPole world is four numbers. Writing them as a named struct rather than a
//! tuple means the compiler knows which one is which, and a reader does too.
//!
//! Python sibling: `python/wm01_state.py`.

/// Physical constants of the classic CartPole task.
///
/// They are `pub` so a learner can check that both languages use the same numbers rather
/// than assume it. Nothing here is tuned.
pub const DT: f64 = 0.02;
pub const GRAVITY: f64 = 9.8;
pub const MASS_CART: f64 = 1.0;
pub const MASS_POLE: f64 = 0.1;
pub const HALF_LENGTH: f64 = 0.5;
pub const FORCE_MAG: f64 = 10.0;
pub const X_LIMIT: f64 = 2.4;
/// 12 degrees in radians: the standard failure angle. `0.20944` is not a magic number,
/// it is `12 * 2 * pi / 360`.
pub const THETA_LIMIT: f64 = 0.209_439_510_239_319_53;
pub const MAX_STEPS: usize = 500;

/// The complete four-number state.
///
/// Short field names (`x`, `v`, `theta`, `omega`) match the equations in the literature.
/// `#[derive(Debug)]` gives free printing; `Clone, Copy` say this value is four `f64`, so
/// passing it does not move ownership away from the caller.
#[derive(Debug, Clone, Copy, PartialEq)]
pub struct State {
    /// Cart position along the rail, in metres.
    pub x: f64,
    /// Cart velocity, in metres per second.
    pub v: f64,
    /// Pole angle from upright, in radians.
    pub theta: f64,
    /// Pole angular velocity, in radians per second.
    pub omega: f64,
}

impl State {
    /// The state at rest, perfectly upright.
    pub const fn upright() -> Self {
        Self {
            x: 0.0,
            v: 0.0,
            theta: 0.0,
            omega: 0.0,
        }
    }

    /// Construct from four numbers, rejecting a non-finite value.
    ///
    /// `f64::NAN` compares false with everything, so it slips through ordinary bounds
    /// checks and then silently poisons every later calculation. Rejecting it at the edge
    /// is much cheaper than debugging it at the end.
    pub fn new(x: f64, v: f64, theta: f64, omega: f64) -> Result<Self, String> {
        for (name, value) in [("x", x), ("v", v), ("theta", theta), ("omega", omega)] {
            if !value.is_finite() {
                return Err(format!("{name} must be finite, got {value}"));
            }
        }
        Ok(Self { x, v, theta, omega })
    }

    /// The two numbers a camera could report: where things are, never how fast.
    ///
    /// Returning a tuple rather than a new struct is deliberate at this rung: the point is
    /// to *see* that two of the four numbers are dropped.
    pub fn visible(self) -> (f64, f64) {
        (self.x, self.theta)
    }

    /// Has the game ended by falling?
    ///
    /// This is the *state* consequence. A step-limit ending is not a failure and is not
    /// decided here.
    pub fn failed(self) -> bool {
        self.x.abs() > X_LIMIT || self.theta.abs() > THETA_LIMIT
    }

    /// Cart position and pole angle on one scale.
    ///
    /// Without this the two numbers differ by a factor of about 11, and any least-squares
    /// fit will weight position errors far more heavily than angle errors simply because
    /// they are numerically larger. The angle is the one that ends the game.
    pub fn normalized(self) -> [f64; 2] {
        [self.x / X_LIMIT, self.theta / THETA_LIMIT]
    }

    /// Inverse of [`State::normalized`] for the two visible numbers.
    pub fn from_normalized(values: [f64; 2]) -> (f64, f64) {
        (values[0] * X_LIMIT, values[1] * THETA_LIMIT)
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn upright_is_all_zeros() {
        let state = State::upright();
        assert_eq!(state, State::new(0.0, 0.0, 0.0, 0.0).expect("finite"));
        assert!(!state.failed());
    }

    #[test]
    fn non_finite_fields_are_rejected_at_the_edge() {
        assert!(State::new(f64::NAN, 0.0, 0.0, 0.0).is_err());
        assert!(State::new(0.0, f64::INFINITY, 0.0, 0.0).is_err());
        assert!(State::new(0.0, 0.0, 0.0, f64::NEG_INFINITY).is_err());
    }

    #[test]
    fn visible_drops_exactly_the_two_velocities() {
        let state = State::new(0.3, 1.7, -0.1, 2.5).expect("finite");
        assert_eq!(state.visible(), (0.3, -0.1));
        // Two different states can share a visible pair, which is the whole reason the
        // article needs memory and this ladder starts without it.
        let other = State::new(0.3, -4.0, -0.1, 0.0).expect("finite");
        assert_eq!(state.visible(), other.visible());
        assert_ne!(state, other);
    }

    #[test]
    fn normalization_puts_the_limits_on_one_scale() {
        let at_limit = State::new(X_LIMIT, 0.0, THETA_LIMIT, 0.0).expect("finite");
        assert_eq!(at_limit.normalized(), [1.0, 1.0]);
        let (x, theta) = State::from_normalized([1.0, 1.0]);
        assert!((x - X_LIMIT).abs() < 1e-15);
        assert!((theta - THETA_LIMIT).abs() < 1e-15);
    }

    #[test]
    fn failure_is_a_state_consequence_on_either_limit() {
        assert!(State::new(X_LIMIT + 0.01, 0.0, 0.0, 0.0)
            .expect("finite")
            .failed());
        assert!(State::new(0.0, 0.0, -(THETA_LIMIT + 0.01), 0.0)
            .expect("finite")
            .failed());
        assert!(!State::new(X_LIMIT - 0.01, 0.0, THETA_LIMIT - 0.01, 0.0)
            .expect("finite")
            .failed());
    }

    #[test]
    fn theta_limit_is_twelve_degrees() {
        let twelve_degrees = 12.0 * 2.0 * std::f64::consts::PI / 360.0;
        assert!((THETA_LIMIT - twelve_degrees).abs() < 1e-15);
    }
}
