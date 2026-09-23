"""Missing optional packages must remain visible as skips, never as passes."""
import numpy as np
import pytest
from shape_lab.persistence import rips_filtration,persistent_homology,diagram,pixel_filtration

X=np.array([[0.,0.],[1.,0.],[1.,1.],[0.,1.]])

def canonical_pairs(d):
    a=np.asarray(d).reshape(-1,2)
    a=a[a[:,1]>a[:,0]]
    return np.array(sorted(map(tuple,a))).reshape(-1,2)

def test_ripser_agrees():
    ripser=pytest.importorskip('ripser')
    reference=persistent_homology(rips_filtration(X))
    result=ripser.ripser(X,maxdim=1,coeff=2)['dgms']
    for k in (0,1):assert np.allclose(canonical_pairs(diagram(reference,k)),canonical_pairs(result[k]),atol=1e-6)

def test_gudhi_rips_and_pixels_agree():
    gd=pytest.importorskip('gudhi')
    simplex_tree=gd.RipsComplex(points=X,max_edge_length=2).create_simplex_tree(max_dimension=2)
    simplex_tree.persistence(homology_coeff_field=2,min_persistence=0,persistence_dim_max=True)
    reference=persistent_homology(rips_filtration(X))
    for k in (0,1):assert np.allclose(canonical_pairs(diagram(reference,k)),canonical_pairs(simplex_tree.persistence_intervals_in_dimension(k)))
    rng=np.random.default_rng(300)
    for image in [np.array([[0,0,0],[0,1,0],[0,0,0]],dtype=float),rng.uniform(size=(4,4))]:
        cubical=gd.CubicalComplex(top_dimensional_cells=image)
        cubical.persistence(homology_coeff_field=2,min_persistence=0)
        reference=persistent_homology(pixel_filtration(image))
        for k in (0,1):assert np.allclose(canonical_pairs(diagram(reference,k)),canonical_pairs(cubical.persistence_intervals_in_dimension(k)))
