from pathlib import Path
import hashlib,json
import numpy as np
from shape_lab.data import ROOT,load_iris_data,load_digit_data

def test_data_hashes():
    manifest=json.loads((ROOT/'data/manifest.json').read_text())
    for path,entry in manifest['files'].items():
        assert hashlib.sha256((ROOT/path).read_bytes()).hexdigest()==entry['sha256']

def test_splits_exhaustive_and_disjoint():
    groups=json.loads((ROOT/'data/splits.json').read_text())
    sets=[set(v) for v in groups.values()]
    assert set.union(*sets)==set(range(1797))
    for i,a in enumerate(sets):
        for b in sets[i+1:]:assert not a&b
    assert [len(groups[k]) for k in ['train','validation','test']]==[1077,360,360]

def test_training_loader_only():
    images,labels,ids=load_digit_data()
    assert images.shape==(1077,8,8)
    assert set(labels)==set(range(10))
    assert images.min()>=0 and images.max()<=16
    assert len(load_iris_data())==150
