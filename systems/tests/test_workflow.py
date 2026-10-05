import unittest,tempfile,json,sys
from pathlib import Path
from unittest.mock import patch
from systems.python.workflow import new_directory, command, source_fingerprints, _resolve
class WorkflowTests(unittest.TestCase):
 def test_new_output(self):
  with tempfile.TemporaryDirectory() as d:
   p=Path(d)/'new';self.assertEqual(new_directory(p),p.resolve())
   with self.assertRaises(FileExistsError):new_directory(p)
 def test_command_failure_is_saved(self):
  with tempfile.TemporaryDirectory() as d:
   p=Path(d);log=p/'failed.json'
   with self.assertRaises(RuntimeError):command([sys.executable,'-c','raise SystemExit(7)'],p,log)
   self.assertEqual(json.loads(log.read_text())['exit_code'],7)
 def test_command_cwd_and_output(self):
  with tempfile.TemporaryDirectory() as d:
   p=Path(d);r=command([sys.executable,'-c','print(19)'],p,p/'ok.json');self.assertEqual(r['stdout'].strip(),'19')
 def test_bare_command_is_resolved_to_an_executable_path(self):
  # A package-manager install (e.g. tsc) is not on the bare-name search path that
  # CreateProcess uses on Windows; resolution must yield an absolute path.
  resolved=_resolve(sys.executable)
  self.assertEqual(resolved,[sys.executable])
 def test_windows_shim_is_wrapped_for_the_shell(self):
  with patch('systems.python.workflow.shutil.which',return_value=r'C:\tools\tsc.cmd'), \
       patch('systems.python.workflow.os.name','nt'), \
       patch('systems.python.workflow.os.environ',{'COMSPEC':r'C:\Windows\System32\cmd.exe'}):
   resolved=_resolve('tsc')
  self.assertEqual(resolved,[r'C:\Windows\System32\cmd.exe','/d','/c',r'C:\tools\tsc.cmd'])
 def test_missing_command_is_left_for_a_clear_failure(self):
  with patch('systems.python.workflow.shutil.which',return_value=None):
   self.assertEqual(_resolve('definitely-not-installed-xyz'),['definitely-not-installed-xyz'])
if __name__=='__main__':unittest.main()
