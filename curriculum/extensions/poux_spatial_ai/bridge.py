"""Original Stage 01 bridge: weighted chunk means, units, and information loss.

Uses only the standard library and the course's existing selected SPL records.
This is NOT a LAS reader, a static scan, or a large-data performance benchmark.
"""
from __future__ import annotations

import argparse
from datetime import datetime, timezone
import hashlib
import json
import math
from numbers import Real
from pathlib import Path
import platform
from typing import Iterable, Sequence


def vector3(values: Sequence[float]) -> list[float]:
    if len(values) != 3:
        raise ValueError('Expected exactly three coordinates.')
    if any(isinstance(v, bool) or not isinstance(v, Real) or not math.isfinite(v) for v in values):
        raise ValueError('Coordinates must be finite real numbers, not strings or booleans.')
    return [float(v) for v in values]


def merge_means(n: int, mean_a: Sequence[float], m: int,
                mean_b: Sequence[float]) -> tuple[int, list[float]]:
    """Combine two means with observation-count weights, not equal batch weights."""
    if any(isinstance(k, bool) or not isinstance(k, int) or k < 0 for k in (n, m)):
        raise ValueError('Counts must be nonnegative integers.')
    a, b = vector3(mean_a), vector3(mean_b)
    if n + m == 0:
        return 0, [0.0, 0.0, 0.0]
    total = n + m
    # Equivalent to (n*a + m*b)/(n+m), without multiplying coordinates by counts.
    result = [math.fsum((n / total * x, m / total * y)) for x, y in zip(a, b)]
    return total, vector3(result)


def stream_centroid(chunks: Iterable[Iterable[Sequence[float]]]) -> tuple[int, list[float]]:
    """One pass with constant-size accumulator; caller controls chunk generation.

    Floating-point agreement is approximate. This does not retain identities,
    timestamps, trajectories, or a distribution—only count and coordinate mean.
    """
    count, mean = 0, [0.0, 0.0, 0.0]
    for chunk in chunks:
        chunk_count, chunk_mean = 0, [0.0, 0.0, 0.0]
        for row in chunk:
            chunk_count, chunk_mean = merge_means(chunk_count, chunk_mean, 1, vector3(row))
        count, mean = merge_means(count, mean, chunk_count, chunk_mean)
    if not count:
        raise ValueError('No valid observations supplied; missing data is not a zero centroid.')
    return count, mean


def analyse(repo: Path) -> dict:
    repo = repo.resolve()
    relative = Path('sports_v8/data/spl_selected_frames.json')
    source = repo / relative
    manifest = json.loads((source.parent / 'manifest.json').read_text(encoding='utf-8'))
    record = next(item for item in manifest['sources'] if item['id'] == 'spl')
    raw = source.read_bytes()
    digest = hashlib.sha256(raw).hexdigest()
    if digest != record['local_sha256']:
        raise ValueError('Source hash differs from the existing course manifest. Investigate before using it.')
    data = json.loads(raw)
    if data.get('xyz_unit') != 'ft':
        raise ValueError('This bridge requires the explicitly documented feet coordinate unit.')
    rows = data['records']
    if len(rows) < 2:
        raise ValueError('At least two records are needed for the unequal-batch experiment.')
    points = [[value * 0.3048 for value in vector3(row['ball'])] for row in rows]
    count, full = stream_centroid([points])
    _, chunked = stream_centroid([points[:1], points[1:]])
    _, a = stream_centroid([points[:1]])
    _, b = stream_centroid([points[1:]])
    wrong = [(x + y) / 2 for x, y in zip(a, b)]
    _, reversed_mean = stream_centroid([reversed(points)])
    shift = [1.0, -2.0, 0.5]  # manufactured translation in metres, not new measurement
    translated = [[v + d for v, d in zip(p, shift)] for p in points]
    _, shifted_mean = stream_centroid([translated])
    checks = {
        'unequal_chunk_matches_whole': math.dist(chunked, full) < 1e-11,
        'mean_ignores_order': math.dist(reversed_mean, full) < 1e-11,
        'translation_round_trip': math.dist([v-d for v, d in zip(shifted_mean, shift)], full) < 1e-11,
    }
    if not all(checks.values()):
        raise ArithmeticError(f'An invariant check failed: {checks}')
    return {
        'experiment': 'Stage 01 -> Poux hub 1: weighted chunks and information loss',
        'data_role': 'existing selected motion records; not a static scene scan',
        'source_file': relative.as_posix(), 'source_sha256': digest,
        'source_manifest_acquisition': manifest.get('acquisition', 'not supplied'),
        'source_license': record.get('license', 'not supplied'),
        'participant_id': data.get('participant_id'), 'trial_id': data.get('trial_id'),
        'records': count, 'coordinates_per_record': 3, 'output_unit': 'm',
        'selected_frames': [row['frame'] for row in rows],
        'centroid_m': full, 'chunked_centroid_m': chunked,
        'incorrect_equal_batch_mean_m': wrong,
        'equal_batch_mean_error_m': math.dist(wrong, full),
        'chunk_sizes': [1, count - 1], 'checks': checks,
        'manufactured_memory_example': {
            'records': 80_000_000, 'columns': 3, 'bytes_per_scalar': 8,
            'xyz_bytes_only': 1_920_000_000,
            'note': 'Arithmetic estimate, not a measured allocation or file-size claim; excludes copies, metadata, indices and neighbors.'},
        'limitations': [
            'A centroid of nonuniformly selected frames is not a time average or release location.',
            'Mean pooling destroys temporal order; reversed motion can have the same mean.',
            'Local hashes prove file continuity, not independent physical truth or source transcription accuracy.',
            'The small JSON is loaded in memory. Only the centroid accumulator is streamed.',
            'No LiDAR, PointNet, reconstruction, Docker or Kubernetes run is performed by this script.'
        ],
    }


def write_run(repo: Path, output: Path) -> Path:
    repo, output = repo.resolve(), output.resolve()
    if not output.is_relative_to(repo / 'my_work'):
        raise ValueError('Choose a fresh result folder beneath this repository\'s my_work/.')
    if output.exists():
        raise FileExistsError(f'Refusing to overwrite {output}')
    result = analyse(repo)
    result['runtime'] = {'python': platform.python_version(), 'platform': platform.system(),
                         'created_utc': datetime.now(timezone.utc).isoformat(),
                         'bridge_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}
    output.mkdir(parents=True, exist_ok=False)
    path = output / 'results.json'
    path.write_text(json.dumps(result, indent=2, allow_nan=False)+'\n', encoding='utf-8')
    return path


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--repo', type=Path, default=Path.cwd())
    parser.add_argument('--output', type=Path, required=True, help='New directory under repo/my_work')
    args = parser.parse_args()
    output = args.output if args.output.is_absolute() else args.repo / args.output
    print(write_run(args.repo, output))


if __name__ == '__main__':
    main()
