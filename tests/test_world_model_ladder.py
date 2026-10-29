"""The Python ladder and the Rust ladder must agree, or one of them has a bug.

This is the only kind of check that makes a second implementation worth writing. If the two
languages produced different numbers, the comparison would be between two experiments rather
than between two languages.

The test is skipped, not failed, when `cargo` is absent: a missing toolchain is `blocked`, and
a blocked run is never reported as a pass.
"""
from __future__ import annotations

import json
import shutil
import subprocess
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
LADDER = ROOT / "optional" / "world_model"
PY_THERE = LADDER / "python"
CRATE = LADDER / "rust_ladder"

sys.path.insert(0, str(PY_THERE))

from ladder import (  # noqa: E402  (path set above)
    wm01_state,
    wm02_action,
    wm03_simulator,
    wm04_dataset,
    wm05_model,
    wm06_rollout,
    wm07_planner,
    wm08_topology,
)


# --------------------------------------------------------------------------- WM01

def test_constants_match_the_reference_module():
    """The ladder must use the same physics as the main reference, not a near-copy."""
    sys.path.insert(0, str(PY_THERE))
    import cartpole

    assert wm01_state.DT == cartpole.DT
    assert wm01_state.X_LIMIT == cartpole.X_LIMIT
    assert wm01_state.THETA_LIMIT == pytest.approx(cartpole.THETA_LIMIT, abs=0)
    assert wm01_state.MAX_STEPS == cartpole.MAX_STEPS


def test_state_rejects_non_finite_fields():
    with pytest.raises(ValueError):
        wm01_state.State(x=float("nan"), v=0.0, theta=0.0, omega=0.0)


# --------------------------------------------------------------------------- WM03

def test_hand_check_numbers_match_the_guide():
    next_state = wm03_simulator.step(wm01_state.State.upright(), wm02_action.Action.RIGHT)
    assert next_state.x == pytest.approx(0.0, abs=1e-12)
    assert next_state.v == pytest.approx(0.195_121_951_2, abs=1e-9)
    assert next_state.theta == pytest.approx(0.0, abs=1e-12)
    assert next_state.omega == pytest.approx(-0.292_682_926_8, abs=1e-9)


def test_python_simulator_matches_the_main_reference():
    """One equation, two modules: they must produce the same numbers."""
    import numpy as np
    import cartpole

    state = wm01_state.State(x=0.31, v=-0.7, theta=0.08, omega=1.3)
    ladder_next = wm03_simulator.step(state, wm02_action.Action.LEFT)
    reference_next = cartpole.step(
        np.array([state.x, state.v, state.theta, state.omega]), 0
    )
    assert ladder_next.x == pytest.approx(reference_next[0], abs=1e-12)
    assert ladder_next.v == pytest.approx(reference_next[1], abs=1e-12)
    assert ladder_next.theta == pytest.approx(reference_next[2], abs=1e-12)
    assert ladder_next.omega == pytest.approx(reference_next[3], abs=1e-12)


# --------------------------------------------------------------------------- WM04

def test_collection_is_deterministic_and_keeps_successors():
    first = wm04_dataset.collect(wm04_dataset.Rng(0), episodes=4, max_steps=60, exploration=0.4)
    second = wm04_dataset.collect(wm04_dataset.Rng(0), episodes=4, max_steps=60, exploration=0.4)
    assert first == second
    assert all(row.successor is not None for row in first)
    # The final transition of an episode carries the label *and* a successor.
    bounds = wm04_dataset.episode_bounds(first)
    for _, end in bounds:
        assert first[end - 1].terminated or first[end - 1].truncated


def test_split_by_episode_never_shares_an_episode():
    rows = wm04_dataset.collect(wm04_dataset.Rng(3), episodes=8, max_steps=80, exploration=0.4)
    train, holdout = wm04_dataset.split_episodes(rows, 0.75)
    assert {row.episode for row in train}.isdisjoint({row.episode for row in holdout})


# --------------------------------------------------------------------------- WM05

def test_the_two_implementations_share_feature_order_and_target():
    rows = wm04_dataset.collect(wm04_dataset.Rng(0), episodes=4, max_steps=60, exploration=0.4)
    row = rows[0]
    features = wm05_model.features(row.state, row.action)
    assert len(features) == wm05_model.FEATURES == 5
    assert features[4] == 1.0
    assert features[2] + features[3] == 1.0, "exactly one action is one-hot"
    assert wm05_model.OUTPUTS == 2


def test_fit_borrows_and_returns_a_model_with_its_own_weights():
    rows = wm04_dataset.collect(wm04_dataset.Rng(0), episodes=6, max_steps=80, exploration=0.4)
    before = len(rows)
    model = wm05_model.DeltaModel.fit(rows, ridge=1e-6)
    assert len(rows) == before
    assert model.samples == before
    assert len(model.weights()) == wm05_model.FEATURES * wm05_model.OUTPUTS


def test_velocities_are_reported_unchanged_not_invented():
    rows = wm04_dataset.collect(wm04_dataset.Rng(0), episodes=6, max_steps=80, exploration=0.4)
    model = wm05_model.DeltaModel.fit(rows, ridge=1e-6)
    probe = wm01_state.State(x=0.7, v=1.2, theta=0.05, omega=-0.4)
    predicted = model.predict(probe, wm02_action.Action.RIGHT)
    assert predicted.v == probe.v
    assert predicted.omega == probe.omega


# --------------------------------------------------------------------------- WM06

