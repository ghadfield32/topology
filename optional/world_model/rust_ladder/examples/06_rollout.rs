//! WM06 — one-step error versus free rollout.
//!
//! Run:
//! ```text
//! cargo +1.90.0 run --offline --locked --example 06_rollout
//! ```
//!
//! Predict first: will the one-step error be larger or smaller than the error after ten
//! imagined steps? Why?
//!
//! Watch the *frozen baseline* column. It assumes nothing ever changes. If the model loses
//! to it, the model has not learned motion at that depth — however good its one-step number
//! looked.

use world_model_ladder::dataset::{collect, episode_bounds, split_episodes, CollectConfig, Rng};
use world_model_ladder::model::DeltaModel;
use world_model_ladder::rollout::{one_step_error, rollout_curve};

fn main() -> Result<(), String> {
    let mut rng = Rng::new(0);
    let rows = collect(
        &mut rng,
        CollectConfig {
            episodes: 40,
            max_steps: 500,
            exploration: 0.25,
            bias_scale: 0.15,
        },
    )?;
    let (train, holdout) = split_episodes(&rows, 0.75)?;
    let model = DeltaModel::fit(train, 1e-6)?;
    let bounds = episode_bounds(holdout);

    let one_step = one_step_error(&model, holdout)?;
    println!("teacher-forced (every step starts from reality):");
    println!("  position error: {:.6} m", one_step.position_m);
    println!("  angle error:    {:.6} rad", one_step.angle_rad);
    println!();

    let curve = rollout_curve(&model, holdout, &bounds, 10)?;
    println!("free rollout (the model eats its own output):");
    println!(
        "  {:>5}  {:>12}  {:>12}  {:>12}  {:>12}",
        "depth", "model m", "frozen m", "model rad", "frozen rad"
    );
    for index in 0..curve.depth.len() {
        println!(
            "  {:>5}  {:>12.6}  {:>12.6}  {:>12.6}  {:>12.6}",
            curve.depth[index],
            curve.model[index].position_m,
            curve.frozen[index].position_m,
            curve.model[index].angle_rad,
            curve.frozen[index].angle_rad
        );
    }
    println!();
    println!(
        "trust horizon (both tolerances): {}",
        curve.trust_horizon(0.05, 0.02)
    );
    println!(
        "deepest depth beating the frozen baseline: {}",
        curve.deepest_depth_beating_frozen()
    );
    println!();
    println!("Two different ceilings:");
    println!("  * how long the model stays accurate;");
    println!("  * how well a random search covers the plan space.");
    println!("They are measured separately because they are not the same number.");
    Ok(())
}
