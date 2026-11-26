import pytest
from prometheus_client import CollectorRegistry

from app.config import AppConfig, ConfigError
from app.main import create_app


def test_normal_application_response_default_version() -> None:
    app = create_app(env={})
    client = app.test_client()

    response = client.get("/")
    assert response.status_code == 200
    assert response.get_json() == {
        "app": "canary-demo-app",
        "version": "v1",
        "message": "Hello from canary-demo-app (v1)",
    }


def test_custom_version_configuration() -> None:
    app = create_app(env={"APP_VERSION": "v2.1.0-canary", "APP_NAME": "payments-api"})
    client = app.test_client()

    response = client.get("/")
    assert response.status_code == 200
    data = response.get_json()
    assert data["app"] == "payments-api"
    assert data["version"] == "v2.1.0-canary"
    assert data["message"] == "Hello from payments-api (v2.1.0-canary)"


def test_health_endpoint_unaffected_by_failure_injection() -> None:
    app = create_app(
        env={
            "FAILURE_MODE": "http_500",
            "FAILURE_RATE": "1.0",
        }
    )
    client = app.test_client()

    response = client.get("/health")
    assert response.status_code == 200
    assert response.get_json() == {"status": "healthy"}


def test_prometheus_metrics_exposure_and_bounded_labels() -> None:
    registry = CollectorRegistry(auto_describe=True)
    app = create_app(env={"APP_VERSION": "v1"}, registry=registry)
    client = app.test_client()

    # Trigger valid endpoints and an arbitrary 404 path
    assert client.get("/").status_code == 200
    assert client.get("/health").status_code == 200
    assert client.get("/arbitrary/unbounded/path/12345").status_code == 404

    # Scrape /metrics twice to verify /metrics does not instrument itself
    metrics_resp_1 = client.get("/metrics")
    metrics_resp_2 = client.get("/metrics")

    assert metrics_resp_1.status_code == 200
    assert "text/plain" in metrics_resp_2.content_type

    body = metrics_resp_2.get_data(as_text=True)

    # Verify root and health counters
    assert 'http_requests_total{endpoint="/",method="GET",status="200"} 1.0' in body
    assert 'http_requests_total{endpoint="/health",method="GET",status="200"} 1.0' in body

    # Verify arbitrary 404 path is collapsed into bounded "unmatched" label
    assert 'http_requests_total{endpoint="unmatched",method="GET",status="404"} 1.0' in body
    assert "/arbitrary/unbounded/path/12345" not in body

    # Verify /metrics is never instrumented
    assert 'endpoint="/metrics"' not in body

    # Verify histogram series exist
    assert 'http_request_duration_seconds_bucket{endpoint="/",le="0.1",method="GET"}' in body
    assert 'http_request_duration_seconds_count{endpoint="/",method="GET"} 1.0' in body


def test_deterministic_http_500_failure_injection() -> None:
    # Deterministic RNG sequence: 0.15 (< 0.5 -> fail), 0.85 (>= 0.5 -> succeed)
    rng_values = iter([0.15, 0.85])
    registry = CollectorRegistry(auto_describe=True)

    app = create_app(
        env={
            "APP_VERSION": "v2",
            "FAILURE_MODE": "http_500",
            "FAILURE_RATE": "0.5",
        },
        registry=registry,
        rng=lambda: next(rng_values),
    )
    client = app.test_client()

    first_resp = client.get("/")
    assert first_resp.status_code == 500
    assert first_resp.get_json()["error"] == "Injected HTTP 500 fault"

    second_resp = client.get("/")
    assert second_resp.status_code == 200
    assert second_resp.get_json()["version"] == "v2"

    metrics_body = client.get("/metrics").get_data(as_text=True)
    assert 'http_requests_total{endpoint="/",method="GET",status="500"} 1.0' in metrics_body
    assert 'http_requests_total{endpoint="/",method="GET",status="200"} 1.0' in metrics_body


def test_deterministic_latency_injection() -> None:
    recorded_sleeps: list[float] = []
    rng_values = iter([0.20, 0.90])

    app = create_app(
        env={
            "FAILURE_MODE": "latency",
            "FAILURE_RATE": "0.5",
            "INJECTED_LATENCY_SECONDS": "0.75",
        },
        rng=lambda: next(rng_values),
        sleep_fn=lambda seconds: recorded_sleeps.append(seconds),
    )
    client = app.test_client()

    # First call (rng=0.20 < 0.5) triggers sleep
    resp_1 = client.get("/")
    assert resp_1.status_code == 200
    assert recorded_sleeps == [0.75]

    # Second call (rng=0.90 >= 0.5) does not trigger sleep
    resp_2 = client.get("/")
    assert resp_2.status_code == 200
    assert recorded_sleeps == [0.75]

    # /health and /metrics must not trigger sleep even when rate is 1.0
    client.get("/health")
    client.get("/metrics")
    assert recorded_sleeps == [0.75]


@pytest.mark.parametrize(
    "invalid_env,expected_substr",
    [
        ({"FAILURE_MODE": "chaos_monkey"}, "Invalid FAILURE_MODE"),
        ({"FAILURE_RATE": "-0.1"}, "FAILURE_RATE must be between 0.0 and 1.0"),
        ({"FAILURE_RATE": "1.05"}, "FAILURE_RATE must be between 0.0 and 1.0"),
        ({"FAILURE_RATE": "not-a-float"}, "Invalid FAILURE_RATE"),
        ({"FAILURE_RATE": "nan"}, "FAILURE_RATE must be between 0.0 and 1.0"),
        ({"INJECTED_LATENCY_SECONDS": "-2.0"}, "INJECTED_LATENCY_SECONDS must be >= 0.0"),
        ({"INJECTED_LATENCY_SECONDS": "abc"}, "Invalid INJECTED_LATENCY_SECONDS"),
        ({"APP_VERSION": "   "}, "APP_VERSION must not be empty"),
    ],
)
def test_invalid_configuration_fails_fast_at_startup(
    invalid_env: dict[str, str],
    expected_substr: str,
) -> None:
    with pytest.raises(ConfigError) as exc_info:
        AppConfig.from_env(invalid_env)
    assert expected_substr in str(exc_info.value)