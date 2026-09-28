//! Native bounded readers for canonical course data. No subprocess or Python dependency.
use crate::math::{require, safe_number, Matrix};
use serde_json::{json, Value};
use sha2::{Digest, Sha256};
use std::{
    collections::BTreeMap,
    fs,
    io::{Cursor, Read},
    path::{Component, Path},
};
const MAX: usize = 256 * 1024 * 1024;
pub fn sha(b: &[u8]) -> String {
    format!("{:x}", Sha256::digest(b))
}
pub fn read_bytes(repo: &str, relative: &str) -> Vec<u8> {
    let p = Path::new(relative);
    require(
        !p.is_absolute() && !p.components().any(|x| matches!(x, Component::ParentDir)),
        "unsafe source path",
    );
    let root = fs::canonicalize(repo).expect("course root unavailable");
    let full = fs::canonicalize(root.join(p)).expect("source unavailable");
    require(full.starts_with(&root), "source escaped root");
    let m = fs::metadata(&full).unwrap();
    require(
        m.is_file() && m.len() <= MAX as u64,
        "source exceeds bound or is not a file",
    );
    {
        let bytes = fs::read(full).expect("cannot read source");
        crate::trace::record(relative, &bytes);
        bytes
    }
}
pub fn read_json(repo: &str, path: &str) -> Value {
    serde_json::from_slice(&read_bytes(repo, path)).expect("invalid JSON")
}
pub fn read_csv(repo: &str, path: &str, delimiter: u8) -> Vec<Vec<String>> {
    let bytes = read_bytes(repo, path);
    let mut reader = csv::ReaderBuilder::new()
        .delimiter(delimiter)
        .has_headers(false)
        .flexible(true)
        .from_reader(bytes.as_slice());
    reader
        .records()
        .map(|r| {
            r.expect("malformed CSV")
                .iter()
                .map(str::to_owned)
                .collect()
        })
        .collect()
}
pub fn column(header: &[String], name: &str) -> usize {
    header
        .iter()
        .position(|x| x == name)
        .unwrap_or_else(|| panic!("missing column {name}"))
}
pub fn numeric(rows: &[Vec<String>], names: &[&str]) -> (Matrix, Vec<usize>) {
    require(!rows.is_empty(), "empty table");
    let cols: Vec<usize> = names.iter().map(|x| column(&rows[0], x)).collect();
    let (mut a, mut idx) = (vec![], vec![]);
    for (i, row) in rows.iter().skip(1).enumerate() {
        require(row.len() == rows[0].len(), "ragged semantic table");
        let mut v = vec![];
        let mut missing = false;
        for &j in &cols {
            let s = row[j].trim();
            if s.is_empty() || s.eq_ignore_ascii_case("na") || s.eq_ignore_ascii_case("nan") {
                missing = true;
                continue;
            }
            let x: f64 = s.parse().expect("invalid selected numeric field");
            require(x.is_finite(), "infinite selected value");
            v.push(x);
        }
        if !missing {
            a.push(v);
            idx.push(i);
        }
    }
    (a, idx)
}
pub fn fv(v: &Value) -> Vec<f64> {
    v.as_array()
        .expect("numeric array expected")
        .iter()
        .map(|x| x.as_f64().expect("numeric value"))
        .collect()
}
#[derive(Clone)]
pub struct Array {
    pub shape: Vec<usize>,
    pub dtype: String,
    pub data: Vec<f64>,
    pub text: Vec<String>,
    pub fortran: bool,
    pub raw_sha: String,
}
impl Array {
    pub fn audit(&self) -> Value {
        let mut v = json!({"shape":self.shape,"dtype":self.dtype,"fortran_order":self.fortran,"payload_sha256":self.raw_sha});
        if self
            .dtype
            .as_bytes()
            .get(1)
            .map(|b| *b == b'b' || *b == b'?')
            .unwrap_or(false)
        {
            v["values"] = json!(self.data.iter().map(|v| *v != 0.).collect::<Vec<_>>());
        } else if self.text.is_empty() {
            v["values"] = json!(self
                .data
                .iter()
                .copied()
                .map(safe_number)
                .collect::<Vec<_>>());
        } else {
            v["values"] = json!(self.text);
        }
        v
    }
}
fn u16x(b: &[u8], big: bool) -> u16 {
    let a: [u8; 2] = b.try_into().unwrap();
    if big {
        u16::from_be_bytes(a)
    } else {
        u16::from_le_bytes(a)
    }
}
fn u32x(b: &[u8], big: bool) -> u32 {
    let a: [u8; 4] = b.try_into().unwrap();
    if big {
        u32::from_be_bytes(a)
    } else {
        u32::from_le_bytes(a)
    }
}
fn u64x(b: &[u8], big: bool) -> u64 {
    let a: [u8; 8] = b.try_into().unwrap();
    if big {
        u64::from_be_bytes(a)
    } else {
        u64::from_le_bytes(a)
    }
}
fn field<'a>(s: &'a str, k: &str) -> &'a str {
    let i = s
        .find(&format!("'{k}'"))
        .or_else(|| s.find(&format!("\"{k}\"")))
        .expect("NPY header field");
    s[i..].split_once(':').unwrap().1.trim_start()
}
pub fn read_npy(b: &[u8]) -> Array {
    require(b.len() >= 10 && &b[..6] == b"\x93NUMPY", "NPY magic/header");
    let major = b[6];
    let (start, n) = match major {
        1 => (10, u16x(&b[8..10], false) as usize),
        2 | 3 => {
            require(b.len() >= 12, "NPY header truncated");
            (12, u32x(&b[8..12], false) as usize)
        }
        _ => panic!("NPY version unsupported"),
    };
    require(
        n <= 1024 * 1024 && start + n <= b.len(),
        "NPY header bounds",
    );
    let h = std::str::from_utf8(&b[start..start + n]).expect("NPY text header");
    let d = field(h, "descr");
    let quote = d.as_bytes()[0] as char;
    require(
        quote == '\'' || quote == '\"',
        "object/structured dtype unsupported",
    );
    let end = d[1..].find(quote).unwrap() + 1;
    let dtype = d[1..end].to_string();
    require(dtype.len() >= 3, "NPY dtype");
    let big = dtype.starts_with('>');
    let kind = dtype.as_bytes()[1] as char;
    let mut width: usize = dtype[2..].parse().expect("NPY dtype width");
    if kind == 'U' {
        width *= 4;
    }
    require(width > 0, "zero-width NPY unsupported");
    let sh = field(h, "shape");
    require(sh.starts_with('('), "NPY shape tuple");
    let end = sh.find(')').expect("NPY shape end");
    let mut shape = vec![];
    for s in sh[1..end].split(',') {
        let s = s.trim();
        if !s.is_empty() {
            shape.push(s.parse::<usize>().expect("NPY negative/invalid dimension"));
        }
    }
    let mut count = 1usize;
    for d in &shape {
        count = count.checked_mul(*d).expect("NPY dimension overflow");
    }
    let need = count.checked_mul(width).expect("NPY size overflow");
    require(
        need <= MAX && b.len() == start + n + need,
        "NPY payload length",
    );
    let payload = &b[start + n..];
    let fortran = field(h, "fortran_order").starts_with("True");
    let (mut data, mut text) = (vec![], vec![]);
    for c in payload.chunks_exact(width) {
        match (kind, width) {
            ('f', 4) => data.push(f32::from_bits(u32x(c, big)) as f64),
            ('f', 8) => data.push(f64::from_bits(u64x(c, big))),
            ('u', 1) => data.push(c[0] as f64),
            ('i', 1) => data.push((c[0] as i8) as f64),
            ('b', 1) | ('?', 1) => data.push(if c[0] == 0 { 0. } else { 1. }),
            ('u', 2) => data.push(u16x(c, big) as f64),
            ('i', 2) => data.push((u16x(c, big) as i16) as f64),
            ('u', 4) => data.push(u32x(c, big) as f64),
            ('i', 4) => data.push((u32x(c, big) as i32) as f64),
            ('u', 8) => {
                let v = u64x(c, big);
                require(
                    v <= 9007199254740992,
                    "uint exceeds exact JSON numeric range",
                );
                data.push(v as f64);
            }
            ('i', 8) => {
                let v = u64x(c, big) as i64;
                require(
                    v.unsigned_abs() <= 9007199254740992,
                    "int exceeds exact JSON numeric range",
                );
                data.push(v as f64);
            }
            ('U', _) => {
                let mut codes: Vec<u32> = c.chunks_exact(4).map(|q| u32x(q, big)).collect();
                while codes.last() == Some(&0) {
                    codes.pop();
                }
                text.push(
                    codes
                        .into_iter()
                        .map(|q| char::from_u32(q).expect("invalid Unicode scalar"))
                        .collect(),
                );
            }
            ('S', _) => {
                let mut q = c;
                while q.last() == Some(&0) {
                    q = &q[..q.len() - 1];
                }
                text.push(String::from_utf8(q.to_vec()).expect("non-UTF8 bytes dtype unsupported"));
            }
            _ => panic!("unsupported NPY dtype {dtype}"),
        }
    }
    if fortran && shape.len() > 1 && count > 0 {
        let old = data.clone();
        let ot = text.clone();
        for ci in 0..count {
            let mut rem = ci;
            let mut coord = vec![0; shape.len()];
            for j in (0..shape.len()).rev() {
                coord[j] = rem % shape[j];
                rem /= shape[j];
            }
            let (mut fi, mut stride) = (0, 1);
            for j in 0..shape.len() {
                fi += coord[j] * stride;
                stride *= shape[j];
            }
            if !old.is_empty() {
                data[ci] = old[fi];
            } else {
                text[ci] = ot[fi].clone();
            }
        }
    }
    Array {
        shape,
        dtype,
        data,
        text,
        fortran,
        raw_sha: sha(payload),
    }
}
pub fn read_npz(repo: &str, path: &str) -> BTreeMap<String, Array> {
    let b = read_bytes(repo, path);
    let mut z = zip::ZipArchive::new(Cursor::new(b)).expect("invalid NPZ ZIP");
    let mut out = BTreeMap::new();
    let mut total = 0usize;
    for i in 0..z.len() {
        let mut f = z.by_index(i).expect("invalid NPZ member");
        let name = f.name().to_string();
        require(
            !name.contains('/') && !name.contains('\\') && name.ends_with(".npy"),
            "unsafe NPZ member",
        );
        total = total
            .checked_add(f.size() as usize)
            .expect("NPZ size overflow");
        require(total <= MAX, "NPZ expansion limit");
        let mut bytes = Vec::new();
        f.by_ref()
            .take((MAX + 1) as u64)
            .read_to_end(&mut bytes)
            .expect("NPZ CRC/read error");
        require(bytes.len() <= MAX, "NPZ too large");
        let key = name.strip_suffix(".npy").unwrap().to_string();
        require(!out.contains_key(&key), "duplicate NPZ name");
        out.insert(key, read_npy(&bytes));
    }
    out
}
pub fn read_png(repo: &str, path: &str) -> Array {
    let b = read_bytes(repo, path);
    let mut d = png::Decoder::new(Cursor::new(&b));
    let palette = b.get(25) == Some(&3);
    d.set_transformations(if palette {
        png::Transformations::EXPAND | png::Transformations::ALPHA
    } else {
        png::Transformations::EXPAND
    });
    let mut r = d.read_info().expect("invalid PNG");
    let size = r.output_buffer_size();
    require(size <= MAX, "PNG expansion bound");
    let mut pixels = vec![0; size];
    let info = r.next_frame(&mut pixels).expect("PNG decoding/CRC failure");
    let channels = info.color_type.samples();
    let bit = info.bit_depth as usize;
    require(bit == 8 || bit == 16, "PNG expected 8 or 16-bit output");
    let raw = &pixels[..info.buffer_size()];
    let data = if bit == 8 {
        raw.iter().map(|v| *v as f64).collect()
    } else {
        raw.chunks_exact(2).map(|c| u16x(c, true) as f64).collect()
    };
    Array {
        shape: vec![info.height as usize, info.width as usize, channels],
        dtype: if bit == 16 {
            "<u2".into()
        } else {
            "|u1".into()
        },
        data,
        text: vec![],
        fortran: false,
        raw_sha: sha(&b),
    }
}
pub fn read_pfm(repo: &str, path: &str) -> Array {
    let b = read_bytes(repo, path);
    let mut fields = b.splitn(4, |v| *v == b'\n');
    let kind = std::str::from_utf8(fields.next().expect("PFM header"))
        .unwrap()
        .trim();
    let c = match kind {
        "PF" => 3,
        "Pf" => 1,
        _ => panic!("PFM magic"),
    };
    let shape: Vec<usize> = std::str::from_utf8(fields.next().expect("PFM size"))
        .unwrap()
        .split_whitespace()
        .map(|x| x.parse().expect("PFM dimension"))
        .collect();
    require(
        shape.len() == 2 && shape.iter().all(|n| *n > 0),
        "PFM dimension",
    );
    let scale: f64 = std::str::from_utf8(fields.next().expect("PFM scale"))
        .unwrap()
        .trim()
        .parse()
        .expect("PFM scale");
    require(scale.is_finite() && scale != 0., "PFM finite nonzero scale");
    let (w, h) = (shape[0], shape[1]);
    let need = w
        .checked_mul(h)
        .and_then(|n| n.checked_mul(c))
        .and_then(|n| n.checked_mul(4))
        .expect("PFM size overflow");
    let raw = fields.next().expect("PFM data");
    require(need <= MAX && raw.len() == need, "PFM length");
    let mut data = vec![0.; w * h * c];
    for y in 0..h {
        for x in 0..w * c {
            let k = ((h - 1 - y) * w * c + x) * 4;
            data[y * w * c + x] =
                f32::from_bits(u32x(&raw[k..k + 4], scale > 0.)) as f64 * scale.abs();
        }
    }
    Array {
        shape: vec![h, w, c],
        dtype: "<f4".into(),
        data,
        text: vec![],
        fortran: false,
        raw_sha: sha(raw),
    }
}
pub fn decode(repo: &str, path: &str) -> Value {
    let b = read_bytes(repo, path);
    let ext = Path::new(path)
        .extension()
        .unwrap_or_default()
        .to_string_lossy()
        .to_lowercase();
    let mut out = json!({"path":path,"sha256":sha(&b),"bytes":b.len()});
    match ext.as_str() {
        "csv" => {
            out["kind"] = json!("table");
            out["rows"] = json!(read_csv(
                repo,
                path,
                if b.split(|x| *x == b'\n')
                    .next()
                    .unwrap_or(&[])
                    .contains(&b';')
                {
                    b';'
                } else {
                    b','
                }
            ));
        }
        "json" => {
            out["kind"] = json!("json");
            out["value"] = read_json(repo, path);
        }
        "npy" => {
            out["kind"] = json!("array");
            out["array"] = read_npy(&b).audit();
        }
        "npz" => {
            out["kind"] = json!("arrays");
            let a = read_npz(repo, path);
            let map: BTreeMap<String, Value> = a.into_iter().map(|(k, v)| (k, v.audit())).collect();
            out["arrays"] = json!(map);
        }
        "pfm" => {
            out["kind"] = json!("array");
            out["array"] = read_pfm(repo, path).audit();
        }
        "png" => {
            out["kind"] = json!("array");
            out["array"] = read_png(repo, path).audit();
        }
        _ => {
            out["kind"] = json!("text");
            out["text"] = json!(String::from_utf8(b).expect("unsupported binary input"));
        }
    }
    out
}
