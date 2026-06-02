# Stage 1: Build the Go binary
FROM golang:1.25-alpine AS builder

WORKDIR /app

# Install build dependencies
RUN apk add --no-cache git

# Copy go.mod and go.sum files
COPY go.mod go.sum ./

# Download dependencies
RUN go mod download

# Copy the rest of the source code
COPY . .

# Build the bot binary
RUN go build -o bot ./cmd/bot/main.go

# Stage 2: Final image
FROM alpine:latest

WORKDIR /app

# Install runtime dependencies
RUN apk add --no-cache ffmpeg ca-certificates

# Copy the binary from the builder stage
COPY --from=builder /app/bot .

# Expose any necessary ports (if applicable)
# EXPOSE 8080

# Command to run the bot
CMD ["./bot"]
