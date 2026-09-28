"""Contracts for tools/verify_language_notebooks.py.

These are fast checks of the verifier's own guarantees. They do not execute 171
notebooks; the full sweep is a separate, deliberate run.
"""
from __future__ import annotations

import importlib.util
import json
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]


def load_verifier():
    spec = importlib.util.spec_from_file_location(
        "shape_nb_verifier", ROOT / "tools/verify_language_notebooks.py"
    )
    mod = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(mod)
    return mod


def test_expected_entries_are_derived_from_the_registry():
    verifier = load_verifier()
    labs = json.loads((ROOT / "native/protocols/labs.json").read_text(encoding="utf-8"))["labs"]
    entries = verifier.expected_entries(("python", "go", "rust"))
    assert len(entries) == len(labs) * 3
    assert {e["lab"] for e in entries} == {lab["key"] for lab in labs}
    assert {e["lang"] for e in entries} == {"python", "go", "rust"}
    assert verifier.audit_set(entries, ("python", "go", "rust")) == []


def test_audit_rejects_a_missing_notebook():
    verifier = load_verifier()
    entries = verifier.expected_entries(("python",))
    entries[0]["path"] = "workbooks/polyglot/python/does_not_exist.ipynb"
    problems = verifier.audit_set(entries, ("python",))
    assert any("missing notebook" in p for p in problems)


def test_audit_rejects_a_duplicate_entry():
    verifier = load_verifier()
    entries = verifier.expected_entries(("python",))
    entries.append(dict(entries[0]))
    problems = verifier.audit_set(entries, ("python",))
    assert any("duplicate expected entry" in p for p in problems)


def test_audit_rejects_an_unexpected_notebook(tmp_path, monkeypatch):
    """A stray notebook that is not in the registry must fail the set audit."""
    verifier = load_verifier()
    fake_root = tmp_path / "polyglot"
    (fake_root / "python").mkdir(parents=True)
    labs = json.loads((ROOT / "native/protocols/labs.json").read_text(encoding="utf-8"))["labs"]
    for lab in labs:
        (fake_root / "python" / f"{lab['key']}.ipynb").write_text("{}", encoding="utf-8")
    (fake_root / "python" / "not_a_registered_lab.ipynb").write_text("{}", encoding="utf-8")

    monkeypatch.setattr(verifier, "NB_ROOT", fake_root)
    entries = verifier.expected_entries(("python",))
    problems = verifier.audit_set(entries, ("python",))
    assert any("unexpected notebook" in p for p in problems), problems


def test_verifier_refuses_an_existing_output_directory(tmp_path):
    verifier = load_verifier()
    target = tmp_path / "already"
    target.mkdir()
    assert verifier.main(["--output", str(target), "--lang", "python", "--limit", "1"]) == 2


def test_partial_coverage_exits_nonzero(tmp_path, monkeypatch):
    """Incomplete coverage must never be reported as acceptance."""
    verifier = load_verifier()
    monkeypatch.setattr(
        verifier,
        "execute_notebook",
        lambda entry, out, timeout: {
            "lab": entry["lab"],
            "lang": entry["lang"],
            "status": "passed",
        },
    )
    monkeypatch.setattr(verifier, "compile_once", lambda langs, out: {})
    rc = verifier.main(
        ["--output", str(tmp_path / "partial"), "--lang", "python", "--limit", "2"]
    )
    assert rc == 1, "a partial run must not exit zero"
    summary = json.loads((tmp_path / "partial" / "coverage.json").read_text(encoding="utf-8"))
    assert summary["coverage"]["complete"] is False
    assert summary["passed"] == 2
    assert summary["failed"] == 0


def test_full_coverage_of_all_entries_exits_zero(tmp_path, monkeypatch):
    verifier = load_verifier()
    monkeypatch.setattr(
        verifier,
        "execute_notebook",
        lambda entry, out, timeout: {
            "lab": entry["lab"],
            "lang": entry["lang"],
            "status": "passed",
        },
    )
    monkeypatch.setattr(verifier, "compile_once", lambda langs, out: {})
    rc = verifier.main(["--output", str(tmp_path / "full"), "--lang", "all"])
    assert rc == 0
    summary = json.loads((tmp_path / "full" / "coverage.json").read_text(encoding="utf-8"))
    assert summary["coverage"]["complete"] is True
    assert summary["passed"] == summary["expected_entries"] == 171


