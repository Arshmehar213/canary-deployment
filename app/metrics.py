from prometheus_client import CollectorRegistry, Counter, Histogram

# Explicit buckets tailored for HTTP microservice latency analysis (5ms to 5s)
HTTP_LATENCY_BUCKETS = (
    0.005,
    0.01,
    0.025,
    0.05,
    0.1,
    0.25,
    0.5,
    1.0,
    2.5,
    5.0,
    float("inf"),
)

# Bounded endpoint mapping to prevent cardinality explosion on arbitrary 404 paths
BOUNDED_ENDPOINTS = {
    "root": "/",
    "health": "/health",
}


class MetricsContainer:
    """Holds Prometheus collectors bound to a specific CollectorRegistry."""

    def __init__(self, registry: CollectorRegistry | None = None) -> None:
        self.registry = registry or CollectorRegistry(auto_describe=True)

        self.http_requests_total = Counter(
            name="http_requests_total",
            documentation="Total count of HTTP requests processed, excluding /metrics.",
            labelnames=("method", "endpoint", "status"),
            registry=self.registry,
        )

        self.http_request_duration_seconds = Histogram(
            name="http_request_duration_seconds",
            documentation="HTTP request latency in seconds, excluding /metrics.",
            labelnames=("method", "endpoint"),
            buckets=HTTP_LATENCY_BUCKETS,
            registry=self.registry,
        )


def resolve_bounded_endpoint(flask_endpoint: str | None) -> str:
    """Map Flask route endpoint names to a fixed set of label values."""
    if flask_endpoint is None:
        return "unmatched"
    return BOUNDED_ENDPOINTS.get(flask_endpoint, "unmatched")