from fastapi import APIRouter, HTTPException

from adaptshield.core.models import ConversationAssessment, ConversationInput
from adaptshield.services.firewall import FirewallService

router = APIRouter(tags=["conversations"])
service = FirewallService()


@router.post("/analyze", response_model=ConversationAssessment)
def analyze_conversation(payload: ConversationInput) -> ConversationAssessment:
    assessment = service.assess(payload)
    return assessment
