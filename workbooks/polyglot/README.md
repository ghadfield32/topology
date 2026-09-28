# Learn any lab in Python, Go or Rust

One notebook triad per learning unit: the same lab, the same registered
inputs, the same comparison — three languages. Start with Python, then Go,
then Rust. See [the guide](../../native/guides/LEARNING_PATHS.md) and the
[import record](../../docs/release/LANGUAGE_NOTEBOOKS.md).

Each notebook is **unassessed**. Nothing here is a second mandatory curriculum.

## Find your way around (the folders have different jobs)

This trips people up, because several folders hold Go or Rust code:

| Path | What it is | Do you edit it? |
|---|---|---|
| `workbooks/polyglot/python/` | **notebooks** that run the canonical Python reference | no |
| `workbooks/polyglot/go/` | **notebooks** that run the real Go program | no |
| `workbooks/polyglot/rust/` | **notebooks** that run the real Rust program | no |
| `native/go/`, `native/rust/` | the **reference source** those notebooks compile | no — read-only reference |
| `my_work/<session>/native/go|rust/` | **your** copy from `native_course.py prepare` | **yes — here** |
| `notebooks/`, `lessons/`, `practice/` | the original course labs and assignments | your learner notebook |

`notebooks/` is the *original course*. It has no `go` or `rust` folder, and it
is not where these notebooks live. There are 57 notebooks per language
(171 in total) under `workbooks/polyglot/`.

Full definitions of every path: [docs/release/REPOSITORY_LAYOUT.md](../../docs/release/REPOSITORY_LAYOUT.md).

Full definitions of every path: [docs/release/REPOSITORY_LAYOUT.md](../../docs/release/REPOSITORY_LAYOUT.md).

```powershell
# the three Stage 01 notebooks, one per language
workbooks/polyglot/python/stage01.ipynb
workbooks/polyglot/go/stage01.ipynb
workbooks/polyglot/rust/stage01.ipynb
```

