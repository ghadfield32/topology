# Build review and resolved findings

This is an inline engineering review, not an independent third-party audit.

The baseline v4 suite passed (296 tests, 2 optional-library skips). New mathematical contracts were observed failing before implementation, then passed. Neural derivative/shape contracts and progress-migration contracts were also observed failing before implementation.

During a parallel refresh of legacy notebooks, the release/version and learning-log changes altered the intentionally broad source-code fingerprint between Stage 11 model selection and Stage 12 evaluation. Stage 12 correctly refused to use the stale selection. No guard was removed. After freezing the relevant source files, Stage 11 and its dependent stages were rerun. The digits holdout remains disclosed; this rerun is not a new confirmatory evaluation.

Other review corrections: the FNO report now distinguishes tensor-element count from real scalar degrees of freedom for complex weights; the copper secant example is rounded consistently; avoidable tensor-to-scalar warnings were removed. No source post's benchmark or hardware claim was promoted to a reproduced result.

Final verification and archive checks are recorded separately. Historical v1–v4 verification pages remain in the archive as historical records, not fresh v5 counts. New source files were not copied with social-network navigation, profile details or unrelated comments.
