# Native-language implementation and evidence plan

Goal: replace schema-only companion use with inspectable native data handling and substantive computation while retaining all source lessons.

The prior full-native design is the requested direction. Work in this isolated extracted folder; preserve learner files, the Python lockfile, and clusters. The remote main branch remains unchanged.

1. Inventory every bundled input file, format and original lab. Write tests for decoding, algebra, persistence, training and failure cases before implementation.
2. Implement native Go and Rust modules. They must not call Python or read reference result files. Preserve explicit data kinds, missingness, IDs and split rules.
3. Add deterministic common teaching protocols with exact/numerical comparisons and a per-lab original-reference gap ledger. A new native teaching protocol is not automatically full original-notebook parity.
4. Execute available compilers/tests/data comparisons and all implemented protocols; retain blocked statuses for absent compilers and runtimes.
5. Write beginner language paths, per-lab source links, migration instructions and safe deployment manifests. Generate the actual ZIP and verify its extraction.

Completion reports distinguish code presence, compilation, execution, data equivalence, protocol equivalence, container execution, cluster execution and independent learner mastery.

## Recorded implementation decision
A separate `learning/native-parity-v16` branch was created in the user's GitHub repository solely to provision an official Rust toolchain and vendor the reader dependencies through a bounded CI job. This was necessary because direct package downloads failed. The toolchain-provisioning job succeeded; native-course compilation and all-unit execution were subsequently performed locally with that toolchain. No native course files were merged into main. The compiler artifact is not distributed inside this ZIP.
