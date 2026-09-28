"""Prove that editing a learner copy changes the program that is evaluated.

The course tells learners to copy `native/go` (or `native/rust`) into a private
folder, change one assumption, and test it. That instruction is only meaningful
if the edit actually changes the compiled program and if a deliberately wrong
implementation actually fails. This module demonstrates both, and confirms the
reference source is left untouched.

Tests-first note: the wrong-implementation assertion was written to fail before
this harness existed; the mutation `b[i][j] |= b[r][j]` (OR instead of XOR) was
first observed to fail `TestRankField` with exit code 1 by hand.
"""
from __future__ import annotations

import hashlib
import json
import os
import shutil
import subprocess
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
GO_REFERENCE = ROOT / "native" / "go" / "engine" / "math.go"

# A deliberate learner error: F2 elimination must XOR rows, not OR them.
WRONG_GO = ("b[i][j] ^= b[r][j]", "b[i][j] |= b[r][j]")
WRONG_RUST = ("b[i][j] ^= b[r][j]", "b[i][j] |= b[r][j]")


def _sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _clean_env() -> dict:
    env = os.environ.copy()
    env["PYTHONUTF8"] = "1"
    env["GOTOOLCHAIN"] = "local"
    env["GOWORK"] = "off"
    return env


def _run(cmd: list[str], cwd: Path, env: dict) -> subprocess.CompletedProcess:
    return subprocess.run(cmd, cwd=cwd, env=env, capture_output=True, text=True, timeout=600)


go_available = shutil.which("go") is not None
cargo_available = shutil.which("cargo") is not None


@pytest.mark.skipif(not go_available, reason="Go toolchain not installed; mutation test needs it")
def test_edited_go_copy_changes_the_compiled_program_and_fails(tmp_path):
    """A wrong learner edit must fail a real native test, not pass silently."""
    assert GO_REFERENCE.is_file(), "reference source must exist"
    reference_before = _sha(GO_REFERENCE)

    private = tmp_path / "learner_go"
    shutil.copytree(ROOT / "native" / "go", private)

    target = private / "engine" / "math.go"
    original = target.read_text(encoding="utf-8")
    assert WRONG_GO[0] in original, "expected the exact F2 XOR line in the reference"
    target.write_text(original.replace(*WRONG_GO), encoding="utf-8")

    env = _clean_env()

    # The package being evaluated must resolve to the PRIVATE copy, not the
    # reference tree. This is what makes "your edit is what gets compiled" true.
    where = _run(["go", "list", "-f", "{{.Dir}}", "./engine"], private, env)
    if where.returncode == 0:
        resolved = Path(where.stdout.strip()).resolve()
        assert resolved == (private / "engine").resolve(), (
            f"Go compiled {resolved}, expected the private copy {private / 'engine'}"
        )

    # Baseline: the untouched reference passes its own tests.
    baseline = _run(["go", "test", "-count=1", "./..."], ROOT / "native" / "go", env)
    assert baseline.returncode == 0, (
        f"reference Go tests must pass before the mutation:\n{baseline.stdout}\n{baseline.stderr}"
    )

    # The edited copy must fail.
    broken = _run(["go", "test", "-count=1", "./..."], private, env)
    assert broken.returncode != 0, (
        "a deliberately wrong learner implementation passed its tests; "
        f"the private copy is not the evaluated program:\n{broken.stdout}"
    )
    combined = broken.stdout + broken.stderr
    assert "FAIL" in combined
    assert "TestRankField" in combined, (
        "the mutation should break the F2 rank test specifically:\n" + combined
    )

    # Repair the private copy and demonstrate a pass again.
    target.write_text(original, encoding="utf-8")
    repaired = _run(["go", "test", "-count=1", "./..."], private, env)
    assert repaired.returncode == 0, (
        f"the repaired learner copy must pass again:\n{repaired.stdout}\n{repaired.stderr}"
    )

    # The reference must be untouched by the learner's private experiment.
    assert _sha(GO_REFERENCE) == reference_before


@pytest.mark.skipif(not go_available, reason="Go toolchain not installed; mutation test needs it")
def test_reference_go_source_differs_from_the_edited_copy(tmp_path):
    """The edit lives only in the private copy, never in the canonical source."""
    private = tmp_path / "learner_go2"
    shutil.copytree(ROOT / "native" / "go", private)
    target = private / "engine" / "math.go"
    target.write_text(
        target.read_text(encoding="utf-8").replace(*WRONG_GO), encoding="utf-8"
    )

    assert target.read_bytes() != GO_REFERENCE.read_bytes()
    assert WRONG_GO[0] in GO_REFERENCE.read_text(encoding="utf-8")
    assert WRONG_GO[1] not in GO_REFERENCE.read_text(encoding="utf-8")


def _rust_can_build(source_dir: Path, tmp_path: Path) -> bool:
    """Rust copy builds only when cargo can reach the vendored sources."""
    vendor = source_dir / "vendor"
    return cargo_available and vendor.is_dir()


@pytest.mark.skipif(
    os.environ.get("SHAPE_TEST_RUST_MUTATION") != "1",
    reason="set SHAPE_TEST_RUST_MUTATION=1 to run the slower Rust mutation build",
)
def test_edited_rust_copy_changes_the_compiled_program_and_fails(tmp_path):
    """The same demonstration for Rust, using the real prepared-copy layout."""
    source = ROOT / "native" / "rust"
    if not _rust_can_build(source, tmp_path):
        pytest.skip("cargo or vendored crates unavailable for offline Rust build")

    reference_math = source / "src" / "math.rs"
    reference_before = _sha(reference_math)

    private = tmp_path / "learner_rust"
    shutil.copytree(source, private, ignore=shutil.ignore_patterns("target"))
    # Point the copy's vendored-source config at the canonical vendor directory.
    # json.dumps produces a correctly quoted TOML string, which matters on Windows
    # where a raw backslash path would be an invalid TOML literal.
    (private / ".cargo").mkdir(exist_ok=True)
    (private / ".cargo" / "config.toml").write_text(
        "[source.crates-io]\nreplace-with = \"vendored-sources\"\n"
        "[source.vendored-sources]\ndirectory = " + json.dumps(str(source / "vendor")) + "\n",
        encoding="utf-8",
    )

    target = private / "src" / "math.rs"
    body = target.read_text(encoding="utf-8")
    if WRONG_RUST[0] not in body:
        pytest.skip("Rust F2 elimination line not found in the expected form")
    target.write_text(body.replace(*WRONG_RUST), encoding="utf-8")

    env = _clean_env()
    env["CARGO_NET_OFFLINE"] = "true"
    env["CARGO_TARGET_DIR"] = str(tmp_path / "target")

    broken = _run(["cargo", "test", "--offline", "--locked"], private, env)
    assert broken.returncode != 0, (
        "a deliberately wrong Rust implementation passed its tests:\n"
        f"{broken.stdout}\n{broken.stderr}"
    )
    assert "FAILED" in broken.stdout + broken.stderr

    # Repair the private copy and demonstrate a pass again.
    target.write_text(body, encoding="utf-8")
    repaired = _run(["cargo", "test", "--offline", "--locked"], private, env)
    assert repaired.returncode == 0, (
        f"the repaired Rust learner copy must pass again:\n{repaired.stdout}\n{repaired.stderr}"
    )

    assert _sha(reference_math) == reference_before
