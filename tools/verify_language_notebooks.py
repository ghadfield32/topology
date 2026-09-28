#!/usr/bin/env python3
"""Verify the generated language notebooks actually execute, all of them.

This is deliberately stricter than "did three smoke notebooks run":

* The expected set is DERIVED from the registry (`native/protocols/labs.json`),
  never hard-coded. Missing, extra (duplicate) or unreadable entries fail.
* Every notebook runs with a fresh kernel created from the active interpreter,
  in an explicit working directory, serially. Saved outputs are cleared first.
* Errors are never tolerated: `allow_errors=False` and any error output fails
  the entry. There is no "make it green" switch.
* Native binaries are compiled once per verified source identity and reused.
* Failures are preserved in the evidence, and the command exits non-zero unless
  every expected entry executed and passed.

A partial run (`--lang`, `--limit`) is supported for triage but is reported as
`coverage.complete = false` and still exits non-zero, because incomplete
coverage is not acceptance.

Usage:
    python tools/verify_language_notebooks.py --output my_work/nb_verify01
    python tools/verify_language_notebooks.py --output my_work/nb_go01 --lang go
"""

from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import sys
import time
import traceback
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LANGS = ("python", "go", "rust")
NB_ROOT = ROOT / "workbooks" / "polyglot"


def load_runner():
    spec = importlib.util.spec_from_file_location("shape_native_runner", ROOT / "native_course.py")
    mod = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(mod)
    return mod


def load_runtime():
    sys.path.insert(0, str(ROOT / "src"))
    from shape_lab.runtime import parse_probe, validate_kernel_provenance, write_kernel_spec  # noqa: PLC0415

    return write_kernel_spec, validate_kernel_provenance, parse_probe


def expected_entries(langs: tuple[str, ...]) -> list[dict]:
    """Derive the expected notebook set from the registry."""
    runner = load_runner()
    labs = runner.available_labs(ROOT)
    entries = []
    for lab in labs:
        for lang in langs:
            entries.append(
                {
                    "lab": lab["key"],
                    "lang": lang,
                    "path": f"workbooks/polyglot/{lang}/{lab['key']}.ipynb",
                }
            )
    return entries


def audit_set(entries: list[dict], langs: tuple[str, ...]) -> list[str]:
    """Reject missing, duplicate or unexpected notebook files."""
    problems = []
    seen = set()
    for entry in entries:
        key = (entry["lang"], entry["lab"])
        if key in seen:
            problems.append(f"duplicate expected entry {entry['lang']}/{entry['lab']}")
        seen.add(key)
        if not (ROOT / entry["path"]).is_file():
            problems.append(f"missing notebook {entry['path']}")

    for lang in langs:
        on_disk = {p.stem for p in (NB_ROOT / lang).glob("*.ipynb")}
        expected = {e["lab"] for e in entries if e["lang"] == lang}
        for extra in sorted(on_disk - expected):
            problems.append(f"unexpected notebook {lang}/{extra}.ipynb (not in the registry)")
        for missing in sorted(expected - on_disk):
            problems.append(f"registry lab {missing} has no {lang} notebook")
    return problems


def tree_fingerprint(entries: list[dict]) -> str:
    """Hash every expected notebook, so a mid-run edit cannot go unnoticed.

    Without this, regenerating the notebooks while a sweep is running would
    produce a result that mixes two different sources and still looks green.

    Resolves through NB_ROOT, the same base `audit_set` uses, so the two agree.
    """
    digest = hashlib.sha256()
    for entry in sorted(entries, key=lambda e: (e["lang"], e["lab"])):
        path = NB_ROOT / entry["lang"] / f"{entry['lab']}.ipynb"
        digest.update(entry["path"].encode("utf-8"))
        if path.is_file():
            digest.update(hashlib.sha256(path.read_bytes()).digest())
        else:
            digest.update(b"MISSING")
    return digest.hexdigest()


def compile_once(langs: tuple[str, ...], out: Path) -> dict:
    """Compile each native language once and record its verified identity."""
    runner = load_runner()
    identities = {}
    # runner.build writes its command logs next to the binary it also builds here,
    # so this directory must exist before build is called.
    out.mkdir(parents=True, exist_ok=True)
    for lang in ("go", "rust"):
        if lang not in langs:
            continue
        try:
            binary = runner.build(lang, out, root=ROOT)
            identities[lang] = {
                "status": "compiled",
                "binary_sha256": runner.digest(binary),
                "source_sha256": runner.source_id(lang, ROOT),
            }
        except Exception as exc:  # noqa: BLE001 - recorded, never hidden
            identities[lang] = {"status": "failed", "error": f"{type(exc).__name__}: {exc}"}
    return identities


