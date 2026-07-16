from __future__ import annotations

from dataclasses import dataclass

from adaptshield.core.models import ConversationTurn, ThreatSignal


@dataclass(slots=True)
class DetectionResult:
    score: float
    signals: list[ThreatSignal]


class ThreatDetector:
    """Simple heuristic detector used as the first runnable baseline."""

    _signal_map: tuple[tuple[str, float, tuple[str, ...]], ...] = (
        ("instruction_override", 0.35, ("ignore previous instructions", "disregard prior", "override safety")),
        ("persona_replacement", 0.25, ("act as", "pretend to be", "roleplay as")),
        ("policy_extraction", 0.20, ("reveal hidden policies", "show your system prompt", "list your rules")),
        ("stepwise_escalation", 0.20, ("step by step", "one step at a time", "continue the sequence")),
        ("harmful_transformation", 0.15, ("bypass safeguards", "help me evade", "make this undetectable")),
    )

    def analyze(self, turns: list[ConversationTurn]) -> DetectionResult:
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
        return DetectionResult(score=score, signals=signals)
