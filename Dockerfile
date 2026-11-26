# Stage 1: Builder
FROM python:3.12-slim-trixie AS builder

WORKDIR /app
COPY requirements.txt ./
RUN pip install --no-cache-dir --prefix=/install -r requirements.txt

# Stage 2: Minimal Runtime
FROM cgr.dev/chainguard/python:latest

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    APP_VERSION="v1" \
    FAILURE_MODE="none" \
    FAILURE_RATE="0.0" \
    INJECTED_LATENCY_SECONDS="0.0" \
    PORT="8080"

WORKDIR /app
COPY --from=builder /install /usr/local
COPY app ./app

EXPOSE 8080
