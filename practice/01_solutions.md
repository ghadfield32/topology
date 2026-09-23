# Stage 01 — coding practice solutions

Attempt the learner notebook first. The following code and checks are the canonical reference, with limited declared input assumptions.

## 01.C1 — Compute a finite preimage

Given a function f, a finite candidate domain, and a target set, return every candidate x whose output lies in the target.

```python
def preimage(f, domain, target):
    return {x for x in domain if f(x) in target}
```

For the square function two inputs can share an output. Both must be returned. The finite calculation illustrates the definition but does not enumerate an infinite real-line preimage.

### Visible checks
```python
assert preimage(lambda x:x*x,range(-3,4),{1,4})=={-2,-1,1,2}
frame=load_iris_data();mapping=dict(zip(frame.sample_id,frame.label))
ids=preimage(mapping.__getitem__,mapping,{0})
assert len(ids)==50
print("Recorded label-0 preimage contains",len(ids),"sample IDs")
```

## 01.C2 — Build equivalence classes

Partition the given integers by remainder modulo the positive integer m. Return a dictionary from remainders to sets.

```python
def residue_classes(values, m):
    groups={}
    for x in values:
        groups.setdefault(x%m,set()).add(x)
    return groups
```

Every input belongs to exactly one class. This is a partition of the supplied integers. A quotient will later use classes themselves as new mathematical objects.

### Visible checks
```python
g=residue_classes(range(-3,4),3)
assert g[0]=={-3,0,3} and g[1]=={-2,1} and g[2]=={-1,2}
assert set().union(*g.values())==set(range(-3,4))
print("Classes:",g)
```

## 01.C3 — Multiply a matrix and vector by hand

For a rectangular numeric list A and a vector x of matching length, implement Ax with loops.

```python
def matvec(A, x):
    return [sum(a*b for a,b in zip(row,x)) for row in A]
```

The assumptions require matching dimensions; zip alone is not a general input validator. Explain the map from a four-coordinate vector to a three-coordinate output for this particular matrix.

### Visible checks
```python
assert matvec([[1,1],[0,0]],[2,-2])==[0,0]
A=load_iris_data().iloc[:3,1:5].to_numpy()
x=np.array([1,0,0,0])
assert np.allclose(matvec(A,x),A[:,0])
print("Selecting one measurement by matrix multiplication:",matvec(A,x))
```

## 01.C4 — Connect rank to nullity

For an integer-valued matrix, return (rank, nullity) over F2 using the supplied rank_mod2. Explain why the number of columns appears.

```python
def rank_nullity_f2(A):
    A=np.asarray(A)
    rank=rank_mod2(A)
    return rank,A.shape[1]-rank
```

The same integer entries define different linear maps over different fields. The F2 sum of all three rows is zero, but the real-valued relation is different.

### Visible checks
```python
A=np.array([[1,1,0],[1,0,1],[0,1,1]])
assert rank_nullity_f2(A)==(2,1)
assert np.linalg.matrix_rank(A)==3
print("F2 rank/nullity",rank_nullity_f2(A),"versus real rank",np.linalg.matrix_rank(A))
```

## 01.C5 — Center a measurement table

Return a copy of a finite nonempty feature matrix with each column mean subtracted. This exercise is exploratory, not a predictive preprocessing fit.

```python
def centered(X):
    X=np.asarray(X,dtype=float)
    return X-X.mean(axis=0)
```

Subtracting the same vector from every point changes the coordinate origin but not pairwise differences. A learned predictive scaler, unlike this exploratory illustration, must fit only on the designated development partition.

### Visible checks
```python
X=load_iris_data().iloc[:,1:5].to_numpy()
Z=centered(X)
assert np.allclose(Z.mean(axis=0),0,atol=1e-12)
assert np.allclose(Z[0]-Z[1],X[0]-X[1])
print("Centered means:",Z.mean(axis=0))
```

