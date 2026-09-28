use super::helpers::*;
use std::path::Path;
pub fn run(repo:&Path)->Result<LabResult,String>{let(mut q,mut p,h)=(1.0,0.0,0.2);let e0=0.5*(q*q+p*p);p-=h*q;q+=h*p;let e1=0.5*(q*q+p*p);Ok(LabResult{lab:"stage24".into(),title:"Symplectic counterexample".into(),metrics:vec![metric_num("energy_before",e0),metric_num("energy_after",e1),metric_num("delta",e1-e0)],notes:vec!["Symplectic does not imply exact per-step energy conservation.".into()]})}
