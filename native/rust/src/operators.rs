//! Trained native function-to-function and differentiable-simulation controls.
use crate::{learning::Tape, math::*};
use serde_json::{json, Value};
pub fn tape_net(t: &Tape, p: &[usize], x: &[f64], h: usize, o: usize) -> Vec<usize> {
    let d = x.len();
    require(p.len() == h * d + h + o * h + o, "operator network shape");
    let mut a = vec![];
    for j in 0..h {
        let mut s = p[h * d + j];
        for k in 0..d {
            s = t.add(s, t.scale(p[j * d + k], x[k]));
        }
        a.push(t.tanh(s));
    }
    let start = h * d + h;
    let mut out = vec![];
    for j in 0..o {
        let mut s = p[start + o * h + j];
        for k in 0..h {
            s = t.add(s, t.mul(p[start + j * h + k], a[k]));
        }
        out.push(s);
    }
    out
}
pub fn train_operator(kind: &str) -> Value {
    let mut rng = Rng { state: 99 };
    let sensors = 8;
    let (mut inputs, mut coeffs) = (vec![], vec![]);
    for _ in 0..24 {
        let c = vec![rng.normal(), rng.normal() * 0.5, rng.normal() * 0.25];
        let mut v = vec![0.; sensors];
        for j in 0..sensors {
            let x = j as f64 / sensors as f64;
            for (k, a) in c.iter().enumerate() {
                v[j] += a * (2. * std::f64::consts::PI * (k + 1) as f64 * x).sin();
            }
        }
        inputs.push(v);
        coeffs.push(c);
    }
    let truth = |c: &[f64], x: f64| -> f64 {
        let mut v = 0.;
        for (k, a) in c.iter().enumerate() {
            let f = 2. * std::f64::consts::PI * (k + 1) as f64;
            v += a * (-0.005 * f * f).exp() * (f * x).sin();
        }
        v
    };
    let nb = 8 * 8 + 8 + 4 * 8 + 4;
    let nt = 8 + 8 + 4 * 8 + 4;
    let np = if kind == "fno" { 4 } else { nb + nt };
    let mut w: Vec<f64> = (0..np).map(|_| 0.2 * rng.normal()).collect();
    let predict = |t: &Tape, p: &[usize], input: &[f64], x: f64| -> usize {
        if kind == "deeponet" {
            let b = tape_net(t, &p[..nb], input, 8, 4);
            let tr = tape_net(t, &p[nb..], &[x], 8, 4);
            let mut v = t.input(0.);
            for k in 0..b.len() {
                v = t.add(v, t.mul(b[k], tr[k]));
            }
            return v;
        }
        let mut v = p[3];
        for k in 1..=3 {
            let (mut re, mut im) = (0., 0.);
            for (j, u) in input.iter().enumerate() {
                let a = 2. * std::f64::consts::PI * (k * j) as f64 / input.len() as f64;
                re += u * a.cos() / input.len() as f64;
                im -= u * a.sin() / input.len() as f64;
            }
            let a = 2. * std::f64::consts::PI * k as f64 * x;
            let basis = 2. * (re * a.cos() - im * a.sin());
            v = t.add(v, t.scale(p[k - 1], basis));
        }
        v
    };
    let epochs = 80;
    let lr = 0.03;
    let mut history = vec![];
    for _ in 0..epochs {
        let t = Tape::new();
        let p: Vec<usize> = w.iter().map(|v| t.input(*v)).collect();
        let mut loss = t.input(0.);
        for n in 0..16 {
            for j in 0..8 {
                let x = j as f64 / 8.;
                let v = predict(&t, &p, &inputs[n], x);
                let e = t.sub(v, t.input(truth(&coeffs[n], x)));
                loss = t.add(loss, t.scale(t.mul(e, e), 1. / 128.));
            }
        }
        history.push(t.val(loss));
        let g = t.back(loss);
        let gn = p.iter().map(|i| g[*i] * g[*i]).sum::<f64>().sqrt();
        let factor = if gn > 10. { 10. / gn } else { 1. };
        for (i, k) in p.iter().enumerate() {
            w[i] -= lr * factor * g[*k];
        }
    }
    let (mut actual, mut pred) = (vec![], vec![]);
    for n in 16..24 {
        for j in 0..16 {
            let x = j as f64 / 16.;
            let t = Tape::new();
            let p: Vec<usize> = w.iter().map(|v| t.input(*v)).collect();
            pred.push(t.val(predict(&t, &p, &inputs[n], x)));
            actual.push(truth(&coeffs[n], x));
        }
    }
    let scope = if kind == "fno" {
        "single learned real spectral multiplier layer; not a multilayer FNO benchmark"
    } else {
        "two trained tanh branch/trunk networks"
    };
    json!({"model":kind,"origin":"manufactured periodic heat equation, diffusion*time=0.005","train_function_ids":(0..16).collect::<Vec<_>>(),"test_function_ids":(16..24).collect::<Vec<_>>(),"epochs":epochs,"loss_history":history,"truth":actual,"predictions":pred,"rmse":rmse(&actual,&pred),"weights":w,"scope":scope})
}
pub fn damping_fit() -> Value {
    let true_gamma = 0.3;
    let dt = 0.05;
    let observed: Vec<f64> = (0..41)
        .map(|i| (-true_gamma * i as f64 * dt).exp())
        .collect();
    let mut gamma = 1.;
    let mut hist = vec![];
    for _ in 0..100 {
        let t = Tape::new();
        let g = t.input(gamma);
        let mut state = t.input(1.);
        let mut loss = t.input(0.);
        for v in &observed[1..] {
            state = t.mul(state, t.exp(t.scale(g, -dt)));
            let e = t.sub(state, t.input(*v));
            loss = t.add(loss, t.scale(t.mul(e, e), 1. / 40.));
        }
        hist.push(t.val(loss));
        let grad = t.back(loss);
        gamma -= 0.2 * grad[g];
    }
    json!({"origin":"manufactured exact damped scalar flow","true_gamma":true_gamma,"fitted_gamma":gamma,"loss_history":hist,"observations":observed,"time_step":dt,"scope":"no noisy real-system parameter-identification claim"})
}
