"""Copy a legacy 13/21-stage record into 31 stages, never overwrite a destination."""
from pathlib import Path
import sys,argparse
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'src'))
from shape_lab.learning import read_log,migrate_to_v5,write_log

def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--source',type=Path,required=True)
    p.add_argument('--destination',type=Path,required=True)
    a=p.parse_args()
    if a.destination.exists():p.error('Destination exists; choose a new filename. No record was overwritten.')
    try:result=migrate_to_v5(read_log(a.source))
    except (ValueError,OSError) as e:p.error(str(e))
    write_log(result,a.destination)
    print('Migrated to',a.destination,'— copy evidence files to their original relative paths and verify them.')
if __name__=='__main__':main()