def test_rollout_reports_error_at_depth_and_grows():
    rows = wm04_dataset.collect(wm04_dataset.Rng(0), episodes=10, max_steps=100, exploration=0.4)
    bounds = wm04_dataset.episode_bounds(rows)
    model = wm05_model.DeltaModel.fit(rows, ridge=1e-6)
    curve = wm06_rollout.rollout_curve(model, rows, bounds, 6)
    assert curve.depth == [1, 2, 3, 4, 5, 6]
    # Error at depth is not the mean over depths: the curve must be able to grow.
    assert curve.model[-1].angle_rad >= curve.model[0].angle_rad


def test_trust_horizon_is_a_stated_rule_not_a_fact():
    curve = wm06_rollout.RolloutCurve(
        depth=[1, 2, 3],
        model=[wm06_rollout.Error(0.001, 0.001),
               wm06_rollout.Error(0.002, 0.002),
               wm06_rollout.Error(0.003, 0.003)],
        frozen=[wm06_rollout.Error(0.01, 0.01)] * 3,
    )
    assert curve.trust_horizon(1.0, 0.0025) == 2
    assert curve.trust_horizon(0.0, 0.0) == 0
    assert curve.deepest_depth_beating_frozen() == 3


# --------------------------------------------------------------------------- WM07

def test_planning_never_changes_the_weights():
    rows = wm04_dataset.collect(wm04_dataset.Rng(0), episodes=10, max_steps=100, exploration=0.4)
    model = wm05_model.DeltaModel.fit(rows, ridge=1e-6)
    before = model.weights()
    wm07_planner.plan(model, wm01_state.State.upright(), wm07_planner.Goal.balance(),
                      horizon=4, sequences=8, rng=wm04_dataset.Rng(5))
    assert model.weights() == before


def test_a_failed_dream_cannot_come_back_alive():
    states = [
        wm01_state.State.upright(),
        wm01_state.State(x=0.1, v=0.0, theta=0.0, omega=0.0),
        wm01_state.State(x=3.0, v=0.0, theta=0.0, omega=0.0),
    ]
    dream = wm07_planner.Dream(states, failed_at=2)
    assert dream.alive_steps() == 2
    assert dream.last_reachable().x == pytest.approx(0.1)


def test_parking_is_scored_in_metres():
    near = wm07_planner.Dream([wm01_state.State(x=0.95, v=0.0, theta=0.0, omega=0.0)])
    far = wm07_planner.Dream([wm01_state.State(x=0.0, v=0.0, theta=0.0, omega=0.0)])
    difference = (wm07_planner.score(wm07_planner.Goal.park(1.0), near)
                  - wm07_planner.score(wm07_planner.Goal.park(1.0), far))
    assert difference == pytest.approx(0.95, abs=1e-9)


# --------------------------------------------------------------------------- WM08

def test_h0_cannot_see_time_reversal():
    rows = wm04_dataset.collect(wm04_dataset.Rng(0), episodes=1, max_steps=60, exploration=0.25)
    states = [row.state for row in rows]
    forward = wm08_topology.h0_at_radius(wm08_topology.project(states), 0.15)
    backward = wm08_topology.h0_at_radius(
        wm08_topology.project(wm08_topology.reversed_states(states)), 0.15
    )
    assert forward == backward


# --------------------------------------------------------------------------- cross-language

@pytest.mark.skipif(shutil.which("cargo") is None, reason="cargo is not on PATH")
def test_rust_and_python_ladders_agree_on_the_saved_record(tmp_path):
    """Run both ladders on the same configuration and compare the numbers.

    A disagreement is a bug in one of them. Fields that legitimately differ — the output
    path — are excluded rather than compared loosely.
    """
    rust_out = tmp_path / "rust_run"
    result = subprocess.run(
        [
            "cargo", "run", "--quiet", "--offline", "--locked",
            "--example", "09_experiment", "--", str(rust_out),
        ],
        cwd=str(CRATE),
        capture_output=True,
        text=True,
        timeout=600,
    )
    assert result.returncode == 0, result.stdout + result.stderr
    rust = json.loads((rust_out / "results.json").read_text(encoding="utf-8"))

    python_out = tmp_path / "python_run"
    code = (
        "import sys; from pathlib import Path; "
        f"sys.path.insert(0, {str(PY_THERE)!r}); "
        "from ladder.wm09_experiment import main; "
        f"main(Path({str(python_out)!r}))"
    )
    python_run = subprocess.run(
        [sys.executable, "-c", code], capture_output=True, text=True, timeout=600
    )
    assert python_run.returncode == 0, python_run.stdout + python_run.stderr
    python = json.loads((python_out / "results.json").read_text(encoding="utf-8"))

    # Exact agreement is required for anything derived only from integers and seeding.
    assert rust["seed"] == python["seed"] == 0
    for section in ("data", "model"):
        for key, value in python["sections"][section].items():
            assert rust["sections"][section][key] == value, f"{section}.{key}"

    # Floating-point agreement to a stated tolerance, because the two languages solve the
    # same 5x5 system by the same algorithm in a different order.
    for section, keys, tolerance in (
        ("one_step", ("position_error_m", "angle_error_rad"), 1e-9),
        ("rollout", ("final_angle_error_rad", "final_frozen_error_rad"), 1e-9),
        ("planning", ("balance_score", "park_score"), 1e-9),
    ):
        for key in keys:
            assert rust["sections"][section][key] == pytest.approx(
                python["sections"][section][key], abs=tolerance
            ), f"{section}.{key}"

    assert rust["sections"]["rollout"]["trust_horizon"] == \
        python["sections"]["rollout"]["trust_horizon"]
    assert rust["sections"]["topology_h0"]["components"] == \
        python["sections"]["topology_h0"]["components"]
    assert rust["assessment"] == python["assessment"] == "not_assessed"
