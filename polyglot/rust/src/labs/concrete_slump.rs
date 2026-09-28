use super::helpers::*;
use std::path::Path;
pub fn run(repo:&Path)->Result<LabResult,String>{generic_case(repo,"concrete_slump","Materials measurements and intervals","data/v7/concrete_slump/table.csv")}
