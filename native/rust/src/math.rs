//! Small explicit f64 kernels. They favor inspection over optimized BLAS speed.
use serde::Serialize;
use serde_json::{json, Value};
use std::collections::BTreeMap;
pub type Matrix = Vec<Vec<f64>>;
pub fn require(ok: bool, msg: &str) {
    assert!(ok, "{msg}");
}
pub fn zeros(n: usize, m: usize) -> Matrix {
    vec![vec![0.; m]; n]
}
pub fn eye(n: usize) -> Matrix {
    let mut a = zeros(n, n);
    for i in 0..n {
        a[i][i] = 1.;
    }
    a
}
pub fn shape(a: &Matrix) -> (usize, usize) {
    require(!a.is_empty() && !a[0].is_empty(), "empty matrix");
    let m = a[0].len();
    for r in a {
        require(r.len() == m, "ragged matrix");
        require(r.iter().all(|x| x.is_finite()), "nonfinite matrix");
    }
    (a.len(), m)
}
pub fn dot(a: &[f64], b: &[f64]) -> f64 {
    require(a.len() == b.len(), "dot length mismatch");
    let mut s = 0.;
    for i in 0..a.len() {
        s += a[i] * b[i];
    }
    s
}
pub fn norm(a: &[f64]) -> f64 {
    dot(a, a).sqrt()
}
pub fn sub(a: &[f64], b: &[f64]) -> Vec<f64> {
    require(a.len() == b.len(), "vector length mismatch");
    a.iter().zip(b).map(|(x, y)| x - y).collect()
}
pub fn distance(a: &[f64], b: &[f64]) -> f64 {
    norm(&sub(a, b))
}
pub fn mean(a: &[f64]) -> f64 {
    require(
        !a.is_empty() && a.iter().all(|x| x.is_finite()),
        "invalid mean",
    );
    let mut s = 0.;
    for x in a {
        s += x;
    }
    s / a.len() as f64
}
pub fn mean_rows(a: &Matrix) -> Vec<f64> {
    let (n, m) = shape(a);
    let mut v = vec![0.; m];
    for r in a {
        for j in 0..m {
            v[j] += r[j] / n as f64;
        }
    }
    v
}
pub fn transpose(a: &Matrix) -> Matrix {
    let (n, m) = shape(a);
    let mut b = zeros(m, n);
    for i in 0..n {
        for j in 0..m {
            b[j][i] = a[i][j];
        }
    }
    b
}
pub fn matmul(a: &Matrix, b: &Matrix) -> Matrix {
    let (n, k) = shape(a);
    let (k2, m) = shape(b);
    require(k == k2, "matrix product dimensions");
    let mut c = zeros(n, m);
    for i in 0..n {
        for h in 0..k {
            for j in 0..m {
                c[i][j] += a[i][h] * b[h][j];
            }
        }
    }
    c
}
pub fn matvec(a: &Matrix, b: &[f64]) -> Vec<f64> {
    let (_, m) = shape(a);
    require(m == b.len(), "matrix-vector dimensions");
    a.iter().map(|r| dot(r, b)).collect()
}
pub fn rank(a: &Matrix, tol: f64) -> usize {
    let (n, m) = shape(a);
    require(tol > 0., "positive tolerance required");
    let mut b = a.clone();
    let mut r = 0;
    for c in 0..m {
        if r == n {
            break;
        }
        let mut p = r;
        for i in r + 1..n {
            if b[i][c].abs() > b[p][c].abs() {
                p = i;
            }
        }
        if b[p][c].abs() <= tol {
            continue;
        }
        b.swap(p, r);
        let pivot = b[r][c];
        for j in c..m {
            b[r][j] /= pivot;
        }
        for i in 0..n {
            if i != r {
                let f = b[i][c];
                for j in c..m {
                    b[i][j] -= f * b[r][j];
                }
            }
        }
        r += 1;
    }
    r
}
pub fn rank2(a: &Matrix) -> usize {
    let (n, m) = shape(a);
    let mut b = vec![vec![0u8; m]; n];
    for i in 0..n {
        for j in 0..m {
            require(a[i][j] == a[i][j].trunc(), "F2 integer input required");
            b[i][j] = (a[i][j] as i64 & 1) as u8;
        }
    }
    let mut r = 0;
    for c in 0..m {
        if r == n {
            break;
        }
        let mut p = r;
        while p < n && b[p][c] == 0 {
            p += 1;
        }
        if p == n {
            continue;
        }
        b.swap(p, r);
        for i in 0..n {
            if i != r && b[i][c] != 0 {
                for j in c..m {
                    b[i][j] ^= b[r][j];
                }
            }
        }
        r += 1;
    }
    r
}
pub fn solve(a: &Matrix, b: &[f64]) -> Vec<f64> {
    let (n, m) = shape(a);
    require(n == m && b.len() == n, "square system required");
    let mut z = a.clone();
    let mut y = b.to_vec();
    for c in 0..n {
        let mut p = c;
        for i in c + 1..n {
            if z[i][c].abs() > z[p][c].abs() {
                p = i;
            }
        }
        require(z[p][c].abs() > 1e-13, "singular linear system");
        z.swap(p, c);
        y.swap(p, c);
        let v = z[c][c];
        for j in c..n {
            z[c][j] /= v;
        }
        y[c] /= v;
        for i in 0..n {
            if i != c {
                let f = z[i][c];
                for j in c..n {
                    z[i][j] -= f * z[c][j];
                }
                y[i] -= f * y[c];
            }
        }
    }
    y
}
pub fn cov(a: &Matrix) -> Matrix {
    let (n, m) = shape(a);
    require(n > 1, "sample covariance needs two rows");
    let mu = mean_rows(a);
    let mut c = zeros(m, m);
    for r in a {
        for i in 0..m {
            for j in 0..m {
                c[i][j] += (r[i] - mu[i]) * (r[j] - mu[j]) / (n - 1) as f64;
            }
        }
    }
    c
}
pub fn eigen_sym(a: &Matrix) -> (Vec<f64>, Matrix) {
    let (n, m) = shape(a);
    require(n == m, "square eigensystem required");
    for i in 0..n {
        for j in 0..n {
            require((a[i][j] - a[j][i]).abs() < 1e-8, "matrix not symmetric");
        }
    }
    let mut b = a.clone();
    let mut v = eye(n);
    for _ in 0..100 * n * n {
        let (mut p, mut q, mut mx) = (0, 0, 0.);
        for i in 0..n {
            for j in i + 1..n {
                if b[i][j].abs() > mx {
                    mx = b[i][j].abs();
                    p = i;
                    q = j;
                }
            }
        }
        if mx < 1e-12 {
            break;
        }
        let theta = 0.5 * (2. * b[p][q]).atan2(b[q][q] - b[p][p]);
        let (c, s) = (theta.cos(), theta.sin());
        let (app, aqq, apq) = (b[p][p], b[q][q], b[p][q]);
        for k in 0..n {
            if k != p && k != q {
                let (x, y) = (b[k][p], b[k][q]);
                b[k][p] = c * x - s * y;
                b[p][k] = b[k][p];
                b[k][q] = s * x + c * y;
                b[q][k] = b[k][q];
            }
            let (x, y) = (v[k][p], v[k][q]);
            v[k][p] = c * x - s * y;
            v[k][q] = s * x + c * y;
        }
        b[p][p] = c * c * app - 2. * s * c * apq + s * s * aqq;
        b[q][q] = s * s * app + 2. * s * c * apq + c * c * aqq;
        b[p][q] = 0.;
        b[q][p] = 0.;
    }
    let mut order: Vec<usize> = (0..n).collect();
    order.sort_by(|i, j| b[*j][*j].total_cmp(&b[*i][*i]));
    let mut e = vec![0.; n];
    let mut w = zeros(n, n);
    for (j, k) in order.iter().enumerate() {
        e[j] = b[*k][*k];
        for i in 0..n {
            w[i][j] = v[i][*k];
        }
    }
    (e, w)
}
#[derive(Clone, Serialize)]
pub struct Scaler {
    #[serde(rename = "Mean")]
    pub mean: Vec<f64>,
    #[serde(rename = "Scale")]
    pub scale: Vec<f64>,
}
impl Scaler {
    pub fn fit(a: &Matrix) -> Self {
        let (n, m) = shape(a);
        let mu = mean_rows(a);
        let mut s = vec![0.; m];
        for r in a {
            for j in 0..m {
                s[j] += (r[j] - mu[j]) * (r[j] - mu[j]) / n as f64;
            }
        }
        for q in &mut s {
            *q = q.sqrt();
            if *q < 1e-12 {
                *q = 1.;
            }
        }
        Self { mean: mu, scale: s }
    }
    pub fn transform(&self, a: &Matrix) -> Matrix {
        let (_, m) = shape(a);
        require(m == self.mean.len(), "scaler columns");
        let mut b = a.clone();
        for r in &mut b {
            for j in 0..m {
                r[j] = (r[j] - self.mean[j]) / self.scale[j];
            }
        }
        b
    }
}
pub struct Rng {
    pub state: u32,
}
impl Rng {
    pub fn next(&mut self) -> u32 {
        if self.state == 0 {
            self.state = 1;
        }
        let mut x = self.state;
        x ^= x << 13;
        x ^= x >> 17;
        x ^= x << 5;
        self.state = x;
        x
    }
    pub fn uniform(&mut self) -> f64 {
        (self.next() as f64 + 0.5) / 4294967296.
    }
    pub fn normal(&mut self) -> f64 {
        (-2. * self.uniform().ln()).sqrt() * (2. * std::f64::consts::PI * self.uniform()).cos()
    }
}
pub fn shuffle(a: &mut [usize], seed: u32) {
    let mut r = Rng { state: seed };
    for i in (1..a.len()).rev() {
        let j = (r.next() % (i + 1) as u32) as usize;
        a.swap(i, j);
    }
}
pub fn rows(a: &Matrix, idx: &[usize]) -> Matrix {
    idx.iter().map(|&k| a[k].clone()).collect()
}
pub fn values(a: &[f64], idx: &[usize]) -> Vec<f64> {
    idx.iter().map(|&k| a[k]).collect()
}
pub fn labels(a: &[i64], idx: &[usize]) -> Vec<i64> {
    idx.iter().map(|&k| a[k]).collect()
}
pub fn stratified(y: &[i64], seed: u32) -> (Vec<usize>, Vec<usize>, Vec<usize>) {
    let mut groups: BTreeMap<i64, Vec<usize>> = BTreeMap::new();
    for (i, k) in y.iter().enumerate() {
        groups.entry(*k).or_default().push(i);
    }
    let (mut tr, mut va, mut te) = (vec![], vec![], vec![]);
    for (h, (_, a)) in groups.iter_mut().enumerate() {
        shuffle(a, seed + 31 * h as u32);
        let (n1, n2) = (a.len() * 6 / 10, a.len() * 8 / 10);
        require(n1 > 0 && n2 > n1 && a.len() > n2, "class too small");
        tr.extend_from_slice(&a[..n1]);
        va.extend_from_slice(&a[n1..n2]);
        te.extend_from_slice(&a[n2..]);
    }
    tr.sort();
    va.sort();
    te.sort();
    (tr, va, te)
}
pub fn accuracy(y: &[i64], p: &[i64]) -> f64 {
    require(!y.is_empty() && y.len() == p.len(), "accuracy length");
    y.iter().zip(p).filter(|(a, b)| a == b).count() as f64 / y.len() as f64
}
pub fn mae(y: &[f64], p: &[f64]) -> f64 {
    require(!y.is_empty() && y.len() == p.len(), "MAE length");
    y.iter().zip(p).map(|(a, b)| (a - b).abs()).sum::<f64>() / y.len() as f64
}
pub fn rmse(y: &[f64], p: &[f64]) -> f64 {
    require(!y.is_empty() && y.len() == p.len(), "RMSE length");
    (y.iter().zip(p).map(|(a, b)| (a - b) * (a - b)).sum::<f64>() / y.len() as f64).sqrt()
}
pub fn softmax(a: &[f64]) -> Vec<f64> {
    require(!a.is_empty(), "empty softmax");
    let mx = a.iter().copied().fold(f64::NEG_INFINITY, f64::max);
    let mut p: Vec<f64> = a.iter().map(|x| (x - mx).exp()).collect();
    let s: f64 = p.iter().sum();
    for v in &mut p {
        *v /= s;
    }
    p
}
pub fn median(a: &[f64]) -> f64 {
    require(!a.is_empty(), "empty median");
    let mut b = a.to_vec();
    b.sort_by(f64::total_cmp);
    (b[(b.len() - 1) / 2] + b[b.len() / 2]) / 2.
}
pub fn describe(a: &[f64]) -> Value {
    require(!a.is_empty(), "empty describe");
    json!({"n":a.len(),"mean":mean(a),"median":median(a),"min":a.iter().copied().fold(f64::INFINITY,f64::min),"max":a.iter().copied().fold(f64::NEG_INFINITY,f64::max)})
}
pub fn safe_number(v: f64) -> Value {
    if v.is_nan() {
        json!("NaN")
    } else if v == f64::INFINITY {
        json!("+Inf")
    } else if v == f64::NEG_INFINITY {
        json!("-Inf")
    } else {
        json!(v)
    }
}
