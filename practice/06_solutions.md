# Stage 06 — coding practice solutions

Attempt the learner notebook first. The following code and checks are the canonical reference, with limited declared input assumptions.

## 06.C1 — Add chains over F2

Represent a chain by the set of simplices with coefficient 1. Return the sum of two chains.

```python
def add_chains(a,b):
    return set(a)^set(b)
```

This is coefficient arithmetic, not geometric deletion. A simplex appearing twice has coefficient 1+1=0 in F2.

### Visible checks
```python
assert add_chains({(0,1),(1,2)},{(1,2),(0,2)})=={(0,1),(0,2)}
assert add_chains({(0,1)},{(0,1)})==set()
print("Repeated simplices cancel over F2")
```

## 06.C2 — Implement binary matrix rank

Implement Gaussian elimination over F2 for a two-dimensional integer array. Return rank; do not call rank_mod2 inside your solution.

```python
def my_rank_f2(matrix):
    A=(np.asarray(matrix,dtype=int)%2).copy();row=0
    for col in range(A.shape[1]):
        candidates=np.flatnonzero(A[row:,col])
        if len(candidates)==0: continue
        pivot=row+int(candidates[0]);A[[row,pivot]]=A[[pivot,row]]
        for i in range(row+1,A.shape[0]):
            if A[i,col]: A[i]^=A[row]
        row+=1
        if row==A.shape[0]: break
    return row
```

Every row operation preserves the row-space dimension over F2. Zero-row and zero-column matrices arise naturally at the ends of chain complexes.

### Visible checks
```python
rng=np.random.default_rng(62)
for shape in [(0,3),(3,0),(3,3),(5,7)]:
    A=rng.integers(0,2,size=shape)
    assert my_rank_f2(A)==rank_mod2(A)
assert my_rank_f2([[1,1,0],[1,0,1],[0,1,1]])==2
print("Binary rank checked on empty and nonempty arrays")
```

## 06.C3 — Use the Betti rank formula

Given the number n_k of k-simplices and ranks of boundary maps out of and into C_k, return beta_k. Assume valid chain-complex data.

```python
def betti_from_ranks(n_k,rank_out,rank_in):
    return n_k-rank_out-rank_in
```

The formula uses rank-nullity and the fact that the incoming boundary image lies inside the outgoing kernel. Arbitrary unrelated matrices need not satisfy that containment.

### Visible checks
```python
assert betti_from_ranks(3,2,0)==1
assert betti_from_ranks(3,2,1)==0
print("Triangle outline H1=1; filled triangle H1=0")
```

## 06.C4 — Compare cycles with boundaries

Return beta_1 for a triangle outline and the filled triangle, in that order, using the supplied finite homology helpers.

```python
def triangle_h1_pair():
    outline=closure([(0,1),(1,2),(0,2)])
    filled=closure([(0,1,2)])
    return betti_numbers(outline,1)[1],betti_numbers(filled,1)[1]
```

This distinction prevents the common mistake that a class dies because a loop-shaped set of edges literally disappears.

### Visible checks
```python
assert triangle_h1_pair()==(1,0)
K=closure([(0,1,2)])
assert np.all((boundary_matrix(K,1)@boundary_matrix(K,2))%2==0)
print("Cycle remains an edge chain, but becomes a boundary when a face enters")
```

## 06.C5 — Count loops across an image threshold

Return H1 Betti numbers of the declared closed-pixel model at each requested threshold.

```python
def image_betti1(image,thresholds):
    f=pixel_filtration(1-np.asarray(image,dtype=float)/16)
    return [betti_numbers([s for s,v in f if v<=t],1)[1] for t in thresholds]
```

The counts can increase and decrease. They are properties of the filtered pixel object, not a guaranteed match to the number of holes a reader sees in the printed digit.

### Visible checks
```python
image,sample_id=digit_example(8)
values=image_betti1(image,[0,.25,.5,.75,1])
assert all(v>=0 for v in values) and values[-1]==0
print("Training image",sample_id,"H1 counts:",values)
```

