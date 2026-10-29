//! WM05 — fit a transition model and use it instead of the simulator.
//!
//! Run:
//! ```text
//! cargo +1.90.0 run --offline --locked --example 05_fit
//! ```
//!
//! The claim this rung makes is narrow and checkable: after `DeltaModel::fit`, the
//! predictions come from the **coefficients**, not from `simulator::step`. The example
//! prints the coefficients and then predicts at a state the simulator never visited.
//!
//! `fit(&training, ridge)` borrows the data; the model owns only its coefficients. That is
//! why you can fit, inspect the data, and fit again.

use world_model_ladder::action::Action;
use world_model_ladder::dataset::{collect, split_episodes, CollectConfig, Rng};
use world_model_ladder::model::DeltaModel;
use world_model_ladder::simulator::step;
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
    let (train, holdout) = split_episodes(&rows, 0.75)?;

    let model = DeltaModel::fit(train, 1e-6)?;
    println!("fitted on {} borrowed transitions", model.samples);
    println!("ridge: {}", model.ridge);
    println!("coefficients (output x feature):");
    for (output, row) in model.coefficients.iter().enumerate() {
        let label = if output == 0 {
            "cart position"
        } else {
            "pole angle  "
        };
        println!("  {label}: {row:?}");
    }
    println!();

    // Compare the fitted prediction with the simulator on the held-out episodes. The model
    // has never seen these transitions.
    let mut model_error = 0.0;
    let mut simulator_error = 0.0;
    for row in holdout.iter().take(500) {
        let predicted = model.predict(row.state, row.action)?;
        // A fitted prediction is compared against the truth. Calling `step` here is the
        // *reference*, not part of the model.
        let reference = step(row.state, row.action)?;
        model_error += (predicted.theta - row.successor.theta).abs();
        simulator_error += (reference.theta - row.successor.theta).abs();
    }
    println!("mean |theta| error over 500 held-out steps:");
    println!("  fitted model:  {:.6} rad", model_error / 500.0);
    println!(
        "  simulator:     {:.6} rad  (this is the truth, so ~0)",
        simulator_error / 500.0
    );
    println!();
    println!("The model is linear and fully observed. It is not the article's GRU, and its");
    println!("numbers must not be compared with the GRU's as though only the language changed.");

    // Predict somewhere the simulator was never asked to go.
    let probe = State::new(0.7, 1.2, 0.05, -0.4)?;
    let predicted = model.predict(probe, Action::Right)?;
    println!();
    println!("probe state:   {probe:?}");
    println!("model says:    {predicted:?}");
    println!("note: velocities are reported unchanged, because this model cannot observe them.");
    Ok(())
}
