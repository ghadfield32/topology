"""Optional GUDHI alpha example. NOT executed in the bundled build environment."""
import importlib.util
if importlib.util.find_spec('gudhi') is None:
    raise SystemExit('NOT RUN: install the crosscheck extra to obtain GUDHI before this optional lab.')
from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'src'))
import numpy as np
import gudhi
from shape_lab.display import save_json
points=np.array([[0.,0.],[1.,0.],[.5,np.sqrt(3)/2]])
st=gudhi.AlphaComplex(points=points).create_simplex_tree()
st.persistence(homology_coeff_field=2,min_persistence=0,persistence_dim_max=True)
intervals=st.persistence_intervals_in_dimension(1)
# Default alpha filtration values are squared radii.
assert intervals.shape==(1,2)
assert np.allclose(intervals,[[.25,1/3]],atol=1e-8)
print('Alpha H1 in squared-radius units:',intervals)
print('Same intervals converted to radius units:',np.sqrt(intervals))
save_json(ROOT/'reports/optional_alpha_results.json',{'squared_radius_H1':intervals,'radius_H1':np.sqrt(intervals),'gudhi_version':gudhi.__version__})
