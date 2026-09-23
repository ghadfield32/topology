# Stage 04 — coding practice solutions

Attempt the learner notebook first. The following code and checks are the canonical reference, with limited declared input assumptions.

## 04.C1 — Compose permutations

Represent a permutation by p[i], the image of i. Return p after q: apply q first, then p.

```python
def compose(p,q):
    return tuple(p[q[i]] for i in range(len(q)))
```

Function composition is associative but need not commute. Recording the convention prevents an apparent disagreement caused only by reversing the order of application.

### Visible checks
```python
r=(1,2,3,0);s=(0,3,2,1)
assert compose(r,s)!=(compose(s,r))
assert compose(r,(0,1,2,3))==r
print("Rotation after reflection:",compose(r,s),"reverse:",compose(s,r))
```

## 04.C2 — Invert a permutation

For a valid permutation of 0..n-1 return the inverse tuple.

```python
def invert_permutation(p):
    inverse=[0]*len(p)
    for i,value in enumerate(p): inverse[value]=i
    return tuple(inverse)
```

An inverse undoes the operation, not the numerical values stored in the representation. A rotation inverse is a rotation in the opposite direction.

### Visible checks
```python
p=(1,2,3,0);q=invert_permutation(p)
assert tuple(p[q[i]] for i in range(4))==(0,1,2,3)
assert q==(3,0,1,2)
print("Inverse:",q)
```

## 04.C3 — Rotate a real image through a group action

Return an image rotated k quarter-turns counterclockwise. Verify that four quarter-turns restore exactly the same array.

```python
def quarter_turn(image,k):
    return np.rot90(np.asarray(image),k=k)
```

The array transformation is exact, but the class meaning need not be invariant: rotating handwriting can change its interpretation. Mathematical symmetry and a task-appropriate data augmentation are different claims.

### Visible checks
```python
image,sample_id=digit_example(6)
assert np.array_equal(quarter_turn(image,4),image)
assert np.array_equal(quarter_turn(quarter_turn(image,1),1),quarter_turn(image,2))
print("C4 action checked on training image",sample_id)
```

## 04.C4 — Write an annulus deformation

For a nonzero point x in an annulus around the origin, return H(x,t)=((1-t)+t/||x||)x for 0<=t<=1.

```python
def radial_homotopy(x,t):
    x=np.asarray(x,dtype=float)
    return ((1-t)+t/np.linalg.norm(x))*x
```

These checks illustrate endpoints and the fixed subspace. The continuous formula and its domain justify the deformation retraction; a finite set of successful tests cannot by itself prove continuity.

### Visible checks
```python
assert np.allclose(radial_homotopy([2,0],0),[2,0])
assert np.allclose(radial_homotopy([2,0],1),[1,0])
for t in np.linspace(0,1,7): assert np.allclose(radial_homotopy([0,1],t),[0,1])
print("Start, end, and fixed-circle conditions checked")
```

## 04.C5 — Reduce a word with inverse pairs

Use lowercase a,b and uppercase A,B for formal generators and inverses. Cancel adjacent inverse pairs until no more remain.

```python
def reduce_word(word):
    stack=[]
    for letter in word:
        if stack and stack[-1].swapcase()==letter: stack.pop()
        else: stack.append(letter)
    return ''.join(stack)
```

This is a formal free-group word model. It shows why loop order can matter in spaces such as a figure-eight. It does not establish the fundamental group of every pictured shape.

### Visible checks
```python
assert reduce_word('abBA')==''
assert reduce_word('abAB')=='abAB'
assert reduce_word('aaA')=='a'
print("A commutator does not cancel in the free-word model:",reduce_word('abAB'))
```

