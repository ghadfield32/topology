"""Offline sports navigation and explicit source verification. No automatic downloads."""
from pathlib import Path
import argparse,json,sys,hashlib,io,urllib.request
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'src'))
import pandas as pd
from shape_lab.sports_v8 import verify_local_data,check_payload,compare_spl,compare_skillcorner

def main():
    p=argparse.ArgumentParser(description=__doc__)
    sub=p.add_subparsers(dest='command',required=True)
    sub.add_parser('verify');sub.add_parser('list')
    q=sub.add_parser('stage');q.add_argument('stage',choices=[f'S{i:02}' for i in range(7)])
    q=sub.add_parser('verify-source');q.add_argument('id',choices=['spl','skillcorner']);q.add_argument('path',type=Path)
    q=sub.add_parser('fetch');q.add_argument('id',choices=['spl','skillcorner']);q.add_argument('--destination',type=Path,required=True);q.add_argument('--accept-data-license',action='store_true')
    args=p.parse_args();data=ROOT/'sports_v8/data';m=json.loads((data/'manifest.json').read_text())
    if args.command=='verify':
        report=verify_local_data(ROOT);print(json.dumps(report,indent=2))
        return 0 if all(r['ok'] for r in report) else 1
    if args.command=='list':print((ROOT/'sports_v8/README.md').read_text());return 0
    if args.command=='stage':print((ROOT/'sports_v8/lessons'/f'{args.stage}.md').read_text());return 0
    entry=next(e for e in m['sources'] if e['id']==args.id)
    if args.command=='fetch':
        if not args.accept_data_license:p.error('Read sports_v8/data licenses; explicitly pass --accept-data-license. SPL is noncommercial/share-alike.')
        if args.destination.exists():p.error('Destination already exists; no overwrite is permitted.')
        # Only curated HTTPS raw.githubusercontent.com endpoints. No credentials.
        with urllib.request.urlopen(entry['url'],timeout=30) as response:
            if not response.geturl().startswith('https://raw.githubusercontent.com/'):
                raise ValueError('Unexpected redirect host; inspect source manually.')
            raw=response.read(10_000_001)
    else:raw=args.path.read_bytes()
    check_payload(raw,entry['expected_git_blob_sha1'])
    if args.id=='spl':report=compare_spl(json.loads((data/entry['file']).read_text()),json.loads(raw))
    else:report=compare_skillcorner(pd.read_csv(data/entry['file']),pd.read_csv(io.BytesIO(raw)))
    report.update(id=args.id,source_sha256=hashlib.sha256(raw).hexdigest(),git_blob=entry['expected_git_blob_sha1'])
    if args.command=='fetch':
        args.destination.parent.mkdir(parents=True,exist_ok=True)
        with args.destination.open('xb') as handle:handle.write(raw)
    print(json.dumps(report,indent=2));return 0
if __name__=='__main__':
    try:raise SystemExit(main())
    except (ValueError,OSError,KeyError) as error:
        print(f'NOT VERIFIED: {error}',file=sys.stderr);raise SystemExit(1)
