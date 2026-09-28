use super::helpers::*;
use std::path::Path;
pub fn run(repo:&Path)->Result<LabResult,String>{let (rows,cols)=csv_shape(&repo_path(repo,"data/raw/iris.csv"))?;Ok(LabResult{lab:"stage00".into(),title:"Start here".into(),metrics:vec![metric_int("iris_rows",rows),metric_int("iris_columns",cols)],notes:vec!["One row is one measured flower record in this snapshot.".into()]})}
