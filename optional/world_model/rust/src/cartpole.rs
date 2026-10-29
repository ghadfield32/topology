//! The same CartPole equations as `python/cartpole.py`, as explicit `f64` arithmetic.
//!
//! Two things Rust makes you write down that Python lets you imply: the state is a
//! fixed-size value type, and every fallible conversion is a `Result`. The struct also
//! makes the "two endings" distinction impossible to forget, because an episode's
//! outcome is an enum rather than two booleans that can both be true.

/// Physical constants of the classic task. They are `pub` because a learner should be
/// able to check that both languages use the same numbers rather than assume it.
pub const DT: f64 = 0.02;
pub const GRAVITY: f64 = 9.8;
pub const MASS_CART: f64 = 1.0;
pub const MASS_POLE: f64 = 0.1;
pub const HALF_LENGTH: f64 = 0.5;
pub const FORCE_MAG: f64 = 10.0;
pub const X_LIMIT: f64 = 2.4;
/// 12 degrees in radians; the standard failure angle.
pub const THETA_LIMIT: f64 = 0.209_439_510_239_319_53;
pub const MAX_STEPS: usize = 500;
pub const ANGULAR_VELOCITY_GAIN: f64 = 0.5;

/// The complete four-number state.
#[derive(Debug, Clone, Copy, PartialEq)]
pub struct State {
    pub cart_position: f64,
    pub cart_velocity: f64,
    pub pole_angle: f64,
    pub pole_angular_velocity: f64,
}

/// What a camera reports: where things are, never how fast.
#[derive(Debug, Clone, Copy, PartialEq)]
pub struct Visible {
    pub cart_position: f64,
    pub pole_angle: f64,
}

impl Visible {
    /// Put both numbers on the same scale. See `python/cartpole.py::normalize_visible`.
    pub fn normalized(self) -> [f64; 2] {
        [self.cart_position / X_LIMIT, self.pole_angle / THETA_LIMIT]
    }

    pub fn from_normalized(values: [f64; 2]) -> Self {
        Self {
            cart_position: values[0] * X_LIMIT,
            pole_angle: values[1] * THETA_LIMIT,
        }
    }
}

impl State {
    pub fn visible(self) -> Visible {
        Visible {
            cart_position: self.cart_position,
            pole_angle: self.pole_angle,
        }
    }

    pub fn failed(self) -> bool {
        self.cart_position.abs() > X_LIMIT || self.pole_angle.abs() > THETA_LIMIT
    }
}

/// Why an episode stopped. Keeping this as an enum is the point: a fall is learnable
/// from the state, a timer expiry is not, so they are different values.
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum Ending {
    Terminated,
    Truncated,
}

#[derive(Debug, Clone)]
pub struct Episode {
    pub states: Vec<State>,
    pub actions: Vec<u8>,
    pub ending: Ending,
}

impl Episode {
    pub fn steps(&self) -> usize {
        self.actions.len()
    }
}

/// Reject an action that is not 0 or 1 instead of coercing it.
pub fn step(state: State, action: u8) -> Result<State, String> {
    if action > 1 {
        return Err(format!("action must be 0 or 1, got {action}"));
    }
    let force = if action == 1 { FORCE_MAG } else { -FORCE_MAG };
    let total_mass = MASS_CART + MASS_POLE;
    let (sin, cos) = state.pole_angle.sin_cos();
    let temp =
        (force + MASS_POLE * HALF_LENGTH * state.pole_angular_velocity.powi(2) * sin) / total_mass;
    let theta_acc = (GRAVITY * sin - cos * temp)
        / (HALF_LENGTH * (4.0 / 3.0 - MASS_POLE * cos * cos / total_mass));
    let x_acc = temp - MASS_POLE * HALF_LENGTH * theta_acc * cos / total_mass;
    Ok(State {
        cart_position: state.cart_position + DT * state.cart_velocity,
        cart_velocity: state.cart_velocity + DT * x_acc,
        pole_angle: state.pole_angle + DT * state.pole_angular_velocity,
        pole_angular_velocity: state.pole_angular_velocity + DT * theta_acc,
    })
}

/// The three-line controller. `bias` tilts an episode so the data contains journeys.
pub fn proportional_controller(state: State, bias: f64) -> u8 {
    let lean = state.pole_angle + ANGULAR_VELOCITY_GAIN * state.pole_angular_velocity + bias;
    u8::from(lean > 0.0)
}

