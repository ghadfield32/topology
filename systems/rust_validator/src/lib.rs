//! Explicit validation errors are data. A memory-safe parser is not automatically a correct measurement model.
use serde::Serialize;
use serde_json::Value;
use std::collections::{HashMap,HashSet};
use std::path::{Path,Component};
use sha2::{Digest,Sha256};
#[derive(Debug,Serialize)] pub struct Summary {pub count:usize,pub known_confidence:usize,pub start:f64,pub end:f64,pub mean:[f64;3]}
#[derive(Debug,Serialize)] pub struct ValidationError{pub code:String,pub location:String,pub message:String}
fn err(code:&str,at:String,message:&str)->ValidationError{ValidationError{code:code.into(),location:at,message:message.into()}}
fn u32le(b:&[u8])->u32{u32::from_le_bytes(b.try_into().expect("caller validates four-byte span"))}
fn f64le(b:&[u8])->f64{f64::from_le_bytes(b.try_into().expect("caller validates eight-byte span"))}
pub fn validate_bytes(b:&[u8])->Result<Summary,String>{
 if b.len()<12||&b[..8]!=b"SHPTRJ01"{return Err("invalid/truncated header".into())}
 let n=u32le(&b[8..12]) as usize;
 if n==0||n>1_000_000||b.len()!=12+48*n{return Err("count/size mismatch".into())}
 let mut s=Summary{count:n,known_confidence:0,start:0.,end:0.,mean:[0.;3]};
 let mut prev_id=None;let mut prev_time=-1.;
 for i in 0..n{let r=&b[12+48*i..12+48*(i+1)];let id=u32le(&r[..4]);let flag=u32le(&r[4..8]);let t=f64le(&r[8..16]);
  let v=[f64le(&r[16..24]),f64le(&r[24..32]),f64le(&r[32..40])];let c=f64le(&r[40..48]);
  if flag>1||!c.is_finite()||(flag==0&&c!=0.)||(flag==1&&!(0. ..=1.).contains(&c)){return Err(format!("record {i}: invalid confidence"))}
  if !t.is_finite()||t<0.||t<=prev_time||prev_id.is_some_and(|p|id<=p){return Err(format!("record {i}: invalid order"))}
  if v.iter().any(|x|!x.is_finite()){return Err(format!("record {i}: nonfinite coordinate"))}
  if i==0{s.start=t};s.end=t;s.known_confidence+=flag as usize;
  for j in 0..3{s.mean[j]+=(v[j]-s.mean[j])/((i+1)as f64);if !s.mean[j].is_finite(){return Err("summary overflow".into())}}
  prev_id=Some(id);prev_time=t;
 }
 Ok(s)
}
pub fn validate_manifest(m:&Value,root:&Path)->Vec<ValidationError>{
 let mut e=Vec::new();
 if m.get("schema").and_then(Value::as_str)!=Some("shape.capture.v1"){e.push(err("schema","schema".into(),"expected shape.capture.v1"));return e}
 let mut cameras=HashSet::new();
 if let Some(cs)=m.get("cameras").and_then(Value::as_array){for (i,c) in cs.iter().enumerate(){
  let id=c.get("id").and_then(Value::as_str).unwrap_or("");
  if id.is_empty()||!cameras.insert(id.to_owned()){e.push(err("camera_id",format!("cameras[{i}]"),"missing or duplicate camera ID"))}
  for k in ["width","height"]{if !c.get(k).and_then(Value::as_u64).is_some_and(|n|n>0&&n<=100_000){e.push(err("dimensions",format!("cameras[{i}].{k}"),"positive bounded integer required"))}}
 }}else{e.push(err("cameras","cameras".into(),"array required"))}
 let mut ids=HashSet::new();let mut times=HashMap::new();
 if let Some(fs)=m.get("frames").and_then(Value::as_array){for(i,f)in fs.iter().enumerate(){
  let cam=f.get("camera").and_then(Value::as_str).unwrap_or("");let id=f.get("id").and_then(Value::as_u64);
  if !cameras.contains(cam){e.push(err("unknown_camera",format!("frames[{i}]"),"camera not declared"))}
  if let Some(id)=id{if !ids.insert((cam.to_owned(),id)){e.push(err("duplicate_frame",format!("frames[{i}]"),"duplicate camera/frame pair"))}}else{e.push(err("frame_id",format!("frames[{i}]"),"unsigned integer required"))}
  match f.get("time").and_then(Value::as_f64){Some(t)if t.is_finite()&&t>=0.=>{if times.get(cam).is_some_and(|p|t<=*p){e.push(err("time_order",format!("frames[{i}]"),"time must increase within camera"))}times.insert(cam.to_owned(),t);},_=>e.push(err("time",format!("frames[{i}]"),"finite nonnegative time required"))}
 }}else{e.push(err("frames","frames".into(),"array required"))}
 if let Some(fs)=m.get("files").and_then(Value::as_array){for(i,f)in fs.iter().enumerate(){let raw=f.get("path").and_then(Value::as_str).unwrap_or("");let p=Path::new(raw);
  if raw.is_empty()||raw.contains('\\')||raw.contains(':')||p.is_absolute()||p.components().any(|c|!matches!(c,Component::Normal(_))){e.push(err("unsafe_path",format!("files[{i}]"),"relative normal components required"));continue}
  let full=root.join(p);
  let inside=full.canonicalize().ok().zip(root.canonicalize().ok()).is_some_and(|(a,b)|a.starts_with(b));
  if !inside||!full.is_file(){e.push(err("missing_or_escaped_file",format!("files[{i}]"),"missing file or symlink escape"));continue}
  if full.metadata().map(|x|x.len()>64*1024*1024).unwrap_or(true){e.push(err("file_size",format!("files[{i}]"),"input exceeds 64 MiB teaching bound"));continue}
  if let Some(expected)=f.get("sha256").and_then(Value::as_str){match std::fs::read(&full){Ok(b)=>{let actual=format!("{:x}",Sha256::digest(&b));if expected!=actual{e.push(err("hash",format!("files[{i}]"),"source hash mismatch"))}},Err(_)=>e.push(err("read",format!("files[{i}]"),"cannot read"))}}
 }}else{e.push(err("files","files".into(),"array required"))}
 e
}
