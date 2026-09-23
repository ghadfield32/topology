# Real stereo sample — provenance and limits

The two motorcycle photographs and reference disparity originate with the Middlebury 2014 stereo data by Nera Nesic, Porter Westling, Xi Wang, York Kitajima, Greg Krathwohl and Daniel Scharstein. This package copied the sample arrays available in the locally installed scikit-image 0.26.0 distribution; it did not acquire new photographs or download them during the build.

- `motorcycle.npz`: left/right RGB arrays and raw reference disparity; `allow_pickle=False` is used on loading.
- `calibration.json`: the downsampled-image calibration, with the original 193.001 mm baseline explicitly converted to 0.193001 m.
- `manifest.json`: observed shapes, finite-reference count and SHA-256 hashes.
- `SCIKIT_IMAGE_LICENSE.txt`: retained notice from the source distribution, without relabelling third-party data as this course's original material.

Source documentation: https://scikit-image.org/docs/stable/api/skimage.data.html#skimage.data.stereo_motorcycle
Original dataset: https://vision.middlebury.edu/stereo/data/scenes2014/

Disparity is `u_left-u_right`, and the principal-point offset is `cx_right-cx_left`. Therefore depth is `f*B/(d+doffs)`. The reference disparity array is actually 500×741, not a three-channel quantity. Its nonfinite values (including infinity) remain raw in the archive and are excluded transparently in numerical operations.

The reference-derived cloud is not an independently measured set of 3D landmarks. It is a mathematical conversion of the supplied disparity and calibration. The sample supplies no real basketball events, camera-clock experiment, writer/person split, VGGT prediction, or guaranteed metre-error distribution. It is one exposed demonstration scene, not a held-out benchmark of the learned model.

Preserve attribution and the upstream terms when reusing the data. The course does not grant new rights over dataset imagery or third-party model checkpoints.