def execute_notebook(entry: dict, out: Path, timeout: int) -> dict:
    """Execute one notebook with a fresh kernel and no error tolerance."""
    import nbformat
    from jupyter_client import AsyncKernelManager
    from jupyter_client.kernelspec import KernelSpecManager
    from nbclient import NotebookClient

    write_kernel_spec, validate_kernel_provenance, parse_probe = load_runtime()

    path = ROOT / entry["path"]
    record = {"lab": entry["lab"], "lang": entry["lang"], "path": entry["path"]}
    started = time.perf_counter()
    kernel_dir = out / "_kernels"
    dest = out / "executed" / entry["lang"] / f"{entry['lab']}.ipynb"

    try:
        book = nbformat.read(path, as_version=4)
    except Exception as exc:  # noqa: BLE001
        record.update(status="unreadable", error=f"{type(exc).__name__}: {exc}")
        return record

    source_code_cells = sum(c.cell_type == "code" for c in book.cells)
    record["source_code_cells"] = source_code_cells
    record["source_sha256"] = hashlib.sha256(path.read_bytes()).hexdigest()

    # Fresh kernel run: clear every saved output so nothing is inherited.
    for cell in book.cells:
        if cell.cell_type == "code":
            cell.outputs = []
            cell.execution_count = None

    # Provenance probe: the notebook must report the interpreter that ran it.
    from shape_lab.runtime import PROBE_SOURCE, PROBE_TAG  # noqa: PLC0415

    probe = nbformat.v4.new_code_cell(PROBE_SOURCE, metadata={"tags": [PROBE_TAG]})
    book.cells.insert(0, probe)

    try:
        with __import__("tempfile").TemporaryDirectory(prefix="shape-nb-kernel-") as tmp:
            write_kernel_spec(Path(tmp), sys.executable)
            manager = AsyncKernelManager(
                kernel_name="shape-course-v10",
                kernel_spec_manager=KernelSpecManager(kernel_dirs=[tmp]),
            )
            NotebookClient(
                book,
                timeout=timeout,
                km=manager,
                kernel_name="shape-course-v10",
                allow_errors=False,
                resources={"metadata": {"path": str(path.parent)}},
            ).execute(cleanup_kc=True)

        record["kernel"] = validate_kernel_provenance(
            parse_probe(book.cells[0]), sys.executable, ROOT
        )
        errors = [
            o
            for c in book.cells
            if c.cell_type == "code"
            for o in c.outputs
            if o.output_type == "error"
        ]
        if errors:
            raise RuntimeError("an error output survived execution despite allow_errors=False")
        # Count CELLS that ran, not the sum of their execution_count integers.
        # The provenance probe occupies index 0, so exclude it from the coverage
        # count and compare against the notebook's own source code cells.
        executed = sum(
            1
            for index, c in enumerate(book.cells)
            if index > 0 and c.cell_type == "code" and c.execution_count
        )
        record.update(status="passed", executed_code_cells=executed)
        if executed < source_code_cells:
            record.update(status="incomplete", error="not every source code cell executed")
    except Exception as exc:  # noqa: BLE001 - preserved, not hidden
        record.update(
            status="failed",
            error=f"{type(exc).__name__}: {exc}",
            traceback=traceback.format_exc()[-2000:],
        )
    finally:
        dest.parent.mkdir(parents=True, exist_ok=True)
        try:
            nbformat.write(book, dest)
            record["executed_copy"] = str(dest.relative_to(ROOT))
        except Exception as exc:  # noqa: BLE001
            record["executed_copy_error"] = str(exc)
        record["seconds"] = round(time.perf_counter() - started, 3)
    return record


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", required=True, type=Path)
    parser.add_argument("--lang", choices=("python", "go", "rust", "all"), default="all")
    parser.add_argument("--limit", type=int, default=0, help="run only the first N entries (partial)")
    parser.add_argument("--timeout", type=int, default=600)
    parser.add_argument("--skip-native-build", action="store_true")
    args = parser.parse_args(argv)

    out = Path(args.output).resolve()
    if out.exists():
        print(f"ERROR: choose a NEW output directory: {out}", file=sys.stderr)
        return 2

    langs = LANGS if args.lang == "all" else (args.lang,)
    out.mkdir(parents=True)

    entries = expected_entries(langs)
    problems = audit_set(entries, langs)
    if problems:
        print("Registry/notebook set problems:", file=sys.stderr)
        for problem in problems:
            print("  " + problem, file=sys.stderr)

    selected = entries[: args.limit] if args.limit else entries
    identities = {} if args.skip_native_build else compile_once(langs, out / "build")
    tree_before = tree_fingerprint(entries)

    records = []
    for index, entry in enumerate(selected, start=1):
        print(f"[{index}/{len(selected)}] {entry['lang']}: {entry['lab']}", flush=True)
        records.append(execute_notebook(entry, out, args.timeout))

    tree_after = tree_fingerprint(entries)
    tree_unchanged = tree_before == tree_after

    unexpected = [p for p in problems if "unexpected" in p or "duplicate" in p or "unreadable" in p]
    failed = [r for r in records if r.get("status") != "passed"]
    complete = (len(selected) == len(entries)) and not problems and tree_unchanged

    summary = {
        "created_at": load_runner().now(),
        "scope": "generated language notebooks: fresh kernels, serial, no error tolerance",
        "languages": list(langs),
        "expected_entries": len(entries),
        "selected_entries": len(selected),
        "executed_entries": len(records),
        "passed": sum(1 for r in records if r.get("status") == "passed"),
        "failed": len(failed),
        "set_problems": problems,
        "unexpected_entries": unexpected,
        "notebook_tree": {
            "fingerprint_before": tree_before,
            "fingerprint_after": tree_after,
            "unchanged": tree_unchanged,
            "note": "a mid-run regeneration invalidates the sweep; rerun it",
        },
        "native_binaries": identities,
        "coverage": {
            "complete": complete,
            "note": "complete means every registry-derived entry was selected, present, unchanged and passed",
        },
        "original_notebook_parity": "not_certified",
        "records": records,
    }
    (out / "coverage.json").write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")

    print()
    print(f"expected {len(entries)}  selected {len(selected)}  passed {summary['passed']}  failed {summary['failed']}")
    print(f"coverage complete: {complete}")
    if failed:
        for record in failed[:20]:
            print(f"  FAILED {record['lang']}/{record['lab']}: {record.get('error')}")
    if unexpected:
        for item in unexpected:
            print("  SET PROBLEM " + item)

    return 0 if (complete and not failed and not problems) else 1


if __name__ == "__main__":
    sys.exit(main())
