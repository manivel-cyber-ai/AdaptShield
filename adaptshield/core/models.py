from __future__ import annotations

from datetime import datetime
from typing import Literal

from pydantic import BaseModel, Field


Role = Literal["system", "developer", "user", "assistant", "tool"]


class ConversationTurn(BaseModel):
    role: Role
    content: str = Field(min_length=1)
    timestamp: datetime | None = None


class ConversationInput(BaseModel):
    conversation_id: str = Field(min_length=1)
    turns: list[ConversationTurn] = Field(min_length=1)


class ThreatSignal(BaseModel):
    name: str
    weight: float
    turn_index: int
    excerpt: str


class RuleDraft(BaseModel):
    name: str
    dsl: str
    explanation: str


class ConversationAssessment(BaseModel):
    conversation_id: str
    threat_score: float
    flagged: bool
    matched_signals: list[ThreatSignal]
    rule: RuleDraft | None = None


class HealthResponse(BaseModel):
    status: str
    app: str
    version: str
