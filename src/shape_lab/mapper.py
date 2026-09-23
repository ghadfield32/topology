"""A small scalar-lens Mapper GRAPH (1-skeleton of its nerve), not a Reeb-graph guarantee."""
import numpy as np
from sklearn.cluster import DBSCAN

def mapper_graph(points,lens,n_intervals=5,overlap=.3,eps=.6):
    x=np.asarray(points,dtype=float); f=np.asarray(lens,dtype=float)
    if x.ndim!=2 or f.shape!=(len(x),) or not len(x) or not np.isfinite(x).all() or not np.isfinite(f).all():
        raise ValueError('Supply finite points and one scalar lens value per observation.')
    if n_intervals<1 or not 0<=overlap<1 or eps<=0:
        raise ValueError('Invalid cover or clustering settings.')
    lo,hi=float(f.min()),float(f.max())
    if hi==lo: bounds=[(lo,hi)]
    else:
        width=(hi-lo)/(n_intervals-(n_intervals-1)*overlap)
        bounds=[(lo+i*width*(1-overlap),lo+i*width*(1-overlap)+width) for i in range(n_intervals)]
        bounds[-1]=(bounds[-1][0],hi)  # exact cover of the largest observed value
    nodes=[]
    for cover_id,(left,right) in enumerate(bounds):
        ids=np.flatnonzero((f>=left)&(f<=right))
        if not len(ids): continue
        labels=DBSCAN(eps=eps,min_samples=1).fit_predict(x[ids])
        for label in sorted(set(labels)):
            members=ids[labels==label]
            nodes.append({'id':len(nodes),'cover_id':cover_id,'members':members.tolist(),
                          'lens_mean':float(f[members].mean()),'feature_mean':float(x[members,0].mean())})
    edges=[]
    for i,a in enumerate(nodes):
        for b in nodes[i+1:]:
            shared=sorted(set(a['members']) & set(b['members']))
            if shared: edges.append({'source':a['id'],'target':b['id'],'shared_members':shared})
    return {'nodes':nodes,'edges':edges,'cover':bounds,'settings':{'overlap':overlap,'eps':eps,'n_intervals':n_intervals}}
