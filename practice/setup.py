from pathlib import Path
import sys, json
from itertools import combinations
import numpy as np
import pandas as pd
ROOT=next((p for p in [Path.cwd(),*Path.cwd().parents] if (p/'data/manifest.json').exists() and (p/'src/shape_lab').exists()),None)
if ROOT is None: raise RuntimeError('Open this notebook inside the extracted course folder.')
sys.path.insert(0,str(ROOT/'src'))
from shape_lab.data import load_iris_data,load_digit_data,digit_example
from shape_lab.algebra import closure,validate_complex,rank_mod2,boundary_matrix,betti_numbers
from shape_lab.topology import component_labels
from shape_lab.persistence import ordered_filtration,rips_filtration,reduce_boundary,persistent_homology,diagram,pixel_filtration,finite_bottleneck
print('Working inside',ROOT.name,'— no network data downloads.')
