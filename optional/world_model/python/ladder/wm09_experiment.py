"""WM09 — save a run nothing can overwrite, then refuse to reuse the directory.

Rust sibling: `src/experiment.rs`. Same record keys, same refusal. `prepare_run` is called
**once**, before the work, and `write_results` refuses to overwrite an existing record.
"""
from __future__ import annotations

import json
from dataclasses import asdict, dataclass
from pathlib import Path

from .wm01_state import State
from .wm04_dataset import Rng, collect, episode_bounds, split_episodes
from .wm05_model import DeltaModel
from .wm06_rollout import one_step_error, rollout_curve
from .wm07_planner import Goal, plan
from .wm08_topology import h0_at_radius, project


@dataclass(frozen=True)
class RunConfig:
    seed: int = 0
    episodes: int = 40
    max_steps: int = 500
    exploration: float = 0.25
    bias_scale: float = 0.15
    ridge: float = 1e-6
    horizon: int = 10
    planning_horizon: int = 6
    sequences: int = 64
    topology_radius: float = 0.15
    tolerance_m: float = 0.05
    tolerance_rad: float = 0.02


def prepare_run(output: Path) -> Path:
    """Create the directory, or refuse. Called exactly once, before any work."""
    output = Path(output)
    if output.exists():
        raise FileExistsError(f"{output} already exists; choose a new output directory")
    output.mkdir(parents=True)
    return output


def write_results(prepared: Path, config: RunConfig, sections: dict[str, dict]) -> Path:
    """Write into a directory the caller already created; never overwrite a record."""
    prepared = Path(prepared)
    if not prepared.is_dir():
        raise ValueError(f"{prepared} is not an existing directory; call prepare_run first")
    destination = prepared / "results.json"
    if destination.exists():
        raise FileExistsError(f"{destination} already exists; this run would overwrite a record")
    payload = dict(asdict(config))
    payload["output"] = str(prepared)
    payload["assessment"] = "not_assessed"
    payload["sections"] = sections
    destination.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    return destination


def main(output: Path | None = None) -> None:
    output = Path(output) if output is not None else Path("my_work/ladder_python01")
    config = RunConfig()
    prepared = prepare_run(output)

    rows = collect(Rng(config.seed), episodes=config.episodes, max_steps=config.max_steps,
                   exploration=config.exploration, bias_scale=config.bias_scale)
    train, holdout = split_episodes(rows, 0.75)
    model = DeltaModel.fit(train, ridge=config.ridge)
    bounds = episode_bounds(holdout)

    one_step = one_step_error(model, holdout)
    curve = rollout_curve(model, holdout, bounds, config.horizon)
    balance = plan(model, State.upright(), Goal.balance(), config.planning_horizon,
                   config.sequences, Rng(config.seed + 1))
    park = plan(model, State.upright(), Goal.park(1.0), config.planning_horizon,
                config.sequences, Rng(config.seed + 2))

    states = [row.state for row in holdout]
    shape = h0_at_radius(project(states), config.topology_radius)

    sections = {
        "data": {
            "transitions": len(rows),
            "train_transitions": len(train),
            "holdout_transitions": len(holdout),
            "episodes": len(episode_bounds(rows)),
        },
        "model": {"samples": model.samples, "ridge": model.ridge,
                  "coefficients": len(model.weights())},
        "one_step": {"position_error_m": one_step.position_m,
                     "angle_error_rad": one_step.angle_rad},
        "rollout": {
            "trust_horizon": curve.trust_horizon(config.tolerance_m, config.tolerance_rad),
            "deepest_depth_beating_frozen": curve.deepest_depth_beating_frozen(),
            "final_angle_error_rad": curve.model[-1].angle_rad,
            "final_frozen_error_rad": curve.frozen[-1].angle_rad,
        },
        "planning": {
            "balance_goal": Goal.balance().name(),
            "balance_score": balance.score,
            "park_goal": Goal.park(1.0).name(),
            "park_score": park.score,
            "weights_unchanged": True,
        },
        "topology_h0": {
            "points": shape.points,
            "radius": config.topology_radius,
            "components": shape.components,
            "merges": shape.merges,
            "caveat": "describes sampled geometry; not evidence about dynamics",
        },
    }
    file = write_results(prepared, config, sections)
    print(f"wrote {file}")
    print()
    print(f"one-step angle error:   {one_step.angle_rad:.6f} rad")
    print(f"trust horizon:          {curve.trust_horizon(config.tolerance_m, config.tolerance_rad)} steps")
    print(f"best balance score:     {balance.score:.4f}")
    print(f"best park(1.0) score:   {park.score:.4f}")
    print(f"H0 components at r={config.topology_radius:.2f}: {shape.components}")
    print()
    print("Run this again with the same argument to see it refuse to overwrite.")


if __name__ == "__main__":
    import sys

    main(Path(sys.argv[1]) if len(sys.argv) > 1 else None)
