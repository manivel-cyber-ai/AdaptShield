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
    weight: float = Field(ge=0.0, le=1.0)
    turn_index: int = Field(ge=0)
    excerpt: str = Field(min_length=1, max_length=180)


class RuleDraft(BaseModel):
    name: str
    dsl: str
    explanation: str


class ConversationAssessment(BaseModel):
    conversation_id: str
    threat_score: float = Field(ge=0.0, le=1.0)
    flagged: bool
    matched_signals: list[ThreatSignal]
    rule: RuleDraft | None = None
    detection_reasoning: str = ""


class HealthResponse(BaseModel):
    status: str
    app: str
    version: str
