"""Execute each new reference exercise independently, not the unfinished learner notebooks."""
from pathlib import Path
import json
import numpy as np
import pytest
ROOT=Path(__file__).resolve().parents[1]
EX=json.loads((ROOT/'practice/bridge_exercises.json').read_text())
@pytest.mark.parametrize('exercise',EX,ids=[e['id'] for e in EX])
def test_reference_exercise(exercise):
    scope={'np':np,'Path':Path,'ROOT':ROOT}
    exec(compile(exercise['solution'],exercise['id'],'exec'),scope)
    exec(compile(exercise['checks'],exercise['id']+' checks','exec'),scope)
