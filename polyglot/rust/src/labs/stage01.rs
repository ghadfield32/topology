use super::helpers::*;
use std::path::Path;
pub fn run(repo:&Path)->Result<LabResult,String>{let r=rank_mod2(&vec![vec![1,1,0],vec![1,0,1],vec![0,1,1]]);Ok(LabResult{lab:"stage01".into(),title:"Mathematical language, proofs, and linear algebra".into(),metrics:vec![metric_int("f2_rank",r)],notes:vec!["Same stored matrix can have different rank over R and F2.".into()]})}
