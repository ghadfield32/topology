# Learn the deployment chain without confusing its acceptance levels

Native compilation and execution passed in the delivery environment. Docker and a live Kubernetes deployment of these new images did **not** run there. This guide supplies reproducible definitions and explicit acceptance steps, not a fictional deployment record. Historical tests of your earlier Python image do not validate a new native image.

## Native → image → Job → evidence

A compiler turns source into an executable. A Docker image packages that executable and input files. Kubernetes schedules a Pod using the image. A Job tracks work intended to complete. A PVC supplies storage that can outlive an individual Pod. These objects solve different problems; none automatically establishes scientific correctness.

### Build the actual images

From the course root:
```
docker build -f native/deploy/Dockerfile.go -t shape-native-go:16 .
docker build -f native/deploy/Dockerfile.rust -t shape-native-rust:16 .
docker run --rm --read-only --network none --cap-drop ALL --security-opt no-new-privileges shape-native-go:16 --lab stage01
docker run --rm --read-only --network none --cap-drop ALL --security-opt no-new-privileges shape-native-rust:16 --lab stage01
```

Both Dockerfiles run their native tests during the build. Rust dependencies are vendored; base-image acquisition still requires a registry connection or cache. Native programs do not need a Python runtime. The container user is non-root. Use the existing Python image separately when running the Python reference or Python-based data audit.

### Persist results with Compose

Create `my_work/native_containers` on the host. On Linux, match the bind mount user to your host UID/GID using COURSE_UID/COURSE_GID, or deliberately provision permissions; do not solve a permission error with `chmod 777` on the entire repository.

```
docker compose -f native/deploy/compose.yaml config
docker compose -f native/deploy/compose.yaml run --rm go --lab stage01 --output /work/go-stage01-01
docker compose -f native/deploy/compose.yaml run --rm rust --lab stage01 --output /work/rust-stage01-01
```

Use new output names. Keep build logs, image IDs/digests and result files. Compare output metrics and consumed source hashes. A successful image build alone is not a successful experiment run.

## Local Kubernetes, explicitly selected

Use your existing disposable context only after checking it. Never replace the context below with a production cluster merely to run a lesson.

```
kind load docker-image shape-native-go:16 --name shape-learning
kind load docker-image shape-native-rust:16 --name shape-learning
kubectl --context kind-shape-learning get nodes
kubectl --context kind-shape-learning create namespace shape-native-study
kubectl --context kind-shape-learning -n shape-native-study create --dry-run=server -f native/deploy/jobs.yaml
```

If the namespace already exists, inspect it before deciding to reuse it; do not delete it automatically. The YAML contains a PVC and two Jobs with generated names. If the PVC already exists, create only the Job documents for a new run. `create` is deliberate: `generateName` is not an idempotent application identifier.

After inspection:
```
kubectl --context kind-shape-learning -n shape-native-study create -f native/deploy/jobs.yaml
kubectl --context kind-shape-learning -n shape-native-study get pods,jobs,pvc
kubectl --context kind-shape-learning -n shape-native-study wait --for=condition=complete job -l course=shape-native --timeout=900s
```

Retrieve logs by the actual generated Job name returned by Kubernetes. Always include the context and namespace. Output folders contain the Pod UID, so a fresh Job cannot overwrite the previous run. `backoffLimit: 0` avoids retrying failed work into an ambiguous output folder.

Both Jobs use the same claim, read-only roots, no service-account token, dropped capabilities, runtime-default seccomp, CPU/memory limits and unique output paths. The claim is ReadWriteOnce: this constrains how storage is attached, not a promise of one Pod or a backup. A local single-node kind cluster is the intended exercise.

### Export before cleanup

`/work` in the Pod refers to the PVC, not automatically your Windows directory. Use your repository's established read-only export-Pod procedure to copy both result.json files into separate local evidence folders. Record their hashes and the running image IDs. Verify them before any deliberate cleanup. No automatic namespace, PVC or cluster deletion is provided.

### Interpret failures at the right layer

Pending: inspect events, requests and PVC binding. ImagePullBackOff: verify the loaded image tag and context. Failed Job: inspect the container termination status and logs. Completed Job with no host files: inspect the PVC and export path. A model with poor accuracy: inspect the scientific protocol rather than rebuilding the cluster.

## CI scope

The supplied optional native workflow compiles and tests Go/Rust, then compares all 57 native units. It does not claim full original-notebook equivalence. Remote execution of this complete native-source workflow is not claimed in the delivery report.

A separate toolchain-provisioning workflow did run successfully on the branch `learning/native-parity-v16`, providing the official Rust compiler and vendor sources used for local verification. That remote toolchain job did not execute this full course. Main was not changed.
