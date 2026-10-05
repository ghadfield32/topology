"""Python side of sys04; C++ OpenCV remains a separately compiled acceptance gate."""
from pathlib import Path
import argparse,json,hashlib
import numpy as np
import cv2
p=argparse.ArgumentParser();p.add_argument('--repo',default='.');p.add_argument('--output',required=True);a=p.parse_args();out=Path(a.output);out.mkdir(parents=True,exist_ok=False)
source=Path(a.repo)/'data/stereo/left.png';image=cv2.imread(str(source),cv2.IMREAD_COLOR)
if image is None:raise RuntimeError('Cannot read registered image')
roi=image[1:5,1:4];own=roi.copy();assert not roi.flags.c_contiguous and own.flags.c_contiguous
K=np.array([[800.,0,320],[0,800,240],[0,0,1]])
px,_=cv2.projectPoints(np.array([[1.,2,10]]),np.zeros(3),np.zeros(3),K,None)
assert np.allclose(px.reshape(-1),[400,400],atol=1e-10)
(out/'results.json').write_text(json.dumps(dict(status='passed',shape=list(image.shape),source_sha256=hashlib.sha256(source.read_bytes()).hexdigest(),roi_contiguous=bool(roi.flags.c_contiguous),copy_contiguous=bool(own.flags.c_contiguous),manufactured_projection=px.tolist(),limitations=['The image is observed; the projection point and camera are manufactured controls.','C++ OpenCV has not been validated by this Python run.']),indent=2))
