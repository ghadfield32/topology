use super::helpers::*;
use std::path::Path;
pub fn run(repo:&Path)->Result<LabResult,String>{generic_case(repo,"grunfeld","Firm-year panel measurements","data/industries/grunfeld/data.csv")}
