use super::helpers::*;
use std::path::Path;
pub fn run(repo:&Path)->Result<LabResult,String>{let(x,y)=(2.0,0.0);let c=x*x+y*y-1.0;let(gx,gy)=(2.0*x,2.0*y);let den=gx*gx+gy*gy;let x1=x-gx*c/den;let y1=y-gy*c/den;Ok(LabResult{lab:"stage25".into(),title:"Constraint projection".into(),metrics:vec![metric_num("residual_after",x1*x1+y1*y1-1.0)],notes:vec!["One linearized correction need not exactly satisfy a nonlinear constraint.".into()]})}
