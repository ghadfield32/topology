//! Native differentiation and training. No Python subprocesses or precomputed predictions.
use crate::math::*;
use serde::Serialize;
use serde_json::{json, Value};
use std::{
    cell::RefCell,
    collections::{BTreeMap, BTreeSet},
};
#[derive(Clone)]
pub struct Node {
    pub value: f64,
    pub parents: Vec<usize>,
    pub weights: Vec<f64>,
}
pub struct Tape {
    nodes: RefCell<Vec<Node>>,
}
impl Tape {
    pub fn new() -> Self {
        Self {
            nodes: RefCell::new(vec![]),
        }
    }
    pub fn node(&self, v: f64, p: Vec<usize>, w: Vec<f64>) -> usize {
        require(v.is_finite(), "nonfinite autodiff value");
        let mut nodes = self.nodes.borrow_mut();
        nodes.push(Node {
            value: v,
            parents: p,
            weights: w,
        });
        nodes.len() - 1
    }
    pub fn input(&self, v: f64) -> usize {
        self.node(v, vec![], vec![])
    }
    pub fn val(&self, i: usize) -> f64 {
        self.nodes.borrow()[i].value
    }
    pub fn add(&self, a: usize, b: usize) -> usize {
        self.node(self.val(a) + self.val(b), vec![a, b], vec![1., 1.])
    }
    pub fn sub(&self, a: usize, b: usize) -> usize {
        self.node(self.val(a) - self.val(b), vec![a, b], vec![1., -1.])
    }
    pub fn mul(&self, a: usize, b: usize) -> usize {
        self.node(
            self.val(a) * self.val(b),
            vec![a, b],
            vec![self.val(b), self.val(a)],
        )
    }
    pub fn div(&self, a: usize, b: usize) -> usize {
        let v = self.val(b);
        require(v != 0., "autodiff division by zero");
        self.node(
            self.val(a) / v,
            vec![a, b],
            vec![1. / v, -self.val(a) / (v * v)],
        )
    }
    pub fn tanh(&self, a: usize) -> usize {
        let v = self.val(a).tanh();
        self.node(v, vec![a], vec![1. - v * v])
    }
    pub fn sin(&self, a: usize) -> usize {
        self.node(self.val(a).sin(), vec![a], vec![self.val(a).cos()])
    }
    pub fn exp(&self, a: usize) -> usize {
        let v = self.val(a).exp();
        self.node(v, vec![a], vec![v])
    }
    pub fn log(&self, a: usize) -> usize {
        let v = self.val(a);
        require(v > 0., "log domain");
        self.node(v.ln(), vec![a], vec![1. / v])
    }
    pub fn scale(&self, a: usize, v: f64) -> usize {
        self.mul(a, self.input(v))
    }
    pub fn back(&self, root: usize) -> Vec<f64> {
        let nodes = self.nodes.borrow();
        let mut g = vec![0.; nodes.len()];
        g[root] = 1.;
        for i in (0..=root).rev() {
            for (j, &p) in nodes[i].parents.iter().enumerate() {
                g[p] += g[i] * nodes[i].weights[j];
            }
        }
        g
    }
}
#[derive(Clone, Copy)]
pub struct Jet {
    pub v: usize,
    pub d: usize,
    pub d2: usize,
}
pub fn jconst(t: &Tape, v: f64) -> Jet {
    Jet {
        v: t.input(v),
        d: t.input(0.),
        d2: t.input(0.),
    }
}
pub fn jvar(t: &Tape, v: f64, active: bool) -> Jet {
    Jet {
        v: t.input(v),
        d: t.input(if active { 1. } else { 0. }),
        d2: t.input(0.),
    }
}
pub fn jadd(t: &Tape, a: Jet, b: Jet) -> Jet {
    Jet {
        v: t.add(a.v, b.v),
        d: t.add(a.d, b.d),
        d2: t.add(a.d2, b.d2),
    }
}
pub fn jmul(t: &Tape, a: Jet, b: Jet) -> Jet {
    Jet {
        v: t.mul(a.v, b.v),
        d: t.add(t.mul(a.d, b.v), t.mul(a.v, b.d)),
        d2: t.add(
            t.add(t.mul(a.d2, b.v), t.scale(t.mul(a.d, b.d), 2.)),
            t.mul(a.v, b.d2),
        ),
    }
}
pub fn jtanh(t: &Tape, a: Jet) -> Jet {
    let v = t.tanh(a.v);
    let f = t.sub(t.input(1.), t.mul(v, v));
    Jet {
        v,
        d: t.mul(f, a.d),
        d2: t.mul(f, t.sub(a.d2, t.scale(t.mul(v, t.mul(a.d, a.d)), 2.))),
    }
}
pub fn jet_network(t: &Tape, p: &[usize], input: &[Jet], h: usize) -> Jet {
    let d = input.len();
    require(p.len() == h * (d + 2) + 1, "network parameter count");
    let mut out = jconst(t, 0.);
    for j in 0..h {
        let mut z = Jet {
            v: p[h * d + j],
            d: t.input(0.),
            d2: t.input(0.),
        };
        for k in 0..d {
            let w = Jet {
                v: p[j * d + k],
                d: t.input(0.),
                d2: t.input(0.),
            };
            z = jadd(t, z, jmul(t, w, input[k]));
        }
        let a = jtanh(t, z);
        let w = Jet {
            v: p[h * d + h + j],
            d: t.input(0.),
            d2: t.input(0.),
        };
        out = jadd(t, out, jmul(t, w, a));
    }
    jadd(
        t,
        out,
        Jet {
            v: p[p.len() - 1],
            d: t.input(0.),
            d2: t.input(0.),
        },
    )
}
pub fn train_physics(kind: &str) -> Value {
    let d = if kind == "hnn" { 2 } else { 1 };
    let h = 8;
    let mut r = Rng { state: 17 };
    let mut weights: Vec<f64> = (0..h * (d + 2) + 1).map(|_| r.normal() * 0.25).collect();
    let epochs = if kind == "pinn" { 180 } else { 120 };
    let lr = if kind == "pinn" { 0.01 } else { 0.015 };
    let mut losses = vec![];
    for _ in 0..epochs {
        let t = Tape::new();
        let p: Vec<usize> = weights.iter().map(|w| t.input(*w)).collect();
        let mut loss = t.input(0.);
        let n = 24;
        for i in 0..n {
            let q = if kind == "pinn" {
                (i + 1) as f64 / (n + 1) as f64
            } else {
                -1.2 + 2.4 * i as f64 / (n - 1) as f64
            };
            let mut x = vec![jvar(&t, q, true)];
            if d == 2 {
                x.push(jvar(&t, (i as f64 * 1.7).sin(), false));
            }
            let z = jet_network(&t, &p, &x, h);
            let err = if kind == "pinn" {
                let factor = jmul(
                    &t,
                    x[0],
                    jadd(&t, jconst(&t, 1.), jmul(&t, jconst(&t, -1.), x[0])),
                );
                let u = jmul(&t, factor, z);
                t.add(
                    u.d2,
                    t.input(std::f64::consts::PI.powi(2) * (std::f64::consts::PI * q).sin()),
                )
            } else {
                t.sub(z.d, t.input(q))
            };
            loss = t.add(loss, t.scale(t.mul(err, err), 1. / n as f64));
            if kind == "hnn" {
                let pp = (i as f64 * 1.7).sin();
                let x2 = [jvar(&t, q, false), jvar(&t, pp, true)];
                let v = jet_network(&t, &p, &x2, h);
                let e = t.sub(v.d, t.input(pp));
                loss = t.add(loss, t.scale(t.mul(e, e), 1. / n as f64));
            }
        }
        losses.push(t.val(loss));
        let g = t.back(loss);
        let gn = p.iter().map(|k| g[*k] * g[*k]).sum::<f64>().sqrt();
        let clip = if gn > 20. { 20. / gn } else { 1. };
        for (i, &k) in p.iter().enumerate() {
            weights[i] -= lr * clip * g[k];
        }
    }
    let (mut grid, mut pred, mut truth) = (vec![], vec![], vec![]);
    for i in 0..81 {
        let q = if kind == "pinn" {
            i as f64 / 80.
        } else {
            -1. + 2. * i as f64 / 80.
        };
        let t = Tape::new();
        let p: Vec<usize> = weights.iter().map(|w| t.input(*w)).collect();
        let mut x = vec![jvar(&t, q, true)];
        if d == 2 {
            x.push(jvar(&t, 0.3, false));
        }
        let z = jet_network(&t, &p, &x, h);
        let (v, target) = if kind == "pinn" {
            (q * (1. - q) * t.val(z.v), (std::f64::consts::PI * q).sin())
        } else {
            (-t.val(z.d), -q)
        };
        grid.push(q);
        pred.push(v);
        truth.push(target);
    }
    json!({"model":kind,"origin":"manufactured analytical system","epochs":epochs,"hidden_width":h,"learning_rate":lr,"loss_history":losses,"grid":grid,"predictions":pred,"truth":truth,"rmse":rmse(&truth,&pred),"weights":weights,"derivatives":"forward second-order jets over a reverse-mode parameter tape","scope":"small native teaching architecture; LNN fixes unit mass and learns only potential"})
}
pub struct Classifier {
    pub w: Matrix,
    pub classes: Vec<i64>,
    pub loss: Vec<f64>,
}
impl Classifier {
    pub fn fit(x: &Matrix, y: &[i64], epochs: usize, lr: f64, penalty: f64) -> Self {
        let (n, d) = shape(x);
        require(n == y.len(), "classifier rows");
        let classes: Vec<i64> = y
            .iter()
            .copied()
            .collect::<BTreeSet<_>>()
            .into_iter()
            .collect();
        require(classes.len() > 1, "classifier needs two classes");
        let lookup: BTreeMap<i64, usize> =
            classes.iter().enumerate().map(|(i, k)| (*k, i)).collect();
        let k = classes.len();
        let mut w = zeros(k, d + 1);
        let mut hist = vec![];
        for _ in 0..epochs {
            let mut g = zeros(k, d + 1);
            let mut loss = 0.;
            for (i, row) in x.iter().enumerate() {
                let logits: Vec<f64> = (0..k).map(|c| dot(&w[c][..d], row) + w[c][d]).collect();
                let p = softmax(&logits);
                loss -= p[lookup[&y[i]]].max(1e-300).ln() / n as f64;
                for c in 0..k {
                    let e = p[c] - if c == lookup[&y[i]] { 1. } else { 0. };
                    for j in 0..d {
                        g[c][j] += e * row[j] / n as f64;
                    }
                    g[c][d] += e / n as f64;
                }
            }
            for c in 0..k {
                for j in 0..d {
                    loss += penalty * w[c][j] * w[c][j] / 2.;
                    g[c][j] += penalty * w[c][j];
                }
                for j in 0..=d {
                    w[c][j] -= lr * g[c][j];
                }
            }
            hist.push(loss);
        }
        Self {
            w,
            classes,
            loss: hist,
        }
    }
    pub fn predict(&self, x: &Matrix) -> (Vec<i64>, Matrix) {
        let (_, d) = shape(x);
        let mut out = vec![];
        let mut probs = vec![];
        for row in x {
            let z: Vec<f64> = (0..self.classes.len())
                .map(|k| dot(&self.w[k][..d], row) + self.w[k][d])
                .collect();
            let p = softmax(&z);
            let mut best = 0;
            for k in 0..p.len() {
                if p[k] > p[best] {
                    best = k;
                }
            }
            out.push(self.classes[best]);
            probs.push(p);
        }
        (out, probs)
    }
}
pub fn fit_predict(x: &Matrix, y: &[i64], tr: &[usize], va: &[usize], te: &[usize]) -> Value {
    let s = Scaler::fit(&rows(x, tr));
    let m = Classifier::fit(&s.transform(&rows(x, tr)), &labels(y, tr), 160, 0.15, 0.01);
    let (p, pr) = m.predict(&s.transform(&rows(x, te)));
    let (pv, _) = m.predict(&s.transform(&rows(x, va)));
    json!({"accuracy":accuracy(&labels(y,te),&p),"validation_accuracy":accuracy(&labels(y,va),&pv),"truth":labels(y,te),"predictions":p,"probabilities":pr,"scaler_mean":s.mean,"scaler_scale":s.scale,"weights":m.w,"loss_history":m.loss})
}
pub fn ridge(x: &Matrix, y: &[f64], lambda: f64) -> (Vec<f64>, f64) {
    let (n, d) = shape(x);
    require(
        n == y.len() && lambda.is_finite() && lambda >= 0.,
        "ridge input",
    );
    let mx = mean_rows(x);
    let mut centered = x.clone();
    for row in &mut centered {
        for j in 0..d {
            row[j] -= mx[j];
        }
    }
    let mu = mean(y);
    let mut a = zeros(d, d);
    let mut b = vec![0.; d];
    for (i, row) in centered.iter().enumerate() {
        for j in 0..d {
            b[j] += row[j] * (y[i] - mu);
            for k in 0..d {
                a[j][k] += row[j] * row[k];
            }
        }
    }
    for j in 0..d {
        a[j][j] += lambda;
    }
    let w = solve(&a, &b);
    let intercept = mu - dot(&mx, &w);
    (w, intercept)
}
pub fn predict_ridge(x: &Matrix, w: &[f64], b: f64) -> Vec<f64> {
    x.iter().map(|r| dot(r, w) + b).collect()
}
pub fn regression_result(
    x: &Matrix,
    y: &[f64],
    tr: &[usize],
    va: &[usize],
    te: &[usize],
    conformal: bool,
) -> Value {
    let s = Scaler::fit(&rows(x, tr));
    let (w, b) = ridge(&s.transform(&rows(x, tr)), &values(y, tr), 1.);
    let p = predict_ridge(&s.transform(&rows(x, te)), &w, b);
    let pv = predict_ridge(&s.transform(&rows(x, va)), &w, b);
    let mut out = json!({"train_rows":tr,"validation_rows":va,"test_rows":te,"truth":values(y,te),"predictions":p,"mae":mae(&values(y,te),&p),"rmse":rmse(&values(y,te),&p),"baseline_mae":mae(&values(y,te),&vec![b;te.len()]),"scaler_mean":s.mean,"scaler_scale":s.scale,"weights":w,"intercept":b});
    if conformal {
        let mut residuals: Vec<f64> = va
            .iter()
            .enumerate()
            .map(|(i, &k)| (y[k] - pv[i]).abs())
            .collect();
        residuals.sort_by(f64::total_cmp);
        let rank = (0.9 * (va.len() + 1) as f64).ceil() as usize;
        require(rank <= residuals.len(), "insufficient calibration");
        let q = residuals[rank - 1];
        let covered = p
            .iter()
            .enumerate()
            .filter(|(i, v)| (y[te[*i]] - **v).abs() <= q)
            .count();
        let bounds: Matrix = p.iter().map(|v| vec![v - q, v + q]).collect();
        out["nominal_coverage"] = json!(0.9);
        out["interval_radius"] = json!(q);
        out["intervals"] = json!(bounds);
        out["covered"] = json!(covered);
        out["calibration_rows"] = json!(va);
        out["interpretation"] =
            json!("marginal split-conformal illustration, no batch-conditional guarantee");
    }
    out
}
pub fn gaussian_penalty(z: &Matrix, dirs: &Matrix) -> (f64, Matrix) {
    let (n, d) = shape(z);
    let (k, _) = shape(dirs);
    let mut g = zeros(n, d);
    let mut loss = 0.;
    let freq = [0.25, 0.5, 1., 1.5, 2.];
    for dir in dirs {
        require(dir.len() == d, "projection dimensions");
        let u: Vec<f64> = z.iter().map(|v| dot(v, dir)).collect();
        for t in freq {
            let (mut re, mut im) = (0., 0.);
            for v in &u {
                re += (t * v).cos() / n as f64;
                im += (t * v).sin() / n as f64;
            }
            let target = (-t * t / 2.).exp();
            let w = (-t * t / 2.).exp() / (k * freq.len()) as f64;
            loss += w * ((re - target) * (re - target) + im * im);
            for (i, v) in u.iter().enumerate() {
                let du =
                    2. * w * t * (-(re - target) * (t * v).sin() + im * (t * v).cos()) / n as f64;
                for j in 0..d {
                    g[i][j] += du * dir[j];
                }
            }
        }
    }
    (loss, g)
}
pub fn directions(d: usize, k: usize, seed: u32) -> Matrix {
    let mut r = Rng { state: seed };
    let mut a = zeros(k, d);
    for row in &mut a {
        for v in row.iter_mut() {
            *v = r.normal();
        }
        let s = norm(row);
        for v in row {
            *v /= s;
        }
    }
    a
}
#[derive(Serialize)]
pub struct Encoder {
    #[serde(rename = "W1")]
    pub w1: Matrix,
    #[serde(rename = "W2")]
    pub w2: Matrix,
    #[serde(rename = "B1")]
    pub b1: Vec<f64>,
    #[serde(rename = "B2")]
    pub b2: Vec<f64>,
}
impl Encoder {
    pub fn new(d: usize, h: usize, z: usize, seed: u32) -> Self {
        let mut r = Rng { state: seed };
        let mut e = Self {
            w1: zeros(h, d),
            w2: zeros(z, h),
            b1: vec![0.; h],
            b2: vec![0.; z],
        };
        for row in &mut e.w1 {
            for v in row {
                *v = r.normal() / (d as f64).sqrt();
            }
        }
        for row in &mut e.w2 {
            for v in row {
                *v = r.normal() / (h as f64).sqrt();
            }
        }
        e
    }
    pub fn forward(&self, x: &Matrix) -> (Matrix, Matrix) {
        let mut h = zeros(x.len(), self.b1.len());
        let mut z = zeros(x.len(), self.b2.len());
        for (i, row) in x.iter().enumerate() {
            for j in 0..self.b1.len() {
                h[i][j] = (dot(&self.w1[j], row) + self.b1[j]).tanh();
            }
            for j in 0..self.b2.len() {
                z[i][j] = dot(&self.w2[j], &h[i]) + self.b2[j];
            }
        }
        (h, z)
    }
    pub fn update(&mut self, x: &Matrix, h: &Matrix, g: &Matrix, lr: f64) {
        let (mut dw1, mut dw2) = (
            zeros(self.w1.len(), self.w1[0].len()),
            zeros(self.w2.len(), self.w2[0].len()),
        );
        let (mut db1, mut db2) = (vec![0.; self.b1.len()], vec![0.; self.b2.len()]);
        for (i, row) in x.iter().enumerate() {
            let mut dh = vec![0.; self.b1.len()];
            for j in 0..self.b2.len() {
                db2[j] += g[i][j];
                for k in 0..self.b1.len() {
                    dw2[j][k] += g[i][j] * h[i][k];
                    dh[k] += g[i][j] * self.w2[j][k];
                }
            }
            for k in 0..self.b1.len() {
                let v = dh[k] * (1. - h[i][k] * h[i][k]);
                db1[k] += v;
                for j in 0..row.len() {
                    dw1[k][j] += v * row[j];
                }
            }
        }
        for i in 0..self.w1.len() {
            self.b1[i] -= lr * db1[i];
            for j in 0..self.w1[i].len() {
                self.w1[i][j] -= lr * dw1[i][j];
            }
        }
        for i in 0..self.w2.len() {
            self.b2[i] -= lr * db2[i];
            for j in 0..self.w2[i].len() {
                self.w2[i][j] -= lr * dw2[i][j];
            }
        }
    }
}
pub fn train_encoder(x: &Matrix, seed: u32, regularized: bool) -> (Encoder, Vec<f64>) {
    let (_, d) = shape(x);
    let mut e = Encoder::new(d, 16, 8, seed);
    let dirs = directions(8, 6, 101);
    let mut rng = Rng { state: seed + 44 };
    let mut losses = vec![];
    let mut order: Vec<usize> = (0..x.len()).collect();
    for epoch in 0..8 {
        shuffle(&mut order, seed + epoch + 1);
        let mut total = 0.;
        for start in (0..order.len()).step_by(64) {
            let idx = &order[start..(start + 64).min(order.len())];
            let batch = rows(x, idx);
            let mut aug = batch.clone();
            for row in &mut aug {
                for v in row {
                    *v += 0.02 * rng.normal();
                }
            }
            let (h, z) = e.forward(&batch);
            let (h2, z2) = e.forward(&aug);
            let (mut g, mut g2) = (zeros(z.len(), 8), zeros(z.len(), 8));
            let mut loss = 0.;
            for i in 0..z.len() {
                for j in 0..8 {
                    let diff = z[i][j] - z2[i][j];
                    loss += diff * diff / (z.len() * 8) as f64;
                    g[i][j] = 2. * diff / (z.len() * 8) as f64;
                    g2[i][j] = -g[i][j];
                }
            }
            if regularized {
                let (p, pg) = gaussian_penalty(&z, &dirs);
                loss += p;
                for i in 0..g.len() {
                    for j in 0..8 {
                        g[i][j] += pg[i][j];
                    }
                }
            }
            let mut joined_x = batch.clone();
            joined_x.extend(aug);
            let mut joined_h = h;
            joined_h.extend(h2);
            let mut joined_g = g;
            joined_g.extend(g2);
            e.update(&joined_x, &joined_h, &joined_g, 0.08);
            total += loss * batch.len() as f64 / x.len() as f64;
        }
        losses.push(total);
    }
    (e, losses)
}
