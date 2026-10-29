//! An independent F2 persistence reduction, so the Python diagram is checked.
//!
//! This is a second implementation of the *same* algorithm the course already owns in
//! `src/shape_lab/persistence.py`: enumerate simplices, order them by filtration value
//! with a deterministic tie order, then reduce boundary columns by symmetric
//! difference and pair each pivot. It is written from the definition rather than
//! translated line by line, which is the only reason agreeing with Python means
//! anything.
//!
//! Conventions, stated so the comparison is fair:
//! * coefficients are `F2`; a column is a set of row indices;
//! * ties are ordered by `(value, dimension, sorted vertex tuple)`, matching the
//!   Python `ordered_filtration` key exactly;
//! * a filtration is truncated at a maximum edge length, and a surviving bar is
//!   reported as essential rather than silently dropped.

use std::collections::{BTreeMap, BTreeSet, HashMap};

/// One simplex with its entry time. Vertices are sorted distinct indices.
#[derive(Debug, Clone, PartialEq)]
pub struct Simplex {
    pub vertices: Vec<usize>,
    pub value: f64,
}

impl Simplex {
    pub fn dimension(&self) -> usize {
        self.vertices.len() - 1
    }
}

/// A persistent homology bar. `death` of `None` means it survived the truncation.
#[derive(Debug, Clone, Copy, PartialEq)]
pub struct Interval {
    pub dimension: usize,
    pub birth: f64,
    pub death: Option<f64>,
}

impl Interval {
    pub fn persistence(&self) -> f64 {
        match self.death {
            Some(death) => (death - self.birth).max(0.0),
            None => f64::INFINITY,
        }
    }
}

/// Summary counts, so a caller never has to re-derive them inconsistently.
#[derive(Debug, Clone, PartialEq)]
pub struct DiagramSummary {
    pub simplex_count: usize,
    pub h0_finite: usize,
    pub h1_finite: usize,
    pub h1_essential: usize,
    pub h1_total_persistence: f64,
    pub h1_max_persistence: f64,
    pub max_edge: f64,
}

/// Euclidean distance in the plane. The course's Rips convention is Euclidean, and
/// this function is the only place the metric is defined.
pub fn distance(a: [f64; 2], b: [f64; 2]) -> f64 {
    ((a[0] - b[0]).powi(2) + (a[1] - b[1]).powi(2)).sqrt()
}

/// Build a Rips filtration through dimension `largest_dimension + 1`.
///
/// Building one dimension higher than the homology you intend to read is what allows
/// bars in the top dimension to die. Reporting H1 from a 2-simplex-only complex would
/// report every loop as essential, which is a truncation artefact, not a measurement.
pub fn rips_filtration(
    points: &[[f64; 2]],
    largest_dimension: usize,
    max_edge: f64,
) -> Result<Vec<Simplex>, String> {
    if points.is_empty() {
        return Err("provide at least one point".to_string());
    }
    if points
        .iter()
        .any(|p| !p[0].is_finite() || !p[1].is_finite())
    {
        return Err("points must be finite".to_string());
    }
    if !max_edge.is_finite() || max_edge <= 0.0 {
        return Err("max_edge must be finite and positive".to_string());
    }
    if largest_dimension > 2 {
        return Err("this educational enumerator supports at most dimension 2".to_string());
    }

    let mut simplices = Vec::new();
    for index in 0..points.len() {
        simplices.push(Simplex {
            vertices: vec![index],
            value: 0.0,
        });
    }
    let mut pairwise = vec![vec![0.0f64; points.len()]; points.len()];
    for i in 0..points.len() {
        for j in 0..points.len() {
            pairwise[i][j] = distance(points[i], points[j]);
        }
    }

    // Enumerate increasing vertex tuples; every face is generated before its coface
    // because a face has fewer vertices.
    let mut current: Vec<Vec<usize>> = (0..points.len()).map(|i| vec![i]).collect();
    for size in 2..=(largest_dimension + 2).min(points.len()) {
        let _ = size;
        let mut next = Vec::new();
        for seed in &current {
            let tail_begin = seed.last().copied().unwrap_or(0) + 1;
            for extension in tail_begin..points.len() {
                let mut vertices = seed.clone();
                vertices.push(extension);
                let value = max_pairwise(&vertices, &pairwise);
                // A simplex above the truncation scale is not part of the complex.
                if value <= max_edge {
                    simplices.push(Simplex {
                        vertices: vertices.clone(),
                        value,
                    });
                    next.push(vertices);
                }
            }
        }
        current = next;
        if current.is_empty() {
            break;
        }
    }
    simplices.sort_by(order_key);
    Ok(simplices)
}

