"""Contracts for the CI workflows: fast by default, full only on demand.

Routine learning sessions must not rebuild or retrain everything. These tests
assert the workflow shape rather than executing CI.
"""
from __future__ import annotations

from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
WORKFLOWS = ROOT / ".github" / "workflows"

yaml = pytest.importorskip("yaml")


def load(name: str) -> dict:
    return yaml.safe_load((WORKFLOWS / name).read_text(encoding="utf-8"))


def test_all_workflows_parse():
    files = sorted(WORKFLOWS.glob("*.yml"))
    assert files, "expected at least one workflow"
    for path in files:
        parsed = yaml.safe_load(path.read_text(encoding="utf-8"))
        assert "jobs" in parsed, f"{path.name} has no jobs"


def test_learning_sessions_do_not_run_the_full_sweep_on_push():
    """A push must not trigger the 171-notebook sweep or a native science sweep."""
    wf = load("language-notebooks.yml")
    jobs = wf["jobs"]
    # The heavy jobs are gated behind manual dispatch.
    for heavy in ("sweep", "native-science"):
        assert "if" in jobs[heavy], f"{heavy} must be conditional"
        condition = jobs[heavy]["if"]
        assert "workflow_dispatch" in condition, f"{heavy} must require manual dispatch"
    # The fast contracts job has no such gate.
    assert "if" not in jobs["contracts"]


def test_workflow_dispatch_offers_fast_and_full():
    wf = load("language-notebooks.yml")
    dispatch = wf[True] if True in wf else wf.get("on", {})
    inputs = dispatch.get("workflow_dispatch", {}).get("inputs", {})
    assert "scope" in inputs
    assert sorted(inputs["scope"]["options"]) == ["fast", "full"]
    assert inputs["scope"]["default"] == "full"


def test_sweep_never_enables_error_tolerance():
    """No run step may pass an error-tolerance flag to the sweep."""
    wf = load("language-notebooks.yml")
    runs = [
        step.get("run", "")
        for job in wf["jobs"].values()
        for step in job.get("steps", [])
    ]
    for command in runs:
        assert "--allow-errors" not in command
        assert "--allow_errors" not in command


def test_sweep_preserves_evidence_even_on_failure():
    wf = load("language-notebooks.yml")
    upload = wf["jobs"]["sweep"]["steps"][-1]
    assert upload["uses"].startswith("actions/upload-artifact")
    assert upload["if"] == "always()"
    assert upload["with"]["if-no-files-found"] == "error"


def test_workflows_pin_the_tested_toolchains():
    for name in ("language-notebooks.yml", "native-course-v16.yml"):
        text = (WORKFLOWS / name).read_text(encoding="utf-8")
        assert "1.90.0" in text, f"{name} should pin the tested Rust compiler"


def test_workflows_declare_read_only_permissions():
    for name in ("language-notebooks.yml", "native-course-v16.yml"):
        wf = load(name)
        assert wf.get("permissions", {}).get("contents") == "read"
