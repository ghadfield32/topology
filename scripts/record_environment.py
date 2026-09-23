"""Record the actual installed runtime and dependency closure, without network access."""
from __future__ import annotations
from datetime import datetime, timezone
import importlib.metadata as metadata
import json
import platform
from pathlib import Path
import sys
import tomllib

from packaging.markers import default_environment
from packaging.requirements import Requirement
from packaging.utils import canonicalize_name

ROOT = Path(__file__).resolve().parents[1]


def main() -> None:
    cfg = tomllib.loads((ROOT / "pyproject.toml").read_text())
    wanted = cfg["project"]["dependencies"] + cfg["build-system"]["requires"]
    for group in ("notebooks", "test", "reader"):
        wanted += cfg["project"]["optional-dependencies"][group]
    marker_environment = default_environment()
    marker_environment["extra"] = ""
    queue = [Requirement(r).name for r in wanted]
    closure, missing = {}, []
    while queue:
        name = queue.pop()
        normalized = canonicalize_name(name)
        if normalized in closure or normalized in missing:
            continue
        try:
            dist = metadata.distribution(name)
        except metadata.PackageNotFoundError:
            missing.append(normalized)
            continue
        closure[normalized] = dist.version
        for spec in dist.requires or []:
            req = Requirement(spec)
            if req.marker is None or req.marker.evaluate(marker_environment):
                queue.append(req.name)
    record = {
        "recorded_at_utc": datetime.now(timezone.utc).isoformat(),
        "python": sys.version,
        "platform": platform.platform(),
        "machine": platform.machine(),
        "implementation": platform.python_implementation(),
        "direct_roots": wanted,
        "dependency_closure": dict(sorted(closure.items())),
        "missing_dependencies": sorted(missing),
        "optional_packages_not_present": [name for name in ("ripser", "gudhi") if metadata.packages_distributions().get(name) is None],
        "scope": "Installed Linux execution environment; not a portable lockfile or a clean network install. Optional crosscheck packages excluded from tested closure.",
    }
    (ROOT / "reports/environment.json").write_text(json.dumps(record, indent=2) + "\n")
    lines = ["# Actual tested Linux dependency snapshot, not a cross-platform lockfile.", "# Selected root extras: notebooks, test, reader; optional crosscheck excluded.", "# Dependencies were followed using this runtime's active environment markers."]
    lines.extend(f"{name}=={version}" for name, version in sorted(closure.items()))
    lines.extend(f"# MISSING: {name}" for name in missing)
    (ROOT / "reports/tested_dependency_snapshot.txt").write_text("\n".join(lines) + "\n")
    print(f"Recorded {len(closure)} installed distributions; missing: {missing}")


if __name__ == "__main__":
    main()
