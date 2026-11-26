import random
import time
from typing import Callable, Mapping

from flask import Flask, Response, g, jsonify, request
from prometheus_client import CONTENT_TYPE_LATEST, CollectorRegistry, generate_latest

from app.config import AppConfig
from app.metrics import MetricsContainer, resolve_bounded_endpoint


def should_inject_failure(failure_rate: float, rng: Callable[[], float]) -> bool:
    """Evaluate whether the current request should trigger failure injection."""
    if failure_rate <= 0.0:
        return False
    if failure_rate >= 1.0:
        return True
    return rng() < failure_rate


def create_app(
    config: AppConfig | None = None,
    env: Mapping[str, str] | None = None,
    registry: CollectorRegistry | None = None,
    rng: Callable[[], float] = random.random,
    sleep_fn: Callable[[float], None] = time.sleep,
) -> Flask:
    """
    Application factory.
    Validates configuration at startup and wires bounded Prometheus instrumentation.
    """
    app_config = config if config is not None else AppConfig.from_env(env)
    metrics = MetricsContainer(registry=registry)

    app = Flask(__name__)
    app.config["APP_CONFIG"] = app_config
    app.config["METRICS"] = metrics

    @app.before_request
    def start_timer() -> None:
        if request.endpoint == "metrics":
            return
        g.request_start_time = time.perf_counter()

    @app.after_request
    def record_metrics(response: Response) -> Response:
        if request.endpoint == "metrics":
            return response

        start_time = getattr(g, "request_start_time", None)
        bounded_endpoint = resolve_bounded_endpoint(request.endpoint)
        method = request.method
        status_code = str(response.status_code)

        if start_time is not None:
            duration = max(0.0, time.perf_counter() - start_time)
            metrics.http_request_duration_seconds.labels(
                method=method,
                endpoint=bounded_endpoint,
            ).observe(duration)

        metrics.http_requests_total.labels(
            method=method,
            endpoint=bounded_endpoint,
            status=status_code,
        ).inc()

        return response

    @app.get("/")
    def root() -> tuple[Response, int]:
        if app_config.failure_mode == "http_500":
            if should_inject_failure(app_config.failure_rate, rng):
                return (
                    jsonify(
                        {
                            "app": app_config.app_name,
                            "version": app_config.app_version,
                            "error": "Injected HTTP 500 fault",
                        }
                    ),
                    500,
                )
        elif app_config.failure_mode == "latency":
            if (
                app_config.injected_latency_seconds > 0.0
                and should_inject_failure(app_config.failure_rate, rng)
            ):
                sleep_fn(app_config.injected_latency_seconds)

        return (
            jsonify(
                {
                    "app": app_config.app_name,
                    "version": app_config.app_version,
                    "message": f"Hello from {app_config.app_name} ({app_config.app_version})",
                }
            ),
            200,
        )

    @app.get("/health")
    def health() -> tuple[Response, int]:
        return jsonify({"status": "healthy"}), 200

    @app.get("/metrics")
    def metrics_endpoint() -> Response:
        payload = generate_latest(metrics.registry)
        return Response(payload, status=200, content_type=CONTENT_TYPE_LATEST)

    return app


def create_wsgi_app() -> Flask:
    """Entrypoint for Gunicorn WSGI server."""
    return create_app()


if __name__ == "__main__":
    flask_app = create_app()
    flask_app.run(host="0.0.0.0", port=8080)