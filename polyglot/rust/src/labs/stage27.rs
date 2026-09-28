use super::helpers::*;
use std::path::Path;
pub fn run(repo:&Path)->Result<LabResult,String>{let g1=[1.0,0.0];let g2=[-1.0,0.0];let d=dot(&g1,&g2);Ok(LabResult{lab:"stage27".into(),title:"Gradient conflict".into(),metrics:vec![metric_num("dot",d),metric_bool("conflict",d<0.0)],notes:vec!["Opposite gradients expose an incompatible first-order objective pair.".into()]})}