fn max_pairwise(vertices: &[usize], pairwise: &[Vec<f64>]) -> f64 {
    let mut value: f64 = 0.0;
    for i in 0..vertices.len() {
        for j in i + 1..vertices.len() {
            let d = pairwise[vertices[i]][vertices[j]];
            if d > value {
                value = d;
            }
        }
    }
    value
}

/// The tie order is part of the algorithm, not an implementation detail: it decides
/// which simplex is the death of a bar when two enter at the same value.
fn order_key(a: &Simplex, b: &Simplex) -> std::cmp::Ordering {
    a.value
        .partial_cmp(&b.value)
        .unwrap_or(std::cmp::Ordering::Equal)
        .then_with(|| a.vertices.len().cmp(&b.vertices.len()))
        .then_with(|| a.vertices.cmp(&b.vertices))
}

/// Reduce boundary columns over F2 and read off the bars.
///
/// The reduction is the textbook one: a column is the set of row indices of its facets.
/// While its lowest row is already owned by another column, add that column's support
/// (symmetric difference, which is addition in F2).
///
/// `include_zero = false` matches the Python reference's default reporting policy: a
/// bar whose birth equals its death is not a feature, it is a simplex pair. Including
/// those by accident is the simplest way to report three loops where there is one.
pub fn persistent_homology(
    simplices: &[Simplex],
    max_dimension: usize,
    include_zero: bool,
) -> Result<Vec<Interval>, String> {
    let index: HashMap<&[usize], usize> = simplices
        .iter()
        .enumerate()
        .map(|(i, s)| (s.vertices.as_slice(), i))
        .collect();
    if index.len() != simplices.len() {
        return Err("duplicate simplices are not permitted".to_string());
    }
    // Every face must be present, or the "boundary" is not a boundary of anything.
    for simplex in simplices {
        if simplex.vertices.len() > 1 {
            for dropped in 0..simplex.vertices.len() {
                let mut facet = simplex.vertices.clone();
                facet.remove(dropped);
                if !index.contains_key(facet.as_slice()) {
                    return Err(format!("missing face {facet:?} of {:?}", simplex.vertices));
                }
            }
        }
    }

    let mut reduced: Vec<BTreeSet<usize>> = Vec::with_capacity(simplices.len());
    let mut low_to_column: BTreeMap<usize, usize> = BTreeMap::new();
    for (column_index, simplex) in simplices.iter().enumerate() {
        let mut column: BTreeSet<usize> = if simplex.vertices.len() > 1 {
            (0..simplex.vertices.len())
                .map(|dropped| {
                    let mut facet = simplex.vertices.clone();
                    facet.remove(dropped);
                    *index.get(facet.as_slice()).expect("faces validated above")
                })
                .collect()
        } else {
            BTreeSet::new()
        };
        while let Some(low) = column.iter().next_back().copied() {
            match low_to_column.get(&low) {
                Some(&owner) => {
                    let previous = reduced[owner].clone();
                    column = column.symmetric_difference(&previous).copied().collect();
                }
                None => break,
            }
        }
        if let Some(low) = column.iter().next_back().copied() {
            low_to_column.insert(low, column_index);
        }
        reduced.push(column);
    }

    let mut intervals = Vec::new();
    for (birth_index, column) in reduced.iter().enumerate() {
        if !column.is_empty() {
            continue;
        }
        let simplex = &simplices[birth_index];
        let dimension = simplex.dimension();
        if dimension > max_dimension {
            continue;
        }
        let death = low_to_column.get(&birth_index).map(|&j| simplices[j].value);
        if !include_zero && death.map(|d| d <= simplex.value).unwrap_or(false) {
            // A zero-length bar is a simplex pair, not a feature.
            continue;
        }
        intervals.push(Interval {
            dimension,
            birth: simplex.value,
            death,
        });
    }
    intervals.sort_by(|a, b| {
        a.dimension
            .cmp(&b.dimension)
            .then(
                a.birth
                    .partial_cmp(&b.birth)
                    .unwrap_or(std::cmp::Ordering::Equal),
            )
            .then(
                a.death
                    .unwrap_or(f64::INFINITY)
                    .partial_cmp(&b.death.unwrap_or(f64::INFINITY))
                    .unwrap_or(std::cmp::Ordering::Equal),
            )
    });
    Ok(intervals)
}

