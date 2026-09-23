"""Independent checks written before the v4 audit implementation."""
from pathlib import Path
from datetime import date
import numpy as np
import pytest


def test_pixel_ring_and_diagonal_contact():
    from shape_lab.audits import pixel_betti_oracle
    ring=np.ones((3,3),bool);ring[1,1]=False
    assert pixel_betti_oracle(ring)==(1,1)
    assert pixel_betti_oracle(np.eye(2,dtype=bool))==(1,0)
    assert pixel_betti_oracle(np.zeros((2,3),bool))==(0,0)
    assert pixel_betti_oracle(np.ones((2,3),bool))==(1,0)

@pytest.mark.parametrize('seed',range(8))
def test_pixel_oracle_agrees_with_chain_algebra(seed):
    from shape_lab.audits import pixel_betti_oracle
    from shape_lab.persistence import pixel_filtration
    from shape_lab.algebra import betti_numbers
    image=np.random.default_rng(seed).uniform(size=(4,5))
    f=pixel_filtration(image)
    for threshold in [-1,.2,.5,.8,2]:
        simplices=[s for s,t in f if t<=threshold]
        assert list(pixel_betti_oracle(image<=threshold))==betti_numbers(simplices,1)

@pytest.mark.parametrize('p',[2,3,5,7])
def test_rank_prime_and_signed_boundaries(p):
    from shape_lab.audits import rank_prime, oriented_boundary
    from shape_lab.algebra import closure
    assert rank_prime([[2]],p)==(0 if p==2 else 1)
    k=closure([(0,1,2,3)])
    d1=oriented_boundary(k,1);d2=oriented_boundary(k,2);d3=oriented_boundary(k,3)
    assert np.array_equal(d1@d2,np.zeros((4,4),int))
    assert np.array_equal(d2@d3,np.zeros((6,1),int))
    assert rank_prime(d1,p)==3
    assert rank_prime(d2,p)==3
    assert rank_prime(d3,p)==1

@pytest.mark.parametrize('p',[1,4,9,15,2.5,True])
def test_nonprime_rejected(p):
    from shape_lab.audits import rank_prime
    with pytest.raises(ValueError):rank_prime([[1]],p)

@pytest.mark.parametrize('x',[
 np.array([[0.,0.],[1.,0.],[1.,1.],[0.,1.]]),
 np.array([[0.,0.],[0.,0.],[1.,0.]]),
 np.array([[1.,2.]]),
 np.random.default_rng(17).normal(size=(12,3))])
def test_h0_prim_matches_persistence(x):
    from shape_lab.audits import h0_merge_times
    from shape_lab.persistence import persistent_homology,rips_filtration,diagram
    bars=diagram(persistent_homology(rips_filtration(x,max_homology=0)),0,finite_only=True)
    times=h0_merge_times(x)
    assert len(times)==len(x)-1
    assert np.allclose(times[times>0],np.sort(bars[:,1]))

@pytest.mark.parametrize('x',[[],[[np.nan,0]],[[1,np.inf]],[[1],[2,3]]])
def test_bad_points_rejected(x):
    from shape_lab.audits import h0_merge_times
    with pytest.raises(ValueError):h0_merge_times(x)


def test_paired_prediction_discordance_and_no_difference():
    from shape_lab.audits import paired_accuracy_audit
    y=np.zeros(8,int);a=np.array([0,0,0,0,1,1,1,1]);b=np.zeros(8,int)
    r=paired_accuracy_audit(y,a,b,resamples=100,seed=3)
    assert r['a_only_correct']==0 and r['b_only_correct']==4
    assert r['difference_b_minus_a']==.5
    assert r['exact_discordance_pvalue']==.125
    same=paired_accuracy_audit(y,a,a,resamples=100,seed=3)
    assert same['exact_discordance_pvalue']==1
    assert same['paired_percentile_interval']==[0.,0.]

@pytest.mark.parametrize('args',[( [0],[],[0]),([],[],[]),([0],[np.nan],[0])])
def test_paired_bad_input(args):
    from shape_lab.audits import paired_accuracy_audit
    with pytest.raises(ValueError):paired_accuracy_audit(*args)


def test_evidence_audit_checks_missing_modified_and_escaping(tmp_path):
    from shape_lab.audits import verify_evidence
    from shape_lab.learning import new_log,record
    root=tmp_path/'course';root.mkdir();f=root/'answer.md';f.write_text('my first answer')
    log=new_log(21)
    record(log,0,'practice',40,'answer.md',root,date(2026,9,20))
    assert verify_evidence(log,root)[0]['status']=='matches'
    f.write_text('my revised answer')
    assert verify_evidence(log,root)[0]['status']=='modified'
    f.unlink()
    assert verify_evidence(log,root)[0]['status']=='missing'
    log['stages']['00']['attempts'][0]['evidence']='../secret.txt'
    assert verify_evidence(log,root)[0]['status']=='outside_root'


def test_boolean_pixel_contract_is_explicit():
    from shape_lab.audits import pixel_betti_oracle
    with pytest.raises(ValueError):pixel_betti_oracle(np.array([[.5,1.]]))
