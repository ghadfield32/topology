"""Execute every new reference activity, and verify unfinished work stays unfinished."""
from pathlib import Path
import json
import nbformat
import pytest
ROOT=Path(__file__).resolve().parents[1]
ACTIVITIES=json.loads((ROOT/'practice/activities.json').read_text())


@pytest.mark.parametrize('activity',ACTIVITIES,ids=[a['id'] for a in ACTIVITIES])
def test_reference_activity(activity,monkeypatch):
    monkeypatch.chdir(ROOT)
    namespace={}
    exec((ROOT/'practice/setup.py').read_text(),namespace)
    exec(activity['solution'],namespace)
    exec(activity['checks'],namespace)


def test_complete_active_practice_matrix():
    assert len(ACTIVITIES)==65
    assert len({a['id'] for a in ACTIVITIES})==65
    for stage in range(13):
        assert sum(a['stage']==stage for a in ACTIVITIES)==5
        path=ROOT/f'practice/learner/{stage:02d}_practice.ipynb'
        nb=nbformat.read(path,4);nbformat.validate(nb)
        assert nb.metadata.shape_lab.intentional_stubs is True
        # Learners may execute and complete their notebooks without breaking the suite.
        assert sum(c.cell_type == 'code' for c in nb.cells) == 11


def test_untouched_learner_function_fails_honestly(monkeypatch):
    """Test an unimplemented starter in isolation, not the learner's edited file."""
    monkeypatch.chdir(ROOT)
    activity = ACTIVITIES[0]
    namespace = {}
    exec((ROOT/'practice/setup.py').read_text(), namespace)
    stub = activity['signature'] + "\n    raise NotImplementedError('00.C1')\n"
    exec(stub, namespace)
    with pytest.raises(NotImplementedError, match='00.C1'):
        exec(activity['checks'], namespace)
