"""Independent NumPy/Pillow decoding oracle, not a Go/Rust calculation proxy."""
from __future__ import annotations
import ast, csv, hashlib, io, json, math, struct, zipfile
from pathlib import Path
import numpy as np
from PIL import Image

def safe(v):
    if isinstance(v, np.generic): v=v.item()
    if isinstance(v,float) and not math.isfinite(v): return 'NaN' if math.isnan(v) else '+Inf' if v>0 else '-Inf'
    if isinstance(v,bytes): return v.decode('utf8')
    return v

def array_audit(b:bytes):
    major=b[6]; offset=10 if major==1 else 12
    length=int.from_bytes(b[8:offset],'little')
    h=ast.literal_eval(b[offset:offset+length].decode('utf8'))
    a=np.load(io.BytesIO(b),allow_pickle=False)
    return dict(shape=list(a.shape),dtype=h['descr'],fortran_order=h['fortran_order'],
                payload_sha256=hashlib.sha256(b[offset+length:]).hexdigest(),
                values=[safe(v) for v in a.ravel(order='C')])

def decode(root:Path,path:str):
    full=(root/path).resolve();full.relative_to(root.resolve());b=full.read_bytes()
    out=dict(path=path,sha256=hashlib.sha256(b).hexdigest(),bytes=len(b))
    ext=full.suffix.lower()
    if ext=='.json':out.update(kind='json',value=json.loads(b))
    elif ext=='.csv':
        s=b.decode('utf-8-sig');delimiter=';' if ';' in s.split('\n')[0] else ','
        out.update(kind='table',rows=[r for r in csv.reader(io.StringIO(s),delimiter=delimiter) if r])
    elif ext=='.npy':out.update(kind='array',array=array_audit(b))
    elif ext=='.npz':
        with zipfile.ZipFile(io.BytesIO(b)) as z:
            arrays={name[:-4]:array_audit(z.read(name)) for name in z.namelist()}
        out.update(kind='arrays',arrays=arrays)
    elif ext=='.png':
        im=Image.open(io.BytesIO(b));im.load()
        if im.mode=='P' or (im.mode=='RGB' and 'transparency' in im.info):im=im.convert('RGBA')
        elif im.mode=='L' and 'transparency' in im.info:im=im.convert('LA')
        elif im.mode=='1':im=im.convert('L')
        a=np.asarray(im)
        if a.ndim==2:a=a[...,None]
        dtype='<u2' if b[24]==16 else '|u1'
        out.update(kind='array',array=dict(shape=list(a.shape),dtype=dtype,fortran_order=False,
          payload_sha256=hashlib.sha256(b).hexdigest(),values=[safe(v) for v in a.ravel()]))
    elif ext=='.pfm':
        kind,dims,scale,raw=b.split(b'\n',3);w,h=map(int,dims.split());scale=float(scale)
        c=3 if kind==b'PF' else 1
        a=np.frombuffer(raw,dtype='<f4' if scale<0 else '>f4').reshape(h,w,c)[::-1].astype(float)*abs(scale)
        out.update(kind='array',array=dict(shape=list(a.shape),dtype='<f4',fortran_order=False,
          payload_sha256=hashlib.sha256(raw).hexdigest(),values=[safe(v) for v in a.ravel()]))
    else:out.update(kind='text',text=b.decode('utf8'))
    return out

def differences(a,b,path='$',atol=0.,rtol=0.,maximum=20):
    errors=[];count=0;max_abs=0.
    def visit(x,y,p):
        nonlocal count,max_abs
        if isinstance(x,bool) or isinstance(y,bool):
            if type(x)!=type(y) or x!=y:errors.append((p,x,y))
        elif isinstance(x,(int,float)) and isinstance(y,(int,float)):
            count+=1;delta=abs(x-y);max_abs=max(max_abs,delta)
            if not math.isfinite(delta) or delta>atol+rtol*max(abs(x),abs(y)):errors.append((p,x,y))
        elif isinstance(x,dict) and isinstance(y,dict):
            if x.keys()!=y.keys():errors.append((p,sorted(x),sorted(y)))
            for k in sorted(x.keys()&y.keys()):visit(x[k],y[k],p+'.'+k)
        elif isinstance(x,list) and isinstance(y,list):
            if len(x)!=len(y):errors.append((p,'length='+str(len(x)),'length='+str(len(y))))
            for i,(u,v)in enumerate(zip(x,y)):visit(u,v,p+f'[{i}]')
        elif x!=y:errors.append((p,x,y))
    visit(a,b,path)
    return dict(passed=not errors,numeric_values_compared=count,max_absolute_difference=max_abs,
                discrepancy_count=len(errors),discrepancies=errors[:maximum])
