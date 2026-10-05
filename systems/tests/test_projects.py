import json,tempfile,unittest
from pathlib import Path
from unittest.mock import patch
from systems.python.projects import prepare,check
from systems.python.workflow import ROOT
class Projects(unittest.TestCase):
 def test_private_source_copied(self):
  with tempfile.TemporaryDirectory()as t:
   out=prepare('sys01',Path(t)/'learner')
   original=ROOT/'systems/c/src/trajectory.c';copy=out/'project/c/src/trajectory.c'
   self.assertEqual(copy.read_bytes(),original.read_bytes());copy.write_text('deliberate private change')
   self.assertNotEqual(copy.read_bytes(),original.read_bytes())
   self.assertEqual(json.loads((out/'project.json').read_text())['assessment'],'not_assessed')
 def test_build_error_not_misclassified_as_missing_dependency(self):
  with tempfile.TemporaryDirectory()as t:
   out=prepare('sys03',Path(t)/'learner')
   with patch('systems.python.projects.command',side_effect=RuntimeError('learner syntax error')):
    result,status=check(out,Path(t)/'run')
   self.assertEqual(status,'failed')
 def test_unknown_unit_refused(self):
  with tempfile.TemporaryDirectory()as t:
   with self.assertRaises(ValueError):prepare('missing',Path(t)/'missing')
 def test_output_refuses_overwrite(self):
  with tempfile.TemporaryDirectory()as t:
   with self.assertRaises(FileExistsError):prepare('sys01',Path(t))
 def test_sys08_copies_both_crates_and_preserves_reference(self):
  with tempfile.TemporaryDirectory()as t:
   out=prepare('sys08',Path(t)/'learner')
   for name in ('pyo3','rust_validator'):
    self.assertTrue((out/'project'/name).is_dir(),f'sys08 must copy {name}')
   lib=ROOT/'systems/rust_validator/src/lib.rs'
   self.assertEqual((out/'project/rust_validator/src/lib.rs').read_bytes(),lib.read_bytes())
 def test_sys08_build_error_is_a_failure_not_a_block(self):
  # A compile/assertion error in available code must be 'failed', never 'blocked'.
  # Opt into the reviewed network path so the dependency gate is passed and the
  # (mocked) build is what raises.
  with tempfile.TemporaryDirectory()as t:
   out=prepare('sys08',Path(t)/'learner')
   with patch('systems.python.projects.os.environ',
              {'SHAPE_MATURIN':'/fake/maturin','SHAPE_PYO3_ALLOW_NETWORK':'1'}), \
        patch('systems.python.projects.command',side_effect=RuntimeError('learner syntax error')):
    _,status=check(out,Path(t)/'run')
   self.assertEqual(status,'failed')
 def test_sys08_missing_maturin_is_blocked_and_named(self):
  with tempfile.TemporaryDirectory()as t:
   out=prepare('sys08',Path(t)/'learner')
   with patch('systems.python.projects.shutil.which',return_value=None)as which:
    _,status=check(out,Path(t)/'run')
   self.assertEqual(status,'blocked')
   which.assert_called()
   report=json.loads((Path(t)/'run/project_check.json').read_text())
   self.assertIn('maturin',report['reason'].lower())
 def test_sys08_vendored_gap_is_reported_and_blocks(self):
  # With maturin present but pyo3 not vendored and no network opt-in, the gate
  # blocks and names the real reason rather than a compiler failure.
  with tempfile.TemporaryDirectory()as t:
   out=prepare('sys08',Path(t)/'learner')
   with patch('systems.python.projects.shutil.which',return_value='/fake/maturin'), \
        patch('systems.python.projects.os.environ',{}), \
        patch('systems.python.projects.command',side_effect=AssertionError('maturin must not run')):
    _,status=check(out,Path(t)/'run')
   self.assertEqual(status,'blocked')
   reason=json.loads((Path(t)/'run/project_check.json').read_text())['reason'].lower()
   self.assertIn('pyo3',reason)

  with tempfile.TemporaryDirectory()as t:
   out=prepare('sys08',Path(t)/'learner')
   (out/'project/pyo3').rename(out/'project/pyo3-moved')
   with patch('systems.python.projects.shutil.which',return_value='/fake/maturin'):
    _,status=check(out,Path(t)/'run')
   self.assertEqual(status,'blocked')
