//! Explicit experiments: every registered unit dispatches to native numerical work.
use crate::{data::*, datasets::*, geometry::*, learning::*, math::*, operators::*, topology::*};
use serde_json::{json, Value};
use std::collections::{BTreeMap, BTreeSet};
fn core_points(repo: &str) -> Matrix {
    let x = iris(repo);
    Scaler::fit(&x[..90].to_vec()).transform(&x[..24].to_vec())
}
fn square() -> Matrix {
    vec![vec![0., 0.], vec![1., 0.], vec![1., 1.], vec![0., 1.]]
}
fn digit(repo: &str) -> Vec<f64> {
    let (x, _, tr, _, _) = digit_data(repo);
    x[tr[0]].clone()
}
pub fn centroid_bridge(repo: &str) -> Value {
    let (x, _, _) = spl(repo);
    let whole = mean_rows(&x);
    let a = mean_rows(&x[..1].to_vec());
    let b = mean_rows(&x[1..].to_vec());
    let weighted: Vec<f64> = (0..3)
        .map(|j| (a[j] + (x.len() - 1) as f64 * b[j]) / x.len() as f64)
        .collect();
    let equal: Vec<f64> = (0..3).map(|j| (a[j] + b[j]) / 2.).collect();
    let mut rev = x.clone();
    rev.reverse();
    json!({"rows":x.len(),"centroid_m":whole,"weighted_centroid_m":weighted,"equal_chunk_centroid_m":equal,"equal_chunk_displacement_m":distance(&whole,&equal),"order_reversal_error":distance(&whole,&mean_rows(&rev)),"scope":"selected nonuniform rows, not time average, release point, or static LiDAR scan"})
}
pub fn whiten(x: &Matrix) -> Value {
    let mu = mean_rows(x);
    let covariance = cov(x);
    let (eig, v) = eigen_sym(&covariance);
    let keep: Vec<usize> = eig
        .iter()
        .enumerate()
        .filter(|(_, e)| **e > 1e-8)
        .map(|(i, _)| i)
        .collect();
    require(!keep.is_empty(), "zero covariance rank");
    let mut out = zeros(x.len(), keep.len());
    for (i, row) in x.iter().enumerate() {
        for (q, k) in keep.iter().enumerate() {
            for j in 0..row.len() {
                out[i][q] += (row[j] - mu[j]) * v[j][*k] / eig[*k].sqrt();
            }
        }
    }
    json!({"mean":mu,"covariance":covariance,"eigenvalues":eig,"retained_components":keep,"whitened_covariance":cov(&out),"whitened":out,"scope":"nonzero covariance directions only; whitening is not Gaussianity or semantic quality"})
}
pub fn representation_training(repo: &str) -> Value {
    let (x, y, tr, va, te) = digit_data(repo);
    let mut scaled = x.clone();
    for row in &mut scaled {
        for v in row {
            *v /= 16.;
        }
    }
    let mut runs = vec![];
    for seed in [11, 23] {
        for regularized in [false, true] {
            let (e, h) = train_encoder(&rows(&scaled, &tr), seed, regularized);
            let (_, z) = e.forward(&scaled);
            let mut r = fit_predict(&z, &y, &tr, &va, &te);
            r["seed"] = json!(seed);
            r["regularized"] = json!(regularized);
            r["encoder_loss"] = json!(h);
            r["encoder_weights"] = json!(e);
            r["training_embedding_covariance"] = json!(cov(&rows(&z, &tr)));
            runs.push(r);
        }
    }
    json!({"train_rows":tr,"validation_rows":va,"test_rows":te,"pixel_baseline":fit_predict(&x,&y,&tr,&va,&te),"runs":runs,"protocol":"native16 64-16-8 tanh encoder;8 epochs;batch64;SGD.08;fixed projected CF penalty;fixed linear probe","scope":"new exposed image-level teaching protocol; not LeJEPA reproduction or athlete generalization"})
}
pub fn loss_controls() -> Value {
    let a = vec![vec![1., 0.], vec![0., 1.], vec![-1., 0.], vec![0., -1.]];
    let b = vec![
        vec![0.9, 0.1],
        vec![0.1, 0.9],
        vec![-0.9, -0.1],
        vec![-0.1, -0.9],
    ];
    let mut inv = 0.;
    for i in 0..4 {
        for j in 0..2 {
            inv += (a[i][j] - b[i][j]) * (a[i][j] - b[i][j]) / 8.;
        }
    }
    let (mut variance, mut covpen) = (0., 0.);
    for c in [cov(&a), cov(&b)] {
        for i in 0..c.len() {
            variance += (1. - (c[i][i] + 1e-4).sqrt()).max(0.) / 4.;
            for j in 0..c.len() {
                if i != j {
                    covpen += c[i][j] * c[i][j] / 4.;
                }
            }
        }
    }
    let (p, g) = gaussian_penalty(&zeros(8, 2), &directions(2, 4, 55));
    let flat: Vec<f64> = g.into_iter().flatten().collect();
    json!({"invariance_mse":inv,"variance_hinge":variance,"offdiagonal_covariance_penalty":covpen,"collapsed_projection_penalty":p,"collapsed_gradient_norm":norm(&flat),"scope":"finite objective controls; positive penalty can have zero gradient at collapse"})
}
pub fn leakage(repo: &str) -> Value {
    let (x, y, _) = classification_data(repo, "seeds");
    let z = Scaler::fit(&x).transform(&x);
    let (mut copies, mut labs, mut groups) = (vec![], vec![], vec![]);
    for i in 0..z.len() {
        for _ in 0..3 {
            copies.push(z[i].clone());
            labs.push(y[i]);
            groups.push(i.to_string());
        }
    }
    let mut idx: Vec<usize> = (0..copies.len()).collect();
    shuffle(&mut idx, 54);
    let (tr, te) = (&idx[..idx.len() * 7 / 10], &idx[idx.len() * 7 / 10..]);
    let (gtr, _, gte) = group_split(&groups);
    let score = |a: &[usize], b: &[usize]| -> Value {
        let set: BTreeSet<String> = a.iter().map(|i| groups[*i].clone()).collect();
        let mut p = vec![];
        let mut overlap = 0;
        for &i in b {
            let mut best = a[0];
            for &j in a {
                if distance(&copies[i], &copies[j]) < distance(&copies[i], &copies[best]) {
                    best = j;
                }
            }
            p.push(labs[best]);
            if set.contains(&groups[i]) {
                overlap += 1;
            }
        }
        json!({"test_rows":b,"predictions":p,"truth":labels(&labs,b),"accuracy":accuracy(&labels(&labs,b),&p),"shared_source_test_rows":overlap})
    };
    json!({"observed_kernels":x.len(),"constructed_rows":copies.len(),"row_split":score(tr,te),"source_group_split":score(&gtr,&gte),"scope":"intentional copied-row leakage demonstration; scaler fit globally to isolate duplication, not a valid evaluation protocol"})
}
fn finite_topologies() -> Value {
    let mut count = 0;
    for family in 0usize..256 {
        if family & 1 == 0 || family & 128 == 0 {
            continue;
        }
        let mut good = true;
        for a in 0..8 {
            if family & (1 << a) == 0 {
                continue;
            }
            for b in 0..8 {
                if family & (1 << b) == 0 {
                    continue;
                }
                if family & (1 << (a | b)) == 0 || family & (1 << (a & b)) == 0 {
                    good = false;
                }
            }
        }
        if good {
            count += 1;
        }
    }
    json!({"three_point_topologies":count,"domain":"all 256 candidate collections of subsets of a labeled three-element set","identity_map_indiscrete_to_discrete_continuous":false,"identity_map_discrete_to_indiscrete_continuous":true})
}
pub fn native_lab(repo: &str, key: &str) -> Value {
    match key {
        "stage00" => {
            let (x, y, features) = classification_data(repo, "seeds");
            let unique: BTreeSet<String> = x.iter().map(|r| format!("{r:?}")).collect();
            let mut counts: BTreeMap<String, usize> = BTreeMap::new();
            for v in y {
                *counts.entry(v.to_string()).or_default() += 1;
            }
            json!({"observations":x.len(),"features":features,"distinct_vectors":unique.len(),"label_counts":counts,"column_means":mean_rows(&x),"scope":"observed kernels; feature rows are not photographs"})
        }
        "stage01" => {
            let x = iris(repo);
            let centered = Scaler::fit(&x).transform(&x);
            let mut aug = x.clone();
            for i in 0..aug.len() {
                aug[i].push(2. * x[i][0] - 3. * x[i][1]);
            }
            let a = vec![vec![1., 1., 0.], vec![1., 0., 1.], vec![0., 1., 1.]];
            let kernel = [-2., 3., 0., 0., 1.];
            let residual = matvec(&aug, &kernel)
                .iter()
                .map(|v| v.abs())
                .fold(0., f64::max);
            json!({"real_rank":rank(&a,1e-10),"f2_rank":rank2(&a),"iris_rank":rank(&x,1e-10),"centered_scaled_rank":rank(&centered,1e-10),"augmented_rank":rank(&aug,1e-10),"known_kernel":kernel,"kernel_residual_max":residual,"finite_preimage_of_square_1_to_9":[-3,-2,-1,1,2,3]})
        }
        "stage02" => {
            let x = core_points(repo);
            let radii = [0.2, 0.5, 1., 2.];
            let counts: Vec<usize> = radii.iter().map(|r| components(&x, *r).len()).collect();
            let d: Matrix = (1..8.min(x.len()))
                .map(|i| {
                    let diff = sub(&x[0], &x[i]);
                    vec![
                        diff.iter().map(|v| v.abs()).sum(),
                        norm(&diff),
                        diff.iter().map(|v| v.abs()).fold(0., f64::max),
                    ]
                })
                .collect();
            json!({"radii":radii,"component_counts":counts,"distances_L1_L2_Linf":d,"squared_distance_counterexample":[4,2],"scope":"scaled sample geometry, not biological topology proof"})
        }
        "stage03" => {
            let mut out = finite_topologies();
            let x = iris(repo);
            let ids: BTreeSet<String> = x.iter().map(|r| format!("{:?}", &r[..2])).collect();
            out["projected_distinct_vectors"] = json!(ids.len());
            out["original_rows"] = json!(x.len());
            out["scope"] = json!(
                "finite checks and a noninjective projection; not a general continuity theorem"
            );
            out
        }
        "stage04" => {
            let p = digit(repo);
            let mut rot = vec![0.; 64];
            for i in 0..8 {
                for j in 0..8 {
                    rot[j * 8 + 7 - i] = p[i * 8 + j];
                }
            }
            json!({"rotation_pixel_distance":distance(&p,&rot),"original_betti":pixel_betti(&p,8,8,8.),"rotated_betti":pixel_betti(&rot,8,8,8.),"dihedral_square_group_size":8,"scope":"rotation preserves this pixel-complex topology, not necessarily the digit class label"})
        }
        "stage06" => {
            let mut out = crate::trace::algebra_control();
            out["observed_digit_diagram"] =
                json!(persistence(&pixel_filtration(&digit(repo), 8, 8)));
            out
        }
        "stage05" => {
            let p = digit(repo);
            json!({"triangle_boundary_betti":betti(&triangle(false)),"filled_triangle_betti":betti(&triangle(true)),"tetrahedron_surface_betti":betti(&tetra(false)),"filled_tetrahedron_betti":betti(&tetra(true)),"real_digit_closed_pixel_betti":pixel_betti(&p,8,8,8.),"real_digit_persistence":persistence(&pixel_filtration(&p,8,8)),"coefficient_field":"F2","scope":"explicit finite complexes and an observed image; interpretation requires pixel convention"})
        }
        "stage07" => {
            let x = core_points(repo);
            json!({"point_rows":x.len(),"rips_diagram":report_h01(&persistence(&rips(&x,1.5,2))),"equilateral_side":2,"cech_common_radius":2./3f64.sqrt(),"cech_pair_radius":1,"rips_filled_triangle_edge_threshold":2,"scope":"Rips plus exact Cech control; general alpha/Delaunay implementation remains in Python reference"})
        }
        "stage08" | "stage09" => {
            let x = core_points(repo);
            json!({"square_diagram":report_h01(&persistence(&rips(&square(),2.,2))),"data_diagram":report_h01(&persistence(&rips(&x,f64::INFINITY,2))),"independent_H0_mst":mst(&x),"coefficient_field":"F2","maximum_simplex_dimension":2,"scope":"H0 and H1; unfilled top-dimensional classes not an H2 inference"})
        }
        "stage10" => {
            let p = digit(repo);
            let mut q = p.clone();
            let mut delta = 0f64;
            for i in 0..q.len() {
                q[i] += 0.05 * (i as f64).sin();
                delta = delta.max((q[i] - p[i]).abs());
            }
            let a = persistence(&pixel_filtration(&p, 8, 8));
            let b = persistence(&pixel_filtration(&q, 8, 8));
            let d: Vec<f64> = (0..2)
                .map(|k| bottleneck(&dimension(&a, k), &dimension(&b, k)))
                .collect();
            json!({"input_linf":delta,"bottleneck_by_dimension":d,"bound_holds":d[0]<=delta+1e-8&&d[1]<=delta+1e-8,"scope":"same pixel complex, sublevel functions of negative intensity; not arbitrary pipeline stability"})
        }
        "stage11" => mapper(&core_points(repo), 5, 0.3, 0.5),
        "stage12" => digit_case(repo),
        "stage13" => {
            let (mut errors, mut coords) = (vec![], vec![]);
            for i in 0..12 {
                let (u, v) = (0.1 * i as f64, 0.3);
                let den = 1. + u * u + v * v;
                let p = vec![2. * u / den, 2. * v / den, (u * u + v * v - 1.) / den];
                let q = [p[0] / (1. - p[2]), p[1] / (1. - p[2])];
                errors.push(distance(&[u, v], &q));
                coords.push(p);
            }
            json!({"sphere_points":coords,"chart_roundtrip_errors":errors,"scope":"stereographic chart excludes north pole; camera projection is not such a chart"})
        }
        "stage14" => {
            let r = quaternion_matrix(&[0.2f64.cos(), 0., 0., 0.2f64.sin()]);
            let ident = matmul(&transpose(&r), &r);
            let c = read_json(repo, "data/stereo/calibration.json");
            let (f, cx, cy) = (
                c["focal_px"].as_f64().unwrap(),
                c["cx_left_px"].as_f64().unwrap(),
                c["cy_px"].as_f64().unwrap(),
            );
            let p = [0.2, -0.1, 3.];
            let uv = [f * p[0] / p[2] + cx, f * p[1] / p[2] + cy];
            let back = [(uv[0] - cx) * p[2] / f, (uv[1] - cy) * p[2] / f, p[2]];
            json!({"rotation":r,"RtR":ident,"pixel_uv":uv,"unprojected":back,"roundtrip_error":distance(&p,&back),"scope":"synthetic point with supplied camera intrinsics; depth is an input, not recovered from one pixel"})
        }
        "stage15" => stereo(repo),
        "stage16" => {
            let x = core_points(repo)[..6].to_vec();
            let mut scores = matmul(&x, &transpose(&x));
            let mut weights = vec![];
            for row in &mut scores {
                for v in row.iter_mut() {
                    *v /= (x[0].len() as f64).sqrt();
                }
                weights.push(softmax(row));
            }
            json!({"attention_weights":weights,"attended_features":matmul(&weights,&x),"scope":"native attention calculation, not pretrained VGGT inference"})
        }
        "stage17" => registration_control(),
        "stage18" | "poux_bridge" => centroid_bridge(repo),
        "stage19" => temporal(),
        "stage20" => {
            json!({"registration_control":registration_control(),"sports_motion":motion(repo),"source_coordinates":"separate controls; no forced alignment between these objects","scope":"spatial-capstone prerequisites, not an independently acquired reconstruction"})
        }
        "stage21" => {
            let mut out = regression_case(repo, "hahn1");
            let err: Vec<f64> = [0.1, 0.01, 0.001]
                .iter()
                .map(|h| {
                    (((0.4f64 + h).sin() - (0.4f64 - h).sin()) / (2. * h) - 0.4f64.cos()).abs()
                })
                .collect();
            out["manufactured_derivative_errors"] = json!(err);
            out
        }
        "stage22" => {
            let (x, t) = (0.2, 2.);
            let y = x / (1. - t * x);
            let back = y / (1. + t * y);
            json!({"initial":x,"time":t,"flow":y,"inverse":back,"finite_blowup_time":1./x,"scope":"x'=x² exact local flow, defined only before blowup"})
        }
        "stage23" => json!({"hnn":train_physics("hnn"),"lnn_restricted":train_physics("lnn")}),
        "stage24" => integrators(),
        "stage25" => constraint_control(),
        "stage26" => train_physics("pinn"),
        "stage27" => gradient_control(),
        "stage28" => {
            json!({"deeponet":train_operator("deeponet"),"spectral_operator":train_operator("fno")})
        }
        "stage29" => {
            json!({"differentiable_scalar_flow_fit":damping_fit(),"row_stochastic_matrix":[[1,0],[1,0]],"input":[1,3],"output":[1,1],"input_sum":4,"output_sum":2,"scope":"row-stochastic attention alone is not a mass-conservation law"})
        }
        "stage30" => {
            json!({"native_training":damping_fit(),"nonlinear_constraint":constraint_control(),"requirement":"independent observed-system capstone still required","scope":"manufactured verification controls do not validate a physical world model"})
        }
        "wine" | "wdbc" | "seeds" => classification(repo, key),
        "stackloss" | "concrete_slump" => regression_case(repo, key),
        "co2" | "nile" | "elnino" => time_case(repo, key),
        "grunfeld" => grunfeld(repo),
        "modechoice" => mode_choice(repo),
        "leakage" => leakage(repo),
        "claims" => {
            json!({"integration":integrators(),"projection":constraint_control(),"gradient_conflicts":gradient_control()})
        }
        "s00" => {
            let (x, t, _) = spl(repo);
            json!({"centroid_m":mean_rows(&x),"selected_frames":x.len(),"independent_trials":1,"time_seconds":t,"landing_offset_m":[read_json(repo,"sports_v8/data/spl_selected_frames.json")["landing_x"].as_f64().unwrap()*0.0254,read_json(repo,"sports_v8/data/spl_selected_frames.json")["landing_y"].as_f64().unwrap()*0.0254],"scope":"mixed units converted, selected observations remain one trial"})
        }
        "s01" => motion(repo),
        "s02" => flight(repo),
        "s03" => profile(repo, true),
        "s04" => {
            let (x, t, _) = spl(repo);
            let mut vals = vec![];
            for i in 0..6 {
                let query = i as f64 * 0.5;
                let last = t
                    .iter()
                    .enumerate()
                    .filter(|(_, v)| **v <= query)
                    .map(|(i, _)| i)
                    .last();
                if let Some(k) = last {
                    vals.push(
                        json!({"time":query,"source_row":k,"age":query-t[k],"position_m":x[k]}),
                    );
                }
            }
            json!({"past_only_holds":vals,"scope":"zero-order hold labels age and does not interpolate future measurements"})
        }
        "s05" => profile(repo, false),
        "s06" => {
            json!({"observations":motion(repo),"flight_diagnostic":flight(repo),"protocol_requirement":"new independent athlete/session measurements and event labels","scope":"no held-out athlete benchmark in the excerpt"})
        }
        "acb" => acb(repo),
        "r01" => whiten(&iris(repo)[..90].to_vec()),
        "r02" => {
            let mut rng = Rng { state: 7 };
            let mut z = zeros(128, 4);
            for row in &mut z {
                for v in row {
                    *v = rng.normal();
                }
            }
            let dirs = directions(4, 16, 11);
            let (loss, g) = gaussian_penalty(&z, &dirs);
            let (cl, cg) = gaussian_penalty(&zeros(128, 4), &dirs);
            json!({"normal_control_penalty":loss,"normal_control_gradient_first_row":g[0],"collapsed_penalty":cl,"collapsed_gradient_first_row":cg[0],"scope":"finite-frequency/projection diagnostics, not proof of multivariate Gaussianity"})
        }
        "r03" => loss_controls(),
        "r04" => representation_training(repo),
        "r05" => {
            let (r, x, _) = profile_rows(repo);
            let j = column(&r[0], "player_id");
            let g: Vec<String> = r[1..].iter().map(|r| r[j].clone()).collect();
            let (tr, va, te) = group_split(&g);
            let mut out = whiten(&rows(&x, &tr));
            out["train_rows"] = json!(tr);
            out["validation_rows"] = json!(va);
            out["test_rows"] = json!(te);
            out["scope"] = json!(
                "training-group covariance only, small selected profiles; no semantic validation"
            );
            out
        }
        _ => panic!("unknown native lab: {key}"),
    }
}
pub fn lab_keys(repo: &str) -> Vec<String> {
    let j = read_json(repo, "native/protocols/labs.json");
    let mut keys: Vec<String> = j["labs"]
        .as_array()
        .unwrap()
        .iter()
        .map(|v| v["key"].as_str().unwrap().to_string())
        .collect();
    keys.sort();
    keys
}
pub fn run(repo: &str, key: &str) -> Value {
    crate::trace::begin();
    require(
        lab_keys(repo).iter().any(|v| v == key),
        "unknown native lab",
    );
    let metrics = native_lab(repo, key);
    json!({"schema":"shape.native.v16","lab":key,"language":"rust","implementation":"native; no Python calls or reference-result reads","protocol":"native16 shared teaching adaptation","metrics":metrics,"original_notebook_parity":"not_certified; see native/COVERAGE.md","status":"completed","inputs":crate::trace::snapshot()})
}
