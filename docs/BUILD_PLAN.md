# Learning Lab Implementation Plan

**Goal:** A runnable, evidence-backed beginner learning archive covering the agreed introductory topology/TDA scope.
**Architecture:** Original stage documents and notebooks share an inspectable mathematical Python package. Real datasets are bundled with attribution. Static HTML provides a no-install reading path.
**Tech Stack:** Python, NumPy, SciPy, pandas, matplotlib, scikit-learn, Ripser, GUDHI, nbformat/nbclient, pytest.
**Spec:** DESIGN.md

## Tasks and verification
1. Verify primary course and library references; preserve supplied source outline separately and record corrections transparently.
2. Write mathematical contract tests for chain boundaries, F2 rank, Betti numbers, Rips filtration, persistence, and malformed inputs; observe missing-feature failures before implementation.
3. Implement the educational package and run full unit suite. Compare persistence against both GUDHI and Ripser using matching conventions.
4. Bundle licensed real datasets and validate their hashes, shapes, labels, and official split. Add reproducible data preparation code.
5. Author orientation plus twelve lessons with code, questions, worked solutions, and explicit interpretation limits. Each stage has a distinct real-data experiment.
6. Execute every notebook from a clean kernel. Save plots, numerical reports, execution logs, and read-only rendered outputs.
7. Build the offline reader, coverage map, glossary, progress ledger, final assessment, and capstone extension protocol.
8. Re-run tests; verify every notebook output, local links, dataset/file hashes, package install, and zip integrity. Save exact versions and disclose platform limits.

## Review focus
Metric vs pseudometric when duplicate observations occur; omitted higher simplices; tied and zero-length bars; ordinary vs reduced homology; official train/test isolation; alpha squared-radius vs Rips edge units; synthetic examples vs evidence; no false learner-completion flags; no redistributed books.
