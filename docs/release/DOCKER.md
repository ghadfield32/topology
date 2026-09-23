# Docker: a separate environment, not a shortcut around evidence

## The mental model

An **image** is a filesystem plus execution configuration. A **container** is a running instance. A **bind mount** exposes a chosen host directory. **Compose** coordinates local services. A native Python test does not prove an image can build or run.

Version 12 ships a Dockerfile using explicit Python 3.13.5 and uv 0.10.0 tags. Tags can move; they are not immutable image digests. Record the resolved image ID and base digest when you actually build. The host `.venv`, private work and secrets are excluded by `.dockerignore`. Dependencies are installed into `/opt/venv`, separate from `/course` and writable work.

## First complete native setup

Follow [FIRST_RUN.md](FIRST_RUN.md) to produce a genuine reviewed `uv.lock`. Without it, the image intentionally refuses to build. The package does not pretend its observed dependency snapshot is a resolved lock.

Install/start a Docker engine with the Compose plugin and inspect `Dockerfile`, `compose.yaml`, and `.dockerignore`. These files can run build commands and mount host directories; treat them as executable configuration.

```bash
uv run --no-sync python tools/docker_verify.py --profile physics --output my_work/docker01
```

The command checks the CLI, Compose and daemon, validates the configuration, builds the image, runs the profile tests and Stage 00, and records commands and logs. It never fabricates a pass when Docker is absent. Read the exact returned scope: a Stage 00 container run is not an all-reference container replay.

## Services and writable paths

The shared Compose policy uses a non-root UID/GID, read-only root filesystem, no new privileges, dropped capabilities, and a temporary writable `/tmp`. The reference course is read-only in the Jupyter service; only `my_work` is mounted writable for answers. The reader does not need private learner files to render public lessons. Jupyter retains its generated authentication token and publishes only on loopback.

```bash
# macOS/Linux. Set an existing profile explicitly for the image build.
export COURSE_PROFILE=physics
mkdir -p my_work
# Linux: match local writable ownership; do not use UID 0 as your normal workflow.
export COURSE_UID=$(id -u)
export COURSE_GID=$(id -g)
docker compose build course
docker compose run --rm course acceptance --profile physics --references first --output /work/acceptance01
docker compose --profile reader up reader
docker compose --profile lab up lab
```

On PowerShell, use `$env:COURSE_PROFILE="physics"` and `New-Item -ItemType Directory -Force my_work`. Omit Unix `id` commands; follow Docker Desktop's host-folder permissions. The native course runs on Windows syntax too, but Windows was not executed in this delivery.

Reader: `http://localhost:8000/`. Jupyter: `http://localhost:8888/`; copy its token URL from the container log. Create a private notebook with `course.py practice` or copy an assignment into `/course/my_work`. Saving over a canonical reference is intentionally denied. It is a feature, not an instruction to loosen all permissions.

## What to inspect when something fails

A daemon error is different from an image resolution error. A missing lock is different from incompatible dependencies. A read-only error may mean you tried to save to `/course` rather than `/work` or `/course/my_work`. An image from a prior profile may lack PyTorch or cross-check libraries; rebuild with the intended profile. A busy port requires another local port binding, not a public interface. A kernel that imports another environment must fail the recorded provenance check.

A v12 native probe actually ran as a non-root Linux UID with root-owned read-only sources and separate writable output. It exposed and fixed workspace permissions. **That is not a Docker execution claim.** This build host has no Docker engine; the live verification command must supply the remaining evidence on your machine or CI.

Primary references: https://docs.astral.sh/uv/guides/integration/docker/ and https://docs.docker.com/reference/compose-file/services/ .
