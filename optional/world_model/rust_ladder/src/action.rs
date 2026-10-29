//! WM02 — represent the allowed actions with an `enum`.
//!
//! Two shoves, no third option. An `enum` makes "there are exactly two" a fact the compiler
//! checks, so a `match` cannot forget a case and no integer can arrive meaning something
//! else.
//!
//! Python sibling: `python/wm02_action.py`.

/// The only two things an agent may do.
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum Action {
    Left,
    Right,
}

impl Action {
    /// The force this action applies, in newtons.
    ///
    /// `match` is exhaustive: adding a variant breaks this function at compile time
    /// instead of silently falling through at run time. That is the entire argument for
    /// an enum over an `i32`.
    pub fn force(self) -> f64 {
        match self {
            Action::Left => -MAGNITUDE,
            Action::Right => MAGNITUDE,
        }
    }

    /// Every action, in a fixed order. Used where an index is needed.
    pub const ALL: [Action; 2] = [Action::Left, Action::Right];

    /// A stable index, for recording a transition in a column of numbers.
    pub fn index(self) -> usize {
        match self {
            Action::Left => 0,
            Action::Right => 1,
        }
    }

    /// Recover an action from its recorded index, or say why not.
    pub fn from_index(index: usize) -> Result<Self, String> {
        match index {
            0 => Ok(Action::Left),
            1 => Ok(Action::Right),
            other => Err(format!("action index {other} is not 0 or 1")),
        }
    }

    pub fn name(self) -> &'static str {
        match self {
            Action::Left => "left",
            Action::Right => "right",
        }
    }
}

/// The shove magnitude. A constant, not a parameter: nothing here is tuned.
pub const MAGNITUDE: f64 = 10.0;

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn the_two_forces_are_opposite() {
        assert_eq!(Action::Left.force(), -10.0);
        assert_eq!(Action::Right.force(), 10.0);
        assert_eq!(Action::Left.force(), -Action::Right.force());
    }

    #[test]
    fn indices_round_trip_and_reject_everything_else() {
        for action in Action::ALL {
            assert_eq!(
                Action::from_index(action.index()).expect("round trip"),
                action
            );
        }
        assert!(Action::from_index(2).is_err());
        assert!(Action::from_index(usize::MAX).is_err());
    }

    #[test]
    fn all_is_in_index_order() {
        for (position, action) in Action::ALL.iter().enumerate() {
            assert_eq!(action.index(), position);
        }
    }

    #[test]
    fn an_action_is_not_a_goal() {
        // "Push right now" and "balance" are different kinds of thing. Encoding both as
        // integers is how a program ends up unable to tell a plan from a preference.
        assert_eq!(Action::ALL.len(), 2);
    }
}
