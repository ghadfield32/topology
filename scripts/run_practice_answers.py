"""Execute reference answers in fresh kernels; never execute unfinished learner files.

python scripts/run_practice_answers.py --stages 0 1 2
Omit --stages to execute all twenty-one. Saved results are reference evidence,
not a score for the person using the course.
"""
from pathlib import Path
import argparse
import json
import time
import nbformat
from nbclient import NotebookClient

ROOT = Path(__file__).resolve().parents[1]

def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--stages', type=int, nargs='*', default=list(range(21)))
    a = p.parse_args()
    if any(s not in range(21) for s in a.stages):
        p.error('Stages must be in 0..20.')
    out = ROOT / 'reports/practice_execution.json'
    report = json.loads(out.read_text()) if out.exists() else {}
    for stage in a.stages:
        tag = f'{stage:02d}'
        path = ROOT / f'practice/answers/{tag}_practice.ipynb'
        print(f'Executing reference answers {tag}', flush=True)
        nb = nbformat.read(path, 4)
        for c in nb.cells:
            if c.cell_type == 'code':
                c.outputs = []; c.execution_count = None
        start = time.perf_counter()
        try:
            NotebookClient(nb, timeout=180, kernel_name='python3',
                           resources={'metadata': {'path': str(ROOT)}}).execute()
        except Exception as exc:
            report[tag] = {'status': 'FAILED', 'error': str(exc)}
            out.write_text(json.dumps(report, indent=2) + '\n')
            raise
        nbformat.write(nb, path)
        report[tag] = {'status': 'PASSED', 'role': 'reference_answers',
                       'code_cells': sum(c.cell_type == 'code' for c in nb.cells),
                       'errors': 0, 'seconds': round(time.perf_counter()-start, 3)}
        out.write_text(json.dumps(report, indent=2) + '\n')
        print(report[tag], flush=True)

if __name__ == '__main__':
    main()
