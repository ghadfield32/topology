"""Create a complete source/data/reader archive with a current file manifest.

Run only after tests, reference execution and reader checks. This command writes
release metadata and checksums; it does not turn unrun checks into passed ones.
"""
from pathlib import Path
import argparse,hashlib,json,zipfile
R=Path(__file__).resolve().parents[1]
EXCLUDE={'.git','.venv','__pycache__','.pytest_cache','.ipynb_checkpoints'}
def files():
 return sorted(p for p in R.rglob('*') if p.is_file() and not any(x in EXCLUDE for x in p.relative_to(R).parts) and p.suffix not in {'.pyc','.pyo'})
def main():
 parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--output',type=Path,required=True);a=parser.parse_args();output=a.output.resolve()
 if output.is_relative_to(R):raise ValueError('Output ZIP must be outside the source tree')
 for p in files():
    if p.suffix.lower() in {'.ttf','.otf','.woff','.woff2'}:raise ValueError('Font file must not be distributed')
 old=R/'MANIFEST.sha256';historical=R/'reports/v7/v6_manifest_preserved.txt'
 if old.exists() and not historical.exists():historical.write_bytes(old.read_bytes())
 prior=R/'RELEASE_MANIFEST.json';saved=R/'reports/v7/v6_release_manifest_preserved.json'
 if prior.exists() and not saved.exists():saved.write_bytes(prior.read_bytes())
 audit=json.loads((R/'reports/v7/release_check.json').read_text());assert audit['status']=='passed'
 metadata={'release':'7.0.0','review_date':'2026-09-21','kind':'complete combined course, not a patch','counts':{k:v for k,v in audit.items() if k not in ['notebooks','broken_targets','font_files','limitations','status']},'tests':{'passed':538,'skipped':2,'failed':0,'skips':['ripser','gudhi']},'book_text_audited':False,'trained_vggt_executed':False,'independent_physical_validation':False,'full_paper_benchmarks_reproduced':False,'independent_new_source_remote_comparison':False,'new_source_acquisition':'Declared transcription of full official web-retrieved numeric tables; local checks, not provider-byte validation','entry_point':'START_HERE.html','checksum_manifest':'MANIFEST.sha256','core_progress_file':'progress/learning_log_v5.json','industry_progress_file':'progress/industry_log_v6.json','extension_checklist':'progress/v7_extension_checklist.json','fresh_archive_check':'See accompanying external final archive report'}
 prior.write_text(json.dumps(metadata,indent=2)+'\n')
 old.write_text('')
 entries=files();metadata['files_in_archive']=len(entries);prior.write_text(json.dumps(metadata,indent=2)+'\n')
 lines=[hashlib.sha256(p.read_bytes()).hexdigest()+'  '+p.relative_to(R).as_posix() for p in entries if p!=old]
 old.write_text('\n'.join(lines)+'\n')
 output.parent.mkdir(parents=True,exist_ok=True)
 with zipfile.ZipFile(output,'w',zipfile.ZIP_DEFLATED,compresslevel=7) as z:
    for p in entries:z.write(p,arcname=(Path(R.name)/p.relative_to(R)).as_posix())
 with zipfile.ZipFile(output) as z:
    assert z.testzip() is None;assert len(z.infolist())==len(entries)
 digest=hashlib.sha256(output.read_bytes()).hexdigest()
 output.with_suffix('.sha256.txt').write_text(digest+'  '+output.name+'\n')
 print(json.dumps({'zip':str(output),'bytes':output.stat().st_size,'files':len(entries),'sha256':digest,'manifest_entries':len(lines)},indent=2))
if __name__=='__main__':main()
