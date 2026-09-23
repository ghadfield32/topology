"""Reporting helpers; plotting defaults are left to matplotlib."""
from pathlib import Path
from dataclasses import asdict,is_dataclass
import json
import numpy as np
import matplotlib.pyplot as plt

def json_safe(value):
    if is_dataclass(value): return json_safe(asdict(value))
    if isinstance(value,dict): return {str(k):json_safe(v) for k,v in value.items()}
    if isinstance(value,(list,tuple)): return [json_safe(v) for v in value]
    if isinstance(value,np.ndarray): return json_safe(value.tolist())
    if isinstance(value,(np.floating,float)):
        return float(value) if np.isfinite(value) else None
    if isinstance(value,np.integer): return int(value)
    if isinstance(value,np.bool_): return bool(value)
    return value

def save_json(path,value):
    p=Path(path); p.parent.mkdir(parents=True,exist_ok=True)
    p.write_text(json.dumps(json_safe(value),indent=2,allow_nan=False),encoding='utf-8')

def show_and_save(path):
    p=Path(path); p.parent.mkdir(parents=True,exist_ok=True)
    plt.tight_layout(); plt.savefig(p,dpi=130,bbox_inches='tight'); plt.show(); plt.close()

def plot_diagram(intervals,dim,title):
    bars=[b for b in intervals if b.dim==dim and np.isfinite(b.death)]
    essential=sum(b.dim==dim and not np.isfinite(b.death) for b in intervals)
    plt.figure(figsize=(6,5))
    upper=max([b.death for b in bars]+[1.])*1.08
    lower=min([b.birth for b in bars]+[0.])
    plt.plot([lower,upper],[lower,upper],linestyle='--',label='diagonal')
    if bars: plt.scatter([b.birth for b in bars],[b.death for b in bars],label=f'finite H{dim} intervals')
    plt.xlabel('Birth'); plt.ylabel('Death'); plt.title(f'{title}\n{essential} interval(s) with infinite death not plotted')
    plt.legend()

def plot_barcode(intervals,dim,title):
    bars=[b for b in intervals if b.dim==dim]
    plt.figure(figsize=(7,max(3,len(bars)*.24)))
    finite=[b.death for b in bars if np.isfinite(b.death)]
    cap=max(finite+[1.])*1.1
    for i,b in enumerate(bars):
        end=b.death if np.isfinite(b.death) else cap
        plt.plot([b.birth,end],[i,i],linewidth=2)
        if not np.isfinite(b.death): plt.text(end,i,' → ∞',va='center')
    plt.xlabel('Filtration parameter'); plt.ylabel('Interval index (not feature identity)'); plt.title(title)