/// Count and measure H0/H1 of a point cloud at one truncation scale.
pub fn summarize(points: &[[f64; 2]], max_edge: f64) -> Result<DiagramSummary, String> {
    if points.len() < 3 {
        return Err("at least three points are needed for a nontrivial H1".to_string());
    }
    let simplices = rips_filtration(points, 1, max_edge)?;
    let intervals = persistent_homology(&simplices, 1, false)?;
    let h0_finite = intervals
        .iter()
        .filter(|i| i.dimension == 0 && i.death.is_some())
        .count();
    let h1: Vec<&Interval> = intervals.iter().filter(|i| i.dimension == 1).collect();
    let h1_finite = h1.iter().filter(|i| i.death.is_some()).count();
    let h1_essential = h1.len() - h1_finite;
    let h1_total: f64 = h1
        .iter()
        .filter(|i| i.death.is_some())
        .map(|i| i.persistence())
        .sum();
    let h1_max = h1
        .iter()
        .filter(|i| i.death.is_some())
        .map(|i| i.persistence())
        .fold(0.0f64, f64::max);
    Ok(DiagramSummary {
        simplex_count: simplices.len(),
        h0_finite,
        h1_finite,
        h1_essential,
        h1_total_persistence: h1_total,
        h1_max_persistence: h1_max,
        max_edge,
    })
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn a_triangle_reports_no_loop_because_birth_and_fill_coincide() {
        // This is the honest answer and it surprises people: the third edge of a
        // triangle arrives at the hypotenuse length, and the 2-simplex that fills the
        // loop arrives at the *same* length. The bar has zero persistence, so the
        // default reporting policy excludes it. Python's diagram agrees exactly.
        let points = [[0.0, 0.0], [1.0, 0.0], [0.0, 1.0]];
        let hollow = summarize(&points, 1.01).expect("summary");
        assert_eq!(hollow.h0_finite, 2);
        assert_eq!(
            hollow.h1_essential, 0,
            "the cycle never closes below the hypotenuse"
        );
        assert_eq!(hollow.h1_finite, 0);

        let filled = summarize(&points, 1.5).expect("summary");
        assert_eq!(filled.h0_finite, 2);
        assert_eq!(
            filled.h1_finite, 0,
            "the loop is born and filled at the same value"
        );
        assert_eq!(filled.h1_essential, 0);
    }

    #[test]
    fn two_points_are_not_enough_for_a_loop() {
        assert!(summarize(&[[0.0, 0.0], [1.0, 0.0]], 1.0).is_err());
    }

    #[test]
    fn missing_faces_are_rejected_not_repaired() {
        let broken = vec![
            Simplex {
                vertices: vec![0],
                value: 0.0,
            },
            Simplex {
                vertices: vec![1],
                value: 0.0,
            },
            Simplex {
                vertices: vec![0, 1],
                value: 1.0,
            },
            Simplex {
                vertices: vec![0, 1, 2],
                value: 2.0,
            },
        ];
        assert!(persistent_homology(&broken, 1, false).is_err());
    }

    #[test]
    fn duplicate_simplices_are_rejected() {
        let duplicated = vec![
            Simplex {
                vertices: vec![0],
                value: 0.0,
            },
            Simplex {
                vertices: vec![0],
                value: 0.0,
            },
        ];
        assert!(persistent_homology(&duplicated, 0, false).is_err());
    }

    #[test]
    fn a_square_at_one_scale_is_a_loop_and_at_another_is_filled() {
        let square = [[0.0, 0.0], [1.0, 0.0], [1.0, 1.0], [0.0, 1.0]];
        let ring = summarize(&square, 1.5).expect("summary");
        assert_eq!(ring.h1_finite, 1, "the diagonal fills it eventually");
        let tight = summarize(&square, 1.001).expect("summary");
        assert_eq!(
            tight.h1_essential, 1,
            "before the diagonal, the cycle survives"
        );
    }

    #[test]
    fn truncation_scale_is_reported_with_the_answer() {
        let points = [[0.0, 0.0], [1.0, 0.0], [0.0, 1.0]];
        let summary = summarize(&points, 1.01).expect("summary");
        assert!((summary.max_edge - 1.01).abs() < 1e-15);
        assert!(summarize(&points, 0.0).is_err());
    }

    #[test]
    fn tie_order_is_deterministic() {
        let points = [[0.0, 0.0], [1.0, 0.0], [1.0, 1.0], [0.0, 1.0]];
        let a = summarize(&points, 2.0).expect("summary");
        let b = summarize(&points, 2.0).expect("summary");
        assert_eq!(a, b);
    }
}
