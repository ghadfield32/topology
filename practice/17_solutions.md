# Stage 17 coding solutions

Attempt your learner notebook before opening this file.

## 17.C1 — apply_similarity

Apply Y=sRX+t to an Nx3 row table. Assume R is already validated as a proper rotation; require positive s.

**Hint:** For a row table use points @ rotation.T.

```python
def apply_similarity(points, scale, rotation, translation):
    if not np.isfinite(scale) or scale<=0:raise ValueError("Positive finite scale required.")
    return scale*np.asarray(points,float)@np.asarray(rotation,float).T+np.asarray(translation,float)
```

The transpose appears because the stored table uses rows; it is the same mapping as the column-vector equation.

### Checks

```python
R=np.array([[0,-1,0],[1,0,0],[0,0,1.]])
assert np.allclose(apply_similarity([[1,0,0]],2,R,[1,1,1]),[[1,3,1]])
```

## 17.C2 — paired_rmse

Compute Euclidean position RMSE for finite, corresponding, nonempty Nx3 tables.

**Hint:** Square distances per point, average over points, then take the square root.

```python
def paired_rmse(predicted, reference):
    p=np.asarray(predicted,float);r=np.asarray(reference,float)
    if p.shape!=r.shape or p.ndim!=2 or p.shape[1]!=3 or not len(p) or not np.isfinite(p).all() or not np.isfinite(r).all():raise ValueError("Finite nonempty corresponding Nx3 tables required.")
    return float(np.sqrt(np.mean(np.sum((p-r)**2,axis=1))))
```

A component-wise mean across all coordinates differs by a factor of √3. State exactly which convention is reported.

### Checks

```python
assert paired_rmse([[3,4,0]],[[0,0,0]])==5
assert paired_rmse([[0,0,0],[0,0,0]],[[0,0,0],[0,0,0]])==0
```

## 17.C3 — split_is_disjoint

Check that each ID list has no duplicate and no ID is used in both roles.

**Hint:** Sets expose both duplicates and overlap.

```python
def split_is_disjoint(anchor_ids, evaluation_ids):
    a=list(anchor_ids);b=list(evaluation_ids)
    return len(a)==len(set(a)) and len(b)==len(set(b)) and not (set(a)&set(b))
```

A disjoint ID check is necessary but not sufficient for statistical independence; nearby points or same-session observations may remain dependent.

### Checks

```python
assert split_is_disjoint([1,2],[3,4])
assert not split_is_disjoint([1,2],[2,3])
assert not split_is_disjoint([1,1],[3])
```