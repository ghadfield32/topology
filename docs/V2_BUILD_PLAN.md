# Learning System 2.0 — implementation and verification plan

## Design
Preserve the supplied 00–12 progression and all existing original lessons, examples, data, and solutions. Add a beginner-first active-learning layer rather than create another disconnected course. The user's request authorizes this continuation. Work in a new extracted copy; keep the original ZIP unchanged.

## Deliverables
1. Thirteen step-by-step workbooks, one per existing stage; a notation/Python/proof foundation; explicit depth and book-coverage limits.
2. Sixty-five new coding activities (five per stage), each with a specification, hints, reference implementation, visible checks, and explanation. Create thirteen intentionally unfinished learner notebooks and thirteen runnable answer notebooks. Do not count learner stubs as executed solutions.
3. Thirty-nine additional retrieval prompts, three per stage, with answer criteria. Keep original 102 exercise/solution pairs distinct.
4. A local, evidence-based learning log and CLI: record practice, independent assessment, and delayed recall separately. Use an explicit proposed review schedule, not a claim of optimal learning science. Keep learner state unassessed in the distribution.
5. A read-only CSV exploration script with explicit columns, small sample limits, data hashes, units/provenance notes, missing-value rejection, and a clear exploratory-only boundary.
6. A stage hub linking lesson, workbook, worked lab, learner practice, answer notebook, retrieval, and evidence gate. Preserve offline use, no font files or external scripts.
7. Fresh execution reports, source-verification notes, checksums, clean-copy tests, and an updated ZIP.

## Verification before release
- Run the original suite before changing anything; result: 79 passed, 2 optional skips.
- Write tests for learning-state semantics, evidence paths, recall delays, and CSV validation before implementing those functions.
- Execute every reference coding activity and notebook; demonstrate that untouched learner stubs fail honestly.
- Rerun the thirteen original notebooks in fresh kernels.
- Check required stage files, local HTML links, notebook schema, absence of saved errors in worked notebooks, and untouched learner progress.
- Attempt optional Ripser/GUDHI installation; preserve skips if unavailable. No cross-platform claim without execution.
- Re-extract the final candidate and run tests, package checks, and checksum verification there.

## Review focus
False mastery from running code; data leakage from hidden label columns; unsupported claims about real datasets; confusion between finite-diagram checks and general stability; stale execution evidence copied from version 1; silently reclassifying old test data as a new holdout.
