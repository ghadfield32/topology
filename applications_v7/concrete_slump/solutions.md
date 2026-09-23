# Coding answer explanations


## concrete_slump.C1

Compute each absolute prediction error while preserving target units.

Subtract matching vectors, then take absolute values.

```python
def absolute_errors(y,prediction):
    """Absolute residuals retain the physical units of the target."""
    y=np.asarray(y,float);p=np.asarray(prediction,float)
    if y.ndim!=1 or p.shape!=y.shape or not y.size or not np.isfinite(y).all() or not np.isfinite(p).all():raise ValueError('Matching finite vectors required')
    return np.abs(y-p)
```

Check:
```python
assert np.allclose(absolute_errors([20,30,40],[22,25,43]),[2,5,3])
```

## concrete_slump.C2

Return lower and upper prediction bounds for a fixed nonnegative radius.

One radius is used on both sides. Do not refit it on these outcomes.

```python
def interval_bounds(prediction,radius):
    """Closed symmetric intervals. Negative lower strength is not silently clipped."""
    p=np.asarray(prediction,float);r=float(radius)
    if p.ndim!=1 or not p.size or not np.isfinite(p).all() or np.isnan(r) or r<0:raise ValueError('Finite predictions and nonnegative radius required')
    return p-r,p+r
```

Check:
```python
lo,hi=interval_bounds([30.],8.)
assert np.allclose(lo,[22.]) and np.allclose(hi,[38.])
```

## concrete_slump.C3

Compute the fraction inside closed lower/upper bounds.

Both inequalities must hold; the boundary counts as covered.

```python
def empirical_coverage(y,lower,upper):
    """Fraction of this finite sample within the supplied closed bounds."""
    y=np.asarray(y,float);lo=np.asarray(lower,float);hi=np.asarray(upper,float)
    if y.ndim!=1 or lo.shape!=y.shape or hi.shape!=y.shape or not y.size or not np.isfinite(y).all() or np.isnan(lo).any() or np.isnan(hi).any() or np.any(lo>hi):raise ValueError('Matching ordered interval bounds required')
    return float(np.mean((lo<=y)&(y<=hi)))
```

Check:
```python
assert empirical_coverage([0,1,2],[-1,0,0],[0,1,1]) == 2/3
```

## concrete_slump.C4

Predict the training mean for n future cases.

The test outcomes are not an argument to this function.

```python
def mean_baseline(training_y,n):
    """A constant prediction fitted only to training outcomes."""
    y=np.asarray(training_y,float)
    if y.ndim!=1 or not y.size or not np.isfinite(y).all() or not isinstance(n,int) or n<1:raise ValueError('Finite training outcomes and positive count required')
    return np.full(n,y.mean())
```

Check:
```python
assert np.allclose(mean_baseline([2.,6.],3),[4,4,4])
```
