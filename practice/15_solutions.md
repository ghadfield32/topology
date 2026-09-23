# Stage 15 coding solutions

Attempt your learner notebook before opening this file.

## 15.C1 — stereo_depth

Compute camera-axis depth with the principal-point offset. Nonfinite disparity or a nonpositive denominator yields NaN. f and B are known positive scalars.

**Hint:** Use Z=fB/(d+offset); do not replace invalid data with zero.

```python
def stereo_depth(disparity, focal, baseline, offset):
    d=np.asarray(disparity,float);den=d+offset
    valid=np.isfinite(d)&(den>0)
    z=np.full(d.shape,np.nan)
    np.divide(focal*baseline,den,out=z,where=valid)
    return z
```

The output unit follows the baseline. Offset is in pixels and is added to disparity before division.

### Checks

```python
z=stereo_depth([50,np.nan,np.inf,-20],1000,.2,20)
assert np.isclose(z[0],200/70)
assert np.isnan(z[1:]).all()
from shape_lab.stereo import reference_sample
_,_,d,c=reference_sample();z=stereo_depth(d,c['focal_px'],c['baseline_m'],c['doffs_px'])
assert z.shape==d.shape and np.all(z[np.isfinite(z)]>0)
```

## 15.C2 — error_and_coverage

For matching-shaped arrays, report MAE over finite paired values and coverage relative to finite reference values. Return None when a denominator is absent.

**Hint:** An accurate result on very few points must not hide missing coverage.

```python
def error_and_coverage(predicted, reference):
    p=np.asarray(predicted,float);r=np.asarray(reference,float)
    if p.shape!=r.shape:raise ValueError("Shapes must match.")
    eligible=np.isfinite(r);valid=eligible&np.isfinite(p)
    return {"mae":float(np.mean(abs(p[valid]-r[valid]))) if valid.any() else None,
            "coverage":float(valid.sum()/eligible.sum()) if eligible.any() else None}
```

Coverage is not evaluated count divided by all array entries when some references are themselves missing.

### Checks

```python
assert error_and_coverage([1,np.nan,5],[2,3,np.nan])=={'mae':1.,'coverage':.5}
assert error_and_coverage([np.nan],[np.nan])=={'mae':None,'coverage':None}
```

## 15.C3 — conditional_depth_sd

Compute the first-order depth standard deviation when only disparity is uncertain and f, B, offset are fixed.

**Hint:** Differentiate fB/(d+offset), then multiply the derivative magnitude by σd.

```python
def conditional_depth_sd(disparity, focal, baseline, offset, disparity_sd):
    if disparity+offset<=0 or disparity_sd<0:raise ValueError("Positive denominator and nonnegative SD required.")
    return focal*baseline/(disparity+offset)**2*disparity_sd
```

This is conditional local uncertainty, not total sensor or model uncertainty. It can fail near degeneracy or with substantial noise.

### Checks

```python
assert np.isclose(conditional_depth_sd(60,1000,.2,20,.2),.00625)
assert conditional_depth_sd(60,1000,.2,20,0)==0
assert conditional_depth_sd(20,1000,.2,20,.2)>conditional_depth_sd(60,1000,.2,20,.2)
```