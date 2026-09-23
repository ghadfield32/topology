# Coding answer explanations


## claims.C1

Return (q²+p²)/2 for a finite two-component vector.

A dot product computes the sum of squares.

```python
def oscillator_energy(z):
    """Nondimensional unit harmonic oscillator H=(q**2+p**2)/2."""
    z=np.asarray(z,float)
    if z.shape!=(2,) or not np.isfinite(z).all():raise ValueError('One finite (q,p) vector required')
    return float(z@z/2)
```

Check:
```python
assert np.isclose(oscillator_energy([.96,-.2]),.4808)
```

## claims.C2

Compute the Frobenius norm of A.T J A-J for a 2x2 map.

J is the canonical skew-symmetric matrix, not the identity.

```python
def symplectic_defect(matrix):
    """Frobenius norm of A.T J A - J for a canonical two-dimensional map."""
    a=np.asarray(matrix,float)
    if a.shape!=(2,2) or not np.isfinite(a).all():raise ValueError('A finite 2x2 map is required')
    j=np.array([[0.,1.],[-1.,0.]])
    return float(np.linalg.norm(a.T@j@a-j))
```

Check:
```python
assert symplectic_defect([[.96,.2],[-.2,1.]]) < 1e-14
```

## claims.C3

Apply one linearized correction for x.x=1, rejecting x=0.

This is not radial normalization; preserve the intended formula.

```python
def sphere_newton_step(x):
    """One linearized correction for C(x)=x.x-1; not exact radial projection."""
    a=np.asarray(x,float)
    if a.ndim!=1 or not a.size or not np.isfinite(a).all() or a@a==0:raise ValueError('Nonzero finite vector required')
    return a-((a@a-1)/(2*(a@a)))*a
```

Check:
```python
x=sphere_newton_step([2.,0.])
assert np.allclose(x,[1.25,0.])
```

## claims.C4

Compute the dot product of matching objective gradients.

A negative value signals a local conflict, not its universal cure.

```python
def gradient_inner_product(g1,g2):
    """A negative inner product indicates conflicting first-order objectives."""
    a=np.asarray(g1,float);b=np.asarray(g2,float)
    if a.ndim!=1 or a.shape!=b.shape or not a.size or not np.isfinite(a).all() or not np.isfinite(b).all():raise ValueError('Matching finite gradients required')
    return float(a@b)
```

Check:
```python
assert gradient_inner_product([1,0],[-1,0]) == -1
```
