# Polyglot Kubernetes practice

The Go and Rust images include the small bundled teaching datasets required by the companion labs. The Jobs therefore do not depend on a node-local hostPath or on your Windows/macOS filesystem.

They are still local-learning manifests, not production deployment manifests. The archive build environment had no Kubernetes runtime, so these resources received static YAML/security checks only.

For a disposable kind cluster:

```bash
docker build -f polyglot/Dockerfile.go -t listening-to-shape-go:14 .
docker build -f polyglot/Dockerfile.rust -t listening-to-shape-rust:14 .
kind load docker-image listening-to-shape-go:14 --name shape-learning
kind load docker-image listening-to-shape-rust:14 --name shape-learning
kubectl --context kind-shape-learning apply -f deploy/polyglot/jobs.yaml
kubectl --context kind-shape-learning wait --for=condition=complete job/shape-go-stage01 --timeout=120s
kubectl --context kind-shape-learning wait --for=condition=complete job/shape-rust-stage01 --timeout=120s
kubectl --context kind-shape-learning logs job/shape-go-stage01
kubectl --context kind-shape-learning logs job/shape-rust-stage01
```

Use a separate namespace if you want to preserve evidence from repeated exercises. Jobs complete; they are not long-running reader services.
