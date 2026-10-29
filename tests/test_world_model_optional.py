"""The world-model worked reference must stay additive, honest and reproducible.

`optional/world_model/` teaches one idea from a public article: train a network to be
the *environment* instead of training it to be the *policy*, so the goal becomes a
function you can edit after training. Python uses PyTorch, which is an optional
dependency; the Rust companion reproduces the algorithmic core with explicit
numerics and no crates at all.

Like `optional/rust_practice/`, this area owns no stage number, no lab key and no
learner assessment. These checks are deliberately fast: the actual training runs are
recorded in `optional/world_model/VERIFICATION.md`, and nothing here claims mastery.
"""
from __future__ import annotations

import importlib.util
import json
import re
import shutil
import subprocess
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
AREA = ROOT / "optional" / "world_model"
PY = AREA / "python"
CRATE = AREA / "rust"
LADDER_CRATE = AREA / "rust_ladder"
FIXTURE = AREA / "fixtures" / "points.json"

np = pytest.importorskip("numpy")


def load(name: str):
    path = PY / f"{name}.py"
    assert path.is_file(), f"missing optional/world_model/python/{name}.py"
    spec = importlib.util.spec_from_file_location(f"world_model_area_{name}", path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


# --------------------------------------------------------------------------- area shape

def test_area_files_and_documentation_exist():
    for path in (
        AREA / "README.md",
        AREA / "SOURCE_AUDIT.md",
        AREA / "EXERCISES.md",
        AREA / "VERIFICATION.md",
        AREA / "LADDER.md",
        PY / "cartpole.py",
        PY / "topology.py",
        PY / "world_model.py",
        PY / "make_fixture.py",
        PY / "ladder" / "wm01_state.py",
        PY / "ladder" / "wm09_experiment.py",
        CRATE / "Cargo.toml",
        CRATE / "Cargo.lock",
        CRATE / "rust-toolchain.toml",
        CRATE / "src" / "lib.rs",
        CRATE / "src" / "main.rs",
        LADDER_CRATE / "Cargo.toml",
        LADDER_CRATE / "Cargo.lock",
        LADDER_CRATE / "rust-toolchain.toml",
        LADDER_CRATE / "src" / "lib.rs",
        FIXTURE,
    ):
        assert path.is_file(), f"missing {path.relative_to(ROOT)}"


def test_the_ladder_has_one_runnable_example_per_rung():
    """The ladder is a build order, so every rung must be runnable on its own."""
    manifest = (LADDER_CRATE / "Cargo.toml").read_text(encoding="utf-8")
    rungs = ["01_state", "02_action", "03_step", "04_collect", "05_fit",
             "06_rollout", "07_plan", "08_topology", "09_experiment"]
    for rung in rungs:
        assert (LADDER_CRATE / "examples" / f"{rung}.rs").is_file(), rung
        assert f'name = "{rung}"' in manifest, f"{rung} is not declared in Cargo.toml"
    pairs = [
        ("state", "wm01_state"), ("action", "wm02_action"),
        ("simulator", "wm03_simulator"), ("dataset", "wm04_dataset"),
        ("model", "wm05_model"), ("rollout", "wm06_rollout"),
        ("planner", "wm07_planner"), ("shape", "wm08_topology"),
        ("experiment", "wm09_experiment"),
    ]
    for rust_module, python_module in pairs:
        assert (LADDER_CRATE / "src" / f"{rust_module}.rs").is_file(), rust_module
        assert (PY / "ladder" / f"{python_module}.py").is_file(), python_module
    assert len(pairs) == len(rungs)


def test_the_ladder_documents_the_first_step_before_the_physics():
    """A beginner route must start with a program that runs, not with a world model."""
    text = (AREA / "LADDER.md").read_text(encoding="utf-8")
    assert "Hello, world!" in text
    assert "cargo run --offline --locked" in text
    # The build order is stated, and the physics comes after the state representation.
    assert text.index("WM01") < text.index("WM03")
    # Each rung must have a predict-before-you-run prompt.
    assert text.count("Predict") >= 3
    # It must not claim to be an assessment.
    assert "not_assessed" in text


def test_area_is_linked_from_the_hand_maintained_learning_index():
    index = (ROOT / "learning" / "README.md").read_text(encoding="utf-8")
    assert "world_model" in index, "the guide must be reachable from learning/README.md"
    layout = (ROOT / "docs/release/REPOSITORY_LAYOUT.md").read_text(encoding="utf-8")
    assert "optional/world_model/" in layout


def test_area_owns_no_catalogue_and_invents_no_stage_number():
    assert not list(AREA.rglob("catalog.json"))
    assert not list(AREA.rglob("labs.json"))
    text = (AREA / "README.md").read_text(encoding="utf-8")
    assert "not a second curriculum" in text.lower()
    assert "not_assessed" in text or "not assessed" in text.lower()
    known = {
        "stage" + s["id"]
        for s in json.loads((ROOT / "curriculum/catalog.json").read_text(encoding="utf-8"))["stages"]
    }
    assert set(re.findall(r"\bstage\d{2}\b", text)) <= known


def test_source_attribution_is_preserved_and_numbers_are_not_ours():
    text = (AREA / "README.md").read_text(encoding="utf-8")
    for token in (
        "Anubhab Banerjee",
        "How to Make Your First World Model from Scratch",
        "github.com/AnubhabBanerjee/CartPole-Daydream",
    ):
        assert token in text, f"attribution lost: {token}"
    audit = (AREA / "SOURCE_AUDIT.md").read_text(encoding="utf-8")
    assert "author" in audit.lower()
    # The article's measurements must be labelled as the author's, not reproduced here.
    assert "not our measurement" in audit.lower() or "the author" in audit.lower()


def test_article_lessons_are_taught_rather_than_only_linked():
    text = (AREA / "README.md").read_text(encoding="utf-8").lower()
    for token in ("objective", "cover the actions", "horizon"):
        assert token in text, f"the article's hard-won lesson is missing: {token}"


# --------------------------------------------------------------------------- cart pole

def test_simulator_separates_termination_from_truncation():
    cp = load("cartpole")
    balanced = cp.rollout(cp.initial_state(), policy=lambda s: cp.proportional_controller(s), max_steps=500)
    assert balanced["steps"] == 500
    assert balanced["terminated"] is False and balanced["truncated"] is True
    fallen = cp.rollout(cp.initial_state(), policy=lambda s: 0, max_steps=500)
    assert fallen["terminated"] is True and fallen["truncated"] is False
    assert fallen["steps"] < 500


def test_proportional_controller_survives_longer_than_flailing():
    cp = load("cartpole")
    controlled = cp.rollout(cp.initial_state(), policy=lambda s: cp.proportional_controller(s), max_steps=500)
    rng = cp.rng(0)
    flailing = cp.rollout(cp.initial_state(), policy=lambda s: int(rng.random() < 0.5), max_steps=500)
    assert controlled["steps"] == 500
    assert flailing["steps"] < 100


def test_visible_state_hides_the_velocities():
    cp = load("cartpole")
    state = cp.initial_state()
    visible = cp.visible(state)
    assert visible.shape == (2,)
    assert not cp.states_are_complete(visible), "a two-number state cannot determine the next step"
    complete = cp.step(state, 1)
    assert cp.states_are_complete(complete), "the full four-number state is complete"
    assert cp.visible(complete).shape == (2,), "a batch-shaped read must still project"


def test_visible_projection_works_on_a_batch():
    cp = load("cartpole")
    states = cp.collect(cp.rng(3), episodes=2)["states"]
    projected = cp.visible(states)
    assert projected.shape == (len(states), 2)
    np.testing.assert_allclose(projected[0], cp.visible(states[0]))


def test_trust_horizon_is_the_last_depth_still_within_tolerance():
    cp = load("cartpole")
    errors = [0.001, 0.010, 0.019, 0.030, 0.400]
    horizon, first_failure = cp.trust_horizon(errors, tolerance=0.02)
    assert horizon == 3
    assert first_failure == errors.index(0.030)
    assert cp.trust_horizon([0.001, 0.002], tolerance=0.02) == (2, None)
    with pytest.raises(ValueError):
        cp.trust_horizon(errors, tolerance=0.0)


def test_collection_covers_both_actions_and_both_endings():
    cp = load("cartpole")
    data = cp.collect(cp.rng(0), episodes=12, exploration=0.5, max_steps=500)
    assert data["actions"].shape == data["observations"].shape[:-1]
    assert set(data["actions"].tolist()) == {0, 1}, "planning asks about actions no policy would choose"
    assert data["terminated"].sum() > 0, "a crash-free dataset cannot teach the crash model"
    # Exactly one ending flag per episode; the flags are per transition, not per row.
    assert int(data["terminated"].sum() + data["truncated"].sum()) == 12
    assert data["observations"].shape[1] == 2, "the model only sees position and angle"


def test_collection_records_truncation_when_nothing_falls():
    cp = load("cartpole")
    # bias_scale=0 keeps every game hovering, so the only possible ending is the timer.
    data = cp.collect(cp.rng(1), episodes=2, exploration=0.0, max_steps=500, bias_scale=0.0)
    assert data["terminated"].sum() == 0, "an unbiased controller balances"
    assert int(data["truncated"].sum()) == 2, "the stopwatch must be recorded separately"
    assert len(data["observations"]) == 1000


# --------------------------------------------------------------------------- topology

def test_collection_validates_its_arguments():
    cp = load("cartpole")
    with pytest.raises(ValueError):
        cp.collect(cp.rng(0), episodes=0)
    with pytest.raises(ValueError):
        cp.collect(cp.rng(0), episodes=1, max_steps=0)
    with pytest.raises(ValueError):
        cp.collect(cp.rng(0), episodes=1, exploration=1.5)
    with pytest.raises(ValueError):
        cp.collect(cp.rng(0), episodes=1, bias_scale=-1.0)


def test_normalization_puts_both_numbers_on_the_same_scale():
    tp = load("topology")
    cp = load("cartpole")
    scaled = tp.normalize([[cp.X_LIMIT, cp.THETA_LIMIT]])
    np.testing.assert_allclose(scaled, [[1.0, 1.0]])


def test_topology_summary_is_descriptive_and_reports_its_scale():
    tp = load("topology")
    fixture = json.loads(FIXTURE.read_text(encoding="utf-8"))
    summary = tp.summarize(fixture["points"], max_edge=fixture["max_edge"])
    assert summary["n_points"] == len(fixture["points"])
    assert summary["max_edge"] == pytest.approx(fixture["max_edge"])
    assert summary["H0_finite"] >= 1
    assert "H1_finite" in summary and "H1_total_persistence" in summary
    boundary = summary["interpretation_boundary"].lower()
    assert "descriptive" in boundary
    assert "not evidence" in boundary or "does not establish" in boundary
    assert "semantics" in boundary, "shape of a 2D cloud is not meaning"


def test_summary_reuses_the_course_persistence_pipeline():
    """The same fixture must give the same intervals as the course's own code."""
    tp = load("topology")
    from shape_lab.persistence import diagram, persistent_homology, rips_filtration

    fixture = json.loads(FIXTURE.read_text(encoding="utf-8"))
    scale = fixture["max_edge"]
    intervals = persistent_homology(rips_filtration(fixture["points"], max_homology=1, max_edge=scale), max_dim=1)
    summary = tp.summarize(fixture["points"], max_edge=scale)
    h1 = diagram(intervals, 1, finite_only=True)
    assert summary["H1_finite"] == len(h1)
    assert summary["H1_total_persistence"] == pytest.approx(float((h1[:, 1] - h1[:, 0]).sum()))


def test_bottleneck_distance_is_zero_for_identical_clouds():
    tp = load("topology")
    fixture = json.loads(FIXTURE.read_text(encoding="utf-8"))
    points = fixture["points"]
    assert tp.bottleneck(points, points, max_edge=fixture["max_edge"]) == pytest.approx(0.0, abs=1e-12)


def test_committed_fixture_is_reproducible():
    make = load("make_fixture")
    assert make.build() == json.loads(FIXTURE.read_text(encoding="utf-8"))


# --------------------------------------------------------------------------- rust companion

def test_rust_crate_stays_dependency_free_and_pinned():
    manifest = (CRATE / "Cargo.toml").read_text(encoding="utf-8")
    assert 'edition = "2021"' in manifest
    assert 'rust-version = "1.83"' in manifest
    tail = manifest.split("[dependencies]", 1)[1].split("\n[", 1)[0]
    assert tail.strip() == "", "the companion must build offline with no crates"
    assert not (CRATE / "vendor").exists()
    assert 'channel = "1.90.0"' in (CRATE / "rust-toolchain.toml").read_text(encoding="utf-8")
    lock = (CRATE / "Cargo.lock").read_text(encoding="utf-8")
    assert lock.count("\n[[package]]") == 1, "a dependency-free crate locks only itself"


def test_ci_runs_the_companion_gates():
    """The crate's lint and format gates must actually be wired into CI.

    A gate documented in a README but never executed is a promise, not a check.
    """
    workflow = (ROOT / ".github" / "workflows" / "polyglot.yml").read_text(encoding="utf-8")
    assert "optional/world_model/rust" in workflow
    for command in (
        "cargo test --offline --locked",
        "cargo fmt --all -- --check",
        "cargo clippy --offline --all-targets -- -D warnings",
    ):
        assert command in workflow, f"CI does not run: {command}"
    assert "'1.90.0'" in workflow, "CI must pin the tested compiler"
    # The ladder must be gated too, including the refuse-to-overwrite contract.
    assert "optional/world_model/rust_ladder" in workflow
    assert "--example 09_experiment" in workflow
    assert "the experiment accepted an existing output directory" in workflow


def test_rust_sources_implement_the_world_model_core():
    text = "\n".join(p.read_text(encoding="utf-8") for p in sorted((CRATE / "src").rglob("*.rs")))
    for token in ("trust_horizon", "free_rollout", "plan", "persistence"):
        assert token in text, f"Rust companion is missing {token}"
    assert "predict" in text and "delta" in text.lower(), "predict the change, not the position"


def test_both_languages_reproduce_the_averaging_bug():
    """The article's central bug must be shown, not merely described, in both languages.

    Python has `terminal_mean` beside an averaging score; Rust has `score_park` beside
    `score_park_average` with a test asserting they rank the same two dreams differently.
    """
    rust = (CRATE / "src" / "goals.rs").read_text(encoding="utf-8")
    assert "score_park_average" in rust
    assert "the averaging rule must prefer hovering" in rust
    assert "terminal_value" in rust
    python = (PY / "world_model.py").read_text(encoding="utf-8")
    assert "terminal_mean" in python


@pytest.mark.skipif(shutil.which("cargo") is None, reason="cargo is not on PATH in this environment")
def test_rust_topology_matches_the_python_pipeline_on_the_same_fixture(tmp_path):
    """Two independent reductions of one filtration must agree on its diagram.

    A disagreement is either a tie-ordering bug or a coefficient bug. Counts and the
    total persistence are invariant under a valid tie ordering, so they are the check.
    """
    tp = load("topology")
    fixture = FIXTURE.read_text(encoding="utf-8")
    out = tmp_path / "rust_topology"
    result = subprocess.run(
        [
            "cargo", "run", "--quiet", "--bin", "world-model-rust", "--",
            "--check-topology", str(FIXTURE), "--output", str(out),
        ],
        cwd=str(CRATE),
        capture_output=True,
        text=True,
        timeout=300,
    )
    assert result.returncode == 0, result.stdout + result.stderr
    rust = json.loads((out / "topology.json").read_text(encoding="utf-8"))
    data = json.loads(fixture)
    python = tp.summarize(data["points"], max_edge=data["max_edge"])
    assert rust["h0_finite"] == python["H0_finite"]
    assert rust["h1_finite"] == python["H1_finite"]
    assert rust["h1_total_persistence"] == pytest.approx(python["H1_total_persistence"], abs=1e-9)
    assert rust["max_persistence"] == pytest.approx(python["H1_max_persistence"], abs=1e-9)


# --------------------------------------------------------------------------- run contract

def test_output_directories_are_never_overwritten(tmp_path):
    wm = load("world_model")
    existing = tmp_path / "previous_run"
    existing.mkdir()
    (existing / "keep.txt").write_text("keep", encoding="utf-8")
    with pytest.raises(FileExistsError):
        wm.ensure_new_output(existing)
    assert (existing / "keep.txt").read_text(encoding="utf-8") == "keep"


def test_blocked_is_not_reported_as_passed():
    """No PyTorch, no result: the module must have an explicit blocked path."""
    text = (PY / "world_model.py").read_text(encoding="utf-8")
    assert "blocked" in text.lower()
    assert "torch" in text
    readme = (AREA / "README.md").read_text(encoding="utf-8").lower()
    assert "blocked" in readme
    assert "not" in readme and "passed" in readme


def test_goal_is_scored_in_physical_units_not_normalized_ones():
    """`PARK_TARGET = 1.0` means one metre, so scoring must not use normalized input.

    A normalized target of 1.0 is 2.4 m away. If the goal compares a normalized position
    against a metric target, the planner is asked for a different destination from the one
    the constant names.
    """
    wm = load("world_model")
    cp = load("cartpole")
    torch = pytest.importorskip("torch")

    def score(final_cart_position_m):
        normalized = cp.normalize_visible([[final_cart_position_m, 0.0]])
        observations = torch.tensor(normalized.reshape(1, 1, 2), dtype=torch.float32)
        logits = torch.tensor([[-1.0]], dtype=torch.float32)
        return float(wm.score_park(observations, logits, target=1.0))

    # A dream that ends exactly at the target must score the full survival value: no
    # distance penalty, no uprightness penalty.
    assert score(1.0) == pytest.approx(1.0, abs=1e-5)
    # One metre away in physical terms costs exactly the position weight.
    assert score(2.0) == pytest.approx(0.0, abs=1e-5)
    # And the penalty must be linear in metres, not in normalized units.
    assert score(1.5) == pytest.approx(0.5, abs=1e-5)


def test_predicted_failure_is_absorbing():
    """A dream that crashes at step 3 cannot be counted alive at step 4."""
    wm = load("world_model")
    torch = pytest.importorskip("torch")
    logits = torch.tensor([[-1.0, 5.0, -1.0, -1.0]], dtype=torch.float32)
    alive = wm.survival_mask(logits)
    assert alive.tolist() == [[True, False, False, False]], (
        "once the crash head fires, every later step is unreachable"
    )


def test_rollout_error_is_reported_at_depth_not_averaged_over_depths():
    """Depth h must mean error *at* h, not the mean error of steps 1..h.

    Averaging makes the curve look flatter than it is and hides the depth where the
    model actually falls apart.
    """
    text = (PY / "world_model.py").read_text(encoding="utf-8")
    assert "error[-1, cartpole.VISIBLE_POLE_ANGLE]" in text, (
        "the reported value must be the last step of the rollout"
    )
    assert "collected_angle.append(float(error[-1" in text
    readme = (AREA / "README.md").read_text(encoding="utf-8").lower()
    assert "at each depth" in readme or "error at depth" in readme


def test_planning_does_not_mutate_the_fitted_weights():
    """A borrowed model must be inspected, not modified, by the planner."""
    wm = load("world_model")
    cp = load("cartpole")
    torch = pytest.importorskip("torch")
    torch.set_num_threads(1)
    data = cp.collect(cp.rng(0), episodes=4)
    model = wm.build_model(torch)
    wm.train(model, torch, data, epochs=1, train_steps=2, seed=0)
    before = [p.detach().clone() for p in model.parameters()]
    wm.plan(model, torch, cp.initial_state(cp.rng(0)), wm.GOAL_BALANCE,
            horizon=3, sequences=4, generator=cp.rng(0))
    after = [p.detach().clone() for p in model.parameters()]
    assert all(torch.equal(a, b) for a, b in zip(before, after)), "planning changed the model"


def test_training_restores_the_best_validation_checkpoint():
    """Reporting the best epoch is not the same as using its weights.

    If the model keeps the final epoch, every measurement below describes a different
    model from the one whose loss was reported as best.
    """
    text = (PY / "world_model.py").read_text(encoding="utf-8")
    assert "load_state_dict" in text, "the best checkpoint must be restored, not only logged"
    assert "best_state" in text


def test_goals_accept_a_runtime_target_without_refitting():
    """Changing the goal must not touch the weights: that is the whole payload."""
    wm = load("world_model")
    torch = pytest.importorskip("torch")
    cp = load("cartpole")

    def score(target):
        normalized = cp.normalize_visible([[2.0, 0.0], [2.2, 0.0]])
        observations = torch.tensor(normalized.reshape(1, 2, 2), dtype=torch.float32)
        logits = torch.tensor([[-1.0, -1.0]], dtype=torch.float32)
        return float(wm.score_park(observations, logits, target=target))

    assert score(2.2) > score(1.0), "the score must follow the target, not a constant"
    text = (PY / "world_model.py").read_text(encoding="utf-8")
    assert "def score_balance" in text
    assert "def score_park" in text
    readme = (AREA / "README.md").read_text(encoding="utf-8")
    assert "score_park" in readme or "goal function" in readme.lower()


def test_goal_is_scored_by_the_end_of_the_dream_not_its_average():
    """The article's central bug: averaging rejects the only working manoeuvre."""
    text = (PY / "world_model.py").read_text(encoding="utf-8")
    assert "terminal_mean" in text
    assert "score_park" in text
    readme = (AREA / "README.md").read_text(encoding="utf-8").lower()
    assert "terminal" in readme
    assert "average" in readme, "the page must name the wrong scoring rule it replaces"


def test_planner_forks_a_carried_memory_rather_than_resetting_it():
    """A blank memory at each decision cannot know the velocities.

    This is a regression guard for a real bug: the first version of the planner
    restarted from zeros on every step, so `score_park` could never plan a journey.
    """
    text = (PY / "world_model.py").read_text(encoding="utf-8")
    assert "advance_memory" in text
    assert "carry_memory" in text
    assert "goal_balance_without_carried_memory" in text
    readme = (AREA / "README.md").read_text(encoding="utf-8").lower()
    assert "memory" in readme and "velocity" in readme


def test_free_rollout_measurement_warms_the_memory_too():
    """The drift measurement must not be dominated by initial ignorance.

    The same bug appeared twice: the planner reset its memory, and so did the rollout
    error sweep. Both are now warmed with real transitions and both record the count.
    """
    text = (PY / "world_model.py").read_text(encoding="utf-8")
    assert "_warm_memory" in text
    assert "memory_warmup_steps" in text
    # The warm-up must be passed through from the run configuration, not hard-coded.
    assert "warmup=warmup" in text


def test_training_windows_include_the_transition_that_carries_the_crash_label():
    """A regression guard for a bug that looked exactly like a weak model.

    An off-by-one in `valid_window_starts` dropped the final transition of every episode,
    which is the only one that can be labelled `terminated`. Training then contained zero
    positives, the crash head learnt "always alive", and the planner discarded every safe
    dream. The symptom is indistinguishable from an undertrained model, so it needs a test.
    """
    wm = load("world_model")
    cp = load("cartpole")
    data = cp.collect(cp.rng(0), episodes=12, exploration=0.5)
    bounds = wm.episode_bounds(data)
    starts = wm.valid_window_starts(bounds, 8)
    assert starts.size > 0
    positives = sum(int(data["terminated"][s + offset]) for s in starts for offset in range(8))
    assert positives > 0, "the crash transition must be inside at least one training window"
    # Every window must also stay inside one episode.
    for start in starts:
        begin, end = next((b, e) for b, e in bounds if b <= start < e)
        assert start + 8 <= end


def test_dataset_records_the_successor_of_the_final_transition():
    wm = load("world_model")
    cp = load("cartpole")
    data = cp.collect(cp.rng(4), episodes=6, exploration=0.4)
    assert data["next_observations"].shape == data["observations"].shape
    bounds = wm.episode_bounds(data)
    for begin, end in bounds:
        # The last recorded transition of an episode ends by falling or by the timer.
        assert data["terminated"][end - 1] or data["truncated"][end - 1]
    assert data["terminated"].sum() > 0


def test_crash_metrics_report_recall_and_false_alarms_together():
    """Accuracy is not a crash-detection metric: the base rate is 99.4%."""
    text = (PY / "world_model.py").read_text(encoding="utf-8")
    assert "def crash_detection_metrics" in text
    assert "false_alarms_per_episode" in text
    assert "recall" in text
    readme = (AREA / "README.md").read_text(encoding="utf-8").lower()
    assert "false alarm" in readme or "false-alarm" in readme


def test_termination_weighting_is_a_pos_weight_not_a_whole_loss_multiplier():
    """Scaling the whole BCE changes step size, not the optimum.

    The optimum of an unscaled BCE on 0.6%-positive labels is still "always alive", so a
    multiplier produces a detector that is confidently wrong about every crash.
    """
    text = (PY / "world_model.py").read_text(encoding="utf-8")
    assert "pos_weight=weight" in text
    assert "TERMINATION_LOSS_SCALE" in text
    assert "termination_loss_scale" in text, "the coefficient must be recorded in results"


def test_tiny_end_to_end_run_reports_not_assessed(tmp_path):
    pytest.importorskip("torch")
    out = tmp_path / "tiny_run"
    result = subprocess.run(
        [
            sys.executable, str(PY / "world_model.py"),
            "--output", str(out),
            "--episodes", "6",
            "--epochs", "1",
            "--train-steps", "6",
            "--eval-episodes", "2",
            "--planning-episodes", "2",
            "--points", "12",
            "--horizon", "8",
            "--planning-horizon", "3",
            "--sequences", "8",
        ],
        capture_output=True,
        text=True,
        timeout=600,
    )
    assert result.returncode == 0, result.stdout + result.stderr
    payload = json.loads((out / "results.json").read_text(encoding="utf-8"))
    assert payload["status"] == "completed"
    assert payload["assessment"] == "not_assessed"
    # Attribution: the code link ends with the author's repository, the article link with
    # the article. Both must be present, and neither may be presented as ours.
    assert payload["source"]["code"].endswith("CartPole-Daydream")
    assert payload["source"]["author"] == "Anubhab Banerjee"
    assert payload["metrics"]["one_step"]["validation_pole_angle_rad"] >= 0.0
    assert payload["metrics"]["free_rollout"]["trust_horizon"] >= 0
    assert payload["metrics"]["crash_detection"]["evaluated_episodes"] >= 1
    assert payload["config"]["termination_loss_scale"] > 0
    assert payload["topology"]["observed"]["H0_finite"] >= 1
    assert "not evidence" in payload["topology"]["observed"]["interpretation_boundary"].lower()
