# Consolidation: one source, one required route

## What changed
The previous archive contained seven cumulative `COMPLETE_COURSE_V2` through `V8` Markdown exports plus `COURSE_GUIDE.md`. Later volumes embedded earlier volumes and inherited several competing start instructions. These eight files are now short compatibility pointers. A single current `COMPLETE_COURSE.md` exports each selected source once. The canonical home is `START_HERE.html`.

`curriculum/catalog.json` owns the 31 stage IDs, prerequisite order, primary lesson, primary worked notebook, independent assignment, reference answers and optional repair resources. The primary lessons are all unique paths. Old explanations remain available as optional clarification or retrieval practice, not additional mandatory introductory reading.

## What was not thrown away
Original source lessons, workbooks, exercises, solutions, data cards, notebooks and data have been retained. A paragraph audit compares whitespace-normalized blocks from the retired exports against retained Markdown. Compilation-only passages not matched there are preserved once, with the old filenames and hashes, in `reference/compilation_history_v9.json`. This is a mechanical preservation audit, not a claim that all mathematical statements in historical text are correct.

The reader builds one HTML page per source, rather than recreating the same lesson separately under many release versions. Resolvable old rendered paths become lightweight aliases to those pages. Pages without an unambiguous source remain available to avoid silently deleting a unique interactive exercise. Counts and mappings are in `reports/v9/reader_build.json`.

## What “no double information” means here
There is one required lesson per core stage, one named worked notebook, a separate independent attempt, and an answer reference. Repeating a definition in an optional primer, revisiting an idea during delayed recall, and applying it to another dataset are intentional learning activities. We do not claim zero semantic repetition across every historical source, problem statement, or answer.

The combined reading volume is an optional export of canonical sources, not an extra book that must also be completed. Code remains in inspectable modules and notebooks; notebooks importing those modules are not duplicate implementations.

## Which instructions win
Use `docs/v9/FIRST_SESSION.md` for current setup and `docs/v9/VERIFICATION.md` for current evidence. Older verification reports are historical records. Older CLI scripts remain compatibility tools; `scripts/course.py` is the main entry point. Existing progress files keep their original filenames to preserve continuity.


## Measured consolidation

Eight overlapping cumulative Markdown exports were retired, with 388 unmatched compilation-only passages retained in the historical record. 1321 older generated HTML pages are lightweight compatibility aliases. The exact required route contains 31 unique primary lesson paths. The original interactive square explorer and historical browser progress widget remain available rather than being replaced by prose.
