use super::helpers::*;
use std::path::Path;
pub fn run(repo:&Path)->Result<LabResult,String>{generic_case(repo,"co2","Atmospheric observations and windows","data/industries/co2/data.csv")}
