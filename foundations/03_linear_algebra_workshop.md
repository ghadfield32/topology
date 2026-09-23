# Foundation D — The linear algebra behind counting holes

Persistent homology becomes computational because finite chains form vector spaces and taking a boundary is a linear map. This foundation explains what those words contribute. You do not need eigenvectors or deep neural networks to begin.

## Linear combinations and independent directions

In ℝ², the vectors e₁=(1,0) and e₂=(0,1) generate every vector: (a,b)=a e₁+b e₂. They form a basis because they span the space and neither is a multiple of the other. The vectors (1,0), (0,1), and (1,1) still span the plane but are not a basis: the third equals the sum of the first two.

A list v₁,…,v_r is linearly independent when the equation a₁v₁+…+a_rv_r=0 forces all coefficients to be zero. The coefficients come from a specified field. Over ℝ, they are real numbers. Over F₂, they are zero or one and all arithmetic is modulo two.

A subspace contains zero and is closed under vector addition and scalar multiplication. The line y=x through the origin is a real subspace. The parallel line y=x+1 is not: it does not contain zero. This explains why an arbitrary cloud of data points is not itself generally a vector subspace.

## A matrix is a rule for moving vectors

Let A=[[1,1],[0,0]]. Then A(x,y)=(x+y,0). The first and second columns are where A sends the two standard basis vectors. Any output is their corresponding linear combination.

The kernel solves A(x,y)=0, so x+y=0. It consists of all (t,−t), a line with one independent direction. The image consists of all (s,0), also a line. The input dimension two decomposes into nullity one plus rank one. This is an instance of the rank-nullity theorem.

A vector in the kernel is not an “input that failed.” It is an input combination whose image is exactly zero. In a boundary map, a cycle is a chain whose boundary is zero, so cycles live in a kernel.

## Binary arithmetic changes dependence

In F₂, 1+1=0 and 1−1=0. Thus adding a row to another row is XOR. Consider

```text
1 1 0
1 0 1
0 1 1
```

Add the first row to the second: it becomes `(0,1,1)`. That is the third row. Add it to the third: the third becomes zero. Two pivot rows remain, so the rank is two over F₂. Over the real numbers the determinant is −2, which is nonzero, so the real rank is three.

The entries did not change, but the legal arithmetic did. A real-valued SVD routine therefore cannot automatically compute the rank needed for F₂ homology.

## Follow a triangle boundary matrix

Order vertices as v₀,v₁,v₂ and edges as e₀₁,e₁₂,e₀₂. Over F₂, each edge has its two endpoints as boundary:

```text
          e01 e12 e02
v0          1   0   1
v1          1   1   0
v2          0   1   1
```

The sum of all three columns is zero. Thus the sum of all three edges is a cycle. Two columns are independent, so the boundary map has rank two. With three edge coordinates, the kernel has dimension one.

For the outline alone there are no triangular faces. Therefore no nonzero edge cycle can be the boundary of a face chain, and β₁=1. Add the filled triangular face. Its boundary column is `(1,1,1)` in edge coordinates. This spans the one-dimensional cycle space. The cycle still exists as a chain, but now it represents zero in homology, so β₁=0.

## Quotients remove declared differences

Suppose Z is a vector space of cycles and B is a subspace of boundaries. Two cycles z and z′ represent the same homology class when z−z′ lies in B. The quotient Z/B is the collection of those equivalence classes, with addition inherited from chains.

Over a field, dim(Z/B)=dim Z−dim B. Combining that identity with rank-nullity gives

```text
beta_k = number of k-simplices
         - rank of the boundary map out of C_k
         - rank of the boundary map into C_k.
```

This works because boundary-of-boundary is zero, so the incoming image really is contained in the outgoing kernel. Without that containment, the proposed quotient would not be the homology construction.

## Coordinates versus invariant information

Boundary matrices change when basis order changes, but the vector-space dimensions do not. A barcode calculation needs a filtration-compatible order; arbitrary reordering across entrance times is not a harmless basis permutation of the same algorithmic input. Distinguish changes to representation from changes to the mathematical problem.

Betti numbers are nonnegative integers. A negative computed Betti number signals a violated assumption or a bug; it is not an unusual kind of negative hole. Empty matrices have rank zero and occur naturally for ∂₀ in ordinary homology.

## Independence checks before continuing

Explain the kernel and image of A=[[1,1],[0,0]] without software. Reduce the three-by-three binary matrix yourself. Verify that the triangle boundary sums to zero. Explain why adding a face changes the quotient rather than deleting the edge cycle.

**Primary follow-up:** R5 for linear maps, bases, and rank; R6 for fields and vector spaces; R1/R2 for chains and homology. See [Sources](../docs/SOURCES.md). All matrices and derivations above are original worked course examples.
