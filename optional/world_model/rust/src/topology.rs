//! Read the committed fixture and report the same shape summary Python reports.
//!
//! The JSON parser is deliberately tiny: this crate has no dependencies, and the
//! fixture is a small machine-written document. Parsing is strict — an unexpected
//! field type is an error rather than a silently skipped array — because a fixture
//! that cannot be read faithfully is not a comparison.

use std::path::Path;

use crate::persistence::{summarize, DiagramSummary};

/// One fixture: the points and the truncation scale they should be read at.
#[derive(Debug, Clone, PartialEq)]
pub struct Fixture {
    pub name: String,
    pub max_edge: f64,
    pub points: Vec<[f64; 2]>,
}

/// Read and summarize the fixture at its own declared scale.
pub fn check(path: &Path) -> Result<DiagramSummary, String> {
    let fixture = load(path)?;
    summarize(&fixture.points, fixture.max_edge)
}

pub fn load(path: &Path) -> Result<Fixture, String> {
    let text = std::fs::read_to_string(path)
        .map_err(|error| format!("cannot read {}: {error}", path.display()))?;
    parse(&text)
}

/// Minimal strict parser for `{ "name": str, "max_edge": num, "points": [[num, num], ...] }`.
pub fn parse(text: &str) -> Result<Fixture, String> {
    let name = parse_string_field(text, "name")?;
    let max_edge = parse_number_field(text, "max_edge")?;
    let points = parse_points(text)?;
    if points.is_empty() {
        return Err("fixture contains no points".to_string());
    }
    if !max_edge.is_finite() || max_edge <= 0.0 {
        return Err("fixture max_edge must be finite and positive".to_string());
    }
    Ok(Fixture {
        name,
        max_edge,
        points,
    })
}

fn value_start(text: &str, key: &str) -> Result<usize, String> {
    let needle = format!("\"{key}\"");
    let at = text
        .find(&needle)
        .ok_or_else(|| format!("fixture is missing \"{key}\""))?;
    let after = at + needle.len();
    let colon = text[after..]
        .find(':')
        .ok_or_else(|| format!("fixture has no value for \"{key}\""))?;
    Ok(after + colon + 1)
}

fn parse_string_field(text: &str, key: &str) -> Result<String, String> {
    let start = value_start(text, key)?;
    let rest = &text[start..];
    let open = rest.find('"').ok_or("expected a quoted string")?;
    let body = &rest[open + 1..];
    let close = body.find('"').ok_or("unterminated string")?;
    Ok(body[..close].to_string())
}

fn parse_number_field(text: &str, key: &str) -> Result<f64, String> {
    let start = value_start(text, key)?;
    let rest = text[start..].trim_start();
    let end = rest
        .find(|c: char| !(c.is_ascii_digit() || matches!(c, '-' | '+' | '.' | 'e' | 'E')))
        .unwrap_or(rest.len());
    rest[..end]
        .trim()
        .parse::<f64>()
        .map_err(|error| format!("cannot parse \"{key}\" as a number: {error}"))
}

fn parse_points(text: &str) -> Result<Vec<[f64; 2]>, String> {
    let start = value_start(text, "points")?;
    let rest = &text[start..];
    let open = rest.find('[').ok_or("points must be an array")?;
    let mut depth = 0usize;
    let mut end = None;
    for (offset, character) in rest[open..].char_indices() {
        match character {
            '[' => depth += 1,
            ']' => {
                depth -= 1;
                if depth == 0 {
                    end = Some(open + offset);
                    break;
                }
            }
            _ => {}
        }
    }
    let end = end.ok_or("unterminated points array")?;
    let body = &rest[open..=end];

    let mut points = Vec::new();
    let mut pair: Vec<f64> = Vec::new();
    let mut depth = 0usize;
    let mut number = String::new();
    for character in body.chars() {
        match character {
            '[' => {
                depth += 1;
                if depth == 2 {
                    pair.clear();
                }
            }
            ']' => {
                if depth == 2 {
                    push_number(&mut pair, &mut number)?;
                    if pair.len() != 2 {
                        return Err(format!("expected a 2-D point, got {pair:?}"));
                    }
                    points.push([pair[0], pair[1]]);
                }
                depth = depth.saturating_sub(1);
            }
            ',' | ' ' | '\n' | '\r' | '\t' => {
                if depth == 2 {
                    push_number(&mut pair, &mut number)?;
                }
            }
            other => {
                if depth == 2 {
                    number.push(other);
                }
            }
        }
    }
    Ok(points)
}

fn push_number(pair: &mut Vec<f64>, number: &mut String) -> Result<(), String> {
    if number.trim().is_empty() {
        return Ok(());
    }
    let parsed = number
        .trim()
        .parse::<f64>()
        .map_err(|error| format!("cannot parse coordinate {number:?}: {error}"))?;
    pair.push(parsed);
    number.clear();
    Ok(())
}

#[cfg(test)]
mod tests {
    use super::*;

    const DOC: &str = r#"{
 "name": "tiny",
 "max_edge": 1.5,
 "points": [[0.0, 0.0], [1.0, 0.0], [0.0, 1.0]]
}"#;

    #[test]
    fn parses_the_fixture_shape() {
        let fixture = parse(DOC).expect("parse");
        assert_eq!(fixture.name, "tiny");
        assert!((fixture.max_edge - 1.5).abs() < 1e-15);
        assert_eq!(fixture.points.len(), 3);
        assert_eq!(fixture.points[1], [1.0, 0.0]);
    }

    #[test]
    fn a_missing_field_is_an_error() {
        assert!(parse(r#"{"name":"x","points":[[0.0,0.0]]}"#).is_err());
        assert!(parse(r#"{"max_edge":1.0,"points":[[0.0,0.0]]}"#).is_err());
    }

    #[test]
    fn a_non_two_dimensional_point_is_rejected() {
        assert!(parse(r#"{"name":"x","max_edge":1.0,"points":[[0.0,0.0,0.0]]}"#).is_err());
    }

    #[test]
    fn an_empty_cloud_is_rejected() {
        assert!(parse(r#"{"name":"x","max_edge":1.0,"points":[]}"#).is_err());
    }

    #[test]
    fn the_committed_fixture_reproduces_a_real_loop() {
        let path = Path::new(env!("CARGO_MANIFEST_DIR")).join("../fixtures/points.json");
        let summary = check(&path).expect("fixture must parse and reduce");
        assert_eq!(summary.h0_finite, 23);
        assert_eq!(summary.h1_finite, 2);
        assert_eq!(summary.h1_essential, 0);
        assert!((summary.h1_total_persistence - 0.5555447016192441).abs() < 1e-9);
    }
}
