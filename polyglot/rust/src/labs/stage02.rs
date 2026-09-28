use super::helpers::*;
use std::path::Path;
pub fn run(repo:&Path)->Result<LabResult,String>{let a=[1.0,2.0];let b=[4.0,6.0];let eu=l2(&a,&b);let man=(a[0]-b[0]).abs()+(a[1]-b[1]).abs();Ok(LabResult{lab:"stage02".into(),title:"Metrics".into(),metrics:vec![metric_num("euclidean",eu),metric_num("manhattan",man)],notes:vec!["Metric choice changes neighborhoods.".into()]})}
