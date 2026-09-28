use super::helpers::*;
use std::path::Path;
pub fn run(repo:&Path)->Result<LabResult,String>{let pts=load_spl_ball(repo)?;let c=weighted_mean(&[pts.clone()]);Ok(LabResult{lab:"stage10".into(),title:"Stability, diagram distances, noise, and scientific uncertainty".into(),metrics:vec![metric_int("selected_ball_points",pts.len()),metric_vec("centroid_m",&c)],notes:vec!["Selected excerpt; not a full tracking corpus.".into()]})}
