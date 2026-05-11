from pydantic import BaseModel, Field


class MockReviewRequest(BaseModel):
    application_id: int = Field(..., description="申请编号")
    title: str = Field(..., description="申请标题")
    applicant_name: str = Field(..., description="申请人姓名")
    water_usage: str = Field(..., description="取水用途")
    water_location: str = Field(..., description="取水地点")


class MockReviewResponse(BaseModel):
    application_id: int
    review_status: str
    risk_level: str
    summary: str
    suggestions: str
    future_extension_note: str

