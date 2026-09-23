"""Independent mathematical oracles beyond pointwise Betti-number agreement."""
from itertools import combinations,permutations
import numpy as np
import pytest
from shape_lab.algebra import rank_mod2,boundary_matrix
from shape_lab.persistence import rips_filtration,persistent_homology,diagram,pixel_filtration,finite_bottleneck
from shape_lab.topology import is_topology,powerset,is_continuous
from shape_lab.mapper import mapper_graph

def kernel_basis(matrix):
    """Independent full Gauss-Jordan construction of a nullspace basis over F2."""
    a=np.asarray(matrix,dtype=np.uint8).copy()%2
    rows,cols=a.shape;pivots=[];r=0
    for c in range(cols):
        possible=np.flatnonzero(a[r:,c])
        if len(possible)==0:continue
        p=r+int(possible[0]);a[[p,r]]=a[[r,p]]
        for j in range(rows):
            if j!=r and a[j,c]:a[j]^=a[r]
        pivots.append(c);r+=1
        if r==rows:break
    free=[c for c in range(cols) if c not in pivots]
    basis=np.zeros((cols,len(free)),dtype=np.uint8)
    for j,c in enumerate(free):
        basis[c,j]=1
        for row,p in enumerate(pivots):basis[p,j]=a[row,c]
    return basis

@pytest.mark.parametrize('seed',range(6))
def test_full_persistence_rank_invariant(seed):
    # Persistent rank catches wrong pairing even when all Betti counts agree.
    X=np.random.default_rng(seed).normal(size=(6,2))
    filtration=rips_filtration(X)
    bars=persistent_homology(filtration)
    thresholds=np.unique([v for _,v in filtration])[::3]
    for s in thresholds:
        A=[simplex for simplex,v in filtration if v<=s]
        for t in thresholds[thresholds>=s]:
            B=[simplex for simplex,v in filtration if v<=t]
            for k in (0,1):
                A_k=sorted([x for x in A if len(x)==k+1])
                B_k=sorted([x for x in B if len(x)==k+1])
                cycles=kernel_basis(boundary_matrix(A,k))
                embedded=np.zeros((len(B_k),cycles.shape[1]),dtype=int)
                positions={x:i for i,x in enumerate(B_k)}
                for i,simplex in enumerate(A_k):embedded[positions[simplex]]=cycles[i]
                boundaries=boundary_matrix(B,k+1)
                rank=rank_mod2(np.column_stack([embedded,boundaries]))-rank_mod2(boundaries)
                expected=sum(b.dim==k and b.birth<=s and b.death>t for b in bars)
                assert rank==expected

@pytest.mark.parametrize('seed',range(10))
def test_pixel_rotation_and_transpose_preserve_diagrams(seed):
    image=np.random.default_rng(seed).integers(0,6,size=(4,5)).astype(float)
    original=persistent_homology(pixel_filtration(image))
    for variant in [image.T,np.rot90(image),np.fliplr(image)]:
        other=persistent_homology(pixel_filtration(variant))
        for k in (0,1):assert np.array_equal(diagram(original,k),diagram(other,k))

def brute_bottleneck(a,b):
    m,n=len(a),len(b);N=m+n
    if not N:return 0.
    cost=np.full((N,N),np.inf)
    for i in range(m):
        for j in range(n):cost[i,j]=max(abs(a[i]-b[j]))
        cost[i,n+i]=(a[i,1]-a[i,0])/2
    for j in range(n):cost[m+j,j]=(b[j,1]-b[j,0])/2
    cost[m:,n:]=0
    return min(max(cost[i,p[i]] for i in range(N)) for p in permutations(range(N)))

@pytest.mark.parametrize('seed',range(10))
def test_bottleneck_against_exhaustive_matchings(seed):
    rng=np.random.default_rng(seed)
    a=np.sort(rng.uniform(size=(2,2)),axis=1)
    b=np.sort(rng.uniform(size=(2,2)),axis=1)
    assert finite_bottleneck(a,b)==pytest.approx(brute_bottleneck(a,b))

def test_finite_topology_and_bijection():
    X={0,1,2};disc=powerset(X);indisc=[set(),X]
    assert is_topology(X,disc) and is_topology(X,indisc)
    assert not is_topology(X,[set(),{0},{1},X])
    identity={x:x for x in X}
    assert is_continuous(X,disc,X,indisc,identity)
    assert not is_continuous(X,indisc,X,disc,identity)

@pytest.mark.parametrize('overlap',[0,.2,.5,.8])
def test_mapper_covers_all_points_and_edges_are_real_intersections(overlap):
    X=np.arange(30,dtype=float).reshape(-1,1)
    graph=mapper_graph(X,X[:,0],n_intervals=5,overlap=overlap,eps=2)
    covered=set().union(*(set(n['members']) for n in graph['nodes']))
    assert covered==set(range(len(X)))
    for edge in graph['edges']:
        a=graph['nodes'][edge['source']];b=graph['nodes'][edge['target']]
        assert edge['shared_members']==sorted(set(a['members'])&set(b['members']))
        assert edge['shared_members']
