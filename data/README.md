# Real datasets, provenance and limitations

## Iris snapshot

`raw/iris.csv` is exported from `sklearn.datasets.load_iris` in scikit-learn 1.8.0. It contains 150 records and four measured features in centimeters, plus original zero-based row IDs, class indices and species names. This is scikit-learn's corrected variant; its documentation notes differences from historical UCI files. The file is not claimed byte-identical to every UCI version.

Source: Fisher, R. (1936), *Iris* [Dataset], UCI Machine Learning Repository, DOI https://doi.org/10.24432/C56C76. Dataset page: https://archive.ics.uci.edu/dataset/53/iris. Variant documentation: https://scikit-learn.org/stable/datasets/toy_dataset.html#iris-plants-dataset.

## Handwritten digits snapshot

`raw/digits.npz` is exported from `sklearn.datasets.load_digits` in scikit-learn 1.8.0. It contains 1,797 images of shape 8×8 and integer intensity range 0–16, labels 0–9, and zero-based IDs preserving snapshot order. The 8×8 values summarize blocks from preprocessed handwriting bitmaps; these are not 28×28 MNIST images and not generated digits.

Source: Alpaydin, E. & Kaynak, C. (1998), *Optical Recognition of Handwritten Digits* [Dataset], UCI Machine Learning Repository, DOI https://doi.org/10.24432/C50P49. Dataset page: https://archive.ics.uci.edu/dataset/80/optical+recognition+of+handwritten+digits. The full UCI collection has 5,620 images and an original train/test partition; scikit-learn's 1,797-image loader corresponds to the original test subset, not the full collection.

We create a new **per-image learning split**, stratified by label, with seeds 20260920 and 20260921: 1,077 train, 360 validation, 360 test. This is documented in `splits.json`. Writer IDs are not available in these arrays. Do not claim that this split tests unseen writers or reproduces the original UCI train/test design. The official full training file was not downloaded because the execution container could not access it.

## License and attribution

Both UCI dataset pages identify their datasets as CC BY 4.0. See https://creativecommons.org/licenses/by/4.0/ for the license. Credit the dataset creators and UCI, retain provenance, and indicate changes. Changes here: export/reformatting, IDs, a new internal digits split, and derived per-image topology features. No original textbook or lecture-note PDFs are redistributed.

Scikit-learn is a BSD-licensed software project. The arrays are used with their dataset attribution; this archive does not change the rights associated with either the upstream code or data.

## Integrity and reconstruction

`manifest.json` records SHA-256 hashes, shapes, source variant, loader version and split sizes. `python scripts/prepare_data.py` recreates the snapshots from the installed scikit-learn loaders. Different loader versions should be treated as a new provenance event even when values appear equal.

`processed/` holds fixed per-image feature caches. Cache identity includes the raw digits file, split file and package source content. These are not fitted scalers. Learned scalers are fitted only in the appropriate model-training pipeline. The test cache is created by the final capstone, not used to select settings.

All example datasets are bundled; no network is required after package installation. There is no real sports or WMS dataset in this archive. Sports applications are explicit proposed capstone extensions.
