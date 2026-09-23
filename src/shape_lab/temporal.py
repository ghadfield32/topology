"""Causal hypotheses and timing exercises. Never certify human contact from proximity."""
from __future__ import annotations
import numpy as np


def _times(times):
    t=np.asarray(times,float)
    if t.ndim!=1 or not np.isfinite(t).all() or np.any(np.diff(t)<=0):raise ValueError('Times must be finite and strictly increasing.')
    return t


def causal_separation_events(times,distance,visible,near:float=.03,far:float=.1,min_near:int=3,min_far:int=2,max_gap_s:float=.05):
    """Past-only near-then-far state machine, with conservative reset on missing evidence.

    Onset is the first far observation in the confirmed far run; decision is
    the later confirmation timestamp. Values are already in a shared frame/unit.
    Proximity is not possession/contact. Each event is only a separation candidate.
    """
    t=_times(times);d=np.asarray(distance,float);v=np.asarray(visible,bool)
    if d.shape!=t.shape or v.shape!=t.shape or not np.isfinite([near,far,max_gap_s]).all() or not 0<=near<far or max_gap_s<=0 or min_near<1 or min_far<1:raise ValueError('Invalid distances, visibility, thresholds or confirmation counts.')
    out=[];n=0;f=0;armed=False;start=None
    for i in range(len(t)):
        if not v[i] or not np.isfinite(d[i]) or d[i]<0 or (i and t[i]-t[i-1]>max_gap_s):
            n=0;f=0;armed=False;start=None;continue
        if d[i]<=near:
            n+=1;f=0;start=None
            if n>=min_near:armed=True
        elif d[i]>=far:
            n=0
            if armed:
                if not f:start=float(t[i])
                f+=1
                if f>=min_far:
                    out.append({'label':'separation_candidate','onset_s':start,'decision_s':float(t[i]),'contact_certified':False,'evidence':'observed_distance_thresholds'})
                    armed=False;f=0;start=None
        else:
            n=0;f=0;start=None
    return out


def match_events(predicted_onsets,reference_onsets,tolerance_s:float=.03):
    """Maximum-cardinality 1D chronological matching within a symmetric tolerance.

    Stable greedy earliest feasible matches; not minimum-error matching among
    equally sized matchings. Every prediction/reference is used at most once.
    """
    p=np.sort(np.asarray(predicted_onsets,float));r=np.sort(np.asarray(reference_onsets,float))
    if p.ndim!=1 or r.ndim!=1 or not np.isfinite(p).all() or not np.isfinite(r).all() or not np.isfinite(tolerance_s) or tolerance_s<0:raise ValueError('Finite onset vectors and nonnegative tolerance required.')
    i=j=0;errors=[]
    while i<len(p) and j<len(r):
        if p[i]<r[j]-tolerance_s:i+=1
        elif r[j]<p[i]-tolerance_s:j+=1
        else:errors.append(float(p[i]-r[j]));i+=1;j+=1
    n=len(errors)
    return {'true_positive':n,'false_positive':len(p)-n,'false_negative':len(r)-n,
            'precision':n/len(p) if len(p) else None,'recall':n/len(r) if len(r) else None,
            'matched_signed_onset_errors_s':errors}


def fifo_latencies(arrival_times,service_times):
    """Single-server FIFO simulation; not measured hardware latency."""
    a=_times(arrival_times);s=np.asarray(service_times,float)
    if s.shape!=a.shape or not np.isfinite(s).all() or np.any(s<0):raise ValueError('Nonnegative finite service time per arrival required.')
    finish=-np.inf;lat=[]
    for t,duration in zip(a,s):
        finish=max(finish,t)+duration;lat.append(finish-t)
    return np.asarray(lat)


def summarize_latencies(latencies):
    x=np.asarray(latencies,float)
    if x.ndim!=1 or not len(x) or not np.isfinite(x).all() or np.any(x<0):raise ValueError('Nonempty nonnegative finite latency vector required.')
    return {'n':len(x),'p50_s':float(np.quantile(x,.5)),'p95_s':float(np.quantile(x,.95)),'max_s':float(x.max())}