/// Play one game. `policy` receives the state and returns an action.
///
/// `FnMut` rather than `Fn` because a genuinely random policy mutates its generator,
/// and refusing that would force a `RefCell` on the caller for no benefit.
pub fn rollout<F>(start: State, mut policy: F, max_steps: usize) -> Result<Episode, String>
where
    F: FnMut(State) -> u8,
{
    if max_steps == 0 {
        return Err("max_steps must be positive".to_string());
    }
    let mut states = vec![start];
    let mut actions = Vec::new();
    let mut state = start;
    for _ in 0..max_steps {
        let action = policy(state);
        let next = step(state, action)?;
        actions.push(action);
        states.push(next);
        state = next;
        if state.failed() {
            return Ok(Episode {
                states,
                actions,
                ending: Ending::Terminated,
            });
        }
    }
    Ok(Episode {
        states,
        actions,
        ending: Ending::Truncated,
    })
}

/// A small deterministic generator. It exists so this crate needs no crates; it is a
/// splitmix-style recurrence, not a statistical recommendation.
#[derive(Debug, Clone)]
pub struct Rng(u64);

impl Rng {
    pub fn new(seed: u64) -> Self {
        Self(seed.wrapping_mul(0x9E37_79B9_7F4A_7C15) ^ 0x5DEE_CE66_D1A4_8FAB)
    }

    pub fn next_u64(&mut self) -> u64 {
        self.0 = self.0.wrapping_add(0x9E37_79B9_7F4A_7C15);
        let mut z = self.0;
        z = (z ^ (z >> 30)).wrapping_mul(0xBF58_476D_1CE4_E5B9);
        z = (z ^ (z >> 27)).wrapping_mul(0x94D0_49BB_1331_11EB);
        z ^ (z >> 31)
    }

    /// A value in `[0, 1)`.
    pub fn unit(&mut self) -> f64 {
        (self.next_u64() >> 11) as f64 / (1u64 << 53) as f64
    }

    /// A value in `[low, high)`.
    pub fn range(&mut self, low: f64, high: f64) -> f64 {
        low + (high - low) * self.unit()
    }

    pub fn below(&mut self, bound: u64) -> u64 {
        self.next_u64() % bound
    }
}

/// The usual small random offset at the start of an episode.
pub fn initial_state(rng: &mut Rng) -> State {
    State {
        cart_position: rng.range(-0.05, 0.05),
        cart_velocity: rng.range(-0.05, 0.05),
        pole_angle: rng.range(-0.05, 0.05),
        pole_angular_velocity: rng.range(-0.05, 0.05),
    }
}

/// One collected transition. Owning the numbers rather than indexing a shared table is
/// what makes the split into train/holdout safe without a lifetime argument.
#[derive(Debug, Clone, Copy)]
pub struct Transition {
    pub visible: Visible,
    pub state: State,
    pub action: u8,
    pub terminated: bool,
    pub truncated: bool,
}

/// Collect with recovery plus random shoves, exactly like the Python collector.
pub fn collect(
    rng: &mut Rng,
    episodes: usize,
    exploration: f64,
    max_steps: usize,
    bias_scale: f64,
) -> Result<Vec<Transition>, String> {
    if episodes == 0 {
        return Err("episodes must be positive".to_string());
    }
    if !(0.0..=1.0).contains(&exploration) {
        return Err("exploration is a probability in [0, 1]".to_string());
    }
    let mut out = Vec::new();
    for _ in 0..episodes {
        let bias = rng.range(-bias_scale, bias_scale);
        let mut state = initial_state(rng);
        for played in 1..=max_steps {
            let action = if rng.unit() < exploration {
                u8::from(rng.below(2) == 1)
            } else {
                proportional_controller(state, bias)
            };
            let next = step(state, action)?;
            let failed = next.failed();
            out.push(Transition {
                visible: state.visible(),
                state,
                action,
                terminated: failed,
                truncated: !failed && played == max_steps,
            });
            state = next;
            if failed {
                break;
            }
        }
    }
    Ok(out)
}

/// Split a flat transition list into episode bounds. Windows must never cross one.
pub fn episode_bounds(rows: &[Transition]) -> Vec<(usize, usize)> {
    let mut bounds = Vec::new();
    let mut begin = 0usize;
    for (index, row) in rows.iter().enumerate() {
        if row.terminated || row.truncated {
            bounds.push((begin, index + 1));
            begin = index + 1;
        }
    }
    if begin < rows.len() {
        bounds.push((begin, rows.len()));
    }
    bounds
}

/// Errors that grow with rollout depth. A `Vec` of `(depth, error)` pairs keeps the
/// measurement explicit; there is no hidden averaging.
pub fn free_rollout_error_growth<F>(
    start: State,
    actions: &[u8],
    model: F,
) -> Result<Vec<(usize, Visible)>, String>
where
    F: Fn(Visible, u8) -> Visible,
{
    if actions.is_empty() {
        return Err("at least one action is required".to_string());
    }
    let mut current = start.visible();
    let mut out = Vec::with_capacity(actions.len());
    for (index, action) in actions.iter().enumerate() {
        current = model(current, *action);
        out.push((index + 1, current));
    }
    Ok(out)
}

