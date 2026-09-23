# Coding answer explanations


## seeds.C1

Return the two dimensions of a 2D array; explain what each dimension counts.

Use the array's shape after checking that it has two axes.

```python
def table_dimensions(x):
    """Rows are observations; columns are the selected fields, not labels by default."""
    a=np.asarray(x)
    if a.ndim!=2: raise ValueError('A two-dimensional table is required')
    return a.shape
```

Check:
```python
assert table_dimensions(np.ones((210, 7))) == (210, 7)
```

## seeds.C2

Calculate 4πA/P² for matching positive area and perimeter arrays.

Square the perimeter, not the area. The circle is an exact control.

```python
def compactness(area,perimeter):
    """4*pi*A/P**2; length units must be consistent before using this formula."""
    a=np.asarray(area,float);p=np.asarray(perimeter,float)
    if a.shape!=p.shape or not np.isfinite(a).all() or not np.isfinite(p).all() or np.any(a<=0) or np.any(p<=0):
        raise ValueError('Matching positive finite areas and perimeters required')
    return 4*np.pi*a/p**2
```

Check:
```python
assert np.allclose(compactness([np.pi], [2*np.pi]), [1.])
```

## seeds.C3

Return training column means and population standard deviations; replace a zero scale with one.

axis=0 aggregates observations, preserving a parameter per feature.

```python
def fit_scaler(x):
    """Population standard deviation (ddof=0); constant columns get scale one."""
    a=np.asarray(x,float)
    if a.ndim!=2 or not a.size or not np.isfinite(a).all():raise ValueError('Finite nonempty 2D data required')
    center=a.mean(axis=0);scale=a.std(axis=0)
    return center,np.where(scale==0,1.,scale)
```

Check:
```python
c,s=fit_scaler([[0.,9.],[2.,9.]])
assert np.allclose(c,[1.,9.]) and np.allclose(s,[1.,1.])
```

## seeds.C4

Return the observed integer-label frequencies as a dictionary.

np.unique can return both values and counts. Do not infer class names.

```python
def class_counts(labels):
    """Counts observed integer classes, without guessing their semantic names."""
    values,counts=np.unique(np.asarray(labels),return_counts=True)
    return {int(k):int(v) for k,v in zip(values,counts)}
```

Check:
```python
assert class_counts([3,1,3,2]) == {1:1,2:1,3:2}
```
