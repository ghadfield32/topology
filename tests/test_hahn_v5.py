from pathlib import Path
import csv,json,hashlib
ROOT=Path(__file__).resolve().parents[1]
def test_nist_excerpt_integrity():
    p=ROOT/'data/physics/hahn1_excerpt.csv'
    manifest=json.loads((p.parent/'manifest.json').read_text())
    rows=list(csv.DictReader(p.open()))
    assert len(rows)==56 and manifest['original_rows']==236
    assert float(rows[0]['temperature_K'])==24.41
    assert float(rows[-1]['expansion_response'])==19.111
    assert [int(r['source_observation']) for r in rows]==list(range(1,57))
    assert hashlib.sha256(p.read_bytes()).hexdigest()==manifest['sha256']
    assert manifest['time_axis'] is False
