use super::helpers::*;
use std::path::Path;
pub fn run(repo:&Path)->Result<LabResult,String>{let pts=vec![vec![0.0,0.0],vec![1.0,0.0],vec![1.0,1.0],vec![0.0,1.0]];let eps=1.01;let mut edges=0;for i in 0..pts.len(){for j in i+1..pts.len(){if l2(&pts[i],&pts[j])<=eps{edges+=1;}}}Ok(LabResult{lab:"stage07".into(),title:"Rips".into(),metrics:vec![metric_num("epsilon",eps),metric_int("edges",edges)],notes:vec!["Unit square perimeter edges enter before diagonals.".into()]})}
