"""The optional Rust practice crate must stay additive, and its compiler cases honest.

This crate teaches ownership, typed errors and API contracts beside the course. It is
*not* a second curriculum: it owns no stage order, no lab catalogue and no learner
assessment. It must also build without network access, so it declares no dependencies
and reuses nothing from `native/rust/vendor`.

These checks are deliberately fast. The compile/test/compiler-case run is recorded in
`optional/rust_practice/VERIFICATION.md`; nothing here claims mastery.
"""
from __future__ import annotations

import importlib.util
import json
import subprocess
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
CRATE = ROOT / "optional" / "rust_practice"
SCRIPT = CRATE / "check_compiler_cases.py"


def load_script():
    spec = importlib.util.spec_from_file_location("shape_rust_practice_cases", SCRIPT)
    mod = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(mod)
    return mod


def test_crate_declares_the_same_floor_and_pinned_toolchain_as_the_course():
    manifest = (CRATE / "Cargo.toml").read_text(encoding="utf-8")
    assert 'edition = "2021"' in manifest
    assert 'rust-version = "1.83"' in manifest
    toolchain = (CRATE / "rust-toolchain.toml").read_text(encoding="utf-8")
    assert 'channel = "1.90.0"' in toolchain


def test_crate_has_no_external_dependencies_and_needs_no_vendor_directory():
    manifest = (CRATE / "Cargo.toml").read_text(encoding="utf-8")
    tail = manifest.split("[dependencies]", 1)[1].split("\n[", 1)[0]
    assert tail.strip() == "", "the practice crate must stay dependency-free to work offline"
    assert not (CRATE / "vendor").exists()
    lock = (CRATE / "Cargo.lock").read_text(encoding="utf-8")
    assert lock.count("\n[[package]]") == 1, "a dependency-free crate locks only itself"
    assert not (CRATE / ".cargo").exists(), "no source replacement is needed without dependencies"


def test_crate_is_not_a_second_curriculum():
    """No stage order, lab key or systems unit may be claimed by this crate."""
    catalog = json.loads((ROOT / "curriculum/catalog.json").read_text(encoding="utf-8"))
    labs = json.loads((ROOT / "native/protocols/labs.json").read_text(encoding="utf-8"))
    systems = json.loads((ROOT / "systems/catalog.json").read_text(encoding="utf-8"))
    assert len(catalog["stages"]) == 31
    assert len(labs["labs"]) == labs["lab_count"] == 57
    units = {u["id"] for u in systems["units"]} if "units" in systems else set()

    keys = {s["id"] for s in catalog["stages"]} | {l["key"] for l in labs["labs"]} | units
    for key in keys:
        assert not (CRATE / "compiler_cases" / key).exists()
    # The crate owns no catalogue of its own.
    assert not list(CRATE.rglob("labs.json"))
    assert not list(CRATE.rglob("catalog.json"))


def test_compiler_cases_file_matches_the_sources_on_disk():
    cases = json.loads((CRATE / "compiler_cases" / "cases.json").read_text(encoding="utf-8"))
    entries = cases["cases"]
    assert len(entries) == len({c["file"] for c in entries}), "one entry per source file"
    rejected = [c for c in entries if c["expect"] == "reject"]
    accepted = [c for c in entries if c["expect"] == "accept"]
    assert len(rejected) == 4, "four specified examples are intended to be rejected"
    assert len(accepted) >= 2, "successful compilation must also be demonstrated"
    on_disk = {p.relative_to(CRATE).as_posix() for p in CRATE.glob("compiler_cases/*/*.rs")}
    assert {c["file"] for c in entries} == on_disk
    for case in rejected:
        assert case.get("error_code", "").startswith("E"), "a rejection states the diagnostic"
    for case in accepted:
        assert "error_code" not in case
    assert cases["edition"] == "2021"


def test_expected_failure_never_accepts_a_missing_compiler():
    mod = load_script()
    verdict = mod.judge({"expect": "reject", "error_code": "E0499"}, 0, "", compiler="1.90.0")
    assert verdict["status"] == "failed", "a rejection that compiled must fail the run"
    assert mod.judge({"expect": "accept"}, 1, "error: aborting", compiler="1.90.0")["status"] == "failed"
    assert mod.judge({"expect": "accept"}, 0, "", compiler="1.90.0")["status"] == "passed"
    assert (
        mod.judge({"expect": "reject", "error_code": "E0499"}, 1, "error[E0499]: ...", compiler="1.90.0")["status"]
        == "passed"
    )
    # Wrong diagnostic code is not the specified learning outcome.
    assert (
        mod.judge({"expect": "reject", "error_code": "E0499"}, 1, "error[E0382]: ...", compiler="1.90.0")["status"]
        == "failed"
    )


def test_missing_toolchain_is_blocked_not_passed(tmp_path):
    """No rustc on PATH must not read as a successful exercise."""
    env = {k: v for k, v in {"SYSTEMROOT": str(Path("C:/Windows")) if sys.platform == "win32" else ""}.items() if v}
    result = subprocess.run(
        [sys.executable, str(SCRIPT), "--output", str(tmp_path / "compiler_blocked")],
        cwd=str(CRATE),
        env=env,
        capture_output=True,
        text=True,
        timeout=120,
    )
    assert result.returncode != 0, result.stdout + result.stderr
    summary = json.loads((tmp_path / "compiler_blocked" / "summary.json").read_text(encoding="utf-8"))
    assert summary["status"] == "blocked"
    assert "rustc" in summary["reason"].lower()
    assert summary["assessment"] == "not_assessed"


def test_script_refuses_to_overwrite_a_previous_run(tmp_path):
    out = tmp_path / "compiler_existing"
    out.mkdir()
    (out / "keep.txt").write_text("keep", encoding="utf-8")
    result = subprocess.run(
        [sys.executable, str(SCRIPT), "--output", str(out)],
        cwd=str(CRATE),
        capture_output=True,
        text=True,
        timeout=120,
    )
    assert result.returncode != 0
    assert (out / "keep.txt").read_text(encoding="utf-8") == "keep"


def test_independent_exercise_is_left_for_the_learner():
    """The worked reference must not absorb the independent assignment."""
    text = (CRATE / "EXERCISES.md").read_text(encoding="utf-8")
    assert "not_assessed" in text
    assert "your own test" in text.lower()
    assert "append_feature_checked" in text, "the independent contract is named, not implemented"


def test_worked_reference_states_what_it_is():
    readme = (CRATE / "README.md").read_text(encoding="utf-8")
    assert "worked reference" in readme.lower()
    assert "not a second curriculum" in readme.lower()
    assert "my_work/" in readme, "runs belong in a private directory"
