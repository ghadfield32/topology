use super::helpers::*;
use std::path::Path;
pub fn run(repo:&Path)->Result<LabResult,String>{let pts=load_spl_ball(repo)?;let c=weighted_mean(&[pts.clone()]);Ok(LabResult{lab:"stage12".into(),title:"Capstone: reproduce, defend, transfer, and audit the book".into(),metrics:vec![metric_int("selected_ball_points",pts.len()),metric_vec("centroid_m",&c)],notes:vec!["Selected excerpt; not a full tracking corpus.".into()]})}
