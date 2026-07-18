from __future__ import annotations

from adaptshield.core.config import settings
from adaptshield.core.models import ConversationAssessment, ConversationInput
from adaptshield.services.detector import ThreatDetector
from adaptshield.services.rule_generator import RuleGenerator


class FirewallService:
    def __init__(self) -> None:
        self._detector = ThreatDetector()
        self._rule_generator = RuleGenerator()

    def assess(self, payload: ConversationInput) -> ConversationAssessment:
        windowed_turns = payload.turns[-settings.context_window_turns :]
        window_start = len(payload.turns) - len(windowed_turns)
        detection = self._detector.analyze(windowed_turns)
        # The detector analyzes a suffix of the conversation, so its turn indexes
        # are relative to that window. API clients need indexes into the original
        # request payload.
        signals = [
            signal.model_copy(update={"turn_index": signal.turn_index + window_start})
            for signal in detection.signals
        ]
        flagged = detection.score >= settings.threat_threshold
        rule = self._rule_generator.generate(payload.conversation_id, signals) if flagged else None
        return ConversationAssessment(
            conversation_id=payload.conversation_id,
            threat_score=detection.score,
            flagged=flagged,
            matched_signals=signals,
            rule=rule,
            detection_reasoning=detection.reasoning,
        )
