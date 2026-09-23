"""Each independent coding activity has executable answer contracts."""
import json
from pathlib import Path
import numpy as np
import pandas as pd
import pytest
P=Path(__file__).resolve().parents[1]/'industry/exercises.json'
EX=json.loads(P.read_text())
@pytest.mark.parametrize('activity',EX,ids=[x['id'] for x in EX])
def test_reference_activity(activity):
    env={'np':np,'pd':pd}
    exec(activity['solution'],env)
    exec(activity['checks'],env)
