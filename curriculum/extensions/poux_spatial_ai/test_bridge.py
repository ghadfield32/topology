"""Small isolated tests; no course environment or downloaded data required."""
import hashlib
import importlib.util
import json
from pathlib import Path
import tempfile
import unittest

MODULE = Path(__file__).with_name('bridge.py')
spec = importlib.util.spec_from_file_location('poux_bridge', MODULE)
bridge = importlib.util.module_from_spec(spec) if MODULE.exists() else None
if bridge is not None:
    spec.loader.exec_module(bridge)


class BridgeTests(unittest.TestCase):
    def setUp(self):
        self.assertIsNotNone(bridge, 'The bridge implementation has not been added yet.')

    def assertVector(self, actual, expected):
        for a, b in zip(actual, expected, strict=True):
            self.assertAlmostEqual(a, b, places=11)

    def test_unequal_chunks_are_weighted(self):
        n, mu = bridge.stream_centroid([[[0, 0, 0]], [[3, 6, 9], [6, 12, 18], [9, 18, 27]]])
        self.assertEqual(n, 4)
        self.assertVector(mu, [4.5, 9, 13.5])

    def test_merge_has_correct_denominator(self):
        n, mu = bridge.merge_means(1, [0, 0, 0], 3, [6, 12, 18])
        self.assertEqual(n, 4)
        self.assertVector(mu, [4.5, 9, 13.5])

    def test_empty_chunks_do_not_change_mean(self):
        self.assertEqual(bridge.stream_centroid([[], [[1, 2, 3]], []]), (1, [1.0, 2.0, 3.0]))

    def test_empty_stream_rejected(self):
        with self.assertRaises(ValueError):
            bridge.stream_centroid([[], []])

    def test_single_point(self):
        self.assertEqual(bridge.stream_centroid([[[2, 4, 8]]]), (1, [2.0, 4.0, 8.0]))

    def test_generators_supported(self):
        chunks = (([float(i), 0.0, 0.0] for i in range(j, j + 2)) for j in [0, 2])
        self.assertVector(bridge.stream_centroid(chunks)[1], [1.5, 0, 0])

    def test_reordered_records_preserve_centroid(self):
        p = [[1, 2, 0], [2, 9, 3], [7, 4, 6]]
        self.assertVector(bridge.stream_centroid([p])[1], bridge.stream_centroid([p[::-1]])[1])

    def test_translation_changes_mean_by_translation(self):
        p = [[1, 2, 3], [4, 5, 6]]
        t = [3, -4, 2]
        translated = [[v + d for v, d in zip(row, t)] for row in p]
        a = bridge.stream_centroid([p])[1]
        b = bridge.stream_centroid([translated])[1]
        self.assertVector(b, [v + d for v, d in zip(a, t)])

    def test_invalid_dimension_rejected(self):
        with self.assertRaises(ValueError):
            bridge.stream_centroid([[[1, 2]]])

    def test_nan_rejected(self):
        with self.assertRaises(ValueError):
            bridge.stream_centroid([[[1, float('nan'), 3]]])

    def test_infinity_rejected(self):
        with self.assertRaises(ValueError):
            bridge.stream_centroid([[[1, 2, float('inf')]]])

    def test_string_rejected(self):
        with self.assertRaises(ValueError):
            bridge.stream_centroid([[['1', 2, 3]]])

    def test_bool_rejected(self):
        with self.assertRaises(ValueError):
            bridge.stream_centroid([[[True, 2, 3]]])

    def test_invalid_count_rejected(self):
        for count in [-1, 0.5, True]:
            with self.subTest(count=count), self.assertRaises(ValueError):
                bridge.merge_means(count, [0, 0, 0], 1, [1, 2, 3])

    def make_fixture(self, root):
        folder = root / 'sports_v8/data'
        folder.mkdir(parents=True)
        data = {'xyz_unit': 'ft', 'participant_id': 'fixture', 'trial_id': 'fixture',
                'records': [{'frame': i, 'ball': [i, 2*i, 3*i]} for i in range(4)]}
        path = folder / 'spl_selected_frames.json'
        path.write_text(json.dumps(data), encoding='utf-8')
        manifest = {'acquisition': 'synthetic test fixture, not observations', 'sources': [{
            'id': 'spl', 'file': path.name, 'local_sha256': hashlib.sha256(path.read_bytes()).hexdigest(),
            'license': 'fixture', 'unit': 'fixture', 'selection': {'frames': list(range(4))}}]}
        (folder / 'manifest.json').write_text(json.dumps(manifest), encoding='utf-8')
        return path

    def test_fixture_units_and_count(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp); self.make_fixture(root)
            result = bridge.analyse(root)
            self.assertEqual(result['records'], 4)
            self.assertVector(result['centroid_m'], [1.5*.3048, 3*.3048, 4.5*.3048])
            self.assertEqual(result['data_role'], 'existing selected motion records; not a static scene scan')

    def test_hash_mismatch_is_failure(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp); path = self.make_fixture(root)
            path.write_text(path.read_text()+'\n', encoding='utf-8')
            with self.assertRaises(ValueError): bridge.analyse(root)

    def test_unknown_units_fail_after_valid_hash(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp); path = self.make_fixture(root)
            data = json.loads(path.read_text()); data['xyz_unit'] = 'unknown'
            path.write_text(json.dumps(data), encoding='utf-8')
            mp = path.with_name('manifest.json'); m = json.loads(mp.read_text())
            m['sources'][0]['local_sha256'] = hashlib.sha256(path.read_bytes()).hexdigest()
            mp.write_text(json.dumps(m), encoding='utf-8')
            with self.assertRaises(ValueError): bridge.analyse(root)

    def test_output_refuses_overwrite(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp); self.make_fixture(root)
            output = root / 'my_work' / 'attempt'
            bridge.write_run(root, output)
            before = (output / 'results.json').read_bytes()
            with self.assertRaises(FileExistsError): bridge.write_run(root, output)
            self.assertEqual(before, (output / 'results.json').read_bytes())

    def test_output_cannot_escape_my_work(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp); self.make_fixture(root)
            with self.assertRaises(ValueError): bridge.write_run(root, root / 'reports')

    def test_source_unchanged(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp); path = self.make_fixture(root); before = path.read_bytes()
            bridge.write_run(root, root / 'my_work' / 'one')
            self.assertEqual(path.read_bytes(), before)


if __name__ == '__main__':
    unittest.main(verbosity=2)
