#!/usr/bin/env python3
"""Separate, individually labelled checks, instead of one blended green light.

Each check is a distinct claim with its own scope, so a pass in one is never
mistaken for a pass in another:

    contracts    generator freshness + notebook contracts + verifier contracts
    python       the current Python test suite, with skip reasons collected
    readers      native data decoders against the independent Python oracle
    native       native algorithm suites (Go and Rust unit tests)
    science      selected independent scientific oracles (NumPy/PyTorch)
    notebooks    the generated workbook runtime sweep (delegated, opt-in)

Deliberately NOT claimed here: original-133-notebook parity. See
`native/COVERAGE.md`; `native_course.py verify --require-original-parity`
refuses that claim on purpose.

Usage:
    python tools/check_matrix.py --list
    python tools/check_matrix.py --only contracts
    python tools/check_matrix.py --only python,readers,native
    python tools/check_matrix.py --only notebooks --output my_work/check_matrix01
"""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

CHECKS = {
    "contracts": {
        "scope": "generator freshness, notebook contracts, verifier contracts (fast, no native run)",
        "argv": [
            sys.executable, "-m", "pytest", "-q", "-ra",
            "tests/test_language_notebooks.py", "tests/test_notebook_verifier.py",
        ],
    },
    "python": {
        "scope": "current Python test suite with skip reasons",
        "argv": [sys.executable, "-m", "pytest", "-q", "-ra"],
    },
    "readers": {
        "scope": "native data decoders vs the independent Python oracle",
        "native": ["data", "verify", "--lang", "all", "--output", "__OUT__"],
    },
    "native": {
        "scope": "native algorithm suites: Go and Rust unit tests",
        "native": ["test", "--lang", "all", "--output", "__OUT__"],
    },
    "science": {
        "scope": "selected independent NumPy/topology/PyTorch oracles",
        "native": ["verify", "--science", "--output", "__OUT__"],
    },
    "notebooks": {
        "scope": "generated workbook runtime sweep (all 171, fresh kernels, serial)",
        "script": "tools/verify_language_notebooks.py",
    },
}

FAST = ("contracts",)

# What each check explicitly does NOT establish.
NOT_CLAIMED = [
    "original 133-notebook native parity (NOT certified; see native/COVERAGE.md)",
    "Docker/OCI image build and runtime acceptance",
    "live Kubernetes cluster admission, scheduling or completed Job",
    "macOS, GPU or remote CI execution",
    "learner mastery or assessment of any kind",
]


def run_check(name: str, out_root: Path) -> dict:
    spec = CHECKS[name]
    started = time.perf_counter()
    if "script" in spec:
        argv = [sys.executable, str(ROOT / spec["script"]),
                "--output", str(out_root / name)]
    elif "native" in spec:
        argv = [sys.executable, str(ROOT / "native_course.py")]
        for token in spec["native"]:
            argv.append(str(out_root / name / "evidence") if token == "__OUT__" else token)
    else:
        argv = spec["argv"]

    # Exit codes are checked explicitly; do not rely on shell error preference.
    proc = subprocess.run(argv, cwd=ROOT, capture_output=True, text=True)
    record = {
        "check": name,
        "scope": spec["scope"],
        "argv": argv,
        "exit_code": proc.returncode,
        "status": "passed" if proc.returncode == 0 else "failed",
        "seconds": round(time.perf_counter() - started, 2),
        "stdout_tail": proc.stdout[-4000:],
        "stderr_tail": proc.stderr[-4000:],
    }
    if name == "python":
        skips = [
            line.strip()
            for line in proc.stdout.splitlines()
            if line.startswith("SKIPPED")
        ]
        record["skips"] = skips
        record["skip_count"] = len(skips)
    return record


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--only", default="", help="comma-separated check names")
    parser.add_argument("--fast", action="store_true", help="run only fast contracts")
    parser.add_argument("--list", action="store_true")
    parser.add_argument("--output", type=Path, help="output directory (needed by native/notebook checks)")
    args = parser.parse_args(argv)

    if args.list:
        for name, spec in CHECKS.items():
            print(f"{name:10s} {spec['scope']}")
        print()
        print("Explicitly NOT claimed by any check:")
        for item in NOT_CLAIMED:
            print("  - " + item)
        return 0

    names = list(FAST) if args.fast else (
        [n.strip() for n in args.only.split(",") if n.strip()] or list(CHECKS)
    )
    unknown = [n for n in names if n not in CHECKS]
    if unknown:
        print(f"Unknown checks: {unknown}", file=sys.stderr)
        return 2

    out_root = Path(args.output).resolve() if args.output else (ROOT / "my_work" / "check_matrix")
    if any("native" in CHECKS[n] or "script" in CHECKS[n] for n in names):
        if not args.output:
            print("--output is required for native/notebook checks", file=sys.stderr)
            return 2
        if out_root.exists():
            print(f"Choose a NEW output directory: {out_root}", file=sys.stderr)
            return 2
    out_root.mkdir(parents=True, exist_ok=True)

    records = [run_check(name, out_root) for name in names]
    summary = {
        "scope": "separate labelled checks; a pass here is not a deployment or parity claim",
        "checks": records,
        "not_claimed": NOT_CLAIMED,
        "original_notebook_parity": "not_certified",
        "passed": sum(1 for r in records if r["status"] == "passed"),
        "failed": sum(1 for r in records if r["status"] == "failed"),
    }
    (out_root / "check_matrix.json").write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")

    print()
    for record in records:
        extra = f"  skips={record.get('skip_count')}" if "skip_count" in record else ""
        print(f"{record['status']:6s} {record['check']:10s} exit={record['exit_code']} {record['seconds']}s{extra}")
    print()
    print("NOT claimed by these checks:")
    for item in NOT_CLAIMED:
        print("  - " + item)
    print()
    print("evidence:", out_root / "check_matrix.json")
    return 0 if summary["failed"] == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
