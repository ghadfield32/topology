"""What the *shape* of the collected observations is, and what it is not.

This module does one job: describe a small 2-D cloud of (cart position, pole angle)
observations with the course's own persistent-homology pipeline, and say plainly that
the answer is a description. A Rips diagram of a 2-D cloud is a property of the
collector, the metric and the truncation scale. It is not evidence that the cart
"knows" anything, and it is not a semantic label.

The same numbers are recomputed independently in `../rust/` so the reduction itself is
checkable rather than trusted.
"""
from __future__ import annotations

import sys
from pathlib import Path

import numpy as np

# These modules are also loaded individually by the contract tests, so a sibling
# import has to resolve without a package around it.
_HERE = Path(__file__).resolve().parent
if str(_HERE) not in sys.path:
    sys.path.insert(0, str(_HERE))

import cartpole  # noqa: E402  (sibling module, path set above)

from shape_lab.persistence import (
    diagram,
    finite_bottleneck,
    persistent_homology,
    rips_filtration,
)

INTERPRETATION_BOUNDARY = (
    'Descriptive summary of one finite 2-D point cloud under the Rips metric. '
    'It is not evidence about CartPole, the planner, or the learner, and the bars '
    'carry no semantics: a loop in this cloud is a feature of where the collector '
    'drove the cart, not a concept the model discovered.'
)


def normalize(observations) -> np.ndarray:
    """Same scale rule as the world model, so the cloud and the input agree."""
    o = np.asarray(observations, dtype=float)
    if o.ndim == 1:
        o = o.reshape(1, -1)
    return o / np.array([cartpole.X_LIMIT, cartpole.THETA_LIMIT], dtype=float)


def summarize(points, max_edge: float) -> dict:
    """Count and measure the intervals of one filtration, and label their scope."""
    x = np.asarray(points, dtype=float)
    if x.ndim != 2 or x.shape[1] != 2:
        raise ValueError('Points must be an (n, 2) array.')
    if x.shape[0] < 3:
        raise ValueError('At least three points are needed for a nontrivial H1.')
    scale = float(max_edge)
    if not scale > 0:
        raise ValueError('max_edge must be positive; it defines the reported scale.')

    entries = rips_filtration(x, max_homology=1, max_edge=scale)
    intervals = persistent_homology(entries, max_dim=1)
    h0 = diagram(intervals, 0, finite_only=True)
    h1 = diagram(intervals, 1, finite_only=True)
    lifetimes = h1[:, 1] - h1[:, 0] if len(h1) else np.empty(0)
    return {
        'n_points': int(x.shape[0]),
        'max_edge': scale,
        'simplex_count': len(entries),
        'H0_finite': int(len(h0)),
        'H1_finite': int(len(h1)),
        'H1_essential': int(sum(1 for i in intervals if i.dim == 1 and not np.isfinite(i.death))),
        'H1_total_persistence': float(lifetimes.sum()) if len(lifetimes) else 0.0,
        'H1_max_persistence': float(lifetimes.max()) if len(lifetimes) else 0.0,
        'scale_is_truncation': True,
        'interpretation_boundary': INTERPRETATION_BOUNDARY,
    }


def bottleneck(a, b, max_edge: float) -> float:
    """Bottleneck distance between the H1 diagrams of two clouds at one scale.

    A small number says two observed clouds have similar loop structure at that scale.
    It does not say they came from similar behaviour, and changing `max_edge` changes
    the answer.
    """
    first = summarize(a, max_edge=max_edge)
    second = summarize(b, max_edge=max_edge)
    if first['H1_finite'] == 0 and second['H1_finite'] == 0:
        return 0.0
    da = _finite_diagram(a, max_edge)
    db = _finite_diagram(b, max_edge)
    return float(finite_bottleneck(da, db))


def _finite_diagram(points, max_edge: float) -> np.ndarray:
    x = np.asarray(points, dtype=float)
    entries = rips_filtration(x, max_homology=1, max_edge=float(max_edge))
    return diagram(persistent_homology(entries, max_dim=1), 1, finite_only=True)
