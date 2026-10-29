//! WM09 — save a run nothing can quietly overwrite.
//!
//! A result that cannot be reproduced is not evidence. This rung defines the record a run
//! must keep, refuses to reuse a directory, and writes deterministic JSON by hand (no
//! crates, no map ordering surprises).
//!
//! Python sibling: `python/wm09_experiment.py`.

use std::fs;
use std::path::{Path, PathBuf};

/// The configuration of one run. Every field ends up in the saved record.
#[derive(Debug, Clone, Copy, PartialEq)]
pub struct RunConfig {
    pub seed: u64,
    pub episodes: usize,
    pub max_steps: usize,
    pub exploration: f64,
    pub bias_scale: f64,
    pub ridge: f64,
    pub horizon: usize,
    pub planning_horizon: usize,
    pub sequences: usize,
    pub topology_radius: f64,
    pub tolerance_m: f64,
    pub tolerance_rad: f64,
}

impl Default for RunConfig {
    fn default() -> Self {
        Self {
            seed: 0,
            episodes: 40,
            max_steps: 500,
            exploration: 0.25,
            bias_scale: 0.15,
            ridge: 1e-6,
            horizon: 12,
            planning_horizon: 5,
            sequences: 64,
            topology_radius: 0.15,
            tolerance_m: 0.05,
            tolerance_rad: 0.02,
        }
    }
}

/// Create a fresh output directory, refusing to reuse one.
///
/// A second run must never land on the first run's files. "It passed" is much easier to
/// believe when the record it points at cannot have been edited by a later run.
pub fn ensure_new_output(path: &Path) -> Result<PathBuf, String> {
    if path.exists() {
        return Err(format!(
            "{} already exists; choose a new output directory",
            path.display()
        ));
    }
    fs::create_dir_all(path).map_err(|error| error.to_string())?;
    Ok(path.to_path_buf())
}

/// Serialize one run as JSON, keyed by section, with stable ordering.
pub fn to_json(
    path: &Path,
    config: &RunConfig,
    sections: &[(&str, Vec<(String, String)>)],
) -> String {
    let mut fields: Vec<String> = Vec::new();
    fields.push(format!(
        "  \"output\": {}",
        json_string(&path.display().to_string())
    ));
    fields.push("  \"assessment\": \"not_assessed\"".to_string());
    fields.push(format!("  \"seed\": {}", config.seed));
    fields.push(format!("  \"episodes\": {}", config.episodes));
    fields.push(format!("  \"max_steps\": {}", config.max_steps));
    fields.push(format!("  \"exploration\": {:.6}", config.exploration));
    fields.push(format!("  \"bias_scale\": {:.6}", config.bias_scale));
    fields.push(format!("  \"ridge\": {:.12}", config.ridge));
    fields.push(format!("  \"horizon\": {}", config.horizon));
    fields.push(format!(
        "  \"planning_horizon\": {}",
        config.planning_horizon
    ));
    fields.push(format!("  \"sequences\": {}", config.sequences));
    fields.push(format!(
        "  \"topology_radius\": {:.6}",
        config.topology_radius
    ));
    fields.push(format!("  \"tolerance_m\": {:.6}", config.tolerance_m));
    fields.push(format!("  \"tolerance_rad\": {:.6}", config.tolerance_rad));

    let mut blocks: Vec<String> = Vec::new();
    for (name, entries) in sections {
        let inner = entries
            .iter()
            .map(|(key, value)| format!("      {}: {}", json_string(key), value))
            .collect::<Vec<_>>()
            .join(",\n");
        blocks.push(format!("    {}: {{\n{inner}\n    }}", json_string(name)));
    }
    if !blocks.is_empty() {
        fields.push(format!("  \"sections\": {{\n{}\n  }}", blocks.join(",\n")));
    }
    format!("{{\n{}\n}}\n", fields.join(",\n"))
}

