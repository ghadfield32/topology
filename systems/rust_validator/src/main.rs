use std::{path::Path,process};
use capture_validator::{validate_bytes,validate_manifest};
fn run()->Result<(),String>{
 let a:Vec<_>=std::env::args().collect();
 if a.len()==3 && a[1]=="--binary" {
  if std::fs::metadata(&a[2]).map_err(|e|e.to_string())?.len()>48_000_012{return Err("oversized source".into())}
  let b=std::fs::read(&a[2]).map_err(|e|e.to_string())?;
  let s=validate_bytes(&b)?;println!("{}",serde_json::to_string(&s).map_err(|e|e.to_string())?);return Ok(())
 }
 if a.len()==4 && a[1]=="--manifest"{
  if std::fs::metadata(&a[2]).map_err(|e|e.to_string())?.len()>4_000_000{return Err("oversized manifest".into())}
  let v=serde_json::from_slice(&std::fs::read(&a[2]).map_err(|e|e.to_string())?).map_err(|e|e.to_string())?;
  let errors=validate_manifest(&v,Path::new(&a[3]));println!("{}",serde_json::json!({"valid":errors.is_empty(),"errors":errors}));
  if !errors.is_empty(){return Err("capture validation failed".into())};return Ok(())
 }
 Err("usage: capture-validator --binary FILE | --manifest JSON ROOT".into())
}
fn main(){if let Err(e)=run(){eprintln!("{e}");process::exit(2)}}
