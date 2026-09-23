"""Content-addressed caches for fixed per-image feature extraction, never for fitted scaling."""
from hashlib import sha256
from pathlib import Path
import numpy as np
from .data import ROOT,load_digit_data
from .features import image_features

def fingerprint():
    digest=sha256()
    for p in [ROOT/'data/raw/digits.npz',ROOT/'data/splits.json',*sorted((ROOT/'src/shape_lab').glob('*.py'))]:
        digest.update(str(p.relative_to(ROOT)).encode()); digest.update(p.read_bytes())
    return digest.hexdigest()

def feature_data(split):
    images,labels,ids=load_digit_data(split)
    stamp=fingerprint()
    path=ROOT/'data/processed'/f'digits_features_{split}.npz'
    if path.exists():
        with np.load(path,allow_pickle=False) as stored:
            if str(stored['fingerprint'].item())==stamp and np.array_equal(stored['ids'],ids):
                return stored['features'].copy(),labels,ids
    print(f'Computing fixed topology features for {split}: {len(images)} images.')
    features=np.vstack([image_features(a) for a in images])
    path.parent.mkdir(parents=True,exist_ok=True)
    np.savez_compressed(path,features=features,ids=ids,fingerprint=stamp)
    return features,labels,ids
