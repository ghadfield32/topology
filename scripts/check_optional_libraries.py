"""Run each optional comparison, reporting missing packages without a false pass."""
from pathlib import Path
import importlib.util,json,subprocess,sys
ROOT=Path(__file__).resolve().parents[1]

def main():
    results={}
    for package,test in [('ripser','test_ripser_agrees'),('gudhi','test_gudhi_rips_and_pixels_agree')]:
        if importlib.util.find_spec(package) is None:
            results[package]={'status':'NOT_RUN','reason':'Optional dependency unavailable.'}
            continue
        completed=subprocess.run([sys.executable,'-m','pytest',f'tests/test_optional_libraries.py::{test}','-q'],cwd=ROOT,text=True,capture_output=True)
        results[package]={'status':'PASSED' if completed.returncode==0 else 'FAILED',
                          'output':completed.stdout+completed.stderr}
    destination=ROOT/'reports/optional_library_checks.json'
    destination.write_text(json.dumps(results,indent=2))
    print(json.dumps(results,indent=2))
    # Missing optional libraries are visible but do not make the core unusable.
    if any(r['status']=='FAILED' for r in results.values()):raise SystemExit(1)
if __name__=='__main__':main()
