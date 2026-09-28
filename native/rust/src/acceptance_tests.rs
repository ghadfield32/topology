use crate::{geometry::*, learning::*, math::*, topology::*, trace::*};
fn near(a: f64, b: f64) {
    assert!(
        a.is_finite() && (a - b).abs() < 1e-9,
        "{a:0.17} != {b:0.17}"
    )
}
#[test]
fn matrix_invalid() {
    for a in [vec![vec![1.], vec![1., 2.]], vec![vec![f64::NAN]]] {
        assert!(std::panic::catch_unwind(|| shape(&a)).is_err())
    }
}
#[test]
fn singular_solve() {
    assert!(
        std::panic::catch_unwind(|| solve(&vec![vec![1., 2.], vec![2., 4.]], &[1., 2.])).is_err()
    )
}
#[test]
fn noninteger_f2() {
    assert!(std::panic::catch_unwind(|| rank2(&vec![vec![0.5]])).is_err())
}
#[test]
fn rank_preserves() {
    let a = vec![vec![1., 2.], vec![2., 4.]];
    let b = a.clone();
    assert_eq!(rank(&a, 1e-12), 1);
    assert_eq!(a, b)
}
#[test]
fn boundary_squared() {
    let a = matmul(
        &boundary_matrix(&triangle(true), 1),
        &boundary_matrix(&triangle(true), 2),
    );
    for r in a {
        for v in r {
            assert_eq!(v as i64 % 2, 0)
        }
    }
}
#[test]
fn betti_examples() {
    for (c, want) in [
        (triangle(false), vec![1, 1]),
        (triangle(true), vec![1, 0, 0]),
        (tetra(false), vec![1, 0, 1]),
        (tetra(true), vec![1, 0, 0, 0]),
    ] {
        assert_eq!(betti(&c), want)
    }
}
#[test]
fn invalid_complexes() {
    for c in [
        vec![Simplex {
            vertices: vec![0, 1],
            value: 0.,
        }],
        vec![Simplex {
            vertices: vec![0, 0],
            value: 0.,
        }],
        vec![
            Simplex {
                vertices: vec![0],
                value: 0.,
            },
            Simplex {
                vertices: vec![0],
                value: 0.,
            },
        ],
        vec![
            Simplex {
                vertices: vec![0],
                value: 1.,
            },
            Simplex {
                vertices: vec![1],
                value: 0.,
            },
            Simplex {
                vertices: vec![0, 1],
                value: 0.,
            },
        ],
    ] {
        assert!(std::panic::catch_unwind(|| ordered(&c)).is_err())
    }
}
#[test]
fn square_invariance() {
    let a = persistence(&rips(
        &vec![vec![0., 0.], vec![1., 0.], vec![1., 1.], vec![0., 1.]],
        2.,
        2,
    ));
    let b = persistence(&rips(
        &vec![vec![4., 6.], vec![4., 5.], vec![5., 5.], vec![5., 6.]],
        2.,
        2,
    ));
    assert_eq!(
        serde_json::to_value(a).unwrap(),
        serde_json::to_value(b).unwrap()
    )
}
#[test]
fn truncation() {
    let d = persistence(&rips(
        &vec![vec![0., 0.], vec![1., 0.], vec![1., 1.], vec![0., 1.]],
        1.,
        2,
    ));
    let h = dimension(&d, 1);
    assert_eq!(h.len(), 1);
    assert!(h[0].death.is_none())
}
#[test]
fn mst_h0() {
    let x = vec![vec![0., 0.], vec![0.7, 0.], vec![2., 1.], vec![3., 2.]];
    let d = persistence(&rips(&x, f64::INFINITY, 1));
    let got: Vec<_> = dimension(&d, 0).iter().filter_map(|v| v.death).collect();
    assert_eq!(got, mst(&x))
}
#[test]
fn bottleneck_diagonal() {
    let a = vec![Interval {
        dimension: 1,
        birth: 0.,
        death: Some(4.),
    }];
    near(bottleneck(&a, &[]), 2.);
    near(bottleneck(&a, &a), 0.)
}
#[test]
fn bottleneck_essential() {
    assert_eq!(
        bottleneck(
            &[Interval {
                dimension: 0,
                birth: 0.,
                death: None
            }],
            &[]
        ),
        f64::INFINITY
    )
}
#[test]
fn closed_pixels() {
    assert_eq!(pixel_betti(&[1., 0., 0., 1.], 2, 2, 0.5), vec![1, 0]);
    assert_eq!(
        pixel_betti(&[1., 1., 1., 1., 0., 1., 1., 1., 1.], 3, 3, 0.5),
        vec![1, 1]
    )
}
#[test]
fn train_only_scaler() {
    let s = Scaler::fit(&vec![vec![0., 2.], vec![2., 2.]]);
    let v = s.transform(&vec![vec![100., 2.]]);
    near(v[0][0], 99.);
    near(v[0][1], 0.)
}
#[test]
fn eigen_residual() {
    let a = vec![vec![3., 1.], vec![1., 3.]];
    let (v, q) = eigen_sym(&a);
    for k in 0..2 {
        for i in 0..2 {
            near((0..2).map(|j| a[i][j] * q[j][k]).sum(), v[k] * q[i][k])
        }
    }
}
#[test]
fn covariance_values() {
    let a = cov(&vec![vec![1., 2.], vec![2., 4.], vec![3., 6.]]);
    near(a[0][0], 1.);
    near(a[0][1], 2.);
    near(a[1][1], 4.)
}
#[test]
fn ad_composite() {
    for x in [-0.7, 0.1, 0.9] {
        let t = Tape::new();
        let v = t.input(x);
        let r = t.add(t.sin(v), t.log(t.exp(t.mul(v, v))));
        let g = t.back(r);
        near(g[v], x.cos() + 2. * x)
    }
}
#[test]
fn jets_parameter_second_derivative() {
    let t = Tape::new();
    let w = t.input(0.4);
    let x = jvar(&t, 0.7, true);
    let z = jtanh(
        &t,
        jmul(
            &t,
            Jet {
                v: w,
                d: t.input(0.),
                d2: t.input(0.),
            },
            x,
        ),
    );
    let u = 0.28f64.tanh();
    near(t.val(z.d), 0.4 * (1. - u * u));
    near(t.val(z.d2), -2. * 0.4 * 0.4 * u * (1. - u * u));
    let g = t.back(z.d2);
    let f = |w: f64| {
        let u = (w * 0.7).tanh();
        -2. * w * w * u * (1. - u * u)
    };
    near(g[w], (f(0.400001) - f(0.399999)) / 0.000002)
}
#[test]
fn gaussian_gradient() {
    let z = vec![vec![-0.2, 0.8], vec![0.3, -0.6], vec![1., 0.4]];
    let d = directions(2, 3, 7);
    let (_, g) = gaussian_penalty(&z, &d);
    for i in 0..3 {
        for j in 0..2 {
            let (mut a, mut b) = (z.clone(), z.clone());
            a[i][j] += 1e-6;
            b[i][j] -= 1e-6;
            near(
                g[i][j],
                (gaussian_penalty(&a, &d).0 - gaussian_penalty(&b, &d).0) / 2e-6,
            )
        }
    }
}
#[test]
fn ridge_linear() {
    let (w, b) = ridge(&vec![vec![-1.], vec![0.], vec![1.]], &[-1., 1., 3.], 0.);
    near(w[0], 2.);
    near(b, 1.)
}
#[test]
fn classifier_probability() {
    let c = Classifier::fit(
        &vec![vec![-2.], vec![-1.], vec![1.], vec![2.]],
        &[0, 0, 1, 1],
        200,
        0.15,
        0.01,
    );
    let (p, q) = c.predict(&vec![vec![-2.], vec![2.]]);
    assert_eq!(p, vec![0, 1]);
    for r in q {
        near(r[0] + r[1], 1.)
    }
}
#[test]
fn groups_disjoint() {
    let g: Vec<_> = ["a", "a", "b", "b", "c", "d", "e", "f", "g", "h"]
        .iter()
        .map(|s| s.to_string())
        .collect();
    let (a, b, c) = group_split(&g);
    let mut seen = std::collections::BTreeMap::new();
    let mut n = 0;
    for (p, ids) in [a, b, c].iter().enumerate() {
        n += ids.len();
        for &i in ids {
            if let Some(prev) = seen.insert(g[i].clone(), p) {
                assert_eq!(p, prev)
            }
        }
    }
    assert_eq!(n, g.len())
}

#[test]
fn reported_homology_dimension() {
    let x = vec![vec![0., 0.], vec![1., 0.], vec![1., 1.], vec![0., 1.]];
    let d = persistence(&rips(&x, 2., 2));
    let r = report_h01(&d);
    assert!(r.iter().all(|v| v.dimension <= 1));
    assert!(r.len() < d.len());
}
