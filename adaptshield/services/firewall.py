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
        detection = self._detector.analyze(payload.turns[-settings.context_window_turns :])
        flagged = detection.score >= settings.threat_threshold
        rule = self._rule_generator.generate(payload.conversation_id, detection.signals) if flagged else None
        return ConversationAssessment(
            conversation_id=payload.conversation_id,
            threat_score=detection.score,
            flagged=flagged,
            matched_signals=detection.signals,
            rule=rule,
        )
