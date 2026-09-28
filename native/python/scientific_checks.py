"""Independent scientific checks of native outputs. Not an implementation proxy.

NumPy/SciPy, the retained Python topology implementation and PyTorch independently
check selected native protocols. This does NOT claim to replay the 133 notebooks.
"""
from __future__ import annotations
import argparse,json,math,sys
from pathlib import Path
import numpy as np
import pandas as pd
from scipy.special import softmax

class RNG:
    def __init__(self,seed):self.state=seed
    def next(self):
        x=self.state or 1;x^=(x<<13)&0xffffffff;x^=x>>17;x^=(x<<5)&0xffffffff
        self.state=x&0xffffffff;return self.state
    def uniform(self):return (self.next()+.5)/4294967296
    def normal(self):return math.sqrt(-2*math.log(self.uniform()))*math.cos(2*math.pi*self.uniform())

def stratified(y):
    out=[[],[],[]]
    for h,c in enumerate(sorted(set(y))):
        ids=np.flatnonzero(y==c).tolist();r=RNG(42+31*h)
        for i in range(len(ids)-1,0,-1):j=r.next()%(i+1);ids[i],ids[j]=ids[j],ids[i]
        a,b=len(ids)*6//10,len(ids)*8//10
        for dst,src in zip(out,[ids[:a],ids[a:b],ids[b:]]):dst.extend(src)
    return [sorted(x)for x in out]

def fit_softmax(x,y,tr,te,epochs=160):
    mean=x[tr].mean(0);scale=x[tr].std(0);scale[scale<1e-12]=1
    z=(x[tr]-mean)/scale;zt=(x[te]-mean)/scale
    classes,encoded=np.unique(y[tr],return_inverse=True)
    a=np.column_stack([z,np.ones(len(z))]);at=np.column_stack([zt,np.ones(len(zt))])
    weights=np.zeros((len(classes),a.shape[1]));history=[]
    for _ in range(epochs):
        p=softmax(a@weights.T,axis=1)
        history.append(float(-np.log(p[np.arange(len(p)),encoded]).mean()+.005*np.sum(weights[:,:-1]**2)))
        p[np.arange(len(p)),encoded]-=1
        g=p.T@a/len(a);g[:,:-1]+=.01*weights[:,:-1];weights-=.15*g
    probs=softmax(at@weights.T,axis=1)
    return weights,classes[probs.argmax(1)],probs,history

def physics_reference(kind):
    import torch
    torch.set_num_threads(1)
    torch.set_default_dtype(torch.float64)
    d,h=(2 if kind=='hnn'else 1),8;r=RNG(17)
    w=torch.tensor([.25*r.normal()for _ in range(h*(d+2)+1)],requires_grad=True)
    epochs,lr=(180,.01)if kind=='pinn'else(120,.015)
    def net(x):
        hidden=torch.tanh(x@w[:h*d].reshape(h,d).T+w[h*d:h*d+h])
        return hidden@w[h*d+h:h*d+2*h]+w[-1]
    loss_history=[]
    for epoch in range(epochs):
        q=torch.linspace(-1.2,1.2,24)
        if kind=='pinn':q=torch.arange(1,25)/25
        x=torch.stack([q,torch.sin(torch.arange(24)*1.7)],1)if d==2 else q[:,None]
        x=x.clone().requires_grad_();y=net(x)
        if kind=='pinn':
            y=x[:,0]*(1-x[:,0])*y
            first=torch.autograd.grad(y.sum(),x,create_graph=True)[0][:,0]
            second=torch.autograd.grad(first.sum(),x,create_graph=True)[0][:,0]
            loss=((second+math.pi**2*torch.sin(math.pi*x[:,0]))**2).mean()
        else:
            gradient=torch.autograd.grad(y.sum(),x,create_graph=True)[0]
            loss=((gradient-x)**2).sum(1).mean()
        loss_history.append(float(loss.detach()))
        g=torch.autograd.grad(loss,w)[0]
        clip=min(1.,20./float(g.norm())) if g.norm()>0 else 1.
        with torch.no_grad():w-=lr*clip*g
    q=torch.linspace(0,1,81) if kind=='pinn'else torch.linspace(-1,1,81)
    x=torch.stack([q,torch.full_like(q,.3)],1)if d==2 else q[:,None]
    x=x.clone().requires_grad_();y=net(x)
    pred=q*(1-q)*y if kind=='pinn'else -torch.autograd.grad(y.sum(),x)[0][:,0]
    return dict(weights=w.detach().tolist(),loss_history=loss_history,predictions=pred.detach().tolist())

