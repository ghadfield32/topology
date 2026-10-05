use pyo3::prelude::*;
use pyo3::exceptions::PyValueError;
#[pyfunction]
fn validate_trajectory(data:&[u8])->PyResult<(usize,Vec<f64>)>{
 let s=capture_validator::validate_bytes(data).map_err(PyValueError::new_err)?;
 Ok((s.count,s.mean.to_vec()))
}
#[pymodule]
fn capture_validation_py(m:&Bound<'_,PyModule>)->PyResult<()>{m.add_function(wrap_pyfunction!(validate_trajectory,m)?)?;Ok(())}
