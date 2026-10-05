use capture_validator::{validate_bytes,validate_manifest};
use serde_json::json;
fn sample()->Vec<u8>{let mut b=b"SHPTRJ01".to_vec();b.extend(1u32.to_le_bytes());b.extend(7u32.to_le_bytes());b.extend(0u32.to_le_bytes());for x in [0f64,1.,2.,3.,0.]{b.extend(x.to_le_bytes());}b}
#[test] fn valid(){let s=validate_bytes(&sample()).unwrap();assert_eq!(s.count,1);assert_eq!(s.mean,[1.,2.,3.]);assert_eq!(s.known_confidence,0);}
#[test] fn truncation(){let mut b=sample();b.pop();assert!(validate_bytes(&b).is_err());}
#[test] fn trailing(){let mut b=sample();b.push(0);assert!(validate_bytes(&b).is_err());}
#[test] fn nan(){let mut b=sample();b[28..36].copy_from_slice(&f64::NAN.to_le_bytes());assert!(validate_bytes(&b).is_err());}
#[test] fn bad_flags(){let mut b=sample();b[16..20].copy_from_slice(&2u32.to_le_bytes());assert!(validate_bytes(&b).is_err());}
#[test] fn bad_count(){let mut b=sample();b[8..12].copy_from_slice(&0u32.to_le_bytes());assert!(validate_bytes(&b).is_err());}
#[test] fn manifest_invalid_schema(){assert!(!validate_manifest(&json!({"schema":0}),std::path::Path::new(".")).is_empty());}
#[test] fn manifest_duplicate_frames(){let x=json!({"schema":"shape.capture.v1","cameras":[{"id":"a","width":10,"height":20}],"frames":[{"id":1,"camera":"a","time":0.0},{"id":1,"camera":"a","time":0.1}],"files":[]});assert!(validate_manifest(&x,std::path::Path::new(".")).iter().any(|e|e.code=="duplicate_frame"));}
#[test] fn manifest_unknown_camera(){let x=json!({"schema":"shape.capture.v1","cameras":[],"frames":[{"id":1,"camera":"bad","time":0.0}],"files":[]});assert!(!validate_manifest(&x,std::path::Path::new(".")).is_empty());}
#[test] fn manifest_path_escape(){let x=json!({"schema":"shape.capture.v1","cameras":[],"frames":[],"files":[{"path":"../secret"}]});assert!(validate_manifest(&x,std::path::Path::new(".")).iter().any(|e|e.code=="unsafe_path"));}
