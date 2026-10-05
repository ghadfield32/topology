"""Independent examples before implementation of the new artifact contract."""
import unittest, tempfile, math, struct
from pathlib import Path
from systems.python.contract import read_binary, write_binary, export_spl, predict, validate_payload

class ContractTests(unittest.TestCase):
    def rows(self):
        return [dict(frame=2,time=0.,x=1.,y=2.,z=3.,confidence=None),
                dict(frame=3,time=.1,x=2.,y=3.,z=4.,confidence=.5)]
    def test_roundtrip(self):
        with tempfile.TemporaryDirectory() as d:
            p=Path(d)/'data.bin';write_binary(p,self.rows()); self.assertEqual(read_binary(p),self.rows())
    def test_no_overwrite(self):
        with tempfile.TemporaryDirectory() as d:
            p=Path(d)/'data.bin';write_binary(p,self.rows())
            with self.assertRaises(FileExistsError):write_binary(p,self.rows())
    def test_invalid_input(self):
        for change in [dict(time=float('nan')),dict(confidence=1.1),dict(frame=-1)]:
            rows=self.rows();rows[0].update(change)
            with tempfile.TemporaryDirectory() as d:
                with self.assertRaises(ValueError):write_binary(Path(d)/'x',rows)
    def test_order(self):
        rows=self.rows();rows[1]['time']=0
        with tempfile.TemporaryDirectory() as d:
            with self.assertRaises(ValueError):write_binary(Path(d)/'x',rows)
    def test_binary_truncation_and_trailing(self):
        with tempfile.TemporaryDirectory() as d:
            p=Path(d)/'x';write_binary(p,self.rows());data=p.read_bytes()
            for variant in [data[:-1],data+b'x',b'BADMAGIC'+data[8:]]:
                p.write_bytes(variant)
                with self.assertRaises(ValueError):read_binary(p)
    def test_ballistics(self):
        p=predict([0.,0.,2.],[1.,0.,3.],.5,9.81)
        self.assertAlmostEqual(p[0],.5);self.assertAlmostEqual(p[2],2+1.5-.5*9.81*.25)
    def test_bad_gravity(self):
        with self.assertRaises(ValueError):predict([0.,0.,0.],[0.,0.,0.],1.,-1)
    def test_payload_rejects_units(self):
        with self.assertRaises(ValueError):validate_payload({'schema':'shape.systems.trajectory.v1','units':'feet'})

if __name__=='__main__':unittest.main()

class PayloadBoundary(unittest.TestCase):
 def payload(self):
  return {'schema':'shape.systems.trajectory.v1','units':'m','observed':[{'time':0.,'x':0.,'y':1.,'z':2.,'confidence':None}],'predicted':[{'time':0.,'x':0.,'y':1.,'z':2.,'confidence':None}],'metadata':{'limitations':['control']}}
 def test_confidence_runtime_rejected(self):
  v=self.payload();v['observed'][0]['confidence']=2
  with self.assertRaises(ValueError):validate_payload(v)
 def test_nontext_limit_rejected(self):
  v=self.payload();v['metadata']['limitations']=[10]
  with self.assertRaises(ValueError):validate_payload(v)
 def test_prediction_overflow(self):
  with self.assertRaises(ValueError):predict([0.,0.,0.],[1e308,0.,0.],1e308)
