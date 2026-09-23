"""Migrate an existing v2 evidence log to a NEW v3 file; never overwrite files."""
from pathlib import Path
import argparse,sys
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'src'))
from shape_lab.learning import read_log,migrate_v2_to_v3,write_log

def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--source',type=Path,required=True);p.add_argument('--output',type=Path,required=True)
    a=p.parse_args()
    if a.output.exists():p.error('Output exists. Choose a new path; no previous progress will be overwritten.')
    write_log(migrate_v2_to_v3(read_log(a.source)),a.output)
    print('Migration complete. Copy your evidence files too; unchanged hashes do not recreate missing work.')
if __name__=='__main__':main()
