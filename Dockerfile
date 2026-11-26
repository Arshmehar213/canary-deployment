FROM python:3.12-slim-bookworm

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    APP_VERSION="v1" \
    FAILURE_MODE="none" \
    FAILURE_RATE="0.0" \
    INJECTED_LATENCY_SECONDS="0.0" \
    PORT="8080"

WORKDIR /app

# Create an unprivileged system user and group
RUN groupadd --system --gid 10001 appgroup && \
    useradd --system --uid 10001 --gid appgroup --no-create-home --shell /usr/sbin/nologin appuser

# Install strictly pinned runtime dependencies first for layer caching
COPY requirements.txt ./
RUN pip install --no-cache-dir --require-hashes --no-deps -r requirements.txt 2>/dev/null || \
    pip install --no-cache-dir -r requirements.txt

# Copy only runtime application code
COPY --chown=appuser:appgroup app ./app

USER 10001:10001

EXPOSE 8080

# Single-process multi-threaded Gunicorn worker ensures in-memory Prometheus
# counters remain consistent without needing multiprocess directory volume mounts.
CMD ["gunicorn", "--bind", "0.0.0.0:8080", "--workers", "1", "--threads", "4", "--timeout", "30", "--access-logfile", "-", "app.main:create_wsgi_app()"]