def run(root:Path,run_dir:Path):
    sys.path.insert(0,str(root/'src'));sys.path.insert(0,str(root))
    from native_course import compare_values
    from shape_lab.persistence import rips_filtration,persistent_homology,pixel_filtration
    checks=[]
    def check(name,got,want,atol=1e-8,rtol=1e-7):
        c=compare_values(got,want,atol,rtol);c['check']=name;checks.append(c)
    def read(lang,key):return json.loads((run_dir/lang/(key+'.json')).read_text())['metrics']
    iris=pd.read_csv(root/'data/raw/iris.csv');x=iris.iloc[:,1:5].to_numpy(float)
    mu=x[:90].mean(0);sd=x[:90].std(0);sd[sd<1e-12]=1;z=(x[:24]-mu)/sd
    dx=z[1:8]-z[0];dist=np.column_stack([np.abs(dx).sum(1),np.linalg.norm(dx,axis=1),np.abs(dx).max(1)])
    splits=json.loads((root/'data/splits.json').read_text());images=np.load(root/'data/raw/digits.npz')['images'];im=images[splits['train'][0]]
    def diagram(f,dim=2):
        ints=persistent_homology(f,max_dim=dim)
        return sorted([{'dimension':v.dim,'birth':v.birth,'death':None if not np.isfinite(v.death) else v.death}for v in ints if not np.isfinite(v.death)or v.death>v.birth+1e-12],key=lambda v:(v['dimension'],v['birth'],math.inf if v['death']is None else v['death']))
    rips=diagram(rips_filtration(z,max_homology=1,max_edge=1.5),dim=1);pixels=diagram(pixel_filtration(-im.astype(float)))
    physics={k:physics_reference(k)for k in ['hnn','lnn','pinn']}
    for lang in ['go','rust']:
        d=read(lang,'stage01');check(lang+'/real_rank',d['real_rank'],int(np.linalg.matrix_rank([[1,1,0],[1,0,1],[0,1,1]])),0,0)
        check(lang+'/iris_rank',d['iris_rank'],int(np.linalg.matrix_rank(x)),0,0)
        check(lang+'/metric_vectors',read(lang,'stage02')['distances_L1_L2_Linf'],dist.tolist())
        check(lang+'/rips_interval_multiset',read(lang,'stage07')['rips_diagram'],rips)
        check(lang+'/pixel_interval_multiset',read(lang,'stage05')['real_digit_persistence'],pixels)
        d=read(lang,'stage14');R=np.array(d['rotation']);check(lang+'/orthogonal_rotation',(R.T@R).tolist(),np.eye(3).tolist());check(lang+'/rotation_determinant',float(np.linalg.det(R)),1.)
        for kind,key in [('hnn','stage23'),('lnn','stage23'),('pinn','stage26')]:
            d=read(lang,key);d=d['hnn'if kind=='hnn'else'lnn_restricted']if key=='stage23'else d
            for field in ['weights','loss_history','predictions']:check(f'{lang}/{kind}/{field}',d[field],physics[kind][field])
        for name in ['wine','wdbc','seeds']:
            d=read(lang,name);path=root/('data/v7/seeds/table.csv'if name=='seeds'else f'data/industries/{name}/data.csv');df=pd.read_csv(path)
            xx=df[d['features']].to_numpy(float);yy=df['variety'if name=='seeds'else'label'].to_numpy(int)
            tr,va,te=stratified(yy)
            check(lang+'/'+name+'/split',[d['train_rows'],d['validation_rows'],d['test_rows']],[tr,va,te],0,0)
            w,p,q,h=fit_softmax(xx,yy,tr,te);result=d['raw_all_training']
            check(lang+'/'+name+'/weights',result['weights'],w.tolist());check(lang+'/'+name+'/predictions',result['predictions'],p.tolist(),0,0)
            check(lang+'/'+name+'/probabilities',result['probabilities'],q.tolist());check(lang+'/'+name+'/training_loss',result['loss_history'],h)
        for name in ['stackloss','concrete_slump']:
            d=read(lang,name);df=pd.read_csv(root/('data/v7/concrete_slump/table.csv'if name=='concrete_slump'else'data/industries/stackloss/data.csv'))
            xx=df[d['features']].to_numpy(float);y=df[d['target']].to_numpy(float);tr,te=d['train_rows'],d['test_rows']
            m=xx[tr].mean(0);s=xx[tr].std(0);s[s<1e-12]=1;zz=(xx[tr]-m)/s;target=y[tr]-y[tr].mean()
            w=np.linalg.solve(zz.T@zz+np.eye(zz.shape[1]),zz.T@target);pred=(xx[te]-m)/s@w+y[tr].mean()
            check(lang+'/'+name+'/ridge_predictions',d['predictions'],pred.tolist())
        d=read(lang,'stage15');cal=json.loads((root/'data/stereo/calibration.json').read_text())
        for i,row in enumerate(d['predictions']):
            expected=cal['focal_px']*cal['baseline_m']/(row['predicted_disparity_px']+cal['doffs_px'])
            check(f'{lang}/stereo_depth/{i}',row['predicted_depth_m'],expected)
    return {'scope':'Selected independent NumPy, retained topology, and PyTorch checks of native-16 protocols; not original-notebook replay','status':'passed'if all(c['passed']for c in checks)else'failed','checks':checks}
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--repo',type=Path,required=True);p.add_argument('--runs',type=Path,required=True);p.add_argument('--output',type=Path,required=True);a=p.parse_args()
    if a.output.exists():raise SystemExit('Output exists; use a new filename')
    report=run(a.repo.resolve(),a.runs.resolve());a.output.write_text(json.dumps(report,indent=2)+'\n');print(report['status'],len(report['checks']));raise SystemExit(report['status']!='passed')
