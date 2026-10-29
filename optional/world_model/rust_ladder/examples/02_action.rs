//! WM02 — represent the allowed actions with an `enum`.
//!
//! Run:
//! ```text
//! cargo +1.90.0 run --offline --locked --example 02_action
//! ```
//!
//! Expected output:
//! ```text
//! left:  -10 N
//! right:  10 N
//! ```
//!
//! Try this, then undo it: add `Idle` to the `Action` enum and compile. The error names
//! every `match` that no longer covers all cases. That is the compiler doing the work an
//! `i32` action would have left to you at run time.

use world_model_ladder::action::Action;

fn main() {
    for action in Action::ALL {
        println!(
            "{:<6} {:>5} N  (index {})",
            action.name(),
            action.force(),
            action.index()
        );
    }
    println!();
    println!("An action is what you can do now. A goal is what you want. They are different");
    println!("kinds of thing, and encoding both as integers is how a program loses that.");
    println!();
    println!("Recovering an action from a recorded index:");
    for index in 0..3 {
        match Action::from_index(index) {
            Ok(action) => println!("  {index} -> {}", action.name()),
            Err(problem) => println!("  {index} -> rejected: {problem}"),
        }
    }
}