/// Write the record into a directory the caller has already created.
///
/// The caller creates the directory exactly once, at the start of the run, so a refused run
/// costs nothing. Re-creating it here would either fail against its own earlier work or
/// silently accept a directory that already held a previous run's files.
pub fn write_into(
    prepared: &Path,
    config: &RunConfig,
    sections: &[(&str, Vec<(String, String)>)],
) -> Result<PathBuf, String> {
    if !prepared.is_dir() {
        return Err(format!(
            "{} is not an existing directory; call ensure_new_output first",
            prepared.display()
        ));
    }
    let body = to_json(prepared, config, sections);
    let file = prepared.join("results.json");
    if file.exists() {
        return Err(format!(
            "{} already exists; this run would overwrite a record",
            file.display()
        ));
    }
    fs::write(&file, body).map_err(|error| error.to_string())?;
    Ok(file)
}

fn json_string(value: &str) -> String {
    let escaped = value.replace('\\', "\\\\").replace('"', "\\\"");
    format!("\"{escaped}\"")
}

/// A number formatted for the record, so a caller cannot accidentally print a raw `f64`
/// with an unstable number of digits.
pub fn number(key: &str, value: f64) -> (String, String) {
    (key.to_string(), format!("{value:.9}"))
}

pub fn integer(key: &str, value: usize) -> (String, String) {
    (key.to_string(), value.to_string())
}

pub fn boolean(key: &str, value: bool) -> (String, String) {
    (key.to_string(), value.to_string())
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn a_second_run_cannot_reuse_the_first_directory() {
        let base = std::env::temp_dir().join(format!(
            "ladder_wm09_{}_{}",
            std::process::id(),
            std::time::SystemTime::now()
                .duration_since(std::time::UNIX_EPOCH)
                .expect("clock")
                .as_nanos()
        ));
        let created = ensure_new_output(&base).expect("first");
        assert_eq!(created, base);
        let kept = base.join("keep.txt");
        fs::write(&kept, "keep").expect("write");
        assert!(ensure_new_output(&base).is_err(), "reuse must be refused");
        assert_eq!(fs::read_to_string(&kept).expect("read"), "keep");
        fs::remove_dir_all(&base).ok();
    }

    #[test]
    fn the_record_contains_the_configuration_and_the_status() {
        let config = RunConfig::default();
        let text = to_json(
            Path::new("my_work/example"),
            &config,
            &[("one_step", vec![number("angle_rad", 0.001)])],
        );
        assert!(text.contains("\"assessment\": \"not_assessed\""));
        assert!(text.contains("\"seed\": 0"));
        assert!(text.contains("\"angle_rad\": 0.001000000"));
        assert!(text.contains("\"one_step\""));
    }

    #[test]
    fn string_values_are_escaped() {
        let text = to_json(Path::new("a\"b"), &RunConfig::default(), &[]);
        assert!(text.contains("a\\\"b"));
    }

    #[test]
    fn saving_writes_the_file_it_names() {
        let base = std::env::temp_dir().join(format!(
            "ladder_wm09_save_{}_{}",
            std::process::id(),
            std::time::SystemTime::now()
                .duration_since(std::time::UNIX_EPOCH)
                .expect("clock")
                .as_nanos()
        ));
        let prepared = ensure_new_output(&base).expect("prepare");
        let file = write_into(
            &prepared,
            &RunConfig::default(),
            &[("data", vec![integer("transitions", 42)])],
        )
        .expect("write");
        let text = fs::read_to_string(&file).expect("read");
        assert!(text.contains("\"transitions\": 42"));
        // A second write into the same run would overwrite the record.
        assert!(write_into(&prepared, &RunConfig::default(), &[]).is_err());
        // And writing into a directory that was never prepared is refused.
        let missing = base.join("never-created");
        assert!(write_into(&missing, &RunConfig::default(), &[]).is_err());
        fs::remove_dir_all(&base).ok();
    }

    #[test]
    fn preparing_once_and_writing_once_is_the_supported_sequence() {
        // Regression: an earlier version created the directory in both `prepare` and
        // `save`, so every real run failed against its own work. The two steps are now
        // separate and each is testable on its own.
        let base = std::env::temp_dir().join(format!(
            "ladder_wm09_seq_{}_{}",
            std::process::id(),
            std::time::SystemTime::now()
                .duration_since(std::time::UNIX_EPOCH)
                .expect("clock")
                .as_nanos()
        ));
        let prepared = ensure_new_output(&base).expect("prepare");
        assert!(!prepared.join("results.json").exists());
        let file = write_into(&prepared, &RunConfig::default(), &[]).expect("write");
        assert!(file.exists());
        fs::remove_dir_all(&base).ok();
    }
}
