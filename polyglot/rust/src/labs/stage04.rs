use super::helpers::*;
use std::path::Path;
pub fn run(repo:&Path)->Result<LabResult,String>{let q=rotate_z([1.0,0.0,0.0],std::f64::consts::FRAC_PI_2);Ok(LabResult{lab:"stage04".into(),title:"Symmetry".into(),metrics:vec![metric_vec("rotated",&q),metric_num("norm",(q[0]*q[0]+q[1]*q[1]+q[2]*q[2]).sqrt())],notes:vec!["Rotation preserves Euclidean length.".into()]})}
