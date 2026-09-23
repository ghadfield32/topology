# Coding answer explanations


## leakage.C1

Return sorted row-index overlap.

Set intersection answers row overlap only.

```python
def shared_rows(left,right):
    """Sorted intersection of row identities, not underlying participant identities."""
    return sorted(set(left)&set(right))
```

Check:
```python
assert shared_rows([0,2],[1,3]) == []
```

## leakage.C2

Return sorted shared unit IDs for two groups of rows.

Resolve rows to source units before intersecting.

```python
def shared_units(left,right,units):
    """Underlying unit IDs may overlap even when row indices do not."""
    u=np.asarray(units)
    return sorted(set(u[left])&set(u[right]))
```

Check:
```python
assert shared_units([0,2],[1,3],['A','A','B','B']) == ['A','B']
```

## leakage.C3

Return row indices in selected units and in all remaining units.

Build a membership mask; keep all copies together.

```python
def partition_by_units(units,selected):
    """Put all rows of each selected unit together; does not prove independence."""
    mask=np.isin(np.asarray(units),list(selected))
    return np.flatnonzero(mask),np.flatnonzero(~mask)
```

Check:
```python
a,b=partition_by_units(['a','b','a','c'],['a'])
assert a.tolist()==[0,2] and b.tolist()==[1,3]
```

## leakage.C4

Apply previously fitted feature centers and positive scales.

Broadcast feature-wise arrays; do not fit anything inside this function.

```python
def apply_scaler(x,center,scale):
    """Apply fixed training parameters. Never refit them on validation or test."""
    x=np.asarray(x,float);c=np.asarray(center,float);s=np.asarray(scale,float)
    if x.ndim!=2 or c.shape!=(x.shape[1],) or s.shape!=c.shape or np.any(s<=0) or not np.isfinite(x).all() or not np.isfinite(c).all() or not np.isfinite(s).all():raise ValueError('Matching finite data and positive scales required')
    return (x-c)/s
```

Check:
```python
assert np.allclose(apply_scaler([[6,2]],[2,2],[2,1]),[[2,0]])
```
