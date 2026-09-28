use super::helpers::*;
use std::path::Path;
pub fn run(repo:&Path)->Result<LabResult,String>{let chunks=vec![vec![vec![1.0,2.0,3.0]],vec![vec![4.0,5.0,6.0],vec![7.0,8.0,9.0]]];let m=weighted_mean(&chunks);Ok(LabResult{lab:"stage18".into(),title:"Streaming".into(),metrics:vec![metric_vec("mean",&m)],notes:vec!["Count-weighted streaming summaries must match whole-data summaries.".into()]})}
