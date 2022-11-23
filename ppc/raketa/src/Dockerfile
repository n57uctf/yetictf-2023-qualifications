FROM golang:1.18-alpine AS build_base

RUN apk add --no-cache git

# Set the Current Working Directory inside the container
WORKDIR /tmp/raketa

# We want to populate the module cache based on the go.{mod,sum} files.
COPY ./go.mod .
COPY ./go.sum .

RUN go mod download

COPY ./main.go .

# Build the Go app
RUN go build -o ./out/main .

# Start fresh from a smaller image
FROM alpine

ENV RAKETA_LISTEN_ADDRESS ":8181"
ENV RAKETA_DB_FILE_PATH "./db.json"
ENV RAKETA_ELEVATE_COST 1000
ENV RAKETA_FLAG "YetiCTF{7510lk0v5k1y_15_7h3_b357_h4ck3r?}"

RUN apk add ca-certificates

COPY --from=build_base /tmp/raketa/out/main /app/main

# This container exposes port 8080 to the outside world
EXPOSE 8181

# Run the binary program produced by `go install`
CMD ["/app/main"]
