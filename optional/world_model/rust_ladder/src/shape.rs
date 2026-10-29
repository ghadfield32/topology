//! WM08 — describe geometry, and say plainly what that description cannot do.
//!
//! This rung computes **H0 connected components** of a projected trajectory. It is a
//! genuinely smaller thing than the sibling crate's `H1` persistence, and the point of
//! starting here is that H0 is easy enough to check by hand.
//!
//! The lesson is a warning, not a result:
//!
//! > Point-cloud topology describes the *sampled geometry* of a trajectory and discards
//! > temporal direction. It cannot tell you whether the model predicts the next state.
//!
//! That is testable, not just assertable: reverse the trajectory, and the point set, the
//! distances and the component count are identical while the sequence of transitions has
//! been reversed. A descriptor that cannot see a reversal is not a dynamics check.
//!
//! Python sibling: `python/wm08_topology.py`.

use crate::state::{State, THETA_LIMIT, X_LIMIT};

/// A point in the normalized visible plane.
#[derive(Debug, Clone, Copy, PartialEq)]
pub struct Point {
    pub x: f64,
    pub theta: f64,
}

impl Point {
    pub fn distance(self, other: Point) -> f64 {
        let dx = self.x - other.x;
        let dy = self.theta - other.theta;
        (dx * dx + dy * dy).sqrt()
    }
}

/// Project a trajectory onto the two normalized visible numbers.
///
/// Both are divided by their own limits, so "1.0" means "at the failure boundary" on either
/// axis. Without that, distance mixes metres with radians.
pub fn project(states: &[State]) -> Vec<Point> {
    states
        .iter()
        .map(|state| Point {
            x: state.x / X_LIMIT,
            theta: state.theta / THETA_LIMIT,
        })
        .collect()
}

/// The 0-dimensional persistence of a point cloud: components that merge as the radius grows.
#[derive(Debug, Clone, PartialEq)]
pub struct H0 {
    /// Number of components at radius zero (one per distinct point).
    pub points: usize,
    /// Number of merges that happen below the final radius.
    pub merges: usize,
    /// Components still separate at the final radius.
    pub components: usize,
}

/// Count H0 components at a single radius, by union-find.
///
/// The radius is **part of the answer**: a different radius can give a different component
/// count, so a report that omits it is not reproducible.
pub fn h0_at_radius(points: &[Point], radius: f64) -> Result<H0, String> {
    if points.is_empty() {
        return Err("no points to analyse".to_string());
    }
    if !radius.is_finite() || radius < 0.0 {
        return Err("radius must be finite and nonnegative".to_string());
    }
    let n = points.len();
    let mut parent: Vec<usize> = (0..n).collect();

    fn find(parent: &mut [usize], mut node: usize) -> usize {
        while parent[node] != node {
            parent[node] = parent[parent[node]];
            node = parent[node];
        }
        node
    }

    let mut merges = 0usize;
    for i in 0..n {
        for j in (i + 1)..n {
            if points[i].distance(points[j]) <= radius {
                let left = find(&mut parent, i);
                let right = find(&mut parent, j);
                if left != right {
                    parent[left] = right;
                    merges += 1;
                }
            }
        }
    }
    let components = (0..n)
        .map(|node| find(&mut parent, node))
        .collect::<std::collections::BTreeSet<_>>()
        .len();
    Ok(H0 {
        points: n,
        merges,
        components,
    })
}

/// Reverse a trajectory.
///
/// Provided as a *lesson*, not a utility: it exists so a test can show that the topology
/// cannot tell the difference.
pub fn reversed(states: &[State]) -> Vec<State> {
    states.iter().rev().copied().collect()
}

#[cfg(test)]
mod tests {
    use super::*;
    use crate::state::State;

    fn trajectory() -> Vec<State> {
        vec![
            State::new(0.0, 0.0, 0.0, 0.0).expect("finite"),
            State::new(0.3, 0.0, 0.0, 0.0).expect("finite"),
            State::new(0.6, 0.0, 0.0, 0.0).expect("finite"),
            State::new(0.9, 0.0, 0.0, 0.0).expect("finite"),
        ]
    }

    #[test]
    fn projection_uses_both_limits() {
        let at_limits = State::new(X_LIMIT, 0.0, THETA_LIMIT, 0.0).expect("finite");
        let point = project(&[at_limits])[0];
        assert!((point.x - 1.0).abs() < 1e-15);
        assert!((point.theta - 1.0).abs() < 1e-15);
    }

    #[test]
    fn a_small_radius_leaves_every_point_alone() {
        let points = project(&trajectory());
        let result = h0_at_radius(&points, 0.001).expect("h0");
        assert_eq!(result.points, 4);
        assert_eq!(result.merges, 0);
        assert_eq!(result.components, 4);
    }

    #[test]
    fn a_large_radius_merges_everything() {
        let points = project(&trajectory());
        let result = h0_at_radius(&points, 10.0).expect("h0");
        assert_eq!(result.components, 1);
        assert_eq!(result.merges, 3, "n-1 merges to reach one component");
    }

    #[test]
    fn reversing_time_does_not_change_the_component_count() {
        // This is the whole lesson of WM08, as a test rather than a sentence.
        let forward = trajectory();
        let backward = reversed(&forward);
        let radius = 0.15;
        let a = h0_at_radius(&project(&forward), radius).expect("h0");
        let b = h0_at_radius(&project(&backward), radius).expect("h0");
        assert_eq!(a, b);
        assert_ne!(forward, backward, "the sequences really are different");
    }

    #[test]
    fn the_radius_is_part_of_the_answer() {
        let points = project(&trajectory());
        let tight = h0_at_radius(&points, 0.10).expect("h0");
        let loose = h0_at_radius(&points, 0.20).expect("h0");
        assert_ne!(
            tight.components, loose.components,
            "a component count without its radius is not reproducible"
        );
    }

    #[test]
    fn bad_inputs_are_errors() {
        assert!(h0_at_radius(&[], 0.1).is_err());
        let points = project(&trajectory());
        assert!(h0_at_radius(&points, -0.1).is_err());
        assert!(h0_at_radius(&points, f64::NAN).is_err());
    }

    #[test]
    fn duplicate_projected_points_merge_at_radius_zero() {
        let state = State::new(0.2, 0.0, 0.05, 0.0).expect("finite");
        let points = project(&[state, state]);
        let result = h0_at_radius(&points, 0.0).expect("h0");
        assert_eq!(result.merges, 1);
        assert_eq!(result.components, 1);
    }
}
