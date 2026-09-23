# Consolidated course design

## Goal
Continue the existing course without introducing another required copy of each explanation. Preserve unique lessons, exercises, measured-data snapshots and their provenance. Give beginners one ordered route with clearly optional remediation, one navigation command and isolated reproducible execution.

## Requirements and decisions
The user explicitly requested implementation, a full ZIP, no repeated required information, cross-industry data including modern sports, and working examples at every stage. We implement within a new extracted workspace and do not change user projects or existing archives.

The canonical catalog owns the 31 core stage IDs, dependencies, lesson, reference lab, learner task, answer and optional repair resources. Existing content remains the source for teaching; old cumulative volumes are retired as navigation aliases. Historical release reports remain history, not current proof of execution.

A runner copies inputs and code into a temporary workspace, starts a fresh kernel, and exports an executed notebook plus experiment outputs to a new destination. It refuses overwrites and destinations inside authored curriculum or code. It reports failures and optional missing packages separately. It never edits learner progress.

A current basketball addition uses the complete small match catalog returned by the official GitHub connector. Reconstruct the exact JSON representation and verify its Git blob hash before use. Full tracking remains an optional source with a manifest and contract checks, not an included video benchmark.

## Verification
First failing existence tests; then catalog uniqueness, local paths, dependency graph, traversal/overwrite protections, reference selection, data hash, identifiers, times, grouping and arithmetic. Re-execute every reference notebook and each stage-entry check. Run the final whole test suite from an extracted archive. Check generated local navigation and browser behavior. Record Linux-only execution, missing optional dependencies, internet restrictions and all failed checks.

## Completion boundary
Software tests cannot certify mathematical mastery, complete-book coverage, unseen-athlete accuracy or universal scientific correctness. Keep formal proof obligations and independent studies visible. No automatic downloads, scheduled work, performance promise or production integration.
