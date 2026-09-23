# Stage 03 — coding practice solutions

Attempt the learner notebook first. The following code and checks are the canonical reference, with limited declared input assumptions.

## 03.C1 — Pull back a set through a map

Given a total mapping dictionary and a codomain subset V, return its inverse image.

```python
def pullback(mapping,V):
    return {x for x,y in mapping.items() if y in V}
```

The operation works even when several inputs share an output. It is exactly the operation appearing in the topological definition of continuity.

### Visible checks
```python
assert pullback({'a':0,'b':1,'c':1},{1})=={'b','c'}
assert pullback({'a':0},set())==set()
print("Inverse images computed")
```

## 03.C2 — Check continuity on finite spaces

Assume the supplied open-set collections are valid topologies and mapping is total. Return whether every codomain open set has an open inverse image.

```python
def continuous_on_finite(mapping,domain_opens,codomain_opens):
    T=set(map(frozenset,domain_opens))
    return all(frozenset(x for x,y in mapping.items() if y in V) in T for V in codomain_opens)
```

The identity is a bijection of the underlying sets, yet changing the topologies can make its inverse discontinuous. This is a concrete reason that continuous bijection is not the definition of homeomorphism.

### Visible checks
```python
discrete=[set(),{0},{1},{0,1}];indiscrete=[set(),{0,1}];f={0:0,1:1}
assert continuous_on_finite(f,discrete,indiscrete)
assert not continuous_on_finite(f,indiscrete,discrete)
print("Identity continuous in one direction, not the reverse")
```

## 03.C3 — Construct an inverse when it exists

Return the inverse dictionary of a finite injective mapping. Raise ValueError when two inputs share an output.

```python
def inverse_mapping(mapping):
    if len(set(mapping.values()))!=len(mapping):
        raise ValueError('The map is not injective.')
    return {y:x for x,y in mapping.items()}
```

This constructs an inverse onto the image. Surjectivity onto a separately declared larger codomain remains a different condition; dictionary inversion alone does not prove it.

### Visible checks
```python
assert inverse_mapping({'a':2,'b':7})=={2:'a',7:'b'}
try: inverse_mapping({'a':1,'b':1})
except ValueError: pass
else: raise AssertionError('Non-injective map accepted')
print("Inverse and non-injective case checked")
```

## 03.C4 — Count graph components

Count connected components of a symmetric boolean adjacency matrix using a search. An isolated vertex is its own component.

```python
def graph_component_count(A):
    A=np.asarray(A,dtype=bool);seen=set();count=0
    for start in range(len(A)):
        if start in seen: continue
        count+=1;stack=[start];seen.add(start)
        while stack:
            v=stack.pop()
            for w in np.flatnonzero(A[v]):
                if int(w) not in seen:
                    seen.add(int(w));stack.append(int(w))
    return count
```

This counts components of the chosen finite graph, not plant species. Different thresholds give different graphs. For the geometric realization of a finite graph, connected and path-connected components agree.

### Visible checks
```python
assert graph_component_count([[0,1,0],[1,0,0],[0,0,0]])==2
X=load_iris_data().iloc[:12,1:5].to_numpy()
D=np.linalg.norm(X[:,None,:]-X[None,:,:],axis=2)
A=D<=.3
assert graph_component_count(A)==len(np.unique(component_labels(A)))
print("Real-data threshold graph components:",graph_component_count(A))
```

## 03.C5 — Measure information lost in a projection

For a feature table X and distinct rows i,j, return (full distance, distance after retaining the first two columns).

```python
def projection_distances(X,i,j):
    delta=np.asarray(X,dtype=float)[i]-np.asarray(X,dtype=float)[j]
    return float(np.linalg.norm(delta)),float(np.linalg.norm(delta[:2]))
```

A continuous projection can identify points that were distinct. A two-dimensional display is therefore not a certificate that the original higher-dimensional dataset has the same topology.

### Visible checks
```python
assert projection_distances([[0,0,0],[0,0,5]],0,1)==(5.,0.)
X=load_iris_data().iloc[:,1:5].to_numpy()
full,projected=projection_distances(X,0,75)
assert projected<=full+1e-12
print("Measured pair full/projected distances:",full,projected)
```

