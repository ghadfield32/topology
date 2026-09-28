use super::helpers::*;
use std::path::Path;
pub fn run(repo:&Path)->Result<LabResult,String>{generic_case(repo,"modechoice","Traveler-level choice sets","data/industries/modechoice/data.csv")}
