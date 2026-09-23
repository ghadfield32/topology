"""Bounded CPU experiments with bundled observations and explicit split records."""
from __future__ import annotations
import hashlib
import json
from pathlib import Path
import numpy as np
import pandas as pd
from . import representations as r
from .data import ROOT, load_digit_data, load_iris_data


def save_result(unit: str, result: dict) -> dict:
    dest=ROOT/'reports'/'representations'/unit
    dest.mkdir(parents=True,exist_ok=True)
    (dest/'results.json').write_text(json.dumps(result,indent=2,allow_nan=False)+'\n')
    return result


def geometry_summary(x: np.ndarray) -> dict:
    cov=r.covariance(x)
    return {'n':int(len(x)),'dimension':int(x.shape[1]),'mean_norm':float(np.linalg.norm(x.mean(0))),
            'mean_coordinate_std':float(np.sqrt(np.diag(cov)).mean()),
            'covariance_identity_frobenius':float(np.linalg.norm(cov-np.eye(x.shape[1]))),
            'effective_rank':r.effective_rank(x)}


IRIS_FEATURES = ['sepal_length_cm','sepal_width_cm','petal_length_cm','petal_width_cm']

def distribution_lab() -> dict:
    iris=load_iris_data();x=iris[IRIS_FEATURES].to_numpy()
    # Deterministic demonstration split, not a classifier test or ecological inference.
    train=x[:100];held=x[100:];mean,w=r.fit_whitener(train)
    atoms=np.tile(np.array([[-1.,-1.],[-1.,1.],[1.,-1.],[1.,1.]]),(32,1))
    am,aw=r.fit_whitener(atoms);white_atoms=(atoms-am)@aw
    rng=np.random.default_rng(2026);normal=rng.normal(size=(128,2))
    directions=r.unit_directions(2,64,87)
    result={'observed_source':'bundled Iris; first 100 rows fit, final 50 demonstration only',
      'features':IRIS_FEATURES,'train_before':geometry_summary(train),'train_after':geometry_summary((train-mean)@w),
      'heldout_after_train_transform':geometry_summary((held-mean)@w),
      'constructed_discrete_whitened':geometry_summary(white_atoms),
      'constructed_discrete_sigreg':r.projected_gaussian_score(white_atoms,directions),
      'constructed_gaussian_sigreg':r.projected_gaussian_score(normal,directions),
      'interpretation':'Identity sample covariance is a moment property, not Gaussianity or semantic usefulness. Iris file order is not randomized; this is a transform check, not a generalization estimate.'}
    return save_result('r01',result)


def projection_lab() -> dict:
    rng=np.random.default_rng(7);g=rng.normal(size=(256,2));flat=np.column_stack([g[:,0],np.zeros(256)])
    samples=np.array([-2.,-.25,.3,1.,2.]);a=np.ones((1,1))
    exact=r.epps_pulley_exact(samples)
    result={'manufactured_controls':True,'exact_integral':exact,
      'quadrature':{str(n):r.projected_gaussian_score(samples[:,None],a,np.linspace(-10,10,n)) for n in [17,65,257,1025]},
      'flat_first_axis':r.projected_gaussian_score(flat,np.array([[1.],[0.]])),
      'flat_second_axis':r.projected_gaussian_score(flat,np.array([[0.],[1.]])),
      'seed_scores':{str(s):r.projected_gaussian_score(g,r.unit_directions(2,32,s)) for s in range(4)},
      'interpretation':'Quadrature, slice selection and sample variation are separate errors; none of these scores is a p-value.'}
    images,_,ids=load_digit_data('train')
    # Raw first 8 varying pixels from train; deterministic PCA fitted only on train.
    from sklearn.decomposition import PCA
    features=PCA(n_components=8,svd_solver='full').fit_transform(images.reshape(len(images),-1)/16)
    result['real_digits_pca']=geometry_summary(features)
    result['real_digits_sample_count']=int(len(ids))
    return save_result('r02',result)


