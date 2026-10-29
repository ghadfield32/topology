//! WM07 — plan by imagining, and change the goal without refitting.
//!
//! Run:
//! ```text
//! cargo +1.90.0 run --offline --locked --example 07_plan
//! ```
//!
//! This is the payload of the whole project. One fitted model, two goals, no retraining.
//! Watch the printed coefficients before and after: they must be identical.
//!
//! Note that this planner is *open loop*: it commits to the best sequence for `horizon`
//! steps. The GRU reference replans after every real step and throws the rest away. Both
//! are worth understanding, and the difference is stated rather than hidden.

use world_model_ladder::dataset::{collect, split_episodes, CollectConfig, Rng};
use world_model_ladder::model::DeltaModel;
use world_model_ladder::planner::{dream, plan, score, Goal};
use world_model_ladder::state::State;

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
    let (train, _) = split_episodes(&rows, 0.75)?;
    let model = DeltaModel::fit(train, 1e-6)?;

    let start = State::upright();
    let goals = [Goal::Balance, Goal::Park(1.0), Goal::Park(0.5)];
    let before = model.weights();

    for goal in goals {
        let mut rng = Rng::new(11);
        let chosen = plan(&model, start, goal, 6, 64, &mut rng)?;
        let dreamt = dream(&model, start, &chosen.actions)?;
        println!(
            "goal: {:<16}  score {:>9.4}  alive {}/{}  final x {:+.4} m",
            goal.name(),
            chosen.score,
            dreamt.alive_steps(),
            dreamt.states.len(),
            dreamt.last_reachable().x
        );
        let sequence: Vec<&str> = chosen.actions.iter().map(|action| action.name()).collect();
        println!("  actions: {}", sequence.join(" "));
        println!("  re-scored by this goal: {:.6}", score(goal, &dreamt));
    }

    let after = model.weights();
    println!();
    println!("coefficients before planning: {before:?}");
    println!("coefficients after planning:  {after:?}");
    println!("unchanged: {}", before == after);
    println!();
    println!("Changing the goal changed the *request*, not the fitted physics.");
    println!("That is why the goal can be edited on a Tuesday without a training run.");
    Ok(())
}
