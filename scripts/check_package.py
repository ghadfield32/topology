"""Check the course's self-contained release structure; no network or browser needed."""
from __future__ import annotations
from html.parser import HTMLParser
import json
from pathlib import Path
from urllib.parse import unquote, urlsplit

import nbformat

ROOT = Path(__file__).resolve().parents[1]

class Links(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.targets: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        for name, value in attrs:
            if name in ("href", "src") and value:
                self.targets.append(value)


def main() -> None:
    all_html = [ROOT / "START_HERE.html", *sorted((ROOT / "site").rglob("*.html"))]
    missing, local_links, external_links = [], 0, 0
    for page in all_html:
        parser = Links()
        parser.feed(page.read_text(encoding="utf-8"))
        for target in parser.targets:
            parsed = urlsplit(target)
            if parsed.scheme or parsed.netloc:
                if parsed.scheme not in ("data", "blob"):
                    external_links += 1
                continue
            if not parsed.path:
                continue
            local_links += 1
            resolved = (page.parent / unquote(parsed.path)).resolve()
            if not resolved.is_relative_to(ROOT) or not resolved.exists():
                missing.append({"page": str(page.relative_to(ROOT)), "target": target})
    if missing:
        raise AssertionError(f"Broken local targets: {missing}")
    metadata = json.loads((ROOT / "docs/stage_metadata.json").read_text())
    assert len(metadata) == 13
    cells = 0
    for s in metadata:
        n = s["n"]
        assert len(s["exercises"]) == len(s["solutions"])
        for relative in [f"lessons/{n:02d}_lesson.md", f"solutions/{n:02d}_solutions.md", f"notebooks/{n:02d}_lab.ipynb", f"site/stages/{n:02d}.html", f"site/notebooks/{n:02d}.html", f"site/solutions/{n:02d}.html"]:
            assert (ROOT / relative).is_file(), relative
        assert (ROOT / f"reports/stage_{n:02d}").is_dir()
        nb = nbformat.read(ROOT / f"notebooks/{n:02d}_lab.ipynb", as_version=4)
        nbformat.validate(nb)
        for cell in nb.cells:
            if cell.cell_type == "code":
                cells += 1
                assert cell.get("execution_count") is not None
                assert not any(output.output_type == "error" for output in cell.get("outputs", []))
    forbidden_fonts = [str(p.relative_to(ROOT)) for p in ROOT.rglob("*") if p.suffix.lower() in (".ttf", ".otf", ".woff", ".woff2")]
    assert not forbidden_fonts
    result = {"status": "PASSED", "html_pages": len(all_html), "existing_local_link_targets_checked": local_links, "external_links_not_retested": external_links, "stages_checked": len(metadata), "executed_notebook_code_cells": cells, "exercise_solution_pairs": sum(len(s["exercises"]) for s in metadata), "broken_local_links": missing, "font_files": forbidden_fonts}
    (ROOT / "reports/package_checks.json").write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
