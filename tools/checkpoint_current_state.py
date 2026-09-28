"""Record the current environment and inventory as explicit checkpoint evidence.

Writes JSON so later phases can compare against a fixed baseline instead of
trusting an old log. Never overwrites an existing output directory.
"""
from __future__ import annotations

import importlib.util
import json
import platform
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def run(cmd: list[str]) -> dict:
    try:
        p = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
        return {"cmd": cmd, "exit_code": p.returncode, "stdout": p.stdout.strip()[:4000]}
    except (OSError, subprocess.SubprocessError) as exc:
        return {"cmd": cmd, "exit_code": -1, "error": str(exc)}


def git(*args: str) -> str:
    return subprocess.run(["git", *args], cwd=ROOT, capture_output=True, text=True).stdout.strip()


def main(out_dir: Path) -> int:
    if out_dir.exists():
        raise SystemExit(f"Choose a NEW output directory: {out_dir}")
    out_dir.mkdir(parents=True)

    spec = importlib.util.spec_from_file_location("runner", ROOT / "native_course.py")
    runner = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(runner)

    labs = runner.available_labs(ROOT)
    catalog = json.loads((ROOT / "curriculum/catalog.json").read_text(encoding="utf-8"))
    registry = json.loads((ROOT / "native/data_registry.json").read_text(encoding="utf-8"))

    nb = sorted((ROOT / "workbooks/polyglot").rglob("*.ipynb"))

    record = {
        "created_at": runner.now(),
        "git": {
            "branch": git("rev-parse", "--abbrev-ref", "HEAD"),
            "head": git("rev-parse", "HEAD"),
            "origin_main": git("rev-parse", "origin/main"),
            "head_equals_origin_main": git("rev-parse", "HEAD") == git("rev-parse", "origin/main"),
            "dirty_entries": len([x for x in git("status", "--porcelain=v1").splitlines() if x]),
            "status_short": git("status", "--porcelain=v1").splitlines(),
        },
        "environment": {
            "platform": platform.platform(),
            "python": sys.version,
            "python_executable": sys.executable,
            "tools": {
                name: (shutil.which(name) or None)
                for name in ("uv", "go", "cargo", "rustc", "docker", "kubectl", "kind", "rtk")
            },
            "tool_versions": {
                name: run([name, "--version"] if name != "go" else [name, "version"])
                for name in ("go", "cargo", "rustc")
                if shutil.which(name)
            },
        },
        "inventory": {
            "core_stages": len(catalog["stages"]),
            "catalog_release": catalog.get("release"),
            "native_labs": len(labs),
            "native_lab_keys_unique": len({r["key"] for r in labs}),
            "registered_data_files": len(registry["files"]),
            "polyglot_notebooks": len(nb),
            "polyglot_by_language": {
                lang: len(list((ROOT / "workbooks/polyglot" / lang).glob("*.ipynb")))
                for lang in ("python", "go", "rust")
            },
        },
        "note": "Prior reported results (774 tests, 171 notebooks, stage01-only execution) "
                "are NOT re-asserted here; this file records the current environment only.",
    }
    (out_dir / "checkpoint.json").write_text(json.dumps(record, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({k: v for k, v in record.items() if k != "git"}, indent=2)[:2000])
    print("wrote", out_dir / "checkpoint.json")
    return 0


if __name__ == "__main__":
    target = Path(sys.argv[1]) if len(sys.argv) > 1 else ROOT / "my_work/checkpoint01"
    sys.exit(main(target))
