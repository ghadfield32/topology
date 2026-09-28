//! Finite simplicial persistence over F2, with explicit filtration conventions.
use crate::math::*;
use serde::Serialize;
use serde_json::{json, Value};
use std::collections::{BTreeMap, BTreeSet};
#[derive(Clone, Serialize)]
pub struct Simplex {
    pub vertices: Vec<usize>,
    pub value: f64,
}
#[derive(Clone, Serialize)]
pub struct Interval {
    pub dimension: usize,
    pub birth: f64,
    pub death: Option<f64>,
}
pub fn ordered(c: &[Simplex]) -> Vec<Simplex> {
    let mut d = c.to_vec();
    for s in &mut d {
        s.vertices.sort();
        require(
            !s.vertices.is_empty() && s.value.is_finite(),
            "invalid simplex",
        );
        require(
            !s.vertices.windows(2).any(|w| w[0] == w[1]),
            "repeated vertex",
        );
    }
    d.sort_by(|a, b| {
        a.value
            .total_cmp(&b.value)
            .then(a.vertices.len().cmp(&b.vertices.len()))
            .then(a.vertices.cmp(&b.vertices))
    });
    let mut seen: BTreeMap<Vec<usize>, usize> = BTreeMap::new();
    for (i, s) in d.iter().enumerate() {
        require(!seen.contains_key(&s.vertices), "duplicate simplex");
        if s.vertices.len() > 1 {
            for q in 0..s.vertices.len() {
                let mut f = s.vertices.clone();
                f.remove(q);
                let j = seen.get(&f).expect("missing face or decreasing filtration");
                require(d[*j].value <= s.value, "decreasing filtration");
            }
        }
        seen.insert(s.vertices.clone(), i);
    }
    d
}
pub fn rips(x: &Matrix, epsilon: f64, maxdim: usize) -> Vec<Simplex> {
    let (n, _) = shape(x);
    require(
        n <= 96 && maxdim <= 3 && epsilon >= 0.,
        "Rips teaching bounds",
    );
    let mut d = zeros(n, n);
    for i in 0..n {
        for j in 0..i {
            d[i][j] = distance(&x[i], &x[j]);
            d[j][i] = d[i][j];
        }
    }
    fn rec(
        v: Vec<usize>,
        start: usize,
        birth: f64,
        d: &Matrix,
        e: f64,
        dim: usize,
        c: &mut Vec<Simplex>,
    ) {
        if !v.is_empty() {
            c.push(Simplex {
                vertices: v.clone(),
                value: birth,
            });
            require(c.len() <= 200000, "simplex budget exceeded");
        }
        if v.len() >= dim + 1 {
            return;
        }
        for j in start..d.len() {
            let mut b = birth;
            let mut ok = true;
            for &i in &v {
                if d[i][j] > e {
                    ok = false;
                    break;
                }
                b = b.max(d[i][j]);
            }
            if ok {
                let mut w = v.clone();
                w.push(j);
                rec(w, j + 1, b, d, e, dim, c);
            }
        }
    }
    let mut c = vec![];
    rec(vec![], 0, 0., &d, epsilon, maxdim, &mut c);
    ordered(&c)
}
pub fn xor_sorted(a: &[usize], b: &[usize]) -> Vec<usize> {
    let (mut i, mut j) = (0, 0);
    let mut out = vec![];
    while i < a.len() || j < b.len() {
        if j == b.len() || (i < a.len() && a[i] < b[j]) {
            out.push(a[i]);
            i += 1;
        } else if i == a.len() || b[j] < a[i] {
            out.push(b[j]);
            j += 1;
        } else {
            i += 1;
            j += 1;
        }
    }
    out
}
pub fn persistence(c: &[Simplex]) -> Vec<Interval> {
    let c = ordered(c);
    let index: BTreeMap<Vec<usize>, usize> = c
        .iter()
        .enumerate()
        .map(|(i, s)| (s.vertices.clone(), i))
        .collect();
    let mut reduced: Vec<Vec<usize>> = vec![vec![]; c.len()];
    let mut pivots: BTreeMap<usize, usize> = BTreeMap::new();
    let mut born = BTreeSet::new();
    let mut out = vec![];
    for (j, s) in c.iter().enumerate() {
        let mut col = vec![];
        if s.vertices.len() > 1 {
            for q in 0..s.vertices.len() {
                let mut f = s.vertices.clone();
                f.remove(q);
                col.push(index[&f]);
            }
            col.sort();
        }
        while let Some(lo) = col.last() {
            if let Some(k) = pivots.get(lo) {
                col = xor_sorted(&col, &reduced[*k]);
            } else {
                break;
            }
        }
        reduced[j] = col.clone();
        if col.is_empty() {
            born.insert(j);
        } else {
            let lo = *col.last().unwrap();
            pivots.insert(lo, j);
            born.remove(&lo);
            if s.value > c[lo].value + 1e-12 {
                out.push(Interval {
                    dimension: c[lo].vertices.len() - 1,
                    birth: c[lo].value,
                    death: Some(s.value),
                });
            }
        }
    }
    for i in born {
        out.push(Interval {
            dimension: c[i].vertices.len() - 1,
            birth: c[i].value,
            death: None,
        });
    }
    out.sort_by(|a, b| {
        a.dimension
            .cmp(&b.dimension)
            .then(a.birth.total_cmp(&b.birth))
            .then(
                a.death
                    .unwrap_or(f64::INFINITY)
                    .total_cmp(&b.death.unwrap_or(f64::INFINITY)),
            )
    });
    out
}
pub fn betti(c: &[Simplex]) -> Vec<usize> {
    let d = c.iter().map(|s| s.vertices.len()).max().unwrap_or(0);
    let mut b = vec![0; d];
    for x in persistence(c) {
        if x.death.is_none() {
            b[x.dimension] += 1;
        }
    }
    b
}
pub fn triangle(filled: bool) -> Vec<Simplex> {
    let mut c = vec![];
    for v in [
        vec![0],
        vec![1],
        vec![2],
        vec![0, 1],
        vec![0, 2],
        vec![1, 2],
    ] {
        c.push(Simplex {
            vertices: v,
            value: 0.,
        });
    }
    if filled {
        c.push(Simplex {
            vertices: vec![0, 1, 2],
            value: 0.,
        });
    }
    c
}
pub fn tetra(filled: bool) -> Vec<Simplex> {
    let mut c = vec![];
    for mask in 1..16 {
        let v: Vec<usize> = (0..4).filter(|j| mask & (1 << j) != 0).collect();
        if v.len() < 4 || filled {
            c.push(Simplex {
                vertices: v,
                value: 0.,
            });
        }
    }
    ordered(&c)
}
pub fn mst(x: &Matrix) -> Vec<f64> {
    let (n, _) = shape(x);
    let mut d = vec![f64::INFINITY; n];
    let mut used = vec![false; n];
    d[0] = 0.;
    let mut edges = vec![];
    for k in 0..n {
        let v = (0..n)
            .filter(|i| !used[*i])
            .min_by(|i, j| d[*i].total_cmp(&d[*j]))
            .unwrap();
        used[v] = true;
        if k > 0 {
            edges.push(d[v]);
        }
        for j in 0..n {
            if !used[j] {
                d[j] = d[j].min(distance(&x[v], &x[j]));
            }
        }
    }
    edges.sort_by(f64::total_cmp);
    edges
}
pub fn components(x: &Matrix, r: f64) -> Vec<Vec<usize>> {
    let (n, _) = shape(x);
    require(r >= 0., "negative radius");
    let mut seen = vec![false; n];
    let mut out = vec![];
    for s in 0..n {
        if seen[s] {
            continue;
        }
        let mut q = vec![s];
        seen[s] = true;
        let mut h = 0;
        while h < q.len() {
            let i = q[h];
            for j in 0..n {
                if !seen[j] && distance(&x[i], &x[j]) <= r {
                    seen[j] = true;
                    q.push(j);
                }
            }
            h += 1;
        }
        q.sort();
        out.push(q);
    }
    out
}
fn find(parent: &mut [usize], mut x: usize) -> usize {
    while parent[x] != x {
        parent[x] = parent[parent[x]];
        x = parent[x];
    }
    x
}
pub fn pixel_betti(p: &[f64], h: usize, w: usize, t: f64) -> Vec<i64> {
    require(h * w == p.len(), "pixel shape");
    let mut vertices = BTreeSet::new();
    let mut edges = BTreeSet::new();
    let mut faces = 0;
    for y in 0..h {
        for x in 0..w {
            if p[y * w + x] < t {
                continue;
            }
            faces += 1;
            let a = y * (w + 1) + x;
            let pts = [a, a + 1, a + w + 1, a + w + 2];
            vertices.extend(pts);
            edges.extend([
                (pts[0], pts[1]),
                (pts[0], pts[2]),
                (pts[1], pts[3]),
                (pts[2], pts[3]),
            ]);
        }
    }
    let mut parent: Vec<usize> = (0..(h + 1) * (w + 1)).collect();
    for (a, b) in &edges {
        let fa = find(&mut parent, *a);
        let fb = find(&mut parent, *b);
        parent[fa] = fb;
    }
    let roots: BTreeSet<usize> = vertices.iter().map(|v| find(&mut parent, *v)).collect();
    let b0 = roots.len() as i64;
    let chi = vertices.len() as i64 - edges.len() as i64 + faces;
    vec![b0, b0 - chi]
}
pub fn pixel_filtration(p: &[f64], h: usize, w: usize) -> Vec<Simplex> {
    require(h * w == p.len(), "pixel shape");
    let mut c: BTreeMap<Vec<usize>, f64> = BTreeMap::new();
    for y in 0..h {
        for x in 0..w {
            let a = y * (w + 1) + x;
            let val = -p[y * w + x];
            for tri in [[a, a + 1, a + w + 2], [a, a + w + 1, a + w + 2]] {
                for mask in 1..8 {
                    let mut v: Vec<usize> = (0..3)
                        .filter(|j| mask & (1 << j) != 0)
                        .map(|j| tri[j])
                        .collect();
                    v.sort();
                    let old = c.entry(v).or_insert(val);
                    *old = old.min(val);
                }
            }
        }
    }
    let s: Vec<Simplex> = c
        .into_iter()
        .map(|(v, f)| Simplex {
            vertices: v,
            value: f,
        })
        .collect();
    ordered(&s)
}
pub fn dimension(d: &[Interval], k: usize) -> Vec<Interval> {
    d.iter().filter(|v| v.dimension == k).cloned().collect()
}
pub fn bottleneck(a: &[Interval], b: &[Interval]) -> f64 {
    let mut dimension = None;
    for v in a.iter().chain(b) {
        require(
            v.birth.is_finite()
                && v.death
                    .map(|d| d.is_finite() && d >= v.birth)
                    .unwrap_or(true),
            "invalid persistence interval",
        );
        if let Some(k) = dimension {
            require(v.dimension == k, "compare one homology dimension at a time")
        } else {
            dimension = Some(v.dimension)
        }
    }
    let mut ae: Vec<f64> = a
        .iter()
        .filter(|v| v.death.is_none())
        .map(|v| v.birth)
        .collect();
    let mut be: Vec<f64> = b
        .iter()
        .filter(|v| v.death.is_none())
        .map(|v| v.birth)
        .collect();
    if ae.len() != be.len() {
        return f64::INFINITY;
    }
    ae.sort_by(f64::total_cmp);
    be.sort_by(f64::total_cmp);
    let essential = ae
        .iter()
        .zip(&be)
        .map(|(x, y)| (x - y).abs())
        .fold(0., f64::max);
    let af: Vec<_> = a.iter().filter(|v| v.death.is_some()).collect();
    let bf: Vec<_> = b.iter().filter(|v| v.death.is_some()).collect();
    let (n, m) = (af.len(), bf.len());
    let total = n + m;
    if total == 0 {
        return essential;
    }
    let mut cost = zeros(total, total);
    let mut candidates = vec![0.];
    for i in 0..total {
        for j in 0..total {
            let d = if i < n && j < m {
                (af[i].birth - bf[j].birth)
                    .abs()
                    .max((af[i].death.unwrap() - bf[j].death.unwrap()).abs())
            } else if i < n {
                (af[i].death.unwrap() - af[i].birth) / 2.
            } else if j < m {
                (bf[j].death.unwrap() - bf[j].birth) / 2.
            } else {
                0.
            };
            cost[i][j] = d;
            candidates.push(d);
        }
    }
    candidates.sort_by(f64::total_cmp);
    fn visit(i: usize, seen: &mut [bool], p: &mut [Option<usize>], cost: &Matrix, e: f64) -> bool {
        for j in 0..p.len() {
            if !seen[j] && cost[i][j] <= e + 1e-12 {
                seen[j] = true;
                if p[j].is_none() || visit(p[j].unwrap(), seen, p, cost, e) {
                    p[j] = Some(i);
                    return true;
                }
            }
        }
        false
    }
    let matches = |e: f64| {
        let mut p = vec![None; total];
        for i in 0..total {
            if !visit(i, &mut vec![false; total], &mut p, &cost, e) {
                return false;
            }
        }
        true
    };
    let (mut lo, mut hi) = (0, candidates.len() - 1);
    while lo < hi {
        let mid = (lo + hi) / 2;
        if matches(candidates[mid]) {
            hi = mid;
        } else {
            lo = mid + 1;
        }
    }
    essential.max(candidates[lo])
}
pub fn topo_feature(query: &[f64], refs: &Matrix) -> Vec<f64> {
    require(refs.len() >= 4, "four reference points required");
    let mut order: Vec<usize> = (0..refs.len()).collect();
    order.sort_by(|i, j| distance(query, &refs[*i]).total_cmp(&distance(query, &refs[*j])));
    let k = 7.min(refs.len());
    let mut cloud = vec![query.to_vec()];
    let mut ds = vec![];
    for i in &order[..k] {
        cloud.push(refs[*i].clone());
        ds.push(distance(query, &refs[*i]));
    }
    let h0 = mst(&cloud);
    let ints = persistence(&rips(&cloud, f64::INFINITY, 2));
    let life: Vec<f64> = ints
        .iter()
        .filter(|v| v.dimension == 1 && v.death.is_some())
        .map(|v| v.death.unwrap() - v.birth)
        .collect();
    let maxlife = life.iter().copied().fold(0., f64::max);
    let sumlife: f64 = life.iter().sum();
    vec![
        mean(&ds),
        ds[0],
        ds[ds.len() - 1],
        mean(&h0),
        h0[h0.len() - 1],
        maxlife,
        sumlife,
    ]
}
pub fn mapper(x: &Matrix, bins: usize, overlap: f64, radius: f64) -> Value {
    require(bins > 1 && (0.0..1.0).contains(&overlap), "Mapper cover");
    let lens: Vec<f64> = x.iter().map(|r| r[0]).collect();
    let lo = lens.iter().copied().fold(f64::INFINITY, f64::min);
    let hi = lens.iter().copied().fold(f64::NEG_INFINITY, f64::max);
    let width = (hi - lo) / (bins as f64 - (bins - 1) as f64 * overlap);
    let step = width * (1. - overlap);
    let mut nodes: Vec<Vec<usize>> = vec![];
    for b in 0..bins {
        let low = lo + b as f64 * step;
        let high = low + width;
        let ids: Vec<usize> = (0..x.len())
            .filter(|i| lens[*i] >= low - 1e-12 && lens[*i] <= high + 1e-12)
            .collect();
        if ids.is_empty() {
            continue;
        }
        for c in components(&rows(x, &ids), radius) {
            nodes.push(c.iter().map(|i| ids[*i]).collect());
        }
    }
    let mut edges = vec![];
    for i in 0..nodes.len() {
        for j in i + 1..nodes.len() {
            if nodes[i].iter().any(|a| nodes[j].contains(a)) {
                edges.push(vec![i, j]);
            }
        }
    }
    {
        edges.sort_by_key(|v| (v[1], v[0]));
        json!({"nodes":nodes,"edges":edges,"cover_bins":bins,"overlap_fraction":overlap,"cluster_radius":radius})
    }
}

/// Omit unvalidated top-dimensional classes when a Rips 2-skeleton supports H0/H1.
pub fn report_h01(d: &[Interval]) -> Vec<Interval> {
    d.iter().filter(|v| v.dimension <= 1).cloned().collect()
}
