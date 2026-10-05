#!/usr/bin/env python3
"""Verify a freshly extracted v17 archive, before merging it with a modified local repo."""
from pathlib import Path
import hashlib,json,sys
ROOT=Path(__file__).resolve().parents[1]
def main():
 manifest=ROOT/'MANIFEST_V17.sha256';errors=[];count=0
 for line in manifest.read_text(encoding='utf8').splitlines():
  if not line or line.startswith('#'):continue
  digest,name=line.split('  ',1);p=(ROOT/name).resolve();count+=1
  if not p.is_relative_to(ROOT)or not p.is_file()or hashlib.sha256(p.read_bytes()).hexdigest()!=digest:errors.append(name)
 print(json.dumps({'status':'passed'if not errors else'failed','manifested_files':count,'mismatches':errors},indent=2));return int(bool(errors))
if __name__=='__main__':raise SystemExit(main())
