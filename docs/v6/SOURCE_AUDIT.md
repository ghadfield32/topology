# Version 6 source and claim audit

Source review date: 20 September 2026. This is an expansion of the existing course, not a new reading of the actual book. The latest message supplied no additional text after “concepts:”; the previously provided posts remain represented in [the v5 source audit](../v5/SOURCE_AUDIT.md), not replaced with invented attachments.

## Evidence classes

**Supplied source claims:** The original posts discuss gradient conflicts in PINNs/PIKANs, Hamiltonian/Lagrangian learning, geometric constraints and smooth charts/flows. Their language, claimed outcomes and qualifications remain in the prior audit. User-supplied material is not treated as independent validation.

**Public source facts checked for v6:** UCI and statsmodels dataset pages, PhysioNet's named PTB-XL release, The Well documentation, SPL's official README and OpenBiomechanics' data license. The [dataset catalogue](DATA_CATALOG.md), [individual cards](../../industry/cards/wdbc.md), and [optional list](OPTIONAL_DATA.md) link the exact primary pages. The web pages were accessible; direct downloads from the build's Python environment were not.

**Actual bytes used:** Local distributions from scikit-learn 1.8.0 and statsmodels 0.14.6. CSV hashes, field counts, missingness, labels and derived splits were verified from these bytes. Current online documentation can describe a newer software version; the package never substitutes its version number for the installed source version.

**Course-designed experiments:** Choice of seed, small fixed model, split, topology descriptor, metric, and counterexample. These are original teaching protocols, not claimed reproductions of a source paper. All saved demonstrations expose their held-out partitions; further changes on those partitions are exploratory.

## Discrepancies and boundaries kept visible

- **CO₂ counts:** the exported data contain 2,284 weekly slots, including 59 missing values; the provider describes 2,225 observations. We retain the missing slots and reject windows crossing missing measurements. The source description and cited sampling reference need not refer to identical measurement procedures; this course does not resolve that ambiguity into a new instrument claim.
- **Modechoice shape:** the loaded distribution has nine data columns before our identifier, whereas the page's headline variable count is eight. The actual schema is listed; the repeated-alternative unit is not collapsed without documenting it.
- **Grunfeld units and availability:** the source uses a 1947-dollar scale without an established multiplier in this export. We do not label it millions of dollars. The source's year-end value is lagged before predicting the next year's investment; historical publication/revision dates are absent.
- **Small manufacturing table:** Stackloss describes 21 days but does not preserve calendar dates in this snapshot. A source-order holdout is explicitly not established forward-time forecasting. Ambiguous airflow and concentration conventions remain source-scale quantities.
- **Healthcare and wine units:** physical units absent from the provider descriptions are marked unknown. No millimetres or mass-concentration units are invented. Scikit-learn's benign/malignant encoding is stated before computing metrics.
- **Optional Bike Sharing counts:** provider summaries and commonly distributed archive counts are not assumed identical. The actual downloaded file must settle this in a future acquisition record.
- **SPL versions:** the current official repository summary and an external competition may describe different subsets. We use the repository's March 2026 summary only for its own catalogue entry, not as evidence that those trials are bundled or evaluated.
- **The Well licensing:** software license and individual simulation-data rights are separate. The selected file's data license remains an explicit acquisition gate. Its introductory 16-dataset count is not asserted to cover every currently listed dataset.

## Accuracy is a process, not a total guarantee

Hash checks detect changed bytes, not inaccurate sensors. Unit tests detect specified implementation failures, not all possible mistakes. A model can satisfy a numerical residual while the governing equation is wrong. A classifier can predict a label without revealing causal structure. A persistence feature can reflect preprocessing or sampling. The learner must state these distinctions in the stage and case assessments.

The required new cases include no neural operator or VGGT inference. Earlier manufactured neural examples remain separately labeled. A global data-cloud barcode is an exploratory cohort descriptor, not a patient-specific measurement, a physical cavity, or a proof of hidden topology.