| Lab | Title | Python | Go | Rust |
|---|---|---|---|---|
| `stage00` | Start here: how to learn, run, and question the results | [py](python/stage00.ipynb) | [go](go/stage00.ipynb) | [rust](rust/stage00.ipynb) |
| `stage01` | Mathematical language, proofs, and linear algebra | [py](python/stage01.ipynb) | [go](go/stage01.ipynb) | [rust](rust/stage01.ipynb) |
| `stage02` | Closeness, metrics, neighborhoods, and topologies | [py](python/stage02.ipynb) | [go](go/stage02.ipynb) | [rust](rust/stage02.ipynb) |
| `stage03` | Continuity, homeomorphisms, connectedness, and compactness | [py](python/stage03.ipynb) | [go](go/stage03.ipynb) | [rust](rust/stage03.ipynb) |
| `stage04` | Groups, symmetries, paths, loops, and homotopy | [py](python/stage04.ipynb) | [go](go/stage04.ipynb) | [rust](rust/stage04.ipynb) |
| `stage05` | Surfaces, simplices, triangulations, and pixel geometry | [py](python/stage05.ipynb) | [go](go/stage05.ipynb) | [rust](rust/stage05.ipynb) |
| `stage06` | Chains, boundaries, homology, and Betti numbers | [py](python/stage06.ipynb) | [go](go/stage06.ipynb) | [rust](rust/stage06.ipynb) |
| `stage07` | From data to shape: Rips, Čech, alpha, and filtrations | [py](python/stage07.ipynb) | [go](go/stage07.ipynb) | [rust](rust/stage07.ipynb) |
| `stage08` | Persistent homology, persistence modules, and reading diagrams | [py](python/stage08.ipynb) | [go](go/stage08.ipynb) | [rust](rust/stage08.ipynb) |
| `stage09` | Implement persistence, trace the algorithm, and test it independently | [py](python/stage09.ipynb) | [go](go/stage09.ipynb) | [rust](rust/stage09.ipynb) |
| `stage10` | Stability, diagram distances, noise, and scientific uncertainty | [py](python/stage10.ipynb) | [go](go/stage10.ipynb) | [rust](rust/stage10.ipynb) |
| `stage11` | Useful representations, Mapper, time windows, and honest machine learning | [py](python/stage11.ipynb) | [go](go/stage11.ipynb) | [rust](rust/stage11.ipynb) |
| `stage12` | Capstone: reproduce, defend, transfer, and audit the book | [py](python/stage12.ipynb) | [go](go/stage12.ipynb) | [rust](rust/stage12.ipynb) |
| `stage13` | From topology to smooth manifolds | [py](python/stage13.ipynb) | [go](go/stage13.ipynb) | [rust](rust/stage13.ipynb) |
| `stage14` | Rotations, rigid transforms, and the camera model | [py](python/stage14.ipynb) | [go](go/stage14.ipynb) | [rust](rust/stage14.ipynb) |
| `stage15` | Measured stereo, calibration, and uncertainty | [py](python/stage15.ipynb) | [go](go/stage15.ipynb) | [rust](rust/stage15.ipynb) |
| `stage16` | Attention and VGGT, from pixels to proposed geometry | [py](python/stage16.ipynb) | [go](go/stage16.ipynb) | [rust](rust/stage16.ipynb) |
| `stage17` | Register, validate, and ask topology the right question | [py](python/stage17.ipynb) | [go](go/stage17.ipynb) | [rust](rust/stage17.ipynb) |
| `stage18` | Make the pipeline efficient without changing the evidence | [py](python/stage18.ipynb) | [go](go/stage18.ipynb) | [rust](rust/stage18.ipynb) |
| `stage19` | From geometry to cautious interaction hypotheses | [py](python/stage19.ipynb) | [go](go/stage19.ipynb) | [rust](rust/stage19.ipynb) |
| `stage20` | Independent spatial capstone and continuing mastery | [py](python/stage20.ipynb) | [go](go/stage20.ipynb) | [rust](rust/stage20.ipynb) |
| `stage21` | Rates, equations, units and what data can identify | [py](python/stage21.ipynb) | [go](go/stage21.ipynb) | [rust](rust/stage21.ipynb) |
| `stage22` | Smooth flows, coordinate changes and invertible networks | [py](python/stage22.ipynb) | [go](go/stage22.ipynb) | [rust](rust/stage22.ipynb) |
| `stage23` | Mechanics, Hamiltonian networks and Lagrangian networks | [py](python/stage23.ipynb) | [go](go/stage23.ipynb) | [rust](rust/stage23.ipynb) |
| `stage24` | Symplectic integration, energy, phase and long rollouts | [py](python/stage24.ipynb) | [go](go/stage24.ipynb) | [rust](rust/stage24.ipynb) |
| `stage25` | Constraints, projections, retractions and rank failure | [py](python/stage25.ipynb) | [go](go/stage25.ipynb) | [rust](rust/stage25.ipynb) |
| `stage26` | Physics-informed learning and inverse problems | [py](python/stage26.ipynb) | [go](go/stage26.ipynb) | [rust](rust/stage26.ipynb) |
| `stage27` | Conflicting gradients, interfaces, separability and PIKANs | [py](python/stage27.ipynb) | [go](go/stage27.ipynb) | [rust](rust/stage27.ipynb) |
| `stage28` | Functions to functions: DeepONet, Fourier operators and baselines | [py](python/stage28.ipynb) | [go](go/stage28.ipynb) | [rust](rust/stage28.ipynb) |
| `stage29` | Differentiable simulation, graph physics and attention constraints | [py](python/stage29.ipynb) | [go](go/stage29.ipynb) | [rust](rust/stage29.ipynb) |
| `stage30` | An independent world-model study: evidence before adoption | [py](python/stage30.ipynb) | [go](go/stage30.ipynb) | [rust](rust/stage30.ipynb) |
| `wdbc` | Healthcare image-summary classification | [py](python/wdbc.ipynb) | [go](go/wdbc.ipynb) | [rust](rust/wdbc.ipynb) |
| `wine` | Food chemistry and topology | [py](python/wine.ipynb) | [go](go/wine.ipynb) | [rust](rust/wine.ipynb) |
| `stackloss` | Manufacturing regression | [py](python/stackloss.ipynb) | [go](go/stackloss.ipynb) | [rust](rust/stackloss.ipynb) |
| `grunfeld` | Firm-year panel measurements | [py](python/grunfeld.ipynb) | [go](go/grunfeld.ipynb) | [rust](rust/grunfeld.ipynb) |
| `co2` | Atmospheric observations and windows | [py](python/co2.ipynb) | [go](go/co2.ipynb) | [rust](rust/co2.ipynb) |
| `nile` | Water-infrastructure time series | [py](python/nile.ipynb) | [go](go/nile.ipynb) | [rust](rust/nile.ipynb) |
| `elnino` | Marine climate | [py](python/elnino.ipynb) | [go](go/elnino.ipynb) | [rust](rust/elnino.ipynb) |
| `modechoice` | Traveler-level choice sets | [py](python/modechoice.ipynb) | [go](go/modechoice.ipynb) | [rust](rust/modechoice.ipynb) |
| `seeds` | Agriculture feature-space geometry | [py](python/seeds.ipynb) | [go](go/seeds.ipynb) | [rust](rust/seeds.ipynb) |
| `concrete_slump` | Materials measurements and intervals | [py](python/concrete_slump.ipynb) | [go](go/concrete_slump.ipynb) | [rust](rust/concrete_slump.ipynb) |
| `leakage` | Identity leakage controls | [py](python/leakage.ipynb) | [go](go/leakage.ipynb) | [rust](rust/leakage.ipynb) |
| `claims` | Physical-claim counterexamples | [py](python/claims.ipynb) | [go](go/claims.ipynb) | [rust](rust/claims.ipynb) |
| `s00` | Sports observations and units | [py](python/s00.ipynb) | [go](go/s00.ipynb) | [rust](rust/s00.ipynb) |
| `s01` | Landmark angles and velocity | [py](python/s01.ipynb) | [go](go/s01.ipynb) | [rust](rust/s01.ipynb) |
| `s02` | Ball-flight model adequacy | [py](python/s02.ipynb) | [go](go/s02.ipynb) | [rust](rust/s02.ipynb) |
| `s03` | Soccer profile topology | [py](python/s03.ipynb) | [go](go/s03.ipynb) | [rust](rust/s03.ipynb) |
| `s04` | Timing and uncertainty | [py](python/s04.ipynb) | [go](go/s04.ipynb) | [rust](rust/s04.ipynb) |
| `s05` | Athlete-group evaluation | [py](python/s05.ipynb) | [go](go/s05.ipynb) | [rust](rust/s05.ipynb) |
| `s06` | Independent sports investigation | [py](python/s06.ipynb) | [go](go/s06.ipynb) | [rust](rust/s06.ipynb) |
| `acb` | ACB 2025–26 source and identity readiness | [py](python/acb.ipynb) | [go](go/acb.ipynb) | [rust](rust/acb.ipynb) |
| `r01` | Distributions, moments, and whitening | [py](python/r01.ipynb) | [go](go/r01.ipynb) | [rust](rust/r01.ipynb) |
| `r02` | Projections, characteristic functions, and SIGReg | [py](python/r02.ipynb) | [go](go/r02.ipynb) | [rust](rust/r02.ipynb) |
| `r03` | Anti-collapse objectives and gradient paths | [py](python/r03.ipynb) | [go](go/r03.ipynb) | [rust](rust/r03.ipynb) |
| `r04` | Train a representation and evaluate frozen probes | [py](python/r04.ipynb) | [go](go/r04.ipynb) | [rust](rust/r04.ipynb) |
| `r05` | Transfer diagnostics without inventing a sports world model | [py](python/r05.ipynb) | [go](go/r05.ipynb) | [rust](rust/r05.ipynb) |
| `poux_bridge` | Poux spatial-AI Stage 01 weighted-streaming bridge | [py](python/poux_bridge.ipynb) | [go](go/poux_bridge.ipynb) | [rust](rust/poux_bridge.ipynb) |

Total: 57 labs × 3 languages = 171 notebooks.

## Run a lab without a notebook

```
uv run --no-sync python native_course.py compare --lab stage01 --output my_work/native_stage01_01
```
