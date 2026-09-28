use crate::{data::sha, math::*, topology::*};
use serde_json::{json, Value};
use std::{
    collections::BTreeMap,
    sync::{Mutex, OnceLock},
};
static INPUTS: OnceLock<Mutex<BTreeMap<String, Value>>> = OnceLock::new();
pub fn begin() {
    INPUTS
        .get_or_init(|| Mutex::new(BTreeMap::new()))
        .lock()
        .unwrap()
        .clear();
}
pub fn record(path: &str, b: &[u8]) {
    INPUTS
        .get_or_init(|| Mutex::new(BTreeMap::new()))
        .lock()
        .unwrap()
        .insert(path.to_owned(), json!({"sha256":sha(b),"bytes":b.len()}));
}
pub fn snapshot() -> Value {
    json!(INPUTS
        .get_or_init(|| Mutex::new(BTreeMap::new()))
        .lock()
        .unwrap()
        .clone())
}
pub fn boundary_matrix(c: &[Simplex], k: usize) -> Matrix {
    require(k > 0, "positive boundary dimension");
    let c = ordered(c);
    let rs: Vec<_> = c.iter().filter(|s| s.vertices.len() == k).collect();
    let cs: Vec<_> = c.iter().filter(|s| s.vertices.len() == k + 1).collect();
    let idx: BTreeMap<Vec<usize>, usize> = rs
        .iter()
        .enumerate()
        .map(|(i, s)| (s.vertices.clone(), i))
        .collect();
    let mut a = zeros(rs.len(), cs.len());
    for (j, s) in cs.iter().enumerate() {
        for q in 0..s.vertices.len() {
            let mut f = s.vertices.clone();
            f.remove(q);
            a[idx[&f]][j] = 1.;
        }
    }
    a
}
pub fn algebra_control() -> Value {
    let c = triangle(true);
    let b1 = boundary_matrix(&c, 1);
    let b2 = boundary_matrix(&c, 2);
    let mut prod = matmul(&b1, &b2);
    for row in &mut prod {
        for x in row {
            *x = (*x as i64 % 2) as f64;
        }
    }
    json!({"boundary_1":b1,"boundary_2":b2,"boundary_squared_mod2":prod,"rank_boundary_1":rank2(&b1),"rank_boundary_2":rank2(&b2),"cycle_dimension_1":b2.len()-rank2(&b1),"homology_dimension_1":b2.len()-rank2(&b1)-rank2(&b2)})
}
