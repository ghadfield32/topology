//! Command-line companion. Same fixture in, same summary out, plus the delta model.
//!
//! Usage:
//! ```text
//! cargo run --quiet --bin world-model-rust -- --check-topology ../fixtures/points.json --output my_work/rust_topology01
//! cargo run --quiet --bin world-model-rust -- --rollout --output my_work/rust_rollout01
//! ```
//!
//! Every run writes to a new directory and refuses to reuse one. A stale record is not
//! evidence, and this binary is not an assessment.

use std::env;
use std::fs;
use std::path::{Path, PathBuf};
use std::process;

use world_model_companion::cartpole::{collect, Rng, MAX_STEPS};
use world_model_companion::linear_model::fit_delta_model;
use world_model_companion::persistence::DiagramSummary;
use world_model_companion::topology;

struct Options {
    fixture: Option<PathBuf>,
    output: PathBuf,
    check_topology: bool,
    rollout: bool,
    episodes: usize,
    horizon: usize,
    seed: u64,
}

impl Default for Options {
    fn default() -> Self {
        Self {
            fixture: None,
            output: PathBuf::from("my_work/world_model_rust01"),
            check_topology: false,
            rollout: false,
            episodes: 24,
            horizon: 12,
            seed: 0,
        }
    }
}

fn parse_args() -> Result<Options, String> {
    let mut options = Options::default();
    let mut args = env::args().skip(1);
    while let Some(argument) = args.next() {
        match argument.as_str() {
            "--fixture" => options.fixture = Some(PathBuf::from(next(&mut args, "--fixture")?)),
            "--output" => options.output = PathBuf::from(next(&mut args, "--output")?),
            "--check-topology" => {
                options.check_topology = true;
                // A following flag is not a fixture path; only consume a real argument.
                if let Some(value) = args.next() {
                    if value.starts_with("--") {
                        return Err(format!("{value} must come after --check-topology's value"));
                    }
                    options.fixture = Some(PathBuf::from(value));
                }
            }
            "--rollout" => options.rollout = true,
            "--episodes" => options.episodes = parse_number(&next(&mut args, "--episodes")?)?,
            "--horizon" => options.horizon = parse_number(&next(&mut args, "--horizon")?)?,
            "--seed" => options.seed = parse_number(&next(&mut args, "--seed")?)?,
            "--help" | "-h" => {
                println!("{}", help_text());
                process::exit(0);
            }
            other => return Err(format!("unknown argument {other}")),
        }
    }
    if !options.check_topology && !options.rollout {
        options.check_topology = true;
        options.rollout = true;
    }
    Ok(options)
}

fn next(args: &mut impl Iterator<Item = String>, flag: &str) -> Result<String, String> {
    args.next()
        .ok_or_else(|| format!("{flag} requires a value"))
}

fn parse_number<T: std::str::FromStr>(text: &str) -> Result<T, String> {
    text.parse::<T>()
        .map_err(|_| format!("cannot parse {text:?}"))
}

fn help_text() -> &'static str {
    "--check-topology [FIXTURE]  reduce the committed fixture and print counts\n\
     --rollout                   fit the linear delta model and report error growth\n\
     --output DIR                new directory to write records into\n\
     --episodes N                collected episodes for the rollout experiment\n\
     --horizon N                 depths to compare\n\
     --seed N                    deterministic generator seed"
}

fn ensure_new_output(path: &Path) -> Result<(), String> {
    if path.exists() {
        return Err(format!(
            "{} already exists; choose a new output directory",
            path.display()
        ));
    }
    fs::create_dir_all(path).map_err(|error| error.to_string())
}

fn main() {
    if let Err(message) = run() {
        eprintln!("ERROR: {message}");
        process::exit(1);
    }
}

fn run() -> Result<(), String> {
    let options = parse_args()?;
    ensure_new_output(&options.output)?;

    let mut written: Vec<&str> = Vec::new();
    if options.check_topology {
        let fixture = options.fixture.clone().unwrap_or_else(|| {
            Path::new(env!("CARGO_MANIFEST_DIR")).join("../fixtures/points.json")
        });
        let summary = topology::check(&fixture)?;
        write_topology(&options.output, &fixture, &summary)?;
        written.push("topology.json");
    }
    if options.rollout {
        let report = rollout_report(options.episodes, options.horizon, options.seed)?;
        fs::write(options.output.join("rollout.json"), format!("{report}\n"))
            .map_err(|error| error.to_string())?;
        written.push("rollout.json");
    }
    println!(
        "{{\"output\": {:?}, \"files\": {:?}, \"status\": \"completed\", \"assessment\": \"not_assessed\"}}",
        options.output.display().to_string(),
        written
    );
    Ok(())
}

