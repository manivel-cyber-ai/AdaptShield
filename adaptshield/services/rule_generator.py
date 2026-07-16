from __future__ import annotations

from adaptshield.core.models import RuleDraft, ThreatSignal


class RuleGenerator:
    def generate(self, conversation_id: str, signals: list[ThreatSignal]) -> RuleDraft:
        signal_names = sorted({signal.name for signal in signals})
        conditions = " AND ".join(f'conversation_contains(signal="{name}")' for name in signal_names)
        if not conditions:
            conditions = 'conversation_contains(signal="unknown")'

        dsl = (
            f'RULE: IF conversation_id="{conversation_id}" AND {conditions} '
            'THEN block AND log AND retrain'
        )
        explanation = (
            "Automatically drafted from matched attack signals so the firewall can "
            "store a reusable defense for similar conversations."
        )
        return RuleDraft(name=f"block_{conversation_id}", dsl=dsl, explanation=explanation)
