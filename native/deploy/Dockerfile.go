FROM golang:1.23.2-bookworm AS build
WORKDIR /src
COPY native/go/ ./
ENV GOTOOLCHAIN=local CGO_ENABLED=0 GOWORK=off
RUN go test -count=1 ./... && go build -trimpath -o /shape-go ./cmd/shape-go
FROM debian:bookworm-slim
RUN mkdir -p /course /work && chown 10001:10001 /work
COPY --from=build /shape-go /usr/local/bin/shape-go
COPY data/ /course/data/
COPY sports_v8/data/ /course/sports_v8/data/
COPY sports_v9/data/ /course/sports_v9/data/
COPY native/protocols/ /course/native/protocols/
WORKDIR /course
USER 10001:10001
ENTRYPOINT ["/usr/local/bin/shape-go", "--repo", "/course"]
CMD ["--lab", "stage01"]
