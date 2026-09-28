"""Resolve which native run a reader should look at — explicitly, never by guessing.

Problems this solves:

* `my_work/` is private and machine-local. A clean QA checkout has no run at all,
  and a learner's machine may have many. Picking "the newest `execution.json`"
  quietly mixes evidence from different source revisions, binaries and inputs.
* Old evidence is still useful, but only in a clearly labelled review mode.

Usage from a notebook:

    import importlib.util, json
    from pathlib import Path
    spec = importlib.util.spec_from_file_location("evidence", ROOT / "tools/evidence_pointer.py")
    ev = importlib.util.module_from_spec(spec); spec.loader.exec_module(ev)

    found = ev.resolve(ROOT, "stage01", run_dir=..., allow_review=True)

Resolution order:
    1. An explicit run directory (the `run_dir` argument).
    2. `my_work/native_evidence.json`, a small manifest a run writes on request.
    3. Nothing. Returning nothing is a valid, expected result.
"""

from __future__ import annotations

import json
from pathlib import Path

MANIFEST_NAME = "native_evidence.json"
REVIEW_DIR_NAME = "native_evidence_review"


def _read_json(path: Path):
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return None


def run_fingerprint(execution: dict) -> str:
    """The identity a run recorded, or an empty string for legacy evidence."""
    identity = execution.get("identity")
    if not isinstance(identity, dict):
        return ""
    languages = identity.get("languages") or {}
    parts = []
    for lang in sorted(languages):
        entry = languages[lang] or {}
        parts.append(f"{lang}:{entry.get('source_sha256')}:{entry.get('binary_sha256')}")
    parts.append(f"inputs:{identity.get('input_fingerprints_sha256')}")
    parts.append(f"protocol:{identity.get('protocol')}")
    return "|".join(parts)


def describe(run_dir: Path, lab: str) -> dict:
    """Summarise one run directory for a specific lab."""
    execution = _read_json(run_dir / "execution.json") or {}
    results = {}
    for lang in ("go", "rust"):
        path = run_dir / lang / f"{lab}.json"
        payload = _read_json(path)
        if payload is not None:
            results[lang] = payload
    return {
        "run_dir": run_dir,
        "execution": execution,
        "results": results,
        "status": execution.get("status"),
        "created_at": execution.get("created_at"),
        "expected_labs": execution.get("expected_labs") or [],
        "has_identity": bool(run_fingerprint(execution)),
        "fingerprint": run_fingerprint(execution),
        "covers_lab": lab in (execution.get("expected_labs") or []),
    }


def _candidate_from_manifest(root: Path) -> Path | None:
    manifest = _read_json(root / "my_work" / MANIFEST_NAME)
    if not isinstance(manifest, dict):
        return None
    run_dir = manifest.get("run_dir")
    if not run_dir:
        return None
    path = Path(run_dir)
    return path if path.is_absolute() else (root / path)


def _scan(root: Path) -> list[Path]:
    found = []
    for parent in (root / "my_work", root / "native" / "evidence"):
        if not parent.is_dir():
            continue
        found.extend(p.parent for p in parent.rglob("execution.json"))
    return sorted(set(found))


def resolve(root, lab, run_dir=None, allow_review=True):
    """Return a describe() dict, or None when no run is available.

    Never returns an arbitrary "latest" run silently: if only stale (legacy,
    identity-less) runs exist, the result is flagged `review_mode=True` and the
    caller is expected to say so out loud.
    """
    root = Path(root)
    candidates: list[tuple[bool, Path]] = []

    if run_dir is not None:
        candidates.append((True, Path(run_dir)))
    manifest_dir = _candidate_from_manifest(root)
    if manifest_dir is not None:
        candidates.append((True, manifest_dir))

    explicit_found = False
    for explicit, path in candidates:
        if not (path / "execution.json").is_file():
            continue
        described = describe(path, lab)
        if not described["covers_lab"]:
            continue
        explicit_found = True
        described["explicit"] = explicit
        described["review_mode"] = not described["has_identity"]
        described["source"] = "explicit" if explicit else "manifest"
        return described

    if not allow_review:
        return None

    # Nothing explicit. Fall back to a clearly labelled review of older evidence.
    reviewed = []
    for path in _scan(root):
        described = describe(path, lab)
        if described["covers_lab"] and described["results"]:
            described["explicit"] = False
            described["review_mode"] = True
            described["source"] = "review_scan"
            reviewed.append(described)
    if not reviewed:
        return None
    reviewed.sort(key=lambda d: str(d["created_at"] or ""), reverse=True)
    chosen = reviewed[0]
    chosen["other_candidates"] = [str(d["run_dir"]) for d in reviewed[1:]]
    chosen["explicit_found_but_unusable"] = explicit_found
    return chosen


def write_manifest(root, lab, run_dir) -> Path:
    """Point later readers at a specific run for a specific lab."""
    root = Path(root)
    path = root / "my_work" / MANIFEST_NAME
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(
            {
                "lab": lab,
                "run_dir": str(Path(run_dir).resolve()),
                "note": "Written by a notebook or verifier. Delete to return to review mode.",
            },
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )
    return path
