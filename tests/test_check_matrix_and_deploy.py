"""Contracts for the check matrix and the native deploy verifier.

These assert the *safety* properties: that checks stay separated, that gaps are
named, and that the deploy verifier refuses to touch a non-disposable context.
"""
from __future__ import annotations

import importlib.util
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]


def load(name: str, rel: str):
    spec = importlib.util.spec_from_file_location(name, ROOT / rel)
    mod = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(mod)
    return mod


@pytest.fixture(scope="module")
def matrix():
    return load("shape_check_matrix", "tools/check_matrix.py")


@pytest.fixture(scope="module")
def deploy():
    return load("shape_deploy_verify", "tools/native_deploy_verify.py")


def test_checks_are_separately_named_and_scoped(matrix):
    assert set(matrix.CHECKS) == {
        "contracts", "python", "readers", "native", "science", "notebooks"
    }
    for name, spec in matrix.CHECKS.items():
        assert spec.get("scope"), f"{name} must state its scope"


def test_not_claimed_list_names_the_gaps(matrix):
    joined = " ".join(matrix.NOT_CLAIMED).lower()
    assert "parity" in joined
    assert "kubernetes" in joined
    assert "mastery" in joined


def test_list_mode_succeeds(matrix):
    assert matrix.main(["--list"]) == 0


def test_unknown_check_is_rejected(matrix):
    assert matrix.main(["--only", "definitely_not_a_check"]) == 2


def test_native_checks_require_an_output_directory(matrix):
    assert matrix.main(["--only", "native"]) == 2
    assert matrix.main(["--only", "notebooks"]) == 2


def test_deploy_context_must_be_disposable(deploy):
    assert deploy.context_is_disposable("kind-shape-learning", ("kind-",))
    assert not deploy.context_is_disposable("docker-desktop", ("kind-",))
    assert not deploy.context_is_disposable("prod-cluster", ("kind-",))
    assert deploy.context_is_disposable("ci-kind-01", ("kind-", "ci-kind-"))


def test_deploy_static_checks_assert_the_shipped_policy(deploy):
    static = deploy.static_config_checks()
    assert static["compose_services"] == ["go", "rust"]
    assert static["read_only_rootfs"] is True
    assert static["network_disabled"] is True
    assert static["no_new_privileges"] is True
    assert static["job_count"] == 2
    assert static["jobs_have_deadline"] is True
    assert static["jobs_pin_namespace"] is True
    # Static parsing must never be presented as runtime evidence.
    assert static["static_only"] is True
    assert "NOT image build" in static["note"]


def test_deploy_refuses_a_production_context(tmp_path):
    """A non-disposable context must be blocked, and the run must exit blocked."""
    deploy = load("shape_deploy_verify2", "tools/native_deploy_verify.py")
    rc = deploy.main(
        [
            "--output", str(tmp_path / "deploy"),
            "--context", "docker-desktop",
            "--jobs",
        ]
    )
    assert rc == 2, "a blocked gate must exit 2, never 0"
    import json

    record = json.loads((tmp_path / "deploy" / "native_deploy.json").read_text(encoding="utf-8"))
    live = record["gates"]["kubernetes_live"]
    assert live["status"] == "blocked"
    assert "disposable" in live["reason"]


def test_deploy_never_deletes_learner_storage(deploy):
    """Cleanup must be scoped to this run's namespace and never PVC-only deletion."""
    source = (ROOT / "tools/native_deploy_verify.py").read_text(encoding="utf-8")
    assert "delete\", \"namespace\"" in source
    assert "delete\", \"pvc\"" not in source
    assert "never delete PVC" in source
