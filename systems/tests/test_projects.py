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
