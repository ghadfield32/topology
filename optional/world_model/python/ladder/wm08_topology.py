"""WM08 — H0 components, and the limitation that makes them honest.

Rust sibling: `src/shape.rs`. The point is the same in both: reversing a trajectory does not
change its point cloud, so a component count cannot detect that time was reversed.
"""
from __future__ import annotations

import math
from dataclasses import dataclass

from .wm01_state import THETA_LIMIT, X_LIMIT, State


@dataclass(frozen=True)
class Point:
    x: float
    theta: float

    def distance(self, other: "Point") -> float:
        return math.hypot(self.x - other.x, self.theta - other.theta)


def project(states: list[State]) -> list[Point]:
    """Both numbers divided by their own limits, so distance is not metres plus radians."""
    return [Point(state.x / X_LIMIT, state.theta / THETA_LIMIT) for state in states]


@dataclass(frozen=True)
class H0:
    points: int
    merges: int
    components: int


def h0_at_radius(points: list[Point], radius: float) -> H0:
    """Union-find at one stated radius. The radius is part of the answer."""
    if not points:
        raise ValueError("no points to analyse")
    if not math.isfinite(radius) or radius < 0:
        raise ValueError("radius must be finite and nonnegative")
    parent = list(range(len(points)))

    def find(node: int) -> int:
        while parent[node] != node:
            parent[node] = parent[parent[node]]
            node = parent[node]
        return node

    merges = 0
    for i in range(len(points)):
        for j in range(i + 1, len(points)):
            if points[i].distance(points[j]) <= radius:
                left, right = find(i), find(j)
                if left != right:
                    parent[left] = right
                    merges += 1
    return H0(len(points), merges, len({find(node) for node in range(len(points))}))


def reversed_states(states: list[State]) -> list[State]:
    return list(reversed(states))


def main() -> None:
    from .wm04_dataset import Rng, collect, episode_bounds

    rows = collect(Rng(0), episodes=2, max_steps=120, exploration=0.25, bias_scale=0.15)
    bounds = episode_bounds(rows)
    for episode, (begin, end) in enumerate(bounds):
        states = [row.state for row in rows[begin:end]]
        points = project(states)
        print(f"episode {episode}: {len(points)} sampled states")
        for radius in (0.05, 0.15, 0.40):
            forward = h0_at_radius(points, radius)
            backward = h0_at_radius(project(reversed_states(states)), radius)
            print(f"  radius {radius:.2f}: components {forward.components:>3}"
                  f" -> after reversing {backward.components:>3}"
                  f"  (identical: {forward == backward})")
    print()
    print("The radius is part of the answer. A component count without its radius is not")
    print("reproducible, and a bar that survives only because the radius truncated its death")
    print("is an artefact of the radius, not a feature of the trajectory.")
    print()
    print("H0 says how the sampled cloud is connected. It says nothing about whether the")
    print("model predicts the next state, and nothing about CartPole.")


if __name__ == "__main__":
    main()
