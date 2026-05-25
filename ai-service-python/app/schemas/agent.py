from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field


def to_camel(value: str) -> str:
    parts = value.split("_")
    return parts[0] + "".join(part.capitalize() for part in parts[1:])


class CamelModel(BaseModel):
    model_config = ConfigDict(alias_generator=to_camel, populate_by_name=True)


class AgentFileItem(CamelModel):
    original_name: str
    storage_path: str
    content_type: str | None = None


class AgentReviewRequest(CamelModel):
    application_id: int
    title: str
    applicant_name: str
    organization_name: str
    contact_phone: str | None = None
    email: str | None = None
    water_usage: str
    water_location: str
    application_period: str
    description: str | None = None
    files: list[AgentFileItem] = Field(default_factory=list)


class AgentIssue(CamelModel):
    category: str
    severity: str
    message: str
    suggestion: str
    evidence: str | None = None


class AgentReviewResponse(CamelModel):
    application_id: int
    review_status: str
    risk_level: str
    summary: str
    suggestions: str
    issues: list[AgentIssue]
    knowledge_sources: list[str]
    completeness_rate: float
    reviewed_at: str
