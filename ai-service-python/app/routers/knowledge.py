from fastapi import APIRouter, HTTPException

from app.schemas.knowledge import (
    CompletenessCheckRequest,
    CompletenessCheckResponse,
    KnowledgeIndexRequest,
    KnowledgeIndexResponse,
    KnowledgeSearchRequest,
    KnowledgeSearchResponse,
    KnowledgeStatusResponse,
)
from app.services.completeness_service import get_completeness_service
from app.services.knowledge_base_service import get_knowledge_base_service

router = APIRouter(prefix="/knowledge", tags=["knowledge"])


@router.get("/status", response_model=KnowledgeStatusResponse)
def knowledge_status() -> KnowledgeStatusResponse:
    return KnowledgeStatusResponse(**get_knowledge_base_service().get_status())


@router.post("/index", response_model=KnowledgeIndexResponse)
def build_knowledge_index(request: KnowledgeIndexRequest) -> KnowledgeIndexResponse:
    try:
        result = get_knowledge_base_service().build_index(force_rebuild=request.force_rebuild)
        return KnowledgeIndexResponse(**result)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@router.post("/search", response_model=KnowledgeSearchResponse)
def knowledge_search(request: KnowledgeSearchRequest) -> KnowledgeSearchResponse:
    try:
        result = get_knowledge_base_service().search(query=request.query, top_k=request.top_k)
        return KnowledgeSearchResponse(**result)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@router.post("/check-completeness", response_model=CompletenessCheckResponse)
def check_completeness(request: CompletenessCheckRequest) -> CompletenessCheckResponse:
    result = get_completeness_service().check_materials(
        application_type=request.application_type,
        materials=request.materials,
    )
    return CompletenessCheckResponse(**result)
