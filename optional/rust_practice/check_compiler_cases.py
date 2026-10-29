#!/usr/bin/env python3
"""Check the compiler cases against the real toolchain, and refuse to fake a result.

A missing compiler, a failed link, or a rejection with the wrong diagnostic is `failed` or
`blocked` — never a pass. The distinction matters: "nothing happened" is not "the borrow
checker rejected it".

    python check_compiler_cases.py --output my_work/compiler01

The outcome is recorded in `summary.json` next to the captured diagnostics. Reruns must use
a new output directory, so an earlier record is never replaced.
"""
from __future__ import annotations

import argparse
import json
import re
import shutil
import subprocess
import sys
from pathlib import Path

CRATE = Path(__file__).resolve().parent
CASES = CRATE / "compiler_cases" / "cases.json"
DIAGNOSTIC = re.compile(r"error\[E(\d{4})\]")
LINK_FAILURE = ("LNK", "linker", "link.exe", "cannot find -l")


def pinned_toolchain() -> str:
    """Read `channel` from rust-toolchain.toml without needing a TOML parser."""
    manifest = CRATE / "rust-toolchain.toml"
    if not manifest.is_file():
        return ""
    for line in manifest.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if line.startswith("channel") and "=" in line:
            return line.split("=", 1)[1].strip().strip('"').strip("'")
    return ""


def resolve_rustc(toolchain: str) -> list[str]:
    """Prefer the project's pinned toolchain, exactly as Cargo would select it.

    A bare `rustc` on PATH can be a different release; compiling the cases with an
    undeclared compiler would make the record describe the wrong toolchain.
    """
    rustup = shutil.which("rustup")
    if toolchain and rustup:
        probe = subprocess.run(
            [rustup, "run", toolchain, "rustc", "-Vv"],
            capture_output=True,
            text=True,
            timeout=120,
        )
        if probe.returncode == 0:
            return [rustup, "run", toolchain, "rustc"]
    rustc = shutil.which("rustc")
    return [rustc] if rustc else []



def new_directory(path: Path) -> Path:
    path = Path(path)
    if path.exists():
        raise FileExistsError(
            f"{path} already exists; use a new output directory for a new run"
        )
    path.mkdir(parents=True)
    return path


def judge(case: dict, returncode: int, output: str, compiler: str) -> dict:
    """Decide one case. Any ambiguity is a failure, not a benefit of the doubt."""
    record = {
        "file": case.get("file", ""),
        "expect": case["expect"],
        "returncode": returncode,
        "compiler": compiler,
    }
    if not compiler:
        record["status"] = "blocked"
        record["reason"] = "no compiler version was recorded"
        return record

    codes = [f"E{m}" for m in DIAGNOSTIC.findall(output)]
    record["diagnostic_codes"] = codes
    linked_badly = any(marker in output for marker in LINK_FAILURE)

    if case["expect"] == "accept":
        if returncode == 0:
            record["status"] = "passed"
            record["reason"] = "compiled as predicted"
        else:
            record["status"] = "failed"
            record["reason"] = (
                "a missing linker or toolchain is not an expected learning outcome"
                if linked_badly
                else "the accepted example did not compile"
            )
        return record

    expected = case["error_code"]
    if returncode == 0:
        record["status"] = "failed"
        record["reason"] = "the example compiled, so the predicted rejection did not happen"
    elif linked_badly and expected not in codes:
        record["status"] = "failed"
        record["reason"] = "linking failed before the borrow checker reported anything"
    elif expected not in codes:
        record["status"] = "failed"
        record["reason"] = f"expected {expected}, observed {codes or 'no coded diagnostic'}"
    else:
        record["status"] = "passed"
        record["reason"] = f"rejected with {expected} as predicted"
    return record


def compiler_versions() -> tuple[str, str, str, list[str]]:
    toolchain = pinned_toolchain()
    command = resolve_rustc(toolchain)
    rustc = shutil.which("rustc")
    cargo = shutil.which("cargo")
    version = ""
    if command:
        done = subprocess.run(
            [*command, "-Vv"], capture_output=True, text=True, timeout=120
        )
        if done.returncode == 0:
            version = done.stdout.splitlines()[0].strip() if done.stdout else ""
    return version, (cargo or ""), toolchain, command


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", required=True, type=Path)
    parser.add_argument(
        "--cases", type=Path, default=CASES, help="case definitions to run"
    )
    args = parser.parse_args(argv)

    out = new_directory(args.output)
    spec = json.loads(args.cases.read_text(encoding="utf-8"))
    compiler, cargo, toolchain, rustc_command = compiler_versions()

    records: list[dict] = []
    status = "passed"
    reason = ""

    if not rustc_command:
        status = "blocked"
        reason = (
            "no rustc on PATH; install the pinned toolchain with "
            "`rustup toolchain install 1.90.0`. A missing compiler is not an expected "
            "learning outcome."
        )
        records = [
            {
                "file": case["file"],
                "expect": case["expect"],
                "status": "blocked",
                "reason": reason,
            }
            for case in spec["cases"]
        ]
    else:
        if toolchain and toolchain not in compiler:
            status = "failed"
            reason = (
                f"rust-toolchain.toml requests {toolchain} but the selected compiler is "
                f"{compiler or 'unknown'}; the record would describe the wrong toolchain"
            )
        for case in spec["cases"]:
            source = CRATE / case["file"]
            if not source.is_file():
                records.append(
                    {
                        "file": case["file"],
                        "expect": case["expect"],
                        "status": "failed",
                        "reason": "case source is missing",
                    }
                )
                continue
            binary = out / (source.stem + (".exe" if sys.platform == "win32" else ""))
            done = subprocess.run(
                [
                    *rustc_command,
                    "--edition",
                    spec["edition"],
                    "--crate-type",
                    "bin",
                    "-o",
                    str(binary),
                    str(source),
                ],
                capture_output=True,
                text=True,
                timeout=300,
            )
            combined = (done.stdout or "") + (done.stderr or "")
            (out / (source.stem + ".log")).write_text(combined, encoding="utf-8")
            records.append(judge(case, done.returncode, combined, compiler))

    failures = [r for r in records if r["status"] == "failed"]
    blocked = [r for r in records if r["status"] == "blocked"]
    if failures:
        status, reason = "failed", (
            reason or f"{len(failures)} case(s) did not match the prediction"
        )
    elif blocked:
        status = "blocked"
        reason = reason or "no compiler available for at least one case"

    summary = {
        "schema": "shape.rust_practice.compiler_check.v1",
        "status": status,
        "reason": reason,
        "compiler": compiler,
        "toolchain_pin": toolchain,
        "toolchain_honoured": bool(toolchain) and toolchain in compiler,
        "cargo": cargo,
        "edition": spec["edition"],
        "counts": {
            "passed": sum(r["status"] == "passed" for r in records),
            "failed": len(failures),
            "blocked": len(blocked),
        },
        "cases": records,
        "scope": spec["scope"],
        "assessment": "not_assessed",
    }
    (out / "summary.json").write_text(
        json.dumps(summary, indent=2) + "\n", encoding="utf-8"
    )

    print(f"compiler  {compiler or 'not found'}")
    for record in records:
        print(f"{record['status']:<8} {record['file']}: {record.get('reason', '')}")
    print(f"status    {status}")

    return 0 if status == "passed" else 2 if status == "blocked" else 1


if __name__ == "__main__":
    raise SystemExit(main())
