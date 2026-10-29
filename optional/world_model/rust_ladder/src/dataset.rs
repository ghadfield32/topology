//! WM04 — collect episodes, keeping the successor and both endings.
//!
//! The most important record in the whole project is one transition, and it must keep seven
//! things. Drop any one of them and a later bug looks like a bad model:
//!
//! | Field | Why it has to be there |
//! |---|---|
//! | `episode` | windows may never span two episodes |
//! | `tick` | where in the episode this happened |
//! | `state` | the input |
//! | `action` | the input |
//! | `successor` | the target — including on the **final** transition |
//! | `terminated` | the pole fell; learnable from the state |
//! | `truncated` | the timer expired; not learnable, not a failure |
//!
//! Python sibling: `python/wm04_dataset.py`.

use crate::action::Action;
use crate::simulator::step;
use crate::state::{State, MAX_STEPS};

/// One observed transition. Owning the numbers rather than indexing a shared table is what
/// makes the train/test split safe without a lifetime argument.
#[derive(Debug, Clone, Copy, PartialEq)]
pub struct Transition {
    pub episode: usize,
    pub tick: usize,
    pub state: State,
    pub action: Action,
    /// The observation *after* the action. Kept explicitly so the final transition of an
    /// episode — the only one that can carry a `terminated` label — still has a target.
    pub successor: State,
    pub terminated: bool,
    pub truncated: bool,
}

impl Transition {
    /// The learning target: how much the two visible numbers change, normalized.
    ///
    /// Predicting the *change* rather than the next value is deliberate. Consecutive states
    /// are nearly identical, so a model asked for the next value scores beautifully by
    /// copying its input and learns no dynamics.
    pub fn visible_delta(&self) -> [f64; 2] {
        let now = self.state.normalized();
        let next = self.successor.normalized();
        [next[0] - now[0], next[1] - now[1]]
    }

    pub fn visible(&self) -> [f64; 2] {
        self.state.normalized()
    }
}

/// Why an episode stopped. Two endings, and they are different facts.
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum Ending {
    /// The pole fell or the cart left the rail. A consequence of the state.
    Terminated,
    /// The step budget ran out with nothing wrong. A stopwatch the model cannot see.
    Truncated,
}

/// A small deterministic generator, so the crate needs no dependencies and any run can be
/// repeated exactly. It is a splitmix-style recurrence, not a statistical recommendation.
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
    State::new(
        rng.range(-0.05, 0.05),
        rng.range(-0.05, 0.05),
        rng.range(-0.05, 0.05),
        rng.range(-0.05, 0.05),
    )
    .expect("a bounded uniform draw is finite")
}

/// The three-line controller: put the cart under the falling pole.
///
/// `bias` tilts an episode so the collected data contains journeys, not only immaculate
/// hovering. A dataset of perfect balancing has never seen the cart move somewhere, and a
/// planner will ask for exactly that.
pub fn proportional_controller(state: State, bias: f64) -> Action {
    let lean = state.theta + 0.5 * state.omega + bias;
    if lean > 0.0 {
        Action::Right
    } else {
        Action::Left
    }
}

/// Collection settings, grouped so a call site says what it means.
#[derive(Debug, Clone, Copy, PartialEq)]
pub struct CollectConfig {
    pub episodes: usize,
    pub max_steps: usize,
    /// Probability of ignoring the controller. Keeps ugly, nearly-doomed states in the data.
    pub exploration: f64,
    /// Per-episode tilt, so some games travel along the rail.
    pub bias_scale: f64,
}

impl Default for CollectConfig {
    fn default() -> Self {
        Self {
            episodes: 40,
            max_steps: MAX_STEPS,
            exploration: 0.25,
            bias_scale: 0.15,
        }
    }
}

/// Play episodes and record every transition.
pub fn collect(rng: &mut Rng, config: CollectConfig) -> Result<Vec<Transition>, String> {
    if config.episodes == 0 {
        return Err("episodes must be positive".to_string());
    }
    if config.max_steps == 0 {
        return Err("max_steps must be positive".to_string());
    }
    if !(0.0..=1.0).contains(&config.exploration) {
        return Err("exploration is a probability in [0, 1]".to_string());
    }
    if !config.bias_scale.is_finite() || config.bias_scale < 0.0 {
        return Err("bias_scale must be finite and nonnegative".to_string());
    }

    let mut out = Vec::new();
    for episode in 0..config.episodes {
        let bias = rng.range(-config.bias_scale, config.bias_scale);
        let mut state = initial_state(rng);
        let mut tick = 0usize;
        while tick < config.max_steps {
            let action = if rng.unit() < config.exploration {
                Action::from_index(rng.below(2) as usize)?
            } else {
                proportional_controller(state, bias)
            };
            let successor = step(state, action)?;
            tick += 1;
            let fell = successor.failed();
            let out_of_time = !fell && tick == config.max_steps;
            out.push(Transition {
                episode,
                tick: tick - 1,
                state,
                action,
                successor,
                terminated: fell,
                truncated: out_of_time,
            });
            state = successor;
            if fell || out_of_time {
                break;
            }
        }
    }
    Ok(out)
}

