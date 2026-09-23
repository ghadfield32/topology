# Source ledger for the v4 consolidation

Checked on September 20, 2026. These are original teaching supplements to the supplied learning plan, not quotations or an endorsed version of the book. The main topology and geometry references remain in [core sources](SOURCES.md) and [v3 geometry sources](SOURCES_V3.md). Existing source-check dates are historical, not silently promoted to a fresh review.

## Primary references used for the new work

| Source | Role in these lessons | Boundary |
|---|---|---|
| [Tinarrage: Topological Data Analysis with Persistent Homology](https://raphaeltinarrage.github.io/EMAp.html) | Verified course sequence, lessons, exercises, videos and notebook links for topology through persistence. | Linked, not redistributed; external availability requires internet. |
| [Hatcher: Algebraic Topology](https://pi.math.cornell.edu/~hatcher/AT/ATpage.html) | Deeper geometric, fundamental-group and homology reading, including the cellular framework behind the projective-plane example. | Official landing page checked; full book not re-audited in this build. No third-party book chapters are bundled. |
| [SciPy: binomtest](https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.binomtest.html) | Exact two-sided binomial calculation on discordant paired outcomes. | Current documentation may describe a different version from the executed environment. See the environment record. No claim that a p-value validates the sampling design. |
| [SciPy: bootstrap](https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.bootstrap.html) | Reference for paired resampling and interval-method distinctions. | Course implementation explicitly resamples paired correctness differences and uses percentile endpoints, not SciPy's default BCa procedure. |
| [scikit-learn: Common pitfalls](https://scikit-learn.org/stable/common_pitfalls.html) | Training-only fitting and preprocessing boundaries. | The demonstration test split is already exposed; it is not a fresh confirmatory result. |
| [statsmodels: Yearly sunspots 1700–2008](https://www.statsmodels.org/stable/datasets/generated/sunspots.html) | Provenance and public-domain statement for the 309-row historical annual series. | Uses the installed 0.14.6 dataset snapshot, not current/revised solar observations. |
| [Middlebury: 2014 stereo datasets](https://vision.middlebury.edu/stereo/data/scenes2014/) | Rectified-camera units and the principal-point correction in disparity-to-depth conversion. | Supplied reference disparity is not an independent physical holdout manufactured by this course. |
| [Ripser.py documentation](https://ripser.scikit-tda.org/en/latest/) | Optional comparison API and homology dimension/coefficient conventions. | Not installed during the build; its comparison is skipped, not passed. |
| [GUDHI Rips manual](https://gudhi.inria.fr/python/latest/rips_complex_user.html) | Diameter convention and distinction between complex dimension and requested homology. | Not installed during the build; no GUDHI agreement claimed. |
| [SciPy minimum_spanning_tree](https://docs.scipy.org/doc/scipy/reference/generated/scipy.sparse.csgraph.minimum_spanning_tree.html) | Comparison of graph conventions with our small dense Prim implementation. | Our implementation preserves explicit zero-weight duplicate-point merges. It is not this library call. |

## Source discrepancy preserved rather than hidden

The statsmodels page describes 309 annual observations covering 1700–2008. A source paragraph also uses the word “monthly,” and a note says YEAR is not returned by load. The installed `load_pandas().data` inspected for this build contains YEAR and SUNACTIVITY with one row per year. The bundled manifest reports the actual table and this discrepancy. It does not invent monthly samples or infer historical release dates. Decimal activity values are preserved; they are not represented as instantaneous integer counts.

## What is newly derived here

The stage sessions, elementary calculations, independent checking code, paired-outcome report, controlled perturbations, real-data selections, and transfer questions are original course material. Their execution evidence is in `reports/consolidation_v4`. Exact examples can verify a computation without establishing a general theorem. A proof supplied in a lesson and a numerical assertion have different evidential roles.

The projective-plane chain example specifies cellular attaching maps and integer boundary maps; its field-dependent calculation is not produced by feeding unsigned simplicial incidence into arbitrary fields. A planar closed-pixel oracle uses connectivity and Euler counting independently of the main boundary-reduction route, but still depends on the same declared foreground convention.

VGGT source descriptions and the optional runner are inherited from v3. This v4 build does not make a new claim about the latest checkpoint, license, benchmark, or inference performance. No trained VGGT-family inference was executed. Consult the exact local artifact and applicable license before a separate model experiment.

The public-domain dataset, existing third-party notices, and all source provenance are kept with the data. External textbook and video content is linked rather than copied into the ZIP. User-supplied planning text is the curriculum basis, not evidence that the unpublished/full book has been inspected.
