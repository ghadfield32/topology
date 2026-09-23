import json
from pathlib import Path
import numpy as np
import pytest
from shape_lab.physics import practice
ROOT=Path(__file__).resolve().parents[1]
ACT=json.loads((ROOT/'physics/practice/activities.json').read_text())
@pytest.mark.parametrize('activity',ACT,ids=[a['id'] for a in ACT])
def test_worked_physics_exercise(activity):
    namespace={'np':np,'pytest':pytest,activity['name']:getattr(practice,activity['name'])}
    exec(activity['checks'],namespace)
