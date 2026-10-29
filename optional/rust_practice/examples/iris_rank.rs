//! A real-data route: measure what appending a dependent feature does to Iris rank.
//!
//! Run from the crate directory:
//!
//! ```text
//! cargo run --offline --release --example iris_rank -- ../../../data/raw/iris.csv
//! ```
//!
//! The input is the course's own `data/raw/iris.csv`. Only the four numeric measurements are
//! used; `sample_id`, `label` and `species` are ignored here. The observation unit is one
//! flower, so the rows are not independent draws from a designed experiment — a limitation
//! printed with the result rather than buried in this comment.

use std::env;
use std::fs;
use std::process::ExitCode;

use rust_practice::{
    append_feature, dependent_feature_kernel, max_abs_row_product, rank, rank_with_feature,
};

const TOLERANCE: f64 = 1e-9;

fn parse_iris(text: &str) -> Result<Vec<[f64; 4]>, String> {
    let mut rows = Vec::new();
    for (index, line) in text.lines().enumerate() {
        let line = line.trim();
        if line.is_empty() {
            continue;
        }
        let cells: Vec<&str> = line.split(',').collect();
        if index == 0 && cells.get(1) == Some(&"sepal_length_cm") {
            continue; // header
        }
        if cells.len() < 5 {
            return Err(format!("line {}: expected at least 5 columns", index + 1));
        }
        let mut row = [0.0_f64; 4];
        for (slot, cell) in row.iter_mut().zip(&cells[1..5]) {
            *slot = cell
                .trim()
                .parse::<f64>()
                .map_err(|_| format!("line {}: `{cell}` is not a number", index + 1))?;
        }
        rows.push(row);
    }
    if rows.is_empty() {
        return Err("no observation rows found".into());
    }
    Ok(rows)
}

fn main() -> ExitCode {
    let path = env::args()
        .nth(1)
        .unwrap_or_else(|| "../../../data/raw/iris.csv".to_string());
    let text = match fs::read_to_string(&path) {
        Ok(t) => t,
        Err(error) => {
            eprintln!("cannot read {path}: {error}");
            return ExitCode::FAILURE;
        }
    };
    let rows = match parse_iris(&text) {
        Ok(r) => r,
        Err(error) => {
            eprintln!("{path}: {error}");
            return ExitCode::FAILURE;
        }
    };

    let (a, b) = (2.0, -3.0);
    let widened = match append_feature(&rows, a, b) {
        Ok(w) => w,
        Err(error) => {
            eprintln!("append_feature rejected the table: {error}");
            return ExitCode::FAILURE;
        }
    };

    let as_vec: Vec<Vec<f64>> = rows.iter().map(|r| r.to_vec()).collect();
    let base_rank = rank(&as_vec, TOLERANCE).expect("validated rows");
    let (before, after) = rank_with_feature(&as_vec, a, b, TOLERANCE).expect("validated rows");
    assert_eq!(before, base_rank, "the two rank paths must agree");

    let kernel = dependent_feature_kernel(a, b).expect("finite coefficients");
    let worst = max_abs_row_product(&widened, &kernel).expect("finite products");

    println!("input                 {path}");
    println!("rows                  {}", rows.len());
    println!("columns before/after  {}/{}", 4, 5);
    println!("appended column       {a}*x0 + {b}*x1");
    println!("tolerance             {TOLERANCE:e}");
    println!("rank before           {base_rank}");
    println!("rank after            {after}");
    println!("max |row . kernel|    {worst:e}");
    println!(
        "dependent column      {}",
        if after == base_rank {
            "did not increase rank, as the algebra requires"
        } else {
            "INCREASED RANK -- investigate"
        }
    );
    println!();
    println!("Scope: numerical rank of a measured flower table under one tolerance.");
    println!("A rank result says nothing about the biology, the sampling design or the");
    println!("predictive value of these measurements.");

    if after == base_rank {
        ExitCode::SUCCESS
    } else {
        ExitCode::FAILURE
    }
}
