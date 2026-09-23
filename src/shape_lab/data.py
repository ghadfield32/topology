"""Read the bundled, attributed datasets. No network or silent synthetic fallback."""
from pathlib import Path
import json
import numpy as np
import pandas as pd

ROOT=Path(__file__).resolve().parents[2]

def load_iris_data():
    return pd.read_csv(ROOT/'data'/'raw'/'iris.csv')

def load_digit_data(split='train'):
    """Default is TRAIN only. Explicit 'all' exposes the complete dataset."""
    with np.load(ROOT/'data'/'raw'/'digits.npz',allow_pickle=False) as data:
        images,labels,ids=data['images'].copy(),data['labels'].copy(),data['sample_ids'].copy()
    if split!='all':
        splits=json.loads((ROOT/'data'/'splits.json').read_text())
        if split not in splits: raise ValueError('Use train, validation, test, or all.')
        selected=np.array(splits[split],dtype=int)
        images,labels,ids=images[selected],labels[selected],ids[selected]
    return images,labels,ids

def digit_example(label=0,occurrence=0):
    images,labels,ids=load_digit_data('train')
    indices=np.flatnonzero(labels==label)
    i=indices[occurrence]
    return images[i],int(ids[i])