/// Half-open `[start, end)` index range per episode.
///
/// Adjacent transitions from one episode are not independent evidence. Splitting by index
/// rather than by episode quietly puts the continuation of a training trajectory into the
/// test set, and every metric then looks better than it is.
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

/// Split episodes, not rows, into train and holdout.
///
/// Returns `(train, holdout)` as slices of the transition list. Taking a fraction of
/// *episodes* is the only split that keeps a trajectory in one side.
pub fn split_episodes(
    rows: &[Transition],
    train_fraction: f64,
) -> Result<(&[Transition], &[Transition]), String> {
    if !(0.0..=1.0).contains(&train_fraction) || train_fraction == 0.0 || train_fraction == 1.0 {
        return Err("train_fraction must be strictly between 0 and 1".to_string());
    }
    let bounds = episode_bounds(rows);
    if bounds.len() < 2 {
        return Err("need at least two episodes to split".to_string());
    }
    let split =
        ((bounds.len() as f64 * train_fraction).round() as usize).clamp(1, bounds.len() - 1);
    let boundary = bounds[split].0;
    Ok((&rows[..boundary], &rows[boundary..]))
}

#[cfg(test)]
mod tests {
    use super::*;

    fn config() -> CollectConfig {
        CollectConfig {
            episodes: 6,
            max_steps: 60,
            exploration: 0.4,
            bias_scale: 0.15,
        }
    }

    #[test]
    fn every_transition_keeps_its_successor() {
        let mut rng = Rng::new(3);
        let rows = collect(&mut rng, config()).expect("collect");
        assert!(!rows.is_empty());
        for row in &rows {
            // The successor is a real state, and the delta is derived, not guessed.
            assert!(row.successor.x.is_finite());
            let delta = row.visible_delta();
            assert_eq!(delta.len(), 2);
            assert!(delta[0].is_finite() && delta[1].is_finite());
        }
    }

    #[test]
    fn the_final_transition_of_each_episode_is_recorded() {
        let mut rng = Rng::new(5);
        let rows = collect(&mut rng, config()).expect("collect");
        let bounds = episode_bounds(&rows);
        assert_eq!(bounds.len(), config().episodes);
        for (_, end) in &bounds {
            let last = &rows[end - 1];
            assert!(
                last.terminated || last.truncated,
                "an episode ends on an ending"
            );
        }
    }

    #[test]
    fn both_endings_occur_and_are_never_both_true() {
        let mut rng = Rng::new(7);
        let rows = collect(&mut rng, config()).expect("collect");
        assert!(
            rows.iter().any(|row| row.terminated),
            "a fall must be in the data"
        );
        assert!(rows.iter().all(|row| !(row.terminated && row.truncated)));
    }

    #[test]
    fn collection_covers_both_actions() {
        let mut rng = Rng::new(11);
        let rows = collect(&mut rng, config()).expect("collect");
        let actions: std::collections::BTreeSet<usize> =
            rows.iter().map(|row| row.action.index()).collect();
        assert_eq!(actions.len(), 2, "a planner asks about both shoves");
    }

    #[test]
    fn split_never_puts_half_an_episode_in_the_holdout() {
        let mut rng = Rng::new(13);
        let rows = collect(&mut rng, config()).expect("collect");
        let (train, holdout) = split_episodes(&rows, 0.67).expect("split");
        assert!(!train.is_empty() && !holdout.is_empty());
        let boundary = train.len();
        assert!(
            rows[boundary - 1].terminated || rows[boundary - 1].truncated,
            "the split must fall on an episode boundary"
        );
        // Every transition in each side belongs to a whole episode.
        let train_episodes: std::collections::BTreeSet<usize> =
            train.iter().map(|row| row.episode).collect();
        let holdout_episodes: std::collections::BTreeSet<usize> =
            holdout.iter().map(|row| row.episode).collect();
        assert!(train_episodes.is_disjoint(&holdout_episodes));
    }

    #[test]
    fn bad_collection_settings_are_errors() {
        let mut rng = Rng::new(17);
        for broken in [
            CollectConfig {
                episodes: 0,
                ..config()
            },
            CollectConfig {
                max_steps: 0,
                ..config()
            },
            CollectConfig {
                exploration: 1.5,
                ..config()
            },
            CollectConfig {
                bias_scale: -0.1,
                ..config()
            },
        ] {
            assert!(collect(&mut rng, broken).is_err());
        }
        assert!(split_episodes(&[], 0.5).is_err());
    }

    #[test]
    fn a_seed_reproduces_the_exact_same_rows() {
        let first = collect(&mut Rng::new(21), config()).expect("collect");
        let second = collect(&mut Rng::new(21), config()).expect("collect");
        assert_eq!(first, second);
        let third = collect(&mut Rng::new(22), config()).expect("collect");
        assert_ne!(first, third);
    }
}
