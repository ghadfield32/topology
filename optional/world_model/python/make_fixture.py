"""Build the committed topology fixture deterministically, with no RNG dependency.

The fixture is a small cloud in the *normalized* observation plane: cart position on
one axis, pole angle on the other, each divided by its limit. That is the same scaling
the world model receives, so the cloud is in the units the model actually sees.

Reproducibility here deliberately avoids a seeded random generator. A linear
congruential recurrence with explicit integer arithmetic gives the same bytes on any
NumPy version and any platform, which matters because a committed fixture is a claim
that the file can be rebuilt.

Run `python make_fixture.py --check` to prove the committed file still matches.
"""
from __future__ import annotations

import argparse
import json
import math
from pathlib import Path

DEFAULT = Path(__file__).resolve().parents[1] / 'fixtures' / 'points.json'
# Large enough to close the ring (deaths occur below it) and small enough that the
# enumeration stays tiny. A scale that truncates deaths would report surviving bars.
MAX_EDGE = 1.0
RING_POINTS = 18
INNER_POINTS = 6


def _unit_noise(seed: int) -> float:
    """A deterministic value in [-1, 1); not a generator, just a stable formula."""
    state = (seed * 1103515245 + 12345) % (2 ** 31)
    state = (state * 1103515245 + 12345) % (2 ** 31)
    return (state / (2 ** 31)) * 2.0 - 1.0


def build() -> dict:
    """One ring with a hole, plus a small cluster inside it.

    A ring in a 2-D cloud produces a persistent H1 interval at a scale larger than the
    gaps between neighbours but smaller than the ring diameter. The inner cluster is
    there so the cloud is not just a synthetic circle: it is what a collector produces
    when most episodes hover near the middle and some swing wide.
    """
    points = []
    for index in range(RING_POINTS):
        angle = 2.0 * math.pi * index / RING_POINTS
        radius = 0.8 + 0.06 * _unit_noise(index + 1)
        wobble_angle = angle + 0.04 * _unit_noise(index + 101)
        points.append([
            round(radius * math.cos(wobble_angle), 6),
            round(radius * math.sin(wobble_angle), 6),
        ])
    for index in range(INNER_POINTS):
        points.append([
            round(0.22 * _unit_noise(index + 201), 6),
            round(0.22 * _unit_noise(index + 301), 6),
        ])
    return {
        'name': 'normalized_cart_pole_observation_cloud',
        'units': 'cart position / X_LIMIT and pole angle / THETA_LIMIT; both are dimensionless',
        'max_edge': MAX_EDGE,
        'provenance': 'manufactured demonstration cloud, not observed CartPole episodes',
        'points': points,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, default=DEFAULT)
    parser.add_argument('--check', action='store_true')
    args = parser.parse_args()
    text = json.dumps(build(), indent=1) + '\n'
    if args.check:
        current = args.output.read_text(encoding='utf-8') if args.output.exists() else None
        if current != text:
            print(f'{args.output} is stale: re-run without --check')
            return 1
        print(f'{args.output} matches')
        return 0
    if args.output.exists():
        raise SystemExit(f'{args.output} already exists; fixtures are not overwritten')
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(text, encoding='utf-8')
    print(args.output)
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
