# Stage 13 coding solutions

Attempt your learner notebook before opening this file.

## 13.C1 — north_chart

Map an N×3 array of unit sphere points to the north-pole stereographic chart. Reject the excluded pole and points off the sphere.

**Hint:** Use the denominator 1-z separately for each row.

```python
def north_chart(points):
    p=np.asarray(points,float)
    if p.ndim!=2 or p.shape[1]!=3 or not np.isfinite(p).all() or not np.allclose(np.linalg.norm(p,axis=1),1,atol=1e-8,rtol=0):
        raise ValueError("Expected finite unit sphere rows.")
    den=1-p[:,2]
    if np.any(den<=1e-12):raise ValueError("North pole excluded or too close.")
    return p[:,:2]/den[:,None]
```

Division creates chart coordinates, not physical metres. The denominator guard is a numerical conditioning policy, not a modification of the mathematical sphere.

### Checks

```python
assert np.allclose(north_chart([[1,0,0],[0,0,-1]]),[[1,0],[0,0]])
from shape_lab.stereo import reference_sample,point_cloud
_,_,d,c=reference_sample();X,rc=point_cloud(d,c,stride=45);r=X/np.linalg.norm(X,axis=1,keepdims=True)
actual=north_chart(r)
assert actual.shape==(len(r),2)
assert np.isfinite(actual).all()
try:north_chart([[0,0,1]])
except ValueError:pass
else:raise AssertionError("The excluded pole must be rejected.")
```

## 13.C2 — inverse_north

Invert the north-pole chart for finite N×2 coordinates.

**Hint:** Write q=a²+b². The third coordinate is (q-1)/(q+1).

```python
def inverse_north(coordinates):
    a=np.asarray(coordinates,float)
    if a.ndim!=2 or a.shape[1]!=2 or not np.isfinite(a).all():raise ValueError("Expected finite N by 2 coordinates.")
    q=np.sum(a*a,axis=1)
    return np.column_stack([2*a[:,0]/(1+q),2*a[:,1]/(1+q),(q-1)/(q+1)])
```

Substitute the result into the forward map. The inverse has no finite coordinate for the excluded north pole.

### Checks

```python
a=np.array([[0.,0.],[1.,0.],[.3,-.8]])
p=inverse_north(a)
assert np.allclose(np.linalg.norm(p,axis=1),1)
assert np.allclose(p[:,:2]/(1-p[:,2,None]),a)
```

## 13.C3 — tangent_projection

Project a 3D vector onto the tangent plane at a unit sphere point. Validate the unit point.

**Hint:** Remove the component parallel to p.

```python
def tangent_projection(point, vector):
    p=np.asarray(point,float);v=np.asarray(vector,float)
    if p.shape!=(3,) or v.shape!=(3,) or not np.isfinite(p).all() or not np.isfinite(v).all() or not np.isclose(p@p,1):raise ValueError("Unit point and finite 3-vector required.")
    return v-p*(p@v)
```

The projection is (I-ppᵀ)v. It is tangent but adding it directly to p generally leaves the sphere unless followed by an appropriate curve or retraction.

### Checks

```python
p=np.array([1.,2.,3.]);p/=np.linalg.norm(p)
v=tangent_projection(p,[.2,-.1,.5])
assert abs(p@v)<1e-12
assert np.allclose(tangent_projection(p,v),v)
assert np.allclose(tangent_projection(p,p),0)
```