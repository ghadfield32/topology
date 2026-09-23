# Stage 02 — coding practice solutions

Attempt the learner notebook first. The following code and checks are the canonical reference, with limited declared input assumptions.

## 02.C1 — Manhattan distance

Calculate the sum of absolute coordinate differences for two equal-length vectors.

```python
def manhattan(x,y):
    return sum(abs(a-b) for a,b in zip(x,y))
```

Different metrics express different notions of closeness. A seven-unit Manhattan distance between (0,0) and (3,4) does not contradict their five-unit Euclidean distance.

### Visible checks
```python
assert manhattan([0,0],[3,4])==7
X=load_iris_data().iloc[:2,1:5].to_numpy()
assert np.isclose(manhattan(X[0],X[1]),np.abs(X[0]-X[1]).sum())
print("First two measured flowers, L1 distance:",manhattan(X[0],X[1]))
```

## 02.C2 — A Euclidean distance matrix

Return the square matrix D whose entry i,j is the Euclidean distance between observations i and j.

```python
def distances(X):
    X=np.asarray(X,dtype=float)
    return np.sqrt(((X[:,None,:]-X[None,:,:])**2).sum(axis=2))
```

An n by n distance matrix is not the original n by d feature matrix. Its entries carry the units and scaling choices of the input coordinates.

### Visible checks
```python
D=distances([[0,0],[3,4],[3,0]])
assert np.allclose(D,[[0,5,3],[5,0,4],[3,4,0]])
X=load_iris_data().iloc[:8,1:5].to_numpy();D=distances(X)
assert np.allclose(D,D.T) and np.allclose(np.diag(D),0)
print("Real-data distance matrix shape:",D.shape)
```

## 02.C3 — Open neighborhoods versus graph thresholds

Given distances from a center, return indices strictly inside radius r. The open-ball definition uses <, not <=.

```python
def open_ball_indices(distances_from_center,r):
    return set(np.flatnonzero(np.asarray(distances_from_center)<r).tolist())
```

Topological open balls and our closed threshold Rips edges use different endpoint conventions. Tiny differences at equal values can change hand-derived birth and death endpoints.

### Visible checks
```python
assert open_ball_indices([0,1,2],1)=={0}
X=load_iris_data().iloc[:10,1:5].to_numpy()
d=np.linalg.norm(X-X[0],axis=1)
print("Sample IDs in radius 0.5 (restricted to first 10 rows):",sorted(open_ball_indices(d,.5)))
```

## 02.C4 — Validate a finite topology

For a finite universe U and a finite collection of candidate open sets, check empty/full membership, containment, and closure under pairwise unions and intersections.

```python
def finite_topology(U,opens):
    U=frozenset(U);T=set(map(frozenset,opens))
    return (frozenset() in T and U in T and all(A<=U for A in T)
            and all(A|B in T and A&B in T for A in T for B in T))
```

For a finite collection, binary union closure yields arbitrary union closure because only finitely many distinct members can contribute. This finite shortcut does not replace the arbitrary-union axiom for infinite spaces.

### Visible checks
```python
assert finite_topology({0,1},[set(),{1},{0,1}])
assert not finite_topology({0,1},[set(),{1}])
assert not finite_topology({0,1,2},[set(),{0},{1},{0,1,2}])
print("Finite topology examples checked")
```

## 02.C5 — Find a neighbor without leaking labels

Return the nearest distinct row position to row i using only the given numeric features. Break ties with the smallest row position.

```python
def nearest_other(X,i):
    X=np.asarray(X,dtype=float)
    d=np.linalg.norm(X-X[i],axis=1)
    d[i]=np.inf
    return int(np.argmin(d))
```

Duplicate measured coordinates can occur at distinct row IDs; they may be valid zero-distance neighbors. That creates a pseudometric on observation identities, not an excuse to silently delete observations.

### Visible checks
```python
assert nearest_other([[0],[1],[3]],1)==0
X=load_iris_data().iloc[:,1:5].to_numpy()
j=nearest_other(X,0)
assert j!=0
print("Nearest other row to Iris sample 0:",j)
```

