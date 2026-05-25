from fastapi import APIRouter

from app.schemas.agent import AgentReviewRequest, AgentReviewResponse
from app.services.agent_review_service import agent

router = APIRouter(prefix="/agent", tags=["agent"])


@router.post("/review", response_model=AgentReviewResponse, response_model_by_alias=True)
def review_application(request: AgentReviewRequest) -> AgentReviewResponse:
    return agent.review(request)