def test_a_failing_entry_makes_the_run_fail(tmp_path, monkeypatch):
    verifier = load_verifier()

    def flaky(entry, out, timeout):
        status = "failed" if entry["lab"] == "stage01" else "passed"
        return {"lab": entry["lab"], "lang": entry["lang"], "status": status, "error": "boom"}

    monkeypatch.setattr(verifier, "execute_notebook", flaky)
    monkeypatch.setattr(verifier, "compile_once", lambda langs, out: {})
    rc = verifier.main(["--output", str(tmp_path / "onefail"), "--lang", "python"])
    assert rc == 1
    summary = json.loads((tmp_path / "onefail" / "coverage.json").read_text(encoding="utf-8"))
    assert summary["failed"] == 1
    assert summary["coverage"]["complete"] is True, "coverage was complete; an entry still failed"


def test_verifier_never_tolerates_errors():
    source = (ROOT / "tools/verify_language_notebooks.py").read_text(encoding="utf-8")
    assert "allow_errors=False" in source
    assert "allow_errors=True" not in source
    assert "original_notebook_parity\": \"not_certified" in source


def test_compile_once_creates_its_output_directory(tmp_path):
    """compile_once must not depend on its caller having made the directory."""
    verifier = load_verifier()
    target = tmp_path / "build"
    assert not target.exists()
    # No native toolchain needed: an absent directory must not be the failure.
    identities = verifier.compile_once((), target)
    assert identities == {}
    assert target.is_dir()


def test_verifier_compiles_native_once_per_identity():
    source = (ROOT / "tools/verify_language_notebooks.py").read_text(encoding="utf-8")
    assert "def compile_once(" in source
    assert "source_id(lang, ROOT)" in source
    assert "binary_sha256" in source


def test_tree_fingerprint_detects_a_changed_notebook(tmp_path, monkeypatch):
    """A mid-run regeneration must invalidate the sweep rather than mix sources."""
    verifier = load_verifier()
    fake_root = tmp_path / "polyglot"
    (fake_root / "python").mkdir(parents=True)
    labs = json.loads((ROOT / "native/protocols/labs.json").read_text(encoding="utf-8"))["labs"]
    for lab in labs:
        (fake_root / "python" / f"{lab['key']}.ipynb").write_text(
            json.dumps({"lab": lab["key"]}), encoding="utf-8"
        )
    monkeypatch.setattr(verifier, "NB_ROOT", fake_root)

    entries = verifier.expected_entries(("python",))
    before = verifier.tree_fingerprint(entries)
    assert verifier.tree_fingerprint(entries) == before, "fingerprint must be stable"

    target = fake_root / "python" / f"{labs[0]['key']}.ipynb"
    target.write_text(json.dumps({"lab": labs[0]["key"], "changed": True}), encoding="utf-8")
    assert verifier.tree_fingerprint(entries) != before, "a changed notebook must change the hash"


def test_incomplete_tree_fails_coverage(tmp_path, monkeypatch):
    """If the tree changes mid-run, coverage must not be reported complete."""
    verifier = load_verifier()
    calls = {"n": 0}
    real = verifier.tree_fingerprint

    def flaky(entries):
        calls["n"] += 1
        base = real(entries)
        return base if calls["n"] == 1 else base + "-changed"

    monkeypatch.setattr(verifier, "tree_fingerprint", flaky)
    monkeypatch.setattr(
        verifier,
        "execute_notebook",
        lambda entry, out, timeout: {"lab": entry["lab"], "lang": entry["lang"], "status": "passed"},
    )
    monkeypatch.setattr(verifier, "compile_once", lambda langs, out: {})
    rc = verifier.main(["--output", str(tmp_path / "changed"), "--lang", "python"])
    assert rc == 1
    summary = json.loads((tmp_path / "changed" / "coverage.json").read_text(encoding="utf-8"))
    assert summary["notebook_tree"]["unchanged"] is False
    assert summary["coverage"]["complete"] is False
