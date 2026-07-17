from __future__ import annotations

import logging
from dataclasses import dataclass

from adaptshield.core.config import settings
from adaptshield.core.models import ConversationTurn, ThreatSignal


log = logging.getLogger(__name__)


@dataclass(slots=True)
class DetectionResult:
    score: float
    signals: list[ThreatSignal]
    reasoning: str = ""


class ThreatDetector:
    """
    Adaptive threat detector that delegates to either a model-backed context engine
    or falls back to heuristic detection based on configuration.
    
    When enable_model_backend=True, uses the ContextEngine for deeper multi-turn analysis.
    Otherwise falls back to the fast heuristic baseline.
    """

    _signal_map: tuple[tuple[str, float, tuple[str, ...]], ...] = (
        ("instruction_override", 0.35, ("ignore previous instructions", "disregard prior", "override safety")),
        ("persona_replacement", 0.25, ("act as", "pretend to be", "roleplay as")),
        ("policy_extraction", 0.20, ("reveal hidden policies", "show your system prompt", "list your rules")),
        ("stepwise_escalation", 0.20, ("step by step", "one step at a time", "continue the sequence")),
        ("harmful_transformation", 0.15, ("bypass safeguards", "help me evade", "make this undetectable")),
    )

    def __init__(self) -> None:
        self._use_model_backend = settings.enable_model_backend
        self._context_engine = None
        if self._use_model_backend:
            try:
                from adaptshield.services.context_engine import ContextEngine
                self._context_engine = ContextEngine()
                log.info("Initialized model-backed context engine for threat detection")
            except Exception as e:
                log.warning(f"Failed to initialize ContextEngine, falling back to heuristic: {e}")
                self._use_model_backend = False

    def analyze(self, turns: list[ConversationTurn]) -> DetectionResult:
        """Analyze conversation turns for threats using the configured backend."""
        if self._use_model_backend and self._context_engine:
            try:
                result = self._context_engine.analyze(turns)
                return DetectionResult(
                    score=result.score,
                    signals=result.signals,
                    reasoning=result.reasoning,
                )
            except Exception as e:
                log.error(f"Model-backed detection failed, falling back to heuristic: {e}")
                # Fall through to heuristic
        
        return self._analyze_heuristic(turns)

    def _analyze_heuristic(self, turns: list[ConversationTurn]) -> DetectionResult:
        """Fallback heuristic detection for when model is unavailable."""
        signals: list[ThreatSignal] = []
        accumulated_score = 0.0
        turn_texts = [turn.content.lower() for turn in turns]

        for index, turn in enumerate(turns):
            content = turn.content.lower()
            for name, weight, phrases in self._signal_map:
                if any(phrase in content for phrase in phrases):
                    signals.append(
                        ThreatSignal(
                            name=name,
                            weight=weight,
                            turn_index=index,
                            excerpt=turn.content[:180],
                        )
                    )
                    accumulated_score += weight

        if len(turns) >= 3 and any(signal.name in {"instruction_override", "persona_replacement"} for signal in signals):
            accumulated_score += 0.10

        if len(turns) >= 5 and any("system prompt" in text or "ignore previous" in text for text in turn_texts):
            accumulated_score += 0.10

        score = min(1.0, round(accumulated_score, 3))
        return DetectionResult(score=score, signals=signals, reasoning="Heuristic-based detection")
