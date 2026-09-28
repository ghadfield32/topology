"""Contracts for the generated Python/Go/Rust learning notebooks.

These tests enforce that the notebook tree stays complete, executable-in-shape,
faithful to a fresh generation, and free of the failure mode this project keeps
warning about: quietly computing a "native" result in Python instead of running
the native program.
"""
from __future__ import annotations

import ast
import importlib.util
import json
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
NB_ROOT = ROOT / "workbooks" / "polyglot"
LABS = json.loads((ROOT / "native/protocols/labs.json").read_text(encoding="utf-8"))["labs"]
KEYS = [lab["key"] for lab in LABS]


def load_generator():
    spec = importlib.util.spec_from_file_location(
        "shape_language_notebooks", ROOT / "tools/build_language_notebooks.py"
    )
    mod = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(mod)
    return mod


def read_nb(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def code_sources(nb: dict) -> list[str]:
    return ["".join(c["source"]) for c in nb["cells"] if c["cell_type"] == "code"]


def test_exactly_three_languages_for_every_lab():
    assert len(KEYS) == len(set(KEYS)) == 57
    for lang in ("python", "go", "rust"):
        found = {p.stem for p in (NB_ROOT / lang).glob("*.ipynb")}
        assert found == set(KEYS), f"{lang} notebooks do not match the 57 lab keys"
    total = sum(len(list((NB_ROOT / lang).glob("*.ipynb"))) for lang in ("python", "go", "rust"))
    assert total == 171


def test_every_notebook_is_valid_nbformat_and_all_code_parses():
    for path in sorted(NB_ROOT.rglob("*.ipynb")):
        nb = read_nb(path)
        assert nb["nbformat"] == 4, path
        assert nb["metadata"]["kernelspec"]["name"] == "python3", path
        assert nb["cells"], path
        for index, source in enumerate(code_sources(nb)):
            try:
                ast.parse(source)
            except SyntaxError as exc:  # pragma: no cover - failure path
                pytest.fail(f"{path} code cell {index} does not parse: {exc}")


def test_committed_tree_matches_a_fresh_generation(tmp_path):
    gen = load_generator()
    gen.main(tmp_path)
    fresh = {
        p.relative_to(tmp_path).as_posix(): p.read_bytes()
        for p in tmp_path.rglob("*")
        if p.is_file()
    }
    committed = {
        p.relative_to(NB_ROOT).as_posix(): p.read_bytes()
        for p in NB_ROOT.rglob("*")
        if p.is_file()
    }
    assert set(fresh) == set(committed), "notebook tree is stale; re-run tools/build_language_notebooks.py"
    differing = [name for name in fresh if fresh[name] != committed[name]]
    assert not differing, f"these notebooks are stale: {differing[:10]}"


def test_go_and_rust_notebooks_do_not_compute_the_lab_in_python():
    """A native notebook must launch the native binary, not re-derive the science."""
    forbidden = ("import numpy", "import torch", "import scipy", "import sklearn")
    for lang in ("go", "rust"):
        for path in sorted((NB_ROOT / lang).glob("*.ipynb")):
            blob = "\n".join(code_sources(read_nb(path)))
            assert "runner.build(" in blob, f"{path} never builds the native program"
            assert "runner.execute_lab(" in blob, f"{path} never runs the native lab"
            for bad in forbidden:
                assert bad not in blob, f"{path} delegates science to Python via {bad!r}"


def test_python_notebooks_read_real_inputs_and_real_evidence():
    for path in sorted((NB_ROOT / "python").glob("*.ipynb")):
        blob = "\n".join(code_sources(read_nb(path)))
        assert "REGISTERED" in blob
        assert "evidence.resolve(" in blob
        assert "runner.compare_values(" in blob
        # Evidence must be resolved explicitly, never by "newest file wins".
        assert "find_latest_native_result" not in blob
        assert "allow_review=False" in blob


def test_python_notebooks_offer_explicit_fresh_and_review_modes():
    """Phase C: two explicit modes, and review mode requires an explicit path."""
    for path in sorted((NB_ROOT / "python").glob("*.ipynb")):
        blob = "\n".join(code_sources(read_nb(path)))
        assert 'MODE = "fresh"' in blob, f"{path} must default to fresh execution"
        assert "MODE not in (\"fresh\", \"review\")" in blob
        assert "PINNED_RUN" in blob, f"{path} must require an explicit pinned run in review mode"
        # Fresh mode must actually create the evidence, not just look for it.
        assert "runner.run_labs(" in blob, f"{path} fresh mode must execute the native labs"
        assert "allow_review=False" in blob, f"{path} must refuse review scanning for its comparison"


def test_evidence_pointer_refuses_a_clean_checkout_and_labels_review_evidence(tmp_path):
    """A clean QA worktree has no run, so strict resolution must return nothing."""
    spec = importlib.util.spec_from_file_location(
        "shape_evidence", ROOT / "tools/evidence_pointer.py"
    )
    ev = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(ev)

    empty = tmp_path / "clean_checkout"
    (empty / "my_work").mkdir(parents=True)
    assert ev.resolve(empty, "stage01", allow_review=False) is None
    assert ev.resolve(empty, "stage01", allow_review=True) is None

    # Legacy evidence with no identity must be reported as review mode.
    run = empty / "my_work" / "old_run"
    (run / "go").mkdir(parents=True)
    (run / "execution.json").write_text(
        json.dumps({"status": "passed", "expected_labs": ["stage01"], "created_at": "2020-01-01T00:00:00Z"}),
        encoding="utf-8",
    )
    (run / "go" / "stage01.json").write_text(json.dumps({"metrics": {"a": 1}}), encoding="utf-8")
    strict = ev.resolve(empty, "stage01", allow_review=False)
    assert strict is None, "identity-less evidence must not satisfy strict resolution"
    reviewed = ev.resolve(empty, "stage01", allow_review=True)
    assert reviewed is not None and reviewed["review_mode"] is True
    assert reviewed["has_identity"] is False


def test_evidence_pointer_prefers_an_explicit_run(tmp_path):
    spec = importlib.util.spec_from_file_location(
        "shape_evidence2", ROOT / "tools/evidence_pointer.py"
    )
    ev = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(ev)

    root = tmp_path / "repo"
    run = root / "my_work" / "run01"
    (run / "go").mkdir(parents=True)
    (run / "execution.json").write_text(
        json.dumps(
            {
                "status": "passed",
                "expected_labs": ["stage01"],
                "created_at": "2026-01-01T00:00:00Z",
                "identity": {
                    "protocol": "native16",
                    "languages": {"go": {"source_sha256": "s", "binary_sha256": "b"}},
                    "input_fingerprints_sha256": "i",
                },
            }
        ),
        encoding="utf-8",
    )
    (run / "go" / "stage01.json").write_text(json.dumps({"metrics": {"a": 1}}), encoding="utf-8")

    found = ev.resolve(root, "stage01", run_dir=run, allow_review=False)
    assert found is not None
    assert found["explicit"] is True
    assert found["review_mode"] is False
    assert found["has_identity"] is True
    assert found["fingerprint"]
    assert found["results"]["go"]["metrics"] == {"a": 1}


def test_notebooks_keep_the_lab_identity_and_boundaries():
    for lab in LABS:
        for lang in ("python", "go", "rust"):
            path = NB_ROOT / lang / f"{lab['key']}.ipynb"
            blob = "\n".join(code_sources(read_nb(path)))
            assert repr(lab["key"]) in blob, f"{path} lost its lab key"
            assert lab["original_scope_gaps"] in blob, f"{path} dropped the scope boundary"
    for lang in ("go", "rust"):
        blob = "\n".join(code_sources(read_nb(NB_ROOT / lang / "stage01.ipynb")))
        assert "native/guides/LEARNING_PATHS.md" in blob


def test_each_language_folder_is_self_guiding():
    """A user opening workbooks/polyglot/<lang>/ must be able to orient there."""
    for lang in ("python", "go", "rust"):
        readme = NB_ROOT / lang / "README.md"
        assert readme.is_file(), f"{lang}/ has no README; the folder is not self-guiding"
        text = readme.read_text(encoding="utf-8")
        assert "../index.html" in text, f"{lang}/README.md does not link back to the index"
        assert "../../native/" in text, f"{lang}/README.md does not point at the native source"
        assert "unassessed" in text.lower()
        if lang != "python":
            # The reference-vs-your-copy distinction is the thing people get wrong.
            assert "native_course.py prepare" in text, (
                f"{lang}/README.md must show how to make an editable private copy"
            )
            assert "my_work/" in text
            assert "reference" in text.lower()
            assert "editable copy" in text.lower()


def test_index_explains_where_go_and_rust_live():
    """The index must pre-empt the 'notebooks/ has no go or rust folder' confusion."""
    text = (NB_ROOT / "README.md").read_text(encoding="utf-8")
    assert "notebooks/" in text
    assert "no `go` or `rust` folder" in text
    for lang in ("python", "go", "rust"):
        assert f"workbooks/polyglot/{lang}/" in text
    assert "native/go/" in text and "native/rust/" in text
    assert "reference source" in text


def test_index_lists_every_lab_and_states_the_total():
    text = (NB_ROOT / "README.md").read_text(encoding="utf-8")
    for key in KEYS:
        assert f"python/{key}.ipynb" in text
        assert f"go/{key}.ipynb" in text
        assert f"rust/{key}.ipynb" in text
    assert "57 labs × 3 languages = 171 notebooks" in text


def test_notebooks_are_not_treated_as_a_second_curriculum():
    """The canonical catalogue must remain the single owner of the 31 stages."""
    catalog = json.loads((ROOT / "curriculum/catalog.json").read_text(encoding="utf-8"))
    assert len(catalog["stages"]) == 31
    assert not (NB_ROOT / "catalog.json").exists()
    guide = (NB_ROOT / "README.md").read_text(encoding="utf-8")
    assert "unassessed" in guide.lower()
    assert "second mandatory curriculum" in guide.lower()


def test_reference_kind_distinguishes_notebooks_from_scripts():
    gen = load_generator()
    by_key = {lab["key"]: lab for lab in LABS}
    assert gen.reference_kind(by_key["stage01"]) == "notebook"
    assert gen.reference_kind(by_key["poux_bridge"]) == "script"
    assert gen.reference_kind({"key": "x", "reference": "a/b.txt"}) == "other"


def test_generator_check_mode_passes_on_the_committed_tree():
    gen = load_generator()
    assert gen.check() == 0


def test_generator_check_mode_detects_a_stale_file(tmp_path):
    """--check must be able to fail, or it is not a check."""
    gen = load_generator()
    gen.main(tmp_path)
    assert gen.check(tmp_path) == 0

    target = tmp_path / "README.md"
    target.write_text(target.read_text(encoding="utf-8") + "\nstale\n", encoding="utf-8")
    assert gen.check(tmp_path) == 1, "a modified artifact must be reported stale"

    # restoring it makes the check pass again
    gen.main(tmp_path)
    assert gen.check(tmp_path) == 0


def test_generator_check_mode_detects_missing_and_unexpected(tmp_path):
    gen = load_generator()
    gen.main(tmp_path)
    (tmp_path / "go" / "stage01.ipynb").unlink()
    (tmp_path / "go" / "not_a_lab.ipynb").write_text("{}", encoding="utf-8")
    assert gen.check(tmp_path) == 1


def test_generator_renders_every_artifact_without_touching_disk(tmp_path):
    """render() is the single source of output and must be side-effect free."""
    gen = load_generator()
    files = gen.render(LABS)
    # 57 labs x 3 languages, plus the root index pair and one README per language.
    assert len(files) == 171 + 2 + 3
    assert not any(tmp_path.iterdir()), "render must not write to disk"
    for rel, content in files.items():
        assert content.endswith("\n"), rel
        json.loads(content) if rel.endswith(".ipynb") else None


def test_every_python_notebook_offers_canonical_reference_execution():
    """The Python route must run the ORIGINAL experiment, in its real form."""
    gen = load_generator()
    for lab in LABS:
        blob = "\n".join(code_sources(read_nb(NB_ROOT / "python" / f"{lab['key']}.ipynb")))
        assert repr(lab["reference"]) in blob, f"{lab['key']} lost its reference path"
        if gen.reference_kind(lab) == "notebook":
            assert "run_references" in blob, f"{lab['key']} never executes its reference"
            assert 'jobs=1' in blob, f"{lab['key']} must run serially by default"
        else:
            # A script reference must be handled explicitly, never run as a notebook.
            assert "run_references" not in blob, f"{lab['key']} treats a script as a notebook"
            assert "not a notebook" in blob.lower(), f"{lab['key']} must say it is not a notebook"


def test_python_notebooks_label_audit_sections_accurately():
    """Input/output audit sections must not read as a re-implementation."""
    for lab in LABS:
        blobs = read_nb(NB_ROOT / "python" / f"{lab['key']}.ipynb")
        markdown = "\n".join(
            "".join(c["source"]) for c in blobs["cells"] if c["cell_type"] == "markdown"
        )
        assert "input audit" in markdown, f"{lab['key']} missing labelled input audit"
        assert "output audit" in markdown, f"{lab['key']} missing labelled output audit"
        assert "Run the canonical Python experiment" in markdown, lab["key"]


def test_go_and_rust_notebooks_do_not_present_a_canonical_python_run():
    """Native notebooks must not silently re-run the original Python experiment."""
    for lang in ("go", "rust"):
        for path in sorted((NB_ROOT / lang).glob("*.ipynb")):
            blob = "\n".join(code_sources(read_nb(path)))
            assert "run_references" not in blob, f"{path} runs the Python reference"
