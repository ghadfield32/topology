# Optional original VGGT experiment — not part of the CPU prerequisites

**Build status: trained-model inference NOT executed.** The adapter's help/syntax and output contract are tested; synthetic contract fixtures are explicitly not model predictions. No weights, official model repository or CUDA environment is bundled. The original model and VGGT-Omega are different targets; this adapter supports only the original public VGGT interface inspected September 20, 2026.

## Before running
Complete projection, stereo, scale and holdout lessons. Use a separate environment following the exact official original-VGGT checkout's instructions. Install its documented PyTorch/CUDA and other dependencies there. Review the exact code and checkpoint licenses. Do not assume the original non-commercial weights inherit the permissions of a separate commercial checkpoint or the code repository.

Keep the checkout clean and record its full commit with `git -C /path/to/vggt rev-parse HEAD`. Use a trusted, already downloaded checkpoint; the adapter never invokes `from_pretrained`, downloads a model, or falls back to unrestricted pickle loading. `weights_only=True` is an additional restriction, not proof that arbitrary code or files are safe.

## First experiment
Use two existing static image files with sufficient overlap. The bundled `data/stereo/left.png` and `right.png` can serve as an exposed demonstration, with the limitations below. GPU fit depends on input resolution, frame count, precision and model version. A four-frame cap is a workload guard, not a claim that it fits every GPU.

```bash
python optional/run_vggt_local.py --help
python optional/run_vggt_local.py   --repo /path/to/vggt   --expected-commit YOUR_FULL_CHECKED_COMMIT_SHA   --checkpoint /path/to/trusted_checkpoint.pt   --images data/stereo/left.png data/stereo/right.png   --max-frames 2   --preprocess crop   --output my_work/vggt_static_run_01   --license-ack
```

Replace the explicit path/commit arguments with the files you actually reviewed; the script refuses missing or mismatched inputs. For a wrapped checkpoint, use `--state-dict-key` only when its documented format specifies that key. Default loading assumes the actual state dictionary, as in the original quick start.

Optional `--queries-npy` accepts an Nx2 array in the first **preprocessed** image's pixel coordinates. Without it, the runner does not request or claim tracks. With it, output tracks remain 2D correspondences, not metric 3D trajectories.

## What is recorded
`run.json` records status, ordered input hashes, exact code revision, checkpoint hash, preprocessing mode, device/precision, synchronized forward-pass duration, peak allocated/reserved GPU memory, output archive hash, and the fact that metric validity is unestablished. `predictions.npz` contains image-grid-aligned model outputs, camera matrices and preprocessed images. The reported model-forward time excludes loading, export, compression, capture and display. A failed run stays labeled failed.

The schema verifies shapes, finite arrays and basic camera conventions. It does not certify correspondences, geometry, scale, confidence calibration, visibility, tracking accuracy or physical contact.

## Explore without pretending to validate

```bash
python optional/inspect_candidate.py   --run my_work/vggt_static_run_01   --frame 0 --max-points 32 --confidence-quantile 0.5   --output my_work/vggt_exploration_01
```

This validates the run archive hash and exports a small single-frame point table with processed `[frame,row,column]` IDs, plus a Rips persistence summary in unvalidated model units. A confidence quantile is a selection rule, not a probability threshold. No metric comparison is performed automatically.

## Registration and pixel correspondence are required before a benchmark
VGGT preprocessing resizes/crops/pads images. The raw stereo disparity cannot be sampled at processed pixel coordinates without a checked mapping. The runner preserves exact processed images and upstream code revision, but does NOT claim that mapping has been validated. Reconstruct the actual raw-to-processed coordinate transformation, including pixel-center convention and crop/pad offsets, and test it on fiducials or known correspondences before aligning reference points.

Use one subset of valid correspondences/landmarks to register the model's frame and scale, then evaluate different holdouts. Measure both geometry error and coverage. Independently measured landmarks are stronger evidence than merely reproducing a disparity-derived formula. The known dataset calibration must never silently be relabeled as a model-predicted calibration.

## Escalate only after static validation
A stationary athlete, slow motion, occlusion and fast interaction are successively different tests. A static-scene result does not establish robustness to fisheye cameras, rolling shutter, unsynchronized consumer devices or non-rigid sports motion. Use the capstone protocol and exact current model documentation before adopting any candidate into a production state.
