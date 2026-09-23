# Stage 18 coding solutions

Attempt your learner notebook before opening this file.

## 18.C1 — fifo_age

Simulate single-server FIFO completion age for strictly increasing finite arrivals and nonnegative service times.

**Hint:** Completion i = max(arrival i, previous completion)+service i.

```python
def fifo_age(arrivals, service_times):
    a=np.asarray(arrivals,float);s=np.asarray(service_times,float)
    if a.ndim!=1 or a.shape!=s.shape or not np.isfinite(a).all() or not np.isfinite(s).all() or np.any(np.diff(a)<=0) or np.any(s<0):raise ValueError("Ordered arrivals and nonnegative times required.")
    finish=-np.inf;out=[]
    for t,d in zip(a,s):
        finish=max(finish,t)+d;out.append(finish-t)
    return np.asarray(out)
```

This simulation shows queueing; it is not measured processing time and does not model parallel workers or dropped frames.

### Checks

```python
assert np.allclose(fifo_age([0,1,2],[2,2,2]),[2,3,4])
assert np.allclose(fifo_age([0,1,2],[.2,.2,.2]),[.2,.2,.2])
```

## 18.C2 — latency_quantiles

Return p50 and p95 for a nonempty finite nonnegative latency vector using NumPy default linear quantile interpolation.

**Hint:** Keep the unit unchanged and declare the quantile convention.

```python
def latency_quantiles(latencies):
    x=np.asarray(latencies,float)
    if x.ndim!=1 or not len(x) or not np.isfinite(x).all() or np.any(x<0):raise ValueError("Finite nonnegative nonempty vector required.")
    return {"p50":float(np.quantile(x,.5)),"p95":float(np.quantile(x,.95))}
```

A p95 from five values is a descriptive statistic with very little tail evidence. More decimal places do not create more observations.

### Checks

```python
q=latency_quantiles([1,2,3,4,5])
assert q['p50']==3 and np.isclose(q['p95'],4.8)
```

## 18.C3 — vector_rigid

Vectorize a rigid transform over a valid finite Nx3 point table. Inputs are already validated for this exercise.

**Hint:** Broadcast the translation over rows.

```python
def vector_rigid(points, rotation, translation):
    return np.asarray(points,float)@np.asarray(rotation,float).T+np.asarray(translation,float)
```

Equal results must be verified before comparing performance. Vectorization does not remove the need to preserve source IDs or timestamps.

### Checks

```python
from shape_lab.stereo import reference_sample,point_cloud
from shape_lab.geometry import exp_so3
_,_,d,c=reference_sample();X,_=point_cloud(d,c,stride=50);R=exp_so3([.1,0,.2]);t=np.array([1.,2.,3.])
assert np.allclose(vector_rigid(X,R,t),np.array([R@x+t for x in X]))
```