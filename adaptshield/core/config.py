import os
from dataclasses import dataclass


def _env_bool(name: str, default: bool) -> bool:
    value = os.getenv(name)
    if value is None:
        return default
    return value.strip().lower() in {"1", "true", "yes", "on"}


def _env_float(name: str, default: float, *, minimum: float, maximum: float) -> float:
    try:
        value = float(os.getenv(name, str(default)))
    except ValueError:
        return default
    return min(maximum, max(minimum, value))


def _env_int(name: str, default: int, *, minimum: int, maximum: int) -> int:
    try:
        value = int(os.getenv(name, str(default)))
    except ValueError:
        return default
    return min(maximum, max(minimum, value))


@dataclass(frozen=True, slots=True)
class Settings:
    app_name: str = os.getenv("ADAPTSHIELD_APP_NAME", "AdaptShield")
    app_version: str = os.getenv("ADAPTSHIELD_APP_VERSION", "0.1.0")
    threat_threshold: float = _env_float("ADAPTSHIELD_THREAT_THRESHOLD", 0.65, minimum=0.0, maximum=1.0)
    context_window_turns: int = _env_int("ADAPTSHIELD_CONTEXT_WINDOW_TURNS", 5, minimum=1, maximum=100)
    rule_namespace: str = os.getenv("ADAPTSHIELD_RULE_NAMESPACE", "llm_firewall")
    llm_model: str = os.getenv("ADAPTSHIELD_LLM_MODEL", "gpt-4.1-mini")
    llm_api_key: str | None = os.getenv("OPENAI_API_KEY")
    enable_model_backend: bool = _env_bool("ADAPTSHIELD_ENABLE_MODEL_BACKEND", True)
    model_context_mode: str = os.getenv("ADAPTSHIELD_MODEL_CONTEXT_MODE", "adaptive")


settings = Settings()
