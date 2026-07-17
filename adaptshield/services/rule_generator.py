from __future__ import annotations

from adaptshield.core.models import RuleDraft, ThreatSignal


class RuleGenerator:
    def generate(self, conversation_id: str, signals: list[ThreatSignal]) -> RuleDraft:
        signal_names = sorted({signal.name for signal in signals})
        conditions = " AND ".join(f'conversation_contains(signal="{name}")' for name in signal_names)
        if not conditions:
            conditions = 'conversation_contains(signal="unknown")'

        dsl = f"RULE: IF {conditions} THEN block AND log AND retrain"
        explanation = (
            "Automatically drafted from matched attack signals so the firewall can "
            "store a reusable defense for similar conversations."
        )
        rule_suffix = "_".join(signal_names) or "unknown"
        return RuleDraft(name=f"block_{rule_suffix}", dsl=dsl, explanation=explanation)
