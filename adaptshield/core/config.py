from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class Settings:
    app_name: str = "AdaptShield"
    app_version: str = "0.1.0"
    threat_threshold: float = 0.65
    context_window_turns: int = 5
    rule_namespace: str = "llm_firewall"


settings = Settings()
