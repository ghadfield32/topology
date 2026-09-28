FROM golang:1.23-bookworm AS build
WORKDIR /src
COPY polyglot/go ./polyglot/go
WORKDIR /src/polyglot/go
RUN go test ./...
RUN CGO_ENABLED=0 go build -o /out/shape-go ./cmd/shape-go
WORKDIR /course
COPY data ./data
COPY sports_v8 ./sports_v8

FROM gcr.io/distroless/static-debian12:nonroot
COPY --from=build /out/shape-go /usr/local/bin/shape-go
COPY --from=build /course /course
WORKDIR /course
ENTRYPOINT ["/usr/local/bin/shape-go"]
