from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class Settings:
    app_name: str = "AdaptShield"
    app_version: str = "0.1.0"
    threat_threshold: float = 0.65
    context_window_turns: int = 5
    rule_namespace: str = "llm_firewall"
    llm_model: str = "gpt-4-turbo-preview"
    llm_api_key: str | None = None
    enable_model_backend: bool = True
    model_context_mode: str = "adaptive"  # "adaptive" or "summary"


settings = Settings()
