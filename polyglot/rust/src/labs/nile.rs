use super::helpers::*;
use std::path::Path;
pub fn run(repo:&Path)->Result<LabResult,String>{generic_case(repo,"nile","Water-infrastructure time series","data/industries/nile/data.csv")}