/// The first depth whose error exceeds `tolerance`, with the number of depths that
/// passed. `None` means every supplied depth passed.
pub fn trust_horizon(errors: &[f64], tolerance: f64) -> Result<(usize, Option<usize>), String> {
    if errors.is_empty() {
        return Err("at least one depth is required".to_string());
    }
    if !tolerance.is_finite() || tolerance <= 0.0 {
        return Err("tolerance must be positive".to_string());
    }
    if errors.iter().any(|value| !value.is_finite()) {
        return Err("errors must be finite".to_string());
    }
    match errors.iter().position(|value| *value > tolerance) {
        Some(index) => Ok((index, Some(index))),
        None => Ok((errors.len(), None)),
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    fn balanced() -> State {
        State {
            cart_position: 0.01,
            cart_velocity: 0.0,
            pole_angle: 0.02,
            pole_angular_velocity: 0.0,
        }
    }

    #[test]
    fn a_controller_balances_and_a_flail_does_not() {
        let good =
            rollout(balanced(), |s| proportional_controller(s, 0.0), MAX_STEPS).expect("rollout");
        assert_eq!(good.steps(), MAX_STEPS);
        assert_eq!(good.ending, Ending::Truncated);

        let mut rng = Rng::new(0);
        let bad = rollout(balanced(), |_| u8::from(rng.below(2) == 1), MAX_STEPS).expect("rollout");
        assert_eq!(bad.ending, Ending::Terminated);
        assert!(bad.steps() < 100);
    }

    #[test]
    fn endings_are_mutually_exclusive_by_construction() {
        let episode =
            rollout(balanced(), |s| proportional_controller(s, 0.0), 20).expect("rollout");
        assert_eq!(episode.ending, Ending::Truncated);
        assert_eq!(episode.steps(), 20);
    }

    #[test]
    fn invalid_actions_are_errors_not_coercions() {
        assert!(step(balanced(), 2).is_err());
        assert!(step(balanced(), 1).is_ok());
    }

    #[test]
    fn visible_state_carries_no_velocity() {
        let state = State {
            cart_position: 0.3,
            cart_velocity: 1.7,
            pole_angle: -0.1,
            pole_angular_velocity: 2.5,
        };
        let visible = state.visible();
        assert_eq!(visible.cart_position, 0.3);
        assert_eq!(visible.pole_angle, -0.1);
        // Normalizing then denormalizing returns the same visibility, not the velocities.
        let round_trip = Visible::from_normalized(visible.normalized());
        assert!((round_trip.cart_position - visible.cart_position).abs() < 1e-15);
        assert!((round_trip.pole_angle - visible.pole_angle).abs() < 1e-15);
    }

    #[test]
    fn collection_covers_both_actions_and_both_endings() {
        let mut rng = Rng::new(7);
        let rows = collect(&mut rng, 12, 0.5, MAX_STEPS, 0.15).expect("collect");
        let actions: std::collections::BTreeSet<u8> = rows.iter().map(|r| r.action).collect();
        assert_eq!(actions.len(), 2, "planning asks about both shoves");
        assert!(rows.iter().any(|r| r.terminated), "a crash must appear");
        let bounded = episode_bounds(&rows);
        assert_eq!(bounded.len(), 12);
        assert_eq!(bounded.last().copied().expect("last").1, rows.len());
    }

    #[test]
    fn windows_cannot_cross_episode_boundaries() {
        let mut rng = Rng::new(11);
        let rows = collect(&mut rng, 4, 0.6, 60, 0.15).expect("collect");
        let bounds = episode_bounds(&rows);
        for (begin, end) in &bounds {
            assert!(*end > *begin);
            assert!(rows[end - 1].terminated || rows[end - 1].truncated);
        }
        assert_eq!(bounds[0].0, 0);
    }

    #[test]
    fn trust_horizon_stops_at_the_first_failure() {
        let errors = [0.001, 0.010, 0.019, 0.030, 0.400];
        assert_eq!(trust_horizon(&errors, 0.02).expect("ok"), (3, Some(3)));
        assert_eq!(trust_horizon(&[0.001, 0.002], 0.02).expect("ok"), (2, None));
        assert!(trust_horizon(&errors, 0.0).is_err());
        assert!(trust_horizon(&[f64::NAN], 0.02).is_err());
        assert!(trust_horizon(&[], 0.02).is_err());
    }

    #[test]
    fn rollout_error_growth_is_reported_per_depth() {
        let frozen = |seen: Visible, _action: u8| seen;
        let growth = free_rollout_error_growth(balanced(), &[0, 1, 0], frozen).expect("growth");
        assert_eq!(growth.len(), 3);
        assert_eq!(growth[0].0, 1);
        assert_eq!(growth[2].1, balanced().visible());
    }
}
