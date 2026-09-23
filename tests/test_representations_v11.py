"""Independent controls for the educational representation implementation."""
import importlib.util
import numpy as np
import pytest

def test_representation_module_present():
    assert importlib.util.find_spec('shape_lab.representations') is not None

@pytest.fixture
def r():
    from shape_lab import representations
    return representations

def test_covariance_hand_calculation(r):
    x=np.array([[1.,2.],[3.,4.],[5.,6.]])
    assert np.allclose(r.covariance(x),[[4,4],[4,4]])

@pytest.mark.parametrize('bad',[np.zeros((1,2)),np.zeros(3),np.array([[1.,np.nan],[2.,3.]])])
def test_bad_matrices_rejected(r,bad):
    with pytest.raises(ValueError): r.covariance(bad)

def test_whiten_train_and_transform_test_separately(r):
    x=np.random.default_rng(1).normal(size=(80,3)) @ np.diag([1,2,4])+4
    mean,transform=r.fit_whitener(x)
    assert np.allclose(r.covariance((x-mean)@transform),np.eye(3),atol=1e-10)
    assert np.allclose(mean,x.mean(0))
    test=x+100
    assert not np.allclose(((test-mean)@transform).mean(0),0)

def test_rank_deficient_whitening_fails(r):
    with pytest.raises(ValueError,match='rank'):r.fit_whitener(np.ones((8,3)))

def test_effective_rank_controls(r):
    assert r.effective_rank(np.zeros((5,3))) == 0
    assert np.isclose(r.effective_rank(np.array([[1,1],[-1,-1],[2,2],[-2,-2]])),1)

def test_ecf_of_two_atoms(r):
    t=np.linspace(-3,3,17)
    assert np.allclose(r.empirical_cf(np.array([-1.,1.]),t),np.cos(t))

def test_quadrature_matches_closed_form_not_same_algorithm(r):
    x=np.array([-2.,-.25,.3,1.,2.])
    estimate=r.projected_gaussian_score(x[:,None],np.ones((1,1)),np.linspace(-10,10,4001))
    assert np.isclose(estimate,r.epps_pulley_exact(x),rtol=1e-9,atol=1e-10)

def test_score_permutation_and_unit_direction_contract(r):
    x=np.random.default_rng(1).normal(size=(40,3)); a=r.unit_directions(3,16,9)
    assert np.isclose(r.projected_gaussian_score(x,a),r.projected_gaussian_score(x[::-1],a))
    with pytest.raises(ValueError,match='unit'):r.projected_gaussian_score(x,a*2)

def test_collapsed_cloud_penalty_positive(r):
    assert r.projected_gaussian_score(np.zeros((64,3)),r.unit_directions(3,8,0)) > 1

def test_unexamined_direction_counterexample(r):
    rng=np.random.default_rng(23); x=np.column_stack([rng.normal(size=200),np.zeros(200)])
    first=r.projected_gaussian_score(x,np.array([[1.],[0.]]))
    second=r.projected_gaussian_score(x,np.array([[0.],[1.]]))
    assert second > first

def test_torch_numpy_and_gradient_agree(r):
    torch=pytest.importorskip('torch')
    x=np.random.default_rng(4).normal(size=(9,3));a=r.unit_directions(3,7,11)
    z=torch.tensor(x,dtype=torch.float64,requires_grad=True)
    score=r.sigreg_torch(z,torch.tensor(a,dtype=torch.float64))
    assert np.isclose(score.item(),r.projected_gaussian_score(x,a))
    score.backward();eps=1e-5
    xp=x.copy();xm=x.copy();xp[2,1]+=eps;xm[2,1]-=eps
    numeric=(r.projected_gaussian_score(xp,a)-r.projected_gaussian_score(xm,a))/(2*eps)
    assert np.isclose(z.grad[2,1].item(),numeric,rtol=1e-5)

def test_exact_symmetric_collapse_can_have_zero_gradient(r):
    torch=pytest.importorskip('torch')
    z=torch.zeros((12,3),dtype=torch.float64,requires_grad=True)
    loss=r.sigreg_torch(z,torch.tensor(r.unit_directions(3,7,1)))
    loss.backward()
    assert loss.item()>0 and torch.all(z.grad==0)

def test_vicreg_and_barlow_are_finite_and_symmetric(r):
    torch=pytest.importorskip('torch');torch.manual_seed(1)
    a=torch.randn(12,3,requires_grad=True);b=torch.randn(12,3)
    for fn in [r.vicreg_loss,r.barlow_loss]:
        la=fn(a,b);lb=fn(b,a)
        assert torch.isfinite(la) and torch.allclose(la,lb,atol=1e-5)
        la.backward(retain_graph=True)
    assert torch.isfinite(a.grad).all()

def test_info_nce_pairing(r):
    torch=pytest.importorskip('torch');a=torch.eye(4)
    assert r.info_nce(a,a,.1)<r.info_nce(a,torch.roll(a,1,0),.1)
    with pytest.raises(ValueError):r.info_nce(a[:1],a[:1],.1)

def test_ema_does_not_mutate_inputs(r):
    torch=pytest.importorskip('torch');old=torch.tensor([1.]);new=torch.tensor([3.])
    assert r.ema(old,new,.75).item()==1.5 and old.item()==1
    with pytest.raises(ValueError):r.ema(old,new,1.2)

def test_group_split_contract(r):
    assert r.assert_disjoint([1,2],[3],[4]) is None
    with pytest.raises(ValueError,match='overlap'):r.assert_disjoint([1,2],[2],[4])

def test_real_measurement_example_excludes_identity_and_label_columns():
    from shape_lab.representation_experiments import IRIS_FEATURES
    assert IRIS_FEATURES == ['sepal_length_cm','sepal_width_cm','petal_length_cm','petal_width_cm']

def test_representation_track_is_unique_and_not_duplicate_core():
    from pathlib import Path
    import json
    root=Path(__file__).resolve().parents[1]
    track=json.loads((root/'curriculum/representation_track.json').read_text())['units']
    assert [x['id'] for x in track]==['r01','r02','r03','r04','r05']
    assert len({x['lesson'] for x in track})==5
    for x in track:
        for key in ['lesson','notebook','learner','answers']:
            assert (root/x[key]).is_file()
        assert 'not a full' in x['scope']

def test_new_answer_notebooks_have_no_unfinished_reference_cells():
    from pathlib import Path
    import nbformat
    root=Path(__file__).resolve().parents[1]
    for path in (root/'representations/answers').glob('*.ipynb'):
        notebook=nbformat.read(path,as_version=4)
        assert all('raise NotImplementedError' not in c.source for c in notebook.cells if c.cell_type=='code')

def test_representation_capstone_declares_generated_dependency():
    from shape_lab.course import DEPENDENCIES
    assert DEPENDENCIES['representations/notebooks/r05.ipynb']==['representations/notebooks/r04.ipynb']
