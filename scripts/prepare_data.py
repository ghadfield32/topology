"""Recreate the bundled snapshots from scikit-learn's installed real datasets.

This does not download data. It is NOT the original UCI 3823/1797 split.
"""
from pathlib import Path
import hashlib,json
import numpy as np
import pandas as pd
from sklearn.datasets import load_iris,load_digits
from sklearn.model_selection import train_test_split
import sklearn

ROOT=Path(__file__).resolve().parents[1]

def main():
    dest=ROOT/'data'/'raw'; dest.mkdir(parents=True,exist_ok=True)
    iris=load_iris()
    names=['sepal_length_cm','sepal_width_cm','petal_length_cm','petal_width_cm']
    frame=pd.DataFrame(iris.data,columns=names)
    frame.insert(0,'sample_id',np.arange(len(frame)))
    frame['label']=iris.target
    frame['species']=[iris.target_names[x] for x in iris.target]
    frame.to_csv(dest/'iris.csv',index=False)
    digits=load_digits()
    np.savez_compressed(dest/'digits.npz',images=digits.images.astype(np.uint8),labels=digits.target.astype(np.uint8),sample_ids=np.arange(len(digits.target)))
    ids=np.arange(len(digits.target))
    development,test=train_test_split(ids,test_size=360,stratify=digits.target,random_state=20260920)
    train,validation=train_test_split(development,test_size=360,stratify=digits.target[development],random_state=20260921)
    splits={k:sorted(map(int,v)) for k,v in [('train',train),('validation',validation),('test',test)]}
    (ROOT/'data'/'splits.json').write_text(json.dumps(splits,indent=2))
    files=[dest/'iris.csv',dest/'digits.npz',ROOT/'data'/'splits.json']
    manifest={'seed':20260920,'sklearn_version':sklearn.__version__,
              'iris':{'rows':150,'features':4,'source_variant':'scikit-learn corrected Iris snapshot; not byte-identical to all UCI variants'},
              'digits':{'rows':1797,'shape':[8,8],'range':[0,16],'source_variant':'scikit-learn copy of UCI original test set; new per-image learning split; writer IDs unavailable'},
              'split_sizes':{k:len(v) for k,v in splits.items()},
              'files':{str(p.relative_to(ROOT)):{'sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'bytes':p.stat().st_size} for p in files}}
    (ROOT/'data'/'manifest.json').write_text(json.dumps(manifest,indent=2))
    print(json.dumps(manifest,indent=2))

if __name__=='__main__': main()
