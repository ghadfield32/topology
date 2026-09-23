import numpy as np
import pytest
from numpy.testing import assert_allclose
from shape_lab.attention import attention, frame_mask, patch_tokens
from shape_lab.temporal import causal_separation_events, match_events, fifo_latencies, summarize_latencies


def test_attention_normalized_and_frame_mask():
    x=np.array([[1.,0],[0,1],[2,0],[0,2]])
    y,w=attention(x,x,x,frame_mask([0,0,1,1]))
    assert_allclose(w.sum(1),1);assert_allclose(w[:2,2:],0)
    z,_=attention(x,x,x)
    assert not np.allclose(y,z)


def test_attention_stable_and_invalid_rows_rejected():
    q=np.ones((3,2))*1e3
    _,w=attention(q,q,q);assert_allclose(w,np.ones((3,3))/3)
    with pytest.raises(ValueError):attention(q,q,q,np.zeros((3,3),bool))


def test_patch_tokens_preserve_row_column_positions():
    a=np.arange(16).reshape(4,4)
    t,rc=patch_tokens(a,2)
    assert t.shape==(4,4);assert_allclose(t[0],[0,1,4,5]);assert_allclose(rc,[[0,0],[0,2],[2,0],[2,2]])


def test_event_needs_observed_near_then_separation_not_proximity_only():
    t=np.arange(8)*.01;d=np.array([.01,.01,.01,.2,.25,.3,.31,.4])
    e=causal_separation_events(t,d,np.ones(8,bool),near=.03,far=.1,min_near=3,min_far=2)
    assert len(e)==1;assert e[0]['onset_s']==.03;assert e[0]['decision_s']==.04
    assert e[0]['label']=='separation_candidate' and not e[0]['contact_certified']
    assert causal_separation_events(t,np.full(8,.2),np.ones(8,bool))==[]


def test_causality_and_occlusion_reset():
    t=np.arange(9)*.01;d=np.array([.01,.01,.01,.2,.25,.3,.1,.1,.1])
    full=causal_separation_events(t,d,np.ones(9,bool))
    for k in range(1,10):
        prefix=causal_separation_events(t[:k],d[:k],np.ones(k,bool))
        assert prefix==[e for e in full if e['decision_s']<=t[k-1]]
    vis=np.ones(9,bool);vis[3]=False
    assert causal_separation_events(t,d,vis)==[]
    with pytest.raises(ValueError):causal_separation_events([.1,.1],[.01,.1],[1,1])


def test_event_matching_one_to_one_and_empty():
    m=match_events([.1,.11],[.1],.02)
    assert m['true_positive']==1 and m['false_positive']==1 and m['false_negative']==0
    m=match_events([],[],.02);assert m['precision'] is None and m['recall'] is None


def test_fifo_and_timestamp_validation():
    d=fifo_latencies([0,.01,.02],[.02,.02,.02]);assert_allclose(d,[.02,.03,.04])
    assert summarize_latencies(d)['p95_s']>=summarize_latencies(d)['p50_s']
    with pytest.raises(ValueError):fifo_latencies([0,.01],[-1,.1])