def mechanisms_lab() -> dict:
    import torch
    torch.set_num_threads(1);torch.manual_seed(99)
    images,_,_=load_digit_data('train');x=torch.tensor(images[:64].reshape(64,-1)/16,dtype=torch.float64)
    a=x@torch.randn(64,8,dtype=torch.float64);b=(x+.03*torch.randn_like(x))@torch.randn(64,8,dtype=torch.float64)
    # Independent maps are a constructed loss-control, NOT learned positive representations.
    same=a+.02*torch.randn_like(a)
    zero=torch.zeros((32,8),dtype=torch.float64,requires_grad=True)
    penalty=r.sigreg_torch(zero,torch.tensor(r.unit_directions(8,32,3)));penalty.backward()
    u=torch.tensor([2.],requires_grad=True);v=torch.tensor([3.],requires_grad=True)
    (u-v.detach()).square().sum().backward()
    out={'data':'64 real training digit images, fixed random projections and manufactured perturbations',
        'agreement_same':float((a-same).square().mean()),'agreement_different':float((a-b).square().mean()),
        'vicreg_same':float(r.vicreg_loss(a,same)),'barlow_same':float(r.barlow_loss(a,same)),
        'info_nce_same':float(r.info_nce(a,same)),'info_nce_shuffled':float(r.info_nce(a,torch.roll(same,1,0))),
        'zero_cloud_penalty':float(penalty.detach()),'zero_cloud_gradient_norm':float(zero.grad.norm()),
        'stop_gradient_online':float(u.grad),'stop_gradient_target_is_none':v.grad is None,
        'ema_hand_example':float(r.ema(torch.tensor([1.]),torch.tensor([3.]),.75)),
        'interpretation':'Separate objective scales are not a model ranking. A positive anti-collapse penalty does not ensure a nonzero gradient at every state.'}
    return save_result('r03',out)


def train_digits(epochs: int=25, seeds: tuple[int,...]=(11,23)) -> dict:
    """Fixed protocol: labels are never passed into pretraining; probes use train/val.

    This is a teaching ablation, not an official LeJEPA reproduction or an untouched
    research benchmark. The supplied historical test partition has been shown before.
    """
    import torch
    from torch import nn
    from sklearn.decomposition import PCA
    from sklearn.linear_model import LogisticRegression
    from sklearn.pipeline import make_pipeline
    from sklearn.preprocessing import StandardScaler
    if epochs<1 or not seeds:raise ValueError('Positive epochs and a nonempty seed list required.')
    torch.set_num_threads(1)
    data={part:load_digit_data(part) for part in ['train','validation','test']}
    r.assert_disjoint(*(v[2] for v in data.values()))
    xx={p:v[0].reshape(len(v[0]),-1).astype(np.float32)/16 for p,v in data.items()}
    yy={p:v[1] for p,v in data.items()}
    dest=ROOT/'reports'/'representations'/'r04';dest.mkdir(parents=True,exist_ok=True)
    protocol={'epochs':epochs,'seeds':list(seeds),'embedding_dimension':12,'batch_size':128,
      'encoder':'64 -> 64 GELU -> 12; no batch normalization, teacher or predictor',
      'optimizer':'AdamW lr=0.002 weight_decay=0.0001','views':'independent additive Gaussian std0.08 and Bernoulli zero masking p0.05; clip to [0,1]',
      'loss':'agreement mean squared coordinate difference, plus for SIGReg average per-view projected Gaussian score; 0.5 weight each',
      'slices':32,'frequency_grid':'17 points [-5,5]','probe_C_grid':[.1,1.,10.],
      'pretraining_labels_used':False,'selection':'Probe C selected by validation accuracy, ties choose first/smaller C; final epoch fixed before evaluation',
      'split_ids':{p:v[2].tolist() for p,v in data.items()},
      'source_sha256':hashlib.sha256((ROOT/'data/raw/digits.npz').read_bytes()).hexdigest(),
      'limitations':['Historical exposed demonstration test set','No writer IDs or writer-disjoint evaluation','Two training seeds, not a powered comparative study','Augmentations not proven label-preserving','No official LeJEPA implementation parity test']}
    (dest/'protocol.json').write_text(json.dumps(protocol,indent=2)+'\n')
    records=[];predictions=[];histories=[]
    def probe(name,z,seed):
        best=None
        for c in protocol['probe_C_grid']:
            model=make_pipeline(StandardScaler(),LogisticRegression(C=c,max_iter=1500,solver='lbfgs'))
            model.fit(z['train'],yy['train'])
            acc=float(model.score(z['validation'],yy['validation']))
            if best is None or acc>best[0]:best=(acc,c,model)
        va,c,model=best;pred=model.predict(z['test'])
        row={'model':name,'seed':seed,'probe_C':c,'validation_accuracy':va,
             'test_correct':int((pred==yy['test']).sum()),'test_n':len(pred),
             'test_accuracy':float((pred==yy['test']).mean()),'embedding_train':geometry_summary(z['train'])}
        records.append(row)
        for identity,truth,prediction in zip(data['test'][2],yy['test'],pred,strict=True):
            predictions.append({'model':name,'seed':seed,'sample_id':int(identity),'truth':int(truth),'prediction':int(prediction)})
    probe('raw_pixels',xx,0)
    pca=PCA(n_components=12,svd_solver='full').fit(xx['train'])
    probe('pca12',{p:pca.transform(x) for p,x in xx.items()},0)
    # Deliberately uninformative control; not a feature map for deployment.
    rng=np.random.default_rng(80)
    probe('label_independent_gaussian',{p:rng.normal(size=(len(x),12)) for p,x in xx.items()},80)
    train=torch.tensor(xx['train'])
    for seed in seeds:
        torch.manual_seed(seed)
        initial=nn.Sequential(nn.Linear(64,64),nn.GELU(),nn.Linear(64,12))
        state={k:v.detach().clone() for k,v in initial.state_dict().items()}
        with torch.no_grad():probe('random_encoder',{p:initial(torch.tensor(x)).numpy() for p,x in xx.items()},seed)
        for method in ['agreement_only','agreement_sigreg']:
            net=nn.Sequential(nn.Linear(64,64),nn.GELU(),nn.Linear(64,12));net.load_state_dict(state)
            opt=torch.optim.AdamW(net.parameters(),lr=.002,weight_decay=.0001)
            views=torch.Generator().manual_seed(seed+1000);directions=torch.Generator().manual_seed(seed+2000)
            order=np.random.default_rng(seed+3000)
            for epoch in range(epochs):
                permutation=order.permutation(len(train));losses=[]
                for start in range(0,len(train),128):
                    batch=train[permutation[start:start+128]]
                    if len(batch)<2:continue
                    def view():
                        v=batch+.08*torch.randn(batch.shape,generator=views)
                        return (v*(torch.rand(batch.shape,generator=views)>.05)).clamp(0,1)
                    za,zb=net(view()),net(view());agreement=(za-zb).square().mean()
                    a=torch.randn(12,32,generator=directions);a=a/a.norm(dim=0,keepdim=True)
                    reg=(r.sigreg_torch(za,a)+r.sigreg_torch(zb,a))/2
                    loss=agreement if method=='agreement_only' else .5*agreement+.5*reg
                    opt.zero_grad();loss.backward();opt.step()
                    losses.append([float(loss.detach()),float(agreement.detach()),float(reg.detach())])
                histories.append({'model':method,'seed':seed,'epoch':epoch+1,
                                  **dict(zip(['objective','agreement','sigreg'],np.mean(losses,axis=0).tolist(),strict=True))})
            with torch.no_grad():z={p:net(torch.tensor(x)).numpy() for p,x in xx.items()}
            probe(method,z,seed)
            np.savez_compressed(dest/f'{method}_seed{seed}_weights.npz',**{k:v.detach().numpy() for k,v in net.state_dict().items()})
    pd.DataFrame(predictions).to_csv(dest/'predictions.csv',index=False)
    pd.DataFrame(histories).to_csv(dest/'training_history.csv',index=False)
    result={'protocol':protocol,'models':records,'torch':torch.__version__,
            'interpretation':'Compare predictive utility AND representation spread. A low task loss or a Gaussian marginal cannot alone establish semantic usefulness.'}
    return save_result('r04',result)


