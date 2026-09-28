use super::helpers::*;
use std::path::Path;
pub fn run(repo:&Path)->Result<LabResult,String>{generic_case(repo,"wdbc","Healthcare image-summary classification","data/industries/wdbc/data.csv")}
