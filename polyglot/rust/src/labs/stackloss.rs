use super::helpers::*;
use std::path::Path;
pub fn run(repo:&Path)->Result<LabResult,String>{generic_case(repo,"stackloss","Manufacturing regression","data/industries/stackloss/data.csv")}