def transfer_lab() -> dict:
    from sklearn.preprocessing import StandardScaler
    profiles=pd.read_csv(ROOT/'sports_v8/data/skillcorner_selected_profiles.csv')
    candidates=['total_distance_full_all','total_metersperminute_full_all','sprint_distance_full_all']
    features=profiles[candidates].to_numpy(float)
    distinct=profiles.player_id.unique();train_ids=distinct[:max(1,len(distinct)//2)]
    train=profiles.player_id.isin(train_ids).to_numpy();test=~train
    r.assert_disjoint(profiles.loc[train,'player_id'],profiles.loc[test,'player_id'])
    scaler=StandardScaler().fit(features[train]);z=scaler.transform(features)
    observed={'n_profile_rows':len(profiles),'n_distinct_players':int(profiles.player_id.nunique()),
       'features':candidates,'train_rows':int(train.sum()),'test_rows':int(test.sum()),
       'train_ids':list(map(int,train_ids)),'test_ids':list(map(int,profiles.loc[test,'player_id'].unique())),
       'train_geometry':geometry_summary(z[train]),'held_geometry':geometry_summary(z[test]),
       'scope':'Selected soccer aggregate rows, not tracking trajectories; no learned sports encoder or performance forecast.'}
    path=ROOT/'reports/representations/r04/results.json'
    if not path.exists():raise FileNotFoundError('Run r04 first or use course.py run --case r05 (dependency-aware).')
    ablation=json.loads(path.read_text())
    return save_result('r05',{'observed_soccer_profiles':observed,'digits_ablation_models':ablation['models'],
       'world_model_gate':{'trained_sports_world_model':False,'causal_video_forecasting_validated':False,
       'requirements':['Independent athlete/session/match groups','Documented frame clocks and units','Past-only context with held-out future target','A persistence/linear dynamics baseline','Outcome-independent geometry validation','Data/weights license review']},
       'interpretation':'The same diagnostics transfer between domains; fitted representations and scientific conclusions do not automatically transfer.'})
