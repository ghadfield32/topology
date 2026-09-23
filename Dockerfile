# Exact tool/runtime tags; tags are not immutable digests. See release limitations.
FROM ghcr.io/astral-sh/uv:0.10.0 AS uv
FROM python:3.13.5-slim-bookworm
COPY --from=uv /uv /usr/local/bin/uv
ENV UV_PYTHON_DOWNLOADS=never UV_PROJECT_ENVIRONMENT=/opt/venv UV_LINK_MODE=copy \
    PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1 MPLBACKEND=Agg \
    OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 \
    PATH="/opt/venv/bin:$PATH" HOME=/tmp/student
ARG COURSE_PROFILE=core
WORKDIR /course
COPY . /course
# A fabricated lockfile would hide an unresolved install. Fail clearly instead.
RUN test -s uv.lock || (echo 'Run python tools/bootstrap.py online and commit uv.lock before building.' >&2; exit 2)
RUN case "$COURSE_PROFILE" in \
    core) uv sync --locked --no-editable --extra notebooks --extra test --extra reader ;; \
    physics) uv sync --locked --no-editable --extra notebooks --extra test --extra reader --extra physics ;; \
    full) uv sync --locked --no-editable --extra notebooks --extra test --extra reader --extra physics --extra crosscheck ;; \
    *) echo 'COURSE_PROFILE must be core, physics or full' >&2; exit 2 ;; esac
RUN groupadd --gid 1000 student && useradd --uid 1000 --gid student --create-home student \
    && mkdir -p /work /tmp/student && chown -R student:student /course /work /tmp/student
USER student
EXPOSE 8000 8888
ENTRYPOINT ["python", "course.py"]
CMD ["doctor"]
