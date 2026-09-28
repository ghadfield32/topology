"""Contract for the repository layout document.

The layout doc is the map people follow, so its claims must stay true. This
checks that the paths it asserts exist and that the ownership rules it states
match what the code actually enforces.
"""
from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LAYOUT = ROOT / "docs" / "release" / "REPOSITORY_LAYOUT.md"

# Directory families described in prose rather than asserted as one path.
FAMILIES = (
    "native/go/",
    "native/rust/",
    "native/guides/labs/",
    "my_work/",
    "workbooks/polyglot/",
)


def test_layout_doc_exists_and_defines_the_core_paths():
    text = LAYOUT.read_text(encoding="utf-8")
    for token in (
        "curriculum/catalog.json",
        "native/protocols/labs.json",
        "tools/build_language_notebooks.py",
        "workbooks/polyglot",
        "native_course.py",
        "course.py",
        "my_work/",
        "notebooks/",
    ):
        assert token in text, f"layout doc does not define {token}"
    assert "No Go or Rust here" in text, "layout doc must warn about notebooks/"


def test_every_path_the_layout_asserts_really_exists():
    text = LAYOUT.read_text(encoding="utf-8")
    missing = []
    for token in sorted(set(re.findall(r"`([A-Za-z0-9_][A-Za-z0-9_./-]*)`", text))):
        if token in FAMILIES:
            continue
        # Only consider things that look like a repo path.
        if "/" not in token and not token.endswith(
            (".json", ".py", ".md", ".yaml", ".yml", ".html", ".ipynb")
        ):
            continue
        if token.endswith("/"):
            continue
        if not (ROOT / token).exists():
            missing.append(token)
    assert not missing, "layout doc references paths that do not exist:\n  " + "\n  ".join(missing)


def test_layout_ownership_rules_match_the_code():
    """The two single-owner files the doc names must really be the only ones."""
    catalogues = [
        p
        for p in ROOT.rglob("catalog.json")
        if "my_work" not in p.parts and ".venv" not in p.parts
    ]
    assert ROOT / "curriculum/catalog.json" in catalogues
    # workbooks/polyglot must not carry its own catalogue.
    assert not list((ROOT / "workbooks/polyglot").rglob("*.json"))

    labs = json.loads((ROOT / "native/protocols/labs.json").read_text(encoding="utf-8"))
    assert labs["lab_count"] == len(labs["labs"]) == 57
    assert not list((ROOT / "workbooks/polyglot").rglob("labs.json"))


def test_layout_documents_the_reference_vs_copy_distinction():
    text = LAYOUT.read_text(encoding="utf-8")
    assert "your copy" in text
    assert "native_course.py prepare" in text
    assert "read-only" in text
