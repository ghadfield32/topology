"""Run from the extracted repository: python course.py --help."""
from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT/'src'))
from shape_lab.cli import main
if __name__=='__main__':
    try:raise SystemExit(main(ROOT))
    except (ValueError,FileExistsError,FileNotFoundError) as exc:
        print(f'NOT COMPLETED: {exc}',file=sys.stderr)
        raise SystemExit(2)
