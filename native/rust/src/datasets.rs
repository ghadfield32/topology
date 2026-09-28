//! Observation-aware experiments on the bundled source snapshots.
use crate::{data::*, geometry::group_split, learning::*, math::*, topology::*};
use serde_json::{json, Value};
use std::collections::{BTreeMap, BTreeSet};
pub fn iris(repo: &str) -> Matrix {
    let r = read_csv(repo, "data/raw/iris.csv", b',');
    numeric(
        &r,
        &[
            "sepal_length_cm",
            "sepal_width_cm",
            "petal_length_cm",
            "petal_width_cm",
        ],
    )
    .0
}
pub fn classification_data(repo: &str, id: &str) -> (Matrix, Vec<i64>, Vec<String>) {
    let path = if id == "seeds" {
        "data/v7/seeds/table.csv".to_string()
    } else {
        format!("data/industries/{id}/data.csv")
    };
    let r = read_csv(repo, &path, b',');
    let target = column(&r[0], if id == "seeds" { "variety" } else { "label" });
    let features = r[0][1..target].to_vec();
    let names: Vec<&str> = features.iter().map(String::as_str).collect();
    let (x, idx) = numeric(&r, &names);
    require(idx.len() == r.len() - 1, "missing classification values");
    let y = r[1..]
        .iter()
        .map(|r| r[target].parse::<i64>().expect("class label"))
        .collect();
    (x, y, features)
}
pub fn classification(repo: &str, id: &str) -> Value {
    let (x, y, features) = classification_data(repo, id);
    let (tr, va, te) = stratified(&y, 42);
    let raw = fit_predict(&x, &y, &tr, &va, &te);
    let s = Scaler::fit(&rows(&x, &tr));
    let z = s.transform(&x);
    let nref = 24.min(tr.len() / 3);
    let refs = rows(&z, &tr[..nref]);
    let supervised = &tr[nref..];
    let tf: Matrix = z.iter().map(|q| topo_feature(q, &refs)).collect();
    let mut combo = x.clone();
    for i in 0..combo.len() {
        combo[i].extend_from_slice(&tf[i]);
    }
    json!({"features":features,"train_rows":tr,"validation_rows":va,"test_rows":te,"fixed_reference_rows":&tr[..nref],"supervised_rows":supervised,"raw_all_training":raw,"raw_same_supervised_rows":fit_predict(&x,&y,supervised,&va,&te),"topology":fit_predict(&tf,&y,supervised,&va,&te),"combined":fit_predict(&combo,&y,supervised,&va,&te),"topological_features":tf,"protocol":"native-16: stratified xorshift split; fixed unlabelled training reference; softmax GD,160 epochs,lr=.15,L2=.01","scope":"new common native protocol, not the original scikit-learn optimizer/protocol"})
}
pub fn digit_data(repo: &str) -> (Matrix, Vec<i64>, Vec<usize>, Vec<usize>, Vec<usize>) {
    let a = read_npz(repo, "data/raw/digits.npz");
    let im = &a["images"];
    let lab = &a["labels"];
    require(
        im.shape.len() == 3 && im.shape[1..] == [8, 8],
        "digit image shape",
    );
    let x: Matrix = im.data.chunks_exact(64).map(|v| v.to_vec()).collect();
    let y: Vec<i64> = lab.data.iter().map(|x| *x as i64).collect();
    let sp = read_json(repo, "data/splits.json");
    let ids = |key: &str| -> Vec<usize> {
        sp[key]
            .as_array()
            .unwrap()
            .iter()
            .map(|v| v.as_u64().unwrap() as usize)
            .collect()
    };
    (x, y, ids("train"), ids("validation"), ids("test"))
}
pub fn digit_features(x: &Matrix) -> Matrix {
    x.iter()
        .map(|p| {
            let mut v = vec![];
            for threshold in [4., 8., 12.] {
                v.extend(pixel_betti(p, 8, 8, threshold).iter().map(|b| *b as f64));
            }
            v.push(mean(p));
            v
        })
        .collect()
}
pub fn digit_case(repo: &str) -> Value {
    let (x, y, tr, va, te) = digit_data(repo);
    let tf = digit_features(&x);
    let mut combo = x.clone();
    for i in 0..combo.len() {
        combo[i].extend_from_slice(&tf[i]);
    }
    json!({"train_rows":tr,"validation_rows":va,"test_rows":te,"raw":fit_predict(&x,&y,&tr,&va,&te),"topology":fit_predict(&tf,&y,&tr,&va,&te),"combined":fit_predict(&combo,&y,&tr,&va,&te),"topology_definition":"closed-pixel Betti0/1 at 4,8,12 plus mean intensity","scope":"native softmax protocol on supplied exposed per-image partition; writer IDs unavailable"})
}
pub fn regression_case(repo: &str, id: &str) -> Value {
    let (mut path, mut features, mut target) = (
        format!("data/industries/{id}/data.csv"),
        vec!["AIRFLOW", "WATERTEMP", "ACIDCONC"],
        "STACKLOSS",
    );
    if id == "concrete_slump" {
        path = "data/v7/concrete_slump/table.csv".into();
        features = vec![
            "cement_kg_m3",
            "slag_kg_m3",
            "fly_ash_kg_m3",
            "water_kg_m3",
            "sp_kg_m3",
            "coarse_aggregate_kg_m3",
            "fine_aggregate_kg_m3",
        ];
        target = "strength_mpa";
    }
    if id == "hahn1" {
        path = "data/physics/hahn1_excerpt.csv".into();
        features = vec!["temperature_K"];
        target = "expansion_response";
    }
    let r = read_csv(repo, &path, b',');
    let mut cols = features.clone();
    cols.push(target);
    let (vals, idx) = numeric(&r, &cols);
    require(
        idx.len() == r.len() - 1,
        "unexpected missing regression field",
    );
    let x: Matrix = vals.iter().map(|v| v[..features.len()].to_vec()).collect();
    let y: Vec<f64> = vals.iter().map(|v| v[features.len()]).collect();
    let mut ids: Vec<usize> = (0..x.len()).collect();
    shuffle(&mut ids, 53);
    let (mut n1, mut n2) = (ids.len() * 6 / 10, ids.len() * 8 / 10);
    if id == "concrete_slump" {
        n1 = 52;
        n2 = 77;
    }
    let mut out = regression_result(
        &x,
        &y,
        &ids[..n1],
        &ids[n1..n2],
        &ids[n2..],
        id == "concrete_slump",
    );
    out["features"] = json!(features);
    out["target"] = json!(target);
    out["source_rows"] = json!(idx);
    out["scope"] = json!(
        "fixed native ridge protocol; random split does not establish future-batch performance"
    );
    out
}
pub fn time_case(repo: &str, id: &str) -> Value {
    let (mut series, mut times) = (vec![], vec![]);
    if id == "sunspots" {
        let r = read_csv(repo, "data/time_series/sunspots_yearly.csv", b',');
        for row in &r[1..] {
            series.push(row[1].parse::<f64>().unwrap());
            times.push(row[0].clone());
        }
    } else {
        let r = read_csv(repo, &format!("data/industries/{id}/data.csv"), b',');
        if id == "elnino" {
            for row in &r[1..] {
                for j in 2..14 {
                    series.push(row[j].parse::<f64>().unwrap());
                    times.push(format!("{}-{:02}", row[1], j - 1));
                }
            }
        } else {
            for row in &r[1..] {
                series.push(if row[2].is_empty() {
                    f64::NAN
                } else {
                    row[2].parse::<f64>().expect("time-series value")
                });
                times.push(row[1].clone());
            }
        }
    }
    let n = series.len();
    let (cut1, cut2, lag) = (n * 6 / 10, n * 8 / 10, 6);
    let (mut x, mut y, mut rt, mut target_ids) = (vec![], vec![], vec![], vec![]);
    let (mut tr, mut va, mut te) = (vec![], vec![], vec![]);
    let mut skipped = 0;
    for t in lag..n {
        let mut good = series[t].is_finite() && series[t - lag..t].iter().all(|v| v.is_finite());
        let bucket = if t >= cut2 {
            good = good && t - lag >= cut2;
            2
        } else if t >= cut1 {
            good = good && t - lag >= cut1;
            1
        } else {
            0
        };
        if !good {
            skipped += 1;
            continue;
        }
        let i = x.len();
        x.push(series[t - lag..t].to_vec());
        y.push(series[t]);
        rt.push(times[t].clone());
        target_ids.push(t);
        match bucket {
            0 => tr.push(i),
            1 => va.push(i),
            _ => te.push(i),
        }
    }
    let mut out = regression_result(&x, &y, &tr, &va, &te, false);
    let naive: Vec<f64> = te.iter().map(|k| x[*k][lag - 1]).collect();
    out["last_value_mae"] = json!(mae(&values(&y, &te), &naive));
    out["original_observation_count"] = json!(n);
    out["target_indices"] = json!(target_ids);
    out["target_times"] = json!(rt);
    out["dropped_windows"] = json!(skipped);
    out["lag"] = json!(lag);
    out["scope"]=json!("strict chronological complete windows contained in one partition, historical snapshot; no causal discovery");
    out
}
pub fn grunfeld(repo: &str) -> Value {
    let r = read_csv(repo, "data/industries/grunfeld/data.csv", b',');
    let fj = column(&r[0], "firm");
    let yj = column(&r[0], "year");
    let mut groups: BTreeMap<String, Vec<Vec<String>>> = BTreeMap::new();
    for row in &r[1..] {
        groups.entry(row[fj].clone()).or_default().push(row.clone());
    }
    let (mut x, mut y, mut identity) = (vec![], vec![], vec![]);
    let (mut tr, mut va, mut te) = (vec![], vec![], vec![]);
    for (firm, rows) in &mut groups {
        rows.sort_by(|a, b| a[yj].cmp(&b[yj]));
        for i in 1..rows.len() {
            let v: Vec<f64> = ["invest", "value", "capital"]
                .iter()
                .map(|c| rows[i - 1][column(&r[0], c)].parse::<f64>().unwrap())
                .collect();
            let target = rows[i][column(&r[0], "invest")].parse::<f64>().unwrap();
            let k = x.len();
            x.push(v);
            y.push(target);
            identity.push(format!("{firm}:{}", rows[i][yj]));
            if i < 12 {
                tr.push(k);
            } else if i < 16 {
                va.push(k);
            } else {
                te.push(k);
            }
        }
    }
    let mut out = regression_result(&x, &y, &tr, &va, &te, false);
    out["firm_year"] = json!(identity);
    out["features"] = json!(["previous investment", "previous value", "previous capital"]);
    out["scope"] = json!("lagged within-firm temporal experiment, not causality");
    out
}
pub fn mode_choice(repo: &str) -> Value {
    let rows0 = read_csv(repo, "data/industries/modechoice/data.csv", b',');
    let cols = ["ttme", "invc", "invt", "gc", "hinc", "psize"];
    let (x, idx) = numeric(&rows0, &cols);
    require(idx.len() == rows0.len() - 1, "choice missing policy");
    let (gj, cj) = (column(&rows0[0], "individual"), column(&rows0[0], "choice"));
    let mut groups = vec![];
    let mut y = vec![];
    let mut members: BTreeMap<String, Vec<usize>> = BTreeMap::new();
    for (i, row) in rows0[1..].iter().enumerate() {
        let g = row[gj].clone();
        groups.push(g.clone());
        members.entry(g).or_default().push(i);
        let v = row[cj].parse::<f64>().unwrap();
        require(v == 0. || v == 1., "binary choice label");
        y.push(v);
    }
    for ids in members.values() {
        require(ids.len() == 4, "complete alternatives required");
        require(
            ids.iter().map(|i| y[*i]).sum::<f64>() == 1.,
            "one chosen alternative required",
        );
    }
    let (tr, va, te) = group_split(&groups);
    let s = Scaler::fit(&rows(&x, &tr));
    let z = s.transform(&x);
    let train_set: BTreeSet<usize> = tr.iter().copied().collect();
    let mut w = vec![0.; cols.len()];
    for _ in 0..250 {
        let mut g = vec![0.; w.len()];
        let mut n = 0;
        for ids in members.values() {
            if !train_set.contains(&ids[0]) {
                continue;
            }
            let scores: Vec<f64> = ids.iter().map(|i| dot(&w, &z[*i])).collect();
            let p = softmax(&scores);
            for (j, i) in ids.iter().enumerate() {
                for k in 0..w.len() {
                    g[k] += (p[j] - y[*i]) * z[*i][k];
                }
            }
            n += 1;
        }
        for k in 0..w.len() {
            w[k] -= 0.1 * (g[k] / n as f64 + 0.01 * w[k]);
        }
    }
    let test_set: BTreeSet<usize> = te.iter().copied().collect();
    let mut predictions = vec![];
    let mut correct = 0;
    for (key, ids) in &members {
        if !test_set.contains(&ids[0]) {
            continue;
        }
        let a: Vec<f64> = ids.iter().map(|i| dot(&w, &z[*i])).collect();
        let p = softmax(&a);
        let mut best = 0;
        for j in 0..p.len() {
            if p[j] > p[best] {
                best = j;
            }
        }
        if y[ids[best]] == 1. {
            correct += 1;
        }
        predictions
            .push(json!({"individual":key,"rows":ids,"probabilities":p,"predicted_row":ids[best]}));
    }
    json!({"features":cols,"train_rows":tr,"validation_rows":va,"test_rows":te,"predictions":predictions,"group_accuracy":correct as f64/predictions.len()as f64,"weights":w,"scope":"conditional-logit teaching implementation; traveler grouping preserved, not population travel shares"})
}
