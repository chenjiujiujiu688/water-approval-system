from fastapi import APIRouter

from app.schemas.review import MockReviewRequest, MockReviewResponse
from app.services.review_service import generate_mock_review

router = APIRouter(prefix="/review", tags=["review"])


@router.post("/mock", response_model=MockReviewResponse)
def mock_review(request: MockReviewRequest) -> MockReviewResponse:
    return generate_mock_review(request)

