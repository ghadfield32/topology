//! WM09 — put it all together and save a run nothing can overwrite.
//!
//! Run:
//! ```text
//! cargo +1.90.0 run --offline --locked --example 09_experiment -- my_work/ladder01
//! ```
//!
//! The output directory must not exist. The second run with the same directory is refused,
//! and that refusal is the feature: a stale record cannot be mistaken for a fresh one.

use std::env;
use std::path::PathBuf;

use world_model_ladder::dataset::{collect, episode_bounds, split_episodes, CollectConfig, Rng};
use world_model_ladder::experiment::{
    boolean, ensure_new_output, integer, number, write_into, RunConfig,
};
use world_model_ladder::model::DeltaModel;
use world_model_ladder::planner::{plan, Goal};
use world_model_ladder::rollout::{one_step_error, rollout_curve};
use world_model_ladder::shape::{h0_at_radius, project};
use world_model_ladder::state::State;

fn main() -> Result<(), String> {
    let output: PathBuf = env::args()
        .nth(1)
        .map(PathBuf::from)
        .unwrap_or_else(|| PathBuf::from("my_work/ladder01"));

    let config = RunConfig {
        seed: 0,
        episodes: 40,
        horizon: 10,
        planning_horizon: 6,
        sequences: 64,
        topology_radius: 0.15,
        ..RunConfig::default()
    };

    // Refuse early, before doing any work, so a refused run costs nothing.
    let prepared = ensure_new_output(&output)?;

    let mut rng = Rng::new(config.seed);
    let rows = collect(
        &mut rng,
        CollectConfig {
            episodes: config.episodes,
            max_steps: config.max_steps,
            exploration: config.exploration,
            bias_scale: config.bias_scale,
        },
    )?;
    let (train, holdout) = split_episodes(&rows, 0.75)?;
    let model = DeltaModel::fit(train, config.ridge)?;
    let bounds = episode_bounds(holdout);

    let one_step = one_step_error(&model, holdout)?;
    let curve = rollout_curve(&model, holdout, &bounds, config.horizon)?;

    let balance = plan(
        &model,
        State::upright(),
        Goal::Balance,
        config.planning_horizon,
        config.sequences,
        &mut Rng::new(config.seed + 1),
    )?;
    let park = plan(
        &model,
        State::upright(),
        Goal::Park(1.0),
        config.planning_horizon,
        config.sequences,
        &mut Rng::new(config.seed + 2),
    )?;

    // Topology on the holdout trajectory, at the stated radius.
    let states: Vec<_> = holdout.iter().map(|row| row.state).collect();
    let shape = h0_at_radius(&project(&states), config.topology_radius)?;

    let sections = vec![
        (
            "data",
            vec![
                integer("transitions", rows.len()),
                integer("train_transitions", train.len()),
                integer("holdout_transitions", holdout.len()),
                integer("episodes", episode_bounds(&rows).len()),
            ],
        ),
        (
            "model",
            vec![
                integer("samples", model.samples),
                number("ridge", model.ridge),
                integer("coefficients", model.weights().len()),
            ],
        ),
        (
            "one_step",
            vec![
                number("position_error_m", one_step.position_m),
                number("angle_error_rad", one_step.angle_rad),
            ],
        ),
        (
            "rollout",
            vec![
                integer(
                    "trust_horizon",
                    curve.trust_horizon(config.tolerance_m, config.tolerance_rad),
                ),
                integer(
                    "deepest_depth_beating_frozen",
                    curve.deepest_depth_beating_frozen(),
                ),
                number(
                    "final_angle_error_rad",
                    curve.model.last().map(|e| e.angle_rad).unwrap_or(0.0),
                ),
                number(
                    "final_frozen_error_rad",
                    curve.frozen.last().map(|e| e.angle_rad).unwrap_or(0.0),
                ),
            ],
        ),
        (
            "planning",
            vec![
                (
                    "balance_goal".to_string(),
                    format!("\"{}\"", Goal::Balance.name()),
                ),
                number("balance_score", balance.score),
                (
                    "park_goal".to_string(),
                    format!("\"{}\"", Goal::Park(1.0).name()),
                ),
                number("park_score", park.score),
                boolean("weights_unchanged", true),
            ],
        ),
        (
            "topology_h0",
            vec![
                integer("points", shape.points),
                number("radius", config.topology_radius),
                integer("components", shape.components),
                integer("merges", shape.merges),
                (
                    "caveat".to_string(),
                    "\"describes sampled geometry; not evidence about dynamics\"".to_string(),
                ),
            ],
        ),
    ];

    let file = write_into(&prepared, &config, &sections)?;
    println!("wrote {}", file.display());
    println!();
    println!("one-step angle error:   {:.6} rad", one_step.angle_rad);
    println!(
        "trust horizon:          {} steps",
        curve.trust_horizon(config.tolerance_m, config.tolerance_rad)
    );
    println!("best balance score:     {:.4}", balance.score);
    println!("best park(1.0) score:   {:.4}", park.score);
    println!(
        "H0 components at r={:.2}: {}",
        config.topology_radius, shape.components
    );
    println!();
    println!("Run this again with the same argument to see it refuse to overwrite.");
    Ok(())
}
