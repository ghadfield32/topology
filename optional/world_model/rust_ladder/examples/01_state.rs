//! WM01 — represent the world with a `struct`.
//!
//! Run:
//! ```text
//! cargo +1.90.0 run --offline --locked --example 01_state
//! ```
//!
//! Predict before you run: change `angle` to `-0.02`. Does that change `velocity`?
//! No. There is no physics in this file. You changed a *stored* value.

use world_model_ladder::state::{State, THETA_LIMIT, X_LIMIT};

fn main() -> Result<(), String> {
    let state = State::new(0.0, 0.0, 0.02, 0.0)?;

    println!("position:          {} m", state.x);
    println!("velocity:          {} m/s", state.v);
    println!("angle:             {} rad", state.theta);
    println!("angular velocity:  {} rad/s", state.omega);
    println!();

    println!("Failing if |x| > {X_LIMIT} m or |theta| > {THETA_LIMIT} rad");
    println!("failed right now:  {}", state.failed());
    println!();

    // The two-number projection. Note what is missing.
    let (x, theta) = state.visible();
    println!("visible (camera):  x = {x} m, theta = {theta} rad");
    println!("normalized:        {:?}", state.normalized());
    println!();

    // Two different worlds with the same visible pair. This is exactly why the article
    // needs memory, and why this ladder starts with the complete state instead.
    let moving = State::new(0.0, 1.7, 0.02, -2.5)?;
    println!("another state with the same visible pair:");
    println!("  visible:         {:?}", moving.visible());
    println!("  full state:      {moving:?}");
    println!("  states equal?    {}", state == moving);
    Ok(())
}
