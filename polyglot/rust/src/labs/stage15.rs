use super::helpers::*;
use std::path::Path;
pub fn run(repo:&Path)->Result<LabResult,String>{let z=700.0*0.12/14.0;Ok(LabResult{lab:"stage15".into(),title:"Stereo depth".into(),metrics:vec![metric_num("depth_m",z)],notes:vec!["Simplified formula assumes compatible calibration conventions.".into()]})}
