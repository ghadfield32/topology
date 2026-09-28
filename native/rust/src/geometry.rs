//! Coordinate, motion, registration and numerical-mechanics experiments.
use crate::{data::*, math::*, topology::*};
use serde_json::{json, Value};
use std::collections::{BTreeMap, BTreeSet};
pub fn rotate_z(x: &[f64], a: f64) -> Vec<f64> {
    require(x.len() == 3, "3D point");
    let (c, s) = (a.cos(), a.sin());
    vec![c * x[0] - s * x[1], s * x[0] + c * x[1], x[2]]
}
pub fn angle(a: &[f64], b: &[f64], c: &[f64]) -> f64 {
    let (u, v) = (sub(a, b), sub(c, b));
    let n = norm(&u) * norm(&v);
    require(n > 1e-15, "degenerate angle");
    (dot(&u, &v) / n).clamp(-1., 1.).acos() * 180. / std::f64::consts::PI
}
pub fn spl(repo: &str) -> (Matrix, Vec<f64>, Vec<Value>) {
    let j = read_json(repo, "sports_v8/data/spl_selected_frames.json");
    require(j["xyz_unit"] == "ft", "SPL feet convention changed");
    let fps = j["sampling_rate"].as_f64().expect("fps");
    require(fps > 0., "invalid fps");
    let rs = j["records"].as_array().unwrap().clone();
    let mut x = vec![];
    let mut ts = vec![];
    for r in &rs {
        let mut p = fv(&r["ball"]);
        require(p.len() == 3, "ball shape");
        for v in &mut p {
            *v *= 0.3048;
        }
        x.push(p);
        ts.push(r["frame"].as_f64().unwrap() / fps);
    }
    require(
        ts.windows(2).all(|w| w[1] > w[0]),
        "nonincreasing timestamps",
    );
    (x, ts, rs)
}
pub fn stereo(repo: &str) -> Value {
    let left = read_png(repo, "data/stereo/left.png");
    let right = read_png(repo, "data/stereo/right.png");
    let arrays = read_npz(repo, "data/stereo/motorcycle.npz");
    let reference = &arrays["disparity_px"];
    let cal = read_json(repo, "data/stereo/calibration.json");
    let (h, w) = (left.shape[0], left.shape[1]);
    require(
        right.shape == left.shape && left.shape[2] == 3,
        "stereo dimensions",
    );
    let gray = |a: &Array| -> Vec<f64> {
        (0..h * w)
            .map(|i| (a.data[3 * i] + a.data[3 * i + 1] + a.data[3 * i + 2]) / 3.)
            .collect()
    };
    let (l, r) = (gray(&left), gray(&right));
    let (mut obs, mut errors, mut de) = (vec![], vec![], vec![]);
    let mut requested = 0;
    let offset = cal["doffs_px"].as_f64().unwrap();
    let factor = cal["focal_px"].as_f64().unwrap() * cal["baseline_m"].as_f64().unwrap();
    for y in (30..h - 30).step_by(55) {
        for x in (110..w - 30).step_by(61) {
            requested += 1;
            let truth = reference.data[y * w + x];
            if !truth.is_finite() || truth + offset <= 0. {
                continue;
            }
            let (mut best, mut bd) = (f64::INFINITY, 0);
            for d in 0..=90 {
                let mut cost = 0.;
                for dy in -2isize..=2 {
                    for dx in -2isize..=2 {
                        let yy = (y as isize + dy) as usize;
                        let xx = (x as isize + dx) as usize;
                        cost += (l[yy * w + xx] - r[yy * w + xx - d]).abs();
                    }
                }
                if cost < best {
                    best = cost;
                    bd = d;
                }
            }
            let pred = bd as f64;
            let z = factor / (pred + offset);
            let zt = factor / (truth + offset);
            errors.push((pred - truth).abs());
            de.push((z - zt).abs());
            obs.push(json!({"u":x,"v":y,"truth_disparity_px":truth,"predicted_disparity_px":pred,"truth_depth_m":zt,"predicted_depth_m":z}));
        }
    }
    let bad = errors.iter().filter(|v| **v > 2.).count();
    json!({"requested_pixels":requested,"eligible_pixels":obs.len(),"patch_width":5,"max_disparity_px":90,"disparity_mae_px":mean(&errors),"disparity_median_abs_px":median(&errors),"bad_over_2px_fraction":bad as f64/errors.len()as f64,"depth_mae_m":mean(&de),"predictions":obs,"convention":"Z=fB/(d+doffs); rectified positive optical-axis depth","scope":"fixed selected pixels, not full-image or camera-calibration validation"})
}
pub fn quaternion_matrix(q: &[f64]) -> Matrix {
    require(q.len() == 4, "quaternion shape");
    let n = norm(q);
    require(n > 1e-14, "zero quaternion");
    let (w, x, y, z) = (q[0] / n, q[1] / n, q[2] / n, q[3] / n);
    vec![
        vec![
            1. - 2. * (y * y + z * z),
            2. * (x * y - z * w),
            2. * (x * z + y * w),
        ],
        vec![
            2. * (x * y + z * w),
            1. - 2. * (x * x + z * z),
            2. * (y * z - x * w),
        ],
        vec![
            2. * (x * z - y * w),
            2. * (y * z + x * w),
            1. - 2. * (x * x + y * y),
        ],
    ]
}
pub fn register(a: &Matrix, b: &Matrix) -> (f64, Matrix, Vec<f64>) {
    let (n, d) = shape(a);
    let (nb, db) = shape(b);
    require(
        n == nb && d == 3 && db == 3 && n >= 3,
        "paired registration shape",
    );
    let (ma, mb) = (mean_rows(a), mean_rows(b));
    let mut s = zeros(3, 3);
    let mut energy = 0.;
    for i in 0..n {
        let (u, v) = (sub(&a[i], &ma), sub(&b[i], &mb));
        energy += dot(&u, &u);
        for j in 0..3 {
            for k in 0..3 {
                s[j][k] += u[j] * v[k];
            }
        }
    }
    require(energy > 1e-12, "degenerate registration");
    let (xx, xy, xz, yx, yy, yz, zx, zy, zz) = (
        s[0][0], s[0][1], s[0][2], s[1][0], s[1][1], s[1][2], s[2][0], s[2][1], s[2][2],
    );
    let nmat = vec![
        vec![xx + yy + zz, yz - zy, zx - xz, xy - yx],
        vec![yz - zy, xx - yy - zz, xy + yx, zx + xz],
        vec![zx - xz, xy + yx, -xx + yy - zz, yz + zy],
        vec![xy - yx, zx + xz, yz + zy, -xx - yy + zz],
    ];
    let (_, v) = eigen_sym(&nmat);
    let q = vec![v[0][0], v[1][0], v[2][0], v[3][0]];
    let rotation = quaternion_matrix(&q);
    let mut score = 0.;
    for i in 0..n {
        score += dot(&sub(&b[i], &mb), &matvec(&rotation, &sub(&a[i], &ma)));
    }
    let scale = score / energy;
    require(scale > 0., "negative scale");
    let rotated = matvec(&rotation, &ma);
    let t: Vec<f64> = (0..3).map(|j| mb[j] - scale * rotated[j]).collect();
    (scale, rotation, t)
}
pub fn registration_control() -> Value {
    let mut rng = Rng { state: 34 };
    let (mut a, mut b) = (vec![], vec![]);
    for _ in 0..24 {
        let p = vec![rng.normal(), rng.normal(), rng.normal()];
        let mut q = rotate_z(&p, 0.4);
        for j in 0..3 {
            q[j] = 2.5 * q[j] + [3., -2., 1.][j];
        }
        a.push(p);
        b.push(q);
    }
    let (s, r, t) = register(&a[..12].to_vec(), &b[..12].to_vec());
    let mut errors = vec![];
    for i in 12..24 {
        let mut p = matvec(&r, &a[i]);
        for j in 0..3 {
            p[j] = s * p[j] + t[j];
        }
        errors.push(distance(&p, &b[i]));
    }
    json!({"scale":s,"rotation":r,"translation":t,"fit_indices":(0..12).collect::<Vec<_>>(),"holdout_indices":(12..24).collect::<Vec<_>>(),"holdout_errors":errors,"max_holdout_error":errors.iter().copied().fold(0.,f64::max),"origin":"manufactured paired nondegenerate cloud; not a learned reconstruction"})
}
pub fn flight(repo: &str) -> Value {
    let (x, t, _) = spl(repo);
    let ids = [3, 4, 5, 6, 7];
    let hold = [8, 9];
    let base = t[ids[0]];
    let a: Matrix = ids
        .iter()
        .map(|k| {
            let dt = t[*k] - base;
            vec![1., dt, dt * dt]
        })
        .collect();
    let y: Vec<f64> = ids.iter().map(|k| x[*k][2]).collect();
    let at = transpose(&a);
    let w = solve(&matmul(&at, &a), &matvec(&at, &y));
    let p: Vec<f64> = hold
        .iter()
        .map(|k| {
            let dt = t[*k] - base;
            dot(&w, &[1., dt, dt * dt])
        })
        .collect();
    let truth: Vec<f64> = hold.iter().map(|k| x[*k][2]).collect();
    let fixed: Matrix = ids.iter().map(|k| vec![1., t[*k] - base]).collect();
    let yf: Vec<f64> = ids
        .iter()
        .enumerate()
        .map(|(i, k)| {
            let dt = t[*k] - base;
            y[i] + 0.5 * 9.80665 * dt * dt
        })
        .collect();
    let ft = transpose(&fixed);
    let wf = solve(&matmul(&ft, &fixed), &matvec(&ft, &yf));
    let pf: Vec<f64> = hold
        .iter()
        .map(|k| {
            let dt = t[*k] - base;
            wf[0] + wf[1] * dt - 0.5 * 9.80665 * dt * dt
        })
        .collect();
    let pc = vec![mean(&y); hold.len()];
    json!({"fit_rows":ids,"later_same_trial_rows":hold,"coefficients":w,"fitted_acceleration_m_s2":2.*w[2],"truth":truth,"quadratic_predictions":p,"quadratic_mae_m":mae(&truth,&p),"fixed_gravity_predictions":pf,"fixed_gravity_mae_m":mae(&truth,&pf),"constant_predictions":pc,"constant_mae_m":mae(&truth,&pc),"scope":"selected frames, no release annotation and no independent athlete test"})
}
pub fn motion(repo: &str) -> Value {
    let (x, t, rs) = spl(repo);
    let angles: Vec<f64> = rs
        .iter()
        .map(|r| {
            angle(
                &fv(&r["right_shoulder"]),
                &fv(&r["right_elbow"]),
                &fv(&r["right_wrist"]),
            )
        })
        .collect();
    let mut vel = vec![];
    for i in 1..x.len() {
        let dt = t[i] - t[i - 1];
        if dt > 0.1 {
            vel.push(json!({"row":i,"valid":false,"reason":"gap exceeds 0.1 seconds"}));
        } else {
            let v: Vec<f64> = sub(&x[i], &x[i - 1]).iter().map(|z| z / dt).collect();
            vel.push(json!({"row":i,"valid":true,"velocity_m_s":v,"dt":dt}));
        }
    }
    json!({"joint_angles_deg":angles,"interval_velocities":vel,"time_seconds":t,"scope":"interval estimates on selected samples; not camera PTS or ground-truth release"})
}
pub fn integrators() -> Value {
    let methods = [
        "explicit_euler",
        "symplectic_euler",
        "verlet",
        "implicit_midpoint",
        "rk4",
    ];
    let mut out = json!({});
    let dt: f64 = 0.05;
    let n = 400;
    for method in methods {
        let (mut q, mut p): (f64, f64) = (1., 0.);
        let mut trace = vec![vec![0., q, p, 0.5]];
        let mut max_err = 0f64;
        for i in 0..n {
            match method {
                "explicit_euler" => {
                    (q, p) = (q + dt * p, p - dt * q);
                }
                "symplectic_euler" => {
                    p -= dt * q;
                    q += dt * p;
                }
                "verlet" => {
                    p -= dt * q / 2.;
                    q += dt * p;
                    p -= dt * q / 2.;
                }
                "implicit_midpoint" => {
                    let den = 1. + dt * dt / 4.;
                    (q, p) = (
                        ((1. - dt * dt / 4.) * q + dt * p) / den,
                        ((1. - dt * dt / 4.) * p - dt * q) / den,
                    );
                }
                _ => {
                    let (a, b) = (q, p);
                    let (aq, ap) = (b, -a);
                    let (bq, bp) = (b + dt * ap / 2., -(a + dt * aq / 2.));
                    let (cq, cp) = (b + dt * bp / 2., -(a + dt * bq / 2.));
                    let (dq, dp) = (b + dt * cp, -(a + dt * cq));
                    q += dt * (aq + 2. * bq + 2. * cq + dq) / 6.;
                    p += dt * (ap + 2. * bp + 2. * cp + dp) / 6.;
                }
            }
            let energy = (q * q + p * p) / 2.;
            max_err = max_err.max((energy - 0.5).abs());
            if i % 10 == 9 {
                trace.push(vec![(i + 1) as f64 * dt, q, p, energy]);
            }
        }
        let err = (q - (n as f64 * dt).cos()).hypot(p + (n as f64 * dt).sin());
        out[method] = json!({"max_energy_error":max_err,"state_error":err,"trace":trace});
    }
    out["symplectic_one_step_control"] = json!({"dt":0.2,"q":0.96,"p":-0.2,"energy":0.4808});
    out
}
pub fn constraint_control() -> Value {
    let mut x = vec![2., 0.];
    let mut res = vec![];
    let mut trajectory = vec![x.clone()];
    for _ in 0..7 {
        let c = dot(&x, &x) - 1.;
        let den = 4. * dot(&x, &x);
        require(den > 1e-14, "singular constraint");
        for v in &mut x {
            *v -= 2. * (*v) * c / den;
        }
        res.push(dot(&x, &x) - 1.);
        trajectory.push(x.clone());
    }
    json!({"constraint_residuals":res,"trajectory":trajectory,"first_residual":res[0],"scope":"Newton-like normal corrections, not an exact one-step projection or a geodesic"})
}
pub fn gradient_control() -> Value {
    let gs = vec![vec![1., 0.], vec![-0.4, 1.], vec![0.2, -0.6]];
    let mut out = vec![];
    for (i, g) in gs.iter().enumerate() {
        let mut v = g.clone();
        for (j, h) in gs.iter().enumerate() {
            if i != j && dot(&v, h) < 0. {
                let f = dot(&v, h) / dot(h, h);
                for k in 0..v.len() {
                    v[k] -= f * h[k];
                }
            }
        }
        out.push(v);
    }
    let mut normalized = out.clone();
    for row in &mut normalized {
        let n = norm(row);
        if n > 1e-12 {
            for x in row {
                *x /= n;
            }
        }
    }
    json!({"input_gradients":gs,"projected_gradients":out,"mean_projected":mean_rows(&out),"mean_normalized_after_projection":mean_rows(&normalized),"opposite_gradients":[[1,0],[-1,0]],"zero_sum":[0,0],"scope":"ordered gradient operations, not a reproduction of full domain-decomposition benchmarks"})
}
pub fn temporal() -> Value {
    let d = [0.04, 0.05, 0.06, 0.2, 0.3, 0.4, 0.1];
    let visible = [true, true, true, true, false, true, true];
    let mut events = vec![];
    for i in 2..d.len() {
        if visible[i] && visible[i - 1] && d[i] > 0.15 && d[i - 1] > 0.15 && d[i - 2] <= 0.15 {
            events.push(i);
        }
    }
    json!({"distance_m":d,"visible":visible,"confirmed_candidate_frames":events,"scope":"manufactured thresholds; proximity is not contact, gaps break confirmation"})
}
pub fn profile_rows(repo: &str) -> (Vec<Vec<String>>, Matrix, Vec<&'static str>) {
    let r = read_csv(
        repo,
        "sports_v8/data/skillcorner_selected_profiles.csv",
        b',',
    );
    let cols = vec![
        "total_distance_full_all",
        "total_metersperminute_full_all",
        "running_distance_full_all",
        "hsr_distance_full_all",
        "sprint_distance_full_all",
    ];
    let (x, idx) = numeric(&r, &cols);
    require(idx.len() == r.len() - 1, "missing profile fields");
    (r, x, cols)
}
pub fn group_split(groups: &[String]) -> (Vec<usize>, Vec<usize>, Vec<usize>) {
    let keys: Vec<String> = groups
        .iter()
        .cloned()
        .collect::<BTreeSet<_>>()
        .into_iter()
        .collect();
    let mut order: Vec<usize> = (0..keys.len()).collect();
    shuffle(&mut order, 73);
    let mut bucket = BTreeMap::new();
    for (i, j) in order.iter().enumerate() {
        let b = if i >= keys.len() * 8 / 10 {
            2
        } else if i >= keys.len() * 6 / 10 {
            1
        } else {
            0
        };
        bucket.insert(keys[*j].clone(), b);
    }
    let (mut tr, mut va, mut te) = (vec![], vec![], vec![]);
    for (i, g) in groups.iter().enumerate() {
        match bucket[g] {
            0 => tr.push(i),
            1 => va.push(i),
            _ => te.push(i),
        }
    }
    (tr, va, te)
}
pub fn profile(repo: &str, topology: bool) -> Value {
    let (r, x, cols) = profile_rows(repo);
    let j = column(&r[0], "player_id");
    let groups: Vec<String> = r[1..].iter().map(|r| r[j].clone()).collect();
    let (tr, va, te) = group_split(&groups);
    let s = Scaler::fit(&rows(&x, &tr));
    let z = s.transform(&x);
    let mut out = json!({"features":cols,"train_rows":tr,"validation_rows":va,"test_rows":te,"athlete_ids":groups,"train_scaler_mean":s.mean,"train_scaler_scale":s.scale,"scaled_profiles":z,"scope":"selected season profiles, not chronological tracks or a representative player ranking"});
    if topology {
        out["diagram"] = json!(report_h01(&persistence(&rips(&z, f64::INFINITY, 2))));
        out["mst_edges"] = json!(mst(&z));
    }
    out
}
pub fn acb(repo: &str) -> Value {
    let j = read_json(repo, "sports_v9/data/matches.json");
    let mut a = j.as_array().unwrap().clone();
    a.sort_by(|a, b| a["date_time"].as_str().cmp(&b["date_time"].as_str()));
    let ids: Vec<i64> = a.iter().map(|v| v["id"].as_i64().unwrap()).collect();
    require(ids.len() == 10, "ten-game teaching snapshot required");
    let scores: Vec<f64> = a
        .iter()
        .map(|v| v["home_score"].as_f64().unwrap() + v["away_score"].as_f64().unwrap())
        .collect();
    let wins = a
        .iter()
        .filter(|v| v["home_score"].as_f64().unwrap() > v["away_score"].as_f64().unwrap())
        .count();
    json!({"chronological_match_ids":ids,"train_match_ids":&ids[..6],"validation_match_ids":&ids[6..8],"test_match_ids":&ids[8..],"total_points":scores,"home_wins":wins,"mean_total_points":mean(&scores),"scope":"ten selected metadata records, not all-season tracking or forecasting"})
}
