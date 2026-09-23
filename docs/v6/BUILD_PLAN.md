# Version 6 implementation and acceptance plan

## Goal
Preserve all 31 existing beginner stages and add an optional cross-industry practice track that is runnable offline with authentic data, explicit provenance, documented reuse terms, teaching notes, and reproducible validation. Do not turn a short teaching dataset into evidence of deployment performance.

## Design and scope
The existing topology/geometry/physics modules remain canonical. New industry utilities consume their persistence implementation, not a second implementation. CSV snapshots and a machine-readable catalogue support eight independent case notebooks. Each original stage gets a transfer guide linking the relevant case and explaining when that data cannot support a physical inference. A separate catalogue covers larger optional datasets; no claims that unavailable downloads have been acquired.

## Execution
1. Record existing archive hash; export eight locally distributed public-domain/CC BY data snapshots with versioned provenance, field dictionaries, missingness, hashes, and explicit splits.
2. Write and run failing tests for group/chronological splitting, training-only scaling, past-only windows, topological descriptors, loss functions, split audits, and snapshot verification.
3. Implement bounded NumPy/SciPy helpers with toy cases and source contracts.
4. Develop eight original case lessons and executed reference notebooks, independent learner assignments and worked answers, 31 stage transfer guides, and a data-reading primer.
5. Preserve original stage links and learner records. Render one v6 entry point plus locally linked case pages. Add tested catalogue/download commands; remote fetches remain opt-in.
6. Run original tests and new tests, execute reference notebooks, scan metadata and HTML links, inspect representative desktop/mobile rendering, build checksums, extract the final ZIP, and rerun verification using the extracted source.

## Review focus
- Group and time leakage; target/ID columns mistaken for measurements.
- Missing values mistaken for zero; windows bridging gaps or using future data.
- Per-example versus whole-dataset homology confused in supervised learning.
- Arbitrary feature coordinate order treated as a physical manifold.
- Reuse terms, raw/derived provenance, and local snapshot versus current source discrepancies.
- Learner progress overwritten; inherited evidence presented as a new run.
- Computational checks presented as clinical, infrastructure, sports, or climate validation.