fn write_topology(out: &Path, fixture: &Path, summary: &DiagramSummary) -> Result<(), String> {
    // The simplex count and the essential count are reported too, because a loop that
    // only survives the truncation is a scale artefact, not a feature.
    let body = format!(
        "{{\n  \"fixture\": {:?},\n  \"max_edge\": {:.12},\n  \"h0_finite\": {},\n  \"h1_finite\": {},\n  \"h1_essential\": {},\n  \"h1_total_persistence\": {:.12},\n  \"max_persistence\": {:.12},\n  \"simplex_count\": {},\n  \"interpretation_boundary\": \"Descriptive summary of one finite 2-D point cloud under the Rips metric; the bars carry no semantics and this is not evidence about CartPole.\",\n  \"implementation\": \"independent Rust F2 reduction over the same filtration\"\n}}\n",
        fixture.display().to_string(),
        summary.max_edge,
        summary.h0_finite,
        summary.h1_finite,
        summary.h1_essential,
        summary.h1_total_persistence,
        summary.h1_max_persistence,
        summary.simplex_count,
    );
    fs::write(out.join("topology.json"), body).map_err(|error| error.to_string())
}

/// Fit the linear delta model on real collected transitions and measure error growth.
///
/// The comparison that matters is against the *frozen* baseline: a model that assumes
/// nothing ever changes. A predictor that loses to it is not a world model at that
/// depth, whatever its training loss said.
fn rollout_report(episodes: usize, horizon: usize, seed: u64) -> Result<String, String> {
    if horizon == 0 {
        return Err("horizon must be positive".to_string());
    }
    let mut rng = Rng::new(seed);
    let rows = collect(&mut rng, episodes, 0.25, MAX_STEPS, 0.15)?;
    let bounds = world_model_companion::cartpole::episode_bounds(&rows);
    let split = (bounds.len() * 8 / 10).max(1);
    let mut samples = Vec::new();
    for (begin, end) in bounds.iter().take(split) {
        // One real transition is enough to fit the delta target: (now, action) -> next.
        for index in *begin..end.saturating_sub(1) {
            samples.push((
                rows[index].visible,
                rows[index].action,
                rows[index + 1].visible,
            ));
        }
    }
    let model = fit_delta_model(&samples, 1e-6)?;

    let mut sums = vec![0.0f64; horizon];
    let mut frozen_sums = vec![0.0f64; horizon];
    let mut counts = vec![0usize; horizon];
    for (begin, end) in bounds.iter().skip(split) {
        let start = rows[*begin].visible;
        let available = end.saturating_sub(*begin);
        let actions: Vec<u8> = rows[*begin..*end].iter().map(|r| r.action).collect();
        let path = model.free_rollout(start, &actions)?;
        for depth in 1..=horizon.min(available) {
            let truth = if *begin + depth < rows.len() {
                rows[*begin + depth].visible
            } else {
                break;
            };
            let predicted = path[depth - 1];
            sums[depth - 1] += (predicted.pole_angle - truth.pole_angle).abs();
            frozen_sums[depth - 1] += (start.pole_angle - truth.pole_angle).abs();
            counts[depth - 1] += 1;
        }
    }

    let mut errors = Vec::new();
    let mut frozen = Vec::new();
    for index in 0..horizon {
        if counts[index] == 0 {
            errors.push(0.0);
            frozen.push(0.0);
        } else {
            errors.push(sums[index] / counts[index] as f64);
            frozen.push(frozen_sums[index] / counts[index] as f64);
        }
    }
    let beaten = errors
        .iter()
        .zip(frozen.iter())
        .filter(|(ours, base)| ours < base)
        .count();
    let (trust, first_failure) = world_model_companion::cartpole::trust_horizon(&errors, 0.02)?;
    Ok(format!(
        "{{\n  \"model\": \"linear one-step delta predictor (ridge {:.1e})\",\n  \"features\": 5,\n  \"train_samples\": {},\n  \"holdout_episodes\": {},\n  \"depth\": {},\n  \"pole_angle_rad\": {},\n  \"pole_angle_rad_frozen_baseline\": {},\n  \"tolerance_rad\": 0.02,\n  \"trust_horizon\": {},\n  \"first_depth_outside_tolerance\": {},\n  \"depths_beaten_by_frozen_baseline\": {},\n  \"limitation\": \"No memory, so the hidden velocities cannot be recovered; this is a lower bound on what the Python recurrent model can do, not a reproduction of it.\",\n  \"assessment\": \"not_assessed\"\n}}\n",
        model.ridge,
        model.samples,
        bounds.len().saturating_sub(split),
        json_array(&(1..=horizon).map(|d| d.to_string()).collect::<Vec<_>>()),
        json_array(&errors.iter().map(|v| format!("{v:.12}")).collect::<Vec<_>>()),
        json_array(&frozen.iter().map(|v| format!("{v:.12}")).collect::<Vec<_>>()),
        trust,
        match first_failure {
            Some(index) => (index + 1).to_string(),
            None => "null".to_string(),
        },
        beaten,
    ))
}

fn json_array(items: &[String]) -> String {
    format!("[{}]", items.join(", "))
}
