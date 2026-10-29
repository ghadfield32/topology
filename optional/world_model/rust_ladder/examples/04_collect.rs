//! WM04 — collect episodes, keeping successors and both endings.
//!
//! Run:
//! ```text
//! cargo +1.90.0 run --offline --locked --example 04_collect
//! ```
//!
//! Predict first: with `exploration = 0.0` and `bias_scale = 0.0`, would you expect any
//! episode to end by *falling*? Probably not — a competent controller balances. If you only
//! collect that data, your model never sees a crash, and a crash detector trained on it is
//! confidently wrong. `bias_scale` and `exploration` exist to prevent exactly that.

use world_model_ladder::dataset::{
    collect, episode_bounds, split_episodes, CollectConfig, Ending, Rng,
};

fn main() -> Result<(), String> {
    let mut rng = Rng::new(0);
    let config = CollectConfig {
        episodes: 20,
        max_steps: 500,
        exploration: 0.25,
        bias_scale: 0.15,
    };
    let rows = collect(&mut rng, config)?;

    let bounds = episode_bounds(&rows);
    let terminated = rows.iter().filter(|row| row.terminated).count();
    let truncated = rows.iter().filter(|row| row.truncated).count();
    println!("transitions:      {}", rows.len());
    println!("episodes:         {}", bounds.len());
    println!("ended by falling: {terminated}");
    println!("ended by timer:   {truncated}");
    println!();

    let first = &rows[0];
    println!("the first record, which keeps seven things:");
    println!("  episode:      {}", first.episode);
    println!("  tick:         {}", first.tick);
    println!("  state:        {:?}", first.state);
    println!("  action:       {}", first.action.name());
    println!("  successor:    {:?}", first.successor);
    println!("  terminated:   {}", first.terminated);
    println!("  truncated:    {}", first.truncated);
    println!("  visible:      {:?}", first.visible());
    println!("  delta:        {:?}", first.visible_delta());
    println!();

    // The final transition of an episode is the one that carries the crash label. It must
    // still have a successor, or the label has no prediction target and gets dropped.
    let (_, end) = bounds[0];
    let last = &rows[end - 1];
    let ending = if last.terminated {
        Ending::Terminated
    } else {
        Ending::Truncated
    };
    println!("last transition of episode 0: {ending:?}");
    println!(
        "  successor still present: {}",
        last.successor.x.is_finite()
    );

    let (train, holdout) = split_episodes(&rows, 0.7)?;
    println!();
    println!(
        "split by episode: train {} transitions, holdout {}",
        train.len(),
        holdout.len()
    );
    let holdout_episodes: std::collections::BTreeSet<usize> =
        holdout.iter().map(|row| row.episode).collect();
    println!("holdout covers {} whole episodes", holdout_episodes.len());
    Ok(())
}
