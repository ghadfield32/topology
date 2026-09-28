pub mod data;
pub mod datasets;
pub mod geometry;
pub mod labs;
pub mod learning;
pub mod math;
pub mod operators;
pub mod topology;
pub mod trace;
#[cfg(test)]
mod tests {
    use super::*;
    #[test]
    fn rank_fields() {
        let a = vec![vec![1., 1., 0.], vec![1., 0., 1.], vec![0., 1., 1.]];
        assert_eq!(math::rank(&a, 1e-10), 3);
        assert_eq!(math::rank2(&a), 2);
    }
    #[test]
    fn solve_control() {
        let r = math::solve(&vec![vec![2., 1.], vec![1., 3.]], &[5., 7.]);
        assert!((r[0] - 1.6).abs() < 1e-12 && (r[1] - 1.8).abs() < 1e-12);
    }
    #[test]
    fn square_persistence() {
        let x = vec![vec![0., 0.], vec![1., 0.], vec![1., 1.], vec![0., 1.]];
        let d = topology::persistence(&topology::rips(&x, f64::INFINITY, 2));
        let h = topology::dimension(&d, 1);
        assert_eq!(h.len(), 1);
        assert_eq!(h[0].birth, 1.);
        assert!((h[0].death.unwrap() - 2f64.sqrt()).abs() < 1e-12);
    }
    #[test]
    fn gradient() {
        let t = learning::Tape::new();
        let x = t.input(0.3);
        let y = t.tanh(x);
        let loss = t.mul(y, y);
        let g = t.back(loss);
        let v = 0.3f64.tanh();
        assert!((g[x] - 2. * v * (1. - v * v)).abs() < 1e-12);
    }
    #[test]
    #[should_panic]
    fn empty_mean_rejected() {
        math::mean_rows(&vec![]);
    }
}

#[cfg(test)]
mod acceptance_tests;
