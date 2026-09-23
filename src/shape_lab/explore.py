"""Explicit, small CSV -> Rips exploration. No predictive inference or silent repair."""
from __future__ import annotations
from hashlib import sha256
from pathlib import Path
import numpy as np
import pandas as pd
from .persistence import rips_filtration, persistent_homology, diagram


def explore_csv(path: Path, columns: list[str], max_points: int = 20,
                seed: int = 20260920, scale: str = 'none',
                source_note: str = '', units: str = '') -> dict:
    if not columns or len(columns) != len(set(columns)) or scale not in {'none', 'standard'}:
        raise ValueError('Select unique explicit numeric columns and scale none or standard.')
    if not isinstance(max_points, int) or not 2 <= max_points <= 24:
        raise ValueError('Use 2..24 points for this intentionally small educational explorer.')
    if not source_note.strip() or not units.strip():
        raise ValueError('State source/provenance and units; use unitless only when justified.')
    path = Path(path)
    frame = pd.read_csv(path)
    if len(frame) < 2 or any(c not in frame for c in columns):
        raise ValueError('Need at least two rows and existing named feature columns.')
    try:
        x = frame[columns].to_numpy(dtype=float)
    except (TypeError, ValueError) as exc:
        raise ValueError('All selected features must be numeric.') from exc
    if not np.isfinite(x).all():
        raise ValueError('Selected columns contain missing or nonfinite data; define a separate cleaning protocol.')
    rng = np.random.default_rng(seed)
    indices = np.sort(rng.choice(len(x), size=min(max_points, len(x)), replace=False))
    sample = x[indices].copy()
    parameters = {}
    if scale == 'standard':
        mean, std = sample.mean(axis=0), sample.std(axis=0)
        if np.any(std == 0):
            raise ValueError('A selected column is constant in this sample; choose features explicitly.')
        sample = (sample - mean) / std
        parameters = {'mean': mean.tolist(), 'population_std': std.tolist(),
                      'fitted_on': 'Selected exploratory sample only; not a predictive pipeline.'}
    f = rips_filtration(sample, max_homology=1)
    bars = persistent_homology(f, max_dim=1)
    dgms = {}
    for k in (0, 1):
        dgms[f'H{k}'] = [[float(b), float(d) if np.isfinite(d) else None] for b, d in diagram(bars, k)]
    return {'scope': 'exploratory_only', 'source_note': source_note, 'units': units,
            'input_sha256': sha256(path.read_bytes()).hexdigest(), 'input_rows': len(frame),
            'selected_columns': columns, 'row_positions_zero_based': indices.tolist(),
            'sample_count': len(sample), 'seed': seed, 'scale': scale, 'scale_parameters': parameters,
            'duplicate_coordinate_rows_in_sample': int(len(sample) - len(np.unique(sample, axis=0))),
            'metric': 'Euclidean on stated coordinates; duplicate IDs give a pseudometric.',
            'coefficient_field': 2, 'max_simplex_dimension': 2, 'rips_parameter': 'maximum edge length',
            'diagrams': dgms, 'unpaired_death_encoding': 'null means survives the supplied filtration',
            'claim_limit': 'No underlying-space recovery, confidence, causality, or predictive improvement is established.'}
