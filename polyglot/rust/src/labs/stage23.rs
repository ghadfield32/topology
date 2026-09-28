use super::helpers::*;
use std::path::Path;
pub fn run(repo:&Path)->Result<LabResult,String>{let(q,p)=(1.0,0.5);let e=0.5*(q*q+p*p);Ok(LabResult{lab:"stage23".into(),title:"Hamiltonian mechanics".into(),metrics:vec![metric_num("energy",e),metric_num("dqdt",p),metric_num("dpdt",-q)],notes:vec!["Manufactured harmonic-oscillator control.".into()]})}
