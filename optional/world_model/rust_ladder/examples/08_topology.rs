//! WM08 — describe geometry without confusing it with dynamics.
//!
//! Run:
//! ```text
//! cargo +1.90.0 run --offline --locked --example 08_topology
//! ```
//!
//! The trajectory is projected to two normalized numbers and its H0 components are counted
//! at a stated radius. Then the trajectory is **reversed**, and the count is computed again.
//!
//! Predict first: will the count change? It should not. That is the lesson, and it is a
//! limitation rather than a feature: a descriptor that cannot see time reversal cannot
//! certify that the model predicts the correct next state.

use world_model_ladder::dataset::{collect, episode_bounds, CollectConfig, Rng};
use world_model_ladder::shape::{h0_at_radius, project, reversed};

fn main() -> Result<(), String> {
    let mut rng = Rng::new(0);
    let rows = collect(
        &mut rng,
        CollectConfig {
            episodes: 2,
            max_steps: 120,
            exploration: 0.25,
            bias_scale: 0.15,
        },
    )?;
    let bounds = episode_bounds(&rows);

    for (episode, (begin, end)) in bounds.iter().enumerate() {
        let states: Vec<_> = rows[*begin..*end].iter().map(|row| row.state).collect();
        let points = project(&states);
        println!("episode {episode}: {} sampled states", points.len());
        for radius in [0.05, 0.15, 0.40] {
            let forward = h0_at_radius(&points, radius)?;
            let backward = h0_at_radius(&project(&reversed(&states)), radius)?;
            println!(
                "  radius {radius:.2}: components {:>3} -> after reversing {:>3}  (identical: {})",
                forward.components,
                backward.components,
                forward == backward
            );
        }
    }
    println!();
    println!("The radius is part of the answer. A component count without its radius is not");
    println!("reproducible, and a small bar that only survives because the radius truncated its");
    println!("death is an artefact of the radius, not a feature of the trajectory.");
    println!();
    println!("H0 says how the sampled cloud is connected. It says nothing about whether the");
    println!("model predicts the next state, and nothing about CartPole.");
    Ok(())
}
