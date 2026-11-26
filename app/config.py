from dataclasses import dataclass
import math
import os
from typing import Mapping

VALID_FAILURE_MODES = frozenset({"none", "http_500", "latency"})


class ConfigError(ValueError):
    """Raised when startup environment configuration is invalid."""


@dataclass(frozen=True)
class AppConfig:
    app_name: str
    app_version: str
    failure_mode: str
    failure_rate: float
    injected_latency_seconds: float

    @classmethod
    def from_env(cls, env: Mapping[str, str] | None = None) -> "AppConfig":
        source = env if env is not None else os.environ

        app_name = source.get("APP_NAME", "canary-demo-app").strip()
        if not app_name:
            raise ConfigError("APP_NAME must not be empty.")

        app_version = source.get("APP_VERSION", "v1").strip()
        if not app_version:
            raise ConfigError("APP_VERSION must not be empty.")

        failure_mode = source.get("FAILURE_MODE", "none").strip().lower()
        if failure_mode not in VALID_FAILURE_MODES:
            allowed = ", ".join(sorted(VALID_FAILURE_MODES))
            raise ConfigError(
                f"Invalid FAILURE_MODE '{failure_mode}'. Must be one of: {allowed}."
            )

        raw_rate = source.get("FAILURE_RATE", "0.0").strip()
        try:
            failure_rate = float(raw_rate)
        except ValueError as exc:
            raise ConfigError(
                f"Invalid FAILURE_RATE '{raw_rate}'. Must be a float between 0.0 and 1.0."
            ) from exc

        if not math.isfinite(failure_rate) or not (0.0 <= failure_rate <= 1.0):
            raise ConfigError(
                f"FAILURE_RATE must be between 0.0 and 1.0 inclusive (got {failure_rate})."
            )

        raw_latency = source.get("INJECTED_LATENCY_SECONDS", "0.0").strip()
        try:
            injected_latency_seconds = float(raw_latency)
        except ValueError as exc:
            raise ConfigError(
                f"Invalid INJECTED_LATENCY_SECONDS '{raw_latency}'. Must be a non-negative number."
            ) from exc

        if not math.isfinite(injected_latency_seconds) or injected_latency_seconds < 0.0:
            raise ConfigError(
                f"INJECTED_LATENCY_SECONDS must be >= 0.0 (got {injected_latency_seconds})."
            )

        return cls(
            app_name=app_name,
            app_version=app_version,
            failure_mode=failure_mode,
            failure_rate=failure_rate,
            injected_latency_seconds=injected_latency_seconds,
        )