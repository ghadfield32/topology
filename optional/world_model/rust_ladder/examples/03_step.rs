//! WM03 — calculate one simulator step.
//!
//! Run:
//! ```text
//! cargo +1.90.0 run --offline --locked --example 03_step
//! ```
//!
//! Hand prediction first: from rest and upright, a right push gives
//! `x = 0`, `v = 0.1951`, `theta = 0`, `omega = -0.2927`.
//!
//! Why are position and angle still zero? Because this Euler update advances them with the
//! *old* velocities, which were zero. The force changes the velocities for the next step.

use world_model_ladder::action::Action;
use world_model_ladder::simulator::{advance_position, step};
use world_model_ladder::state::{State, MAX_STEPS};

fn main() -> Result<(), String> {
    println!("one position update: {}", advance_position(1.0, 0.4, 0.02)?);
    println!("  by hand: 1.0 + 0.4 * 0.02 = {}", 1.0 + 0.4 * 0.02);
    println!();

    let start = State::upright();
    for action in Action::ALL {
        let next = step(start, action)?;
        println!(
            "from rest, push {:<5} -> x {:+.6}  v {:+.6}  theta {:+.6}  omega {:+.6}",
            action.name(),
            next.x,
            next.v,
            next.theta,
            next.omega
        );
    }
    println!();

    // Let the controller balance, and count how long it survives.
    let mut state = State::upright();
    let mut survived = 0usize;
    for _ in 0..MAX_STEPS {
        let action = if state.theta + 0.5 * state.omega > 0.0 {
            Action::Right
        } else {
            Action::Left
        };
        state = step(state, action)?;
        survived += 1;
        if state.failed() {
            break;
        }
    }
    println!("hand controller survived {survived} of {MAX_STEPS} steps");
    println!("final state: {state:?}");
    println!();
    println!("Validation is a value, not a panic: a bad call returns Err(String).");
    println!("Rejected dt: {:?}", advance_position(0.0, 0.0, 0.0).err());
    Ok(())
}
