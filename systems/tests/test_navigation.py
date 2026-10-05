import importlib.util,json,tempfile,unittest
from pathlib import Path
from systems.python.workflow import ROOT
class Navigation(unittest.TestCase):
 def test_generator(self):
  p=ROOT/'systems/tools/generate_workbooks.py'
  s=importlib.util.spec_from_file_location('gen17',p);m=importlib.util.module_from_spec(s);s.loader.exec_module(m)
  expected=m.render(ROOT);nb=[p for p in expected if p.endswith('.ipynb')]
  self.assertEqual(len(nb),181)
  self.assertEqual(len([p for p in nb if '/systems/'not in p]),171)
  for path in nb:
   value=json.loads(expected[path]);ids=[c['id']for c in value['cells']];self.assertEqual(len(ids),len(set(ids)))
   for c in value['cells']:
    if c['cell_type']=='code':compile(c['source'],path,'exec')
  self.assertEqual(expected,m.render(ROOT))
 def test_routes_execute_not_reuse_results(self):
  from systems.python.notebook_runner import commands
  p=commands('stage01','python',Path('/tmp/fresh'));self.assertIn('course.py',str(p[1]));self.assertIn('--stage',p)
  for lang in ['go','rust']:
   c=commands('stage01',lang,Path('/tmp/fresh'));self.assertEqual(c[c.index('--lang')+1],lang)
  with self.assertRaises(ValueError):commands('unknown','go',Path('/tmp/fresh'))
 def test_core_catalog_has_31(self):
  self.assertEqual(len(json.loads((ROOT/'curriculum/catalog.json').read_text())['stages']),31)
