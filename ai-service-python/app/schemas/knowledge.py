from __future__ import annotations

from pydantic import BaseModel, Field


class KnowledgeIndexRequest(BaseModel):
    force_rebuild: bool = Field(True, description="是否重建向量库")


class KnowledgeIndexResponse(BaseModel):
    indexed: bool
    document_count: int
    chunk_count: int
    embedding_backend: str
    source_files: list[str]


class KnowledgeSearchRequest(BaseModel):
    query: str = Field(..., min_length=1, description="检索问题")
    top_k: int = Field(4, ge=1, le=10, description="返回结果数量")


class KnowledgeSearchHit(BaseModel):
    content: str
    source: str
    source_path: str
    file_type: str
    chunk_index: int
    similarity_score: float
    distance_score: float


class KnowledgeSearchResponse(BaseModel):
    query: str
    total: int
    embedding_backend: str
    hits: list[KnowledgeSearchHit]


class CompletenessCheckRequest(BaseModel):
    application_type: str = Field("default", description="申请类型")
    materials: list[str] = Field(default_factory=list, description="已提交材料名称列表")


class CompletenessItem(BaseModel):
    material_name: str
    description: str
    status: str


class CompletenessCheckResponse(BaseModel):
    application_type: str
    submitted_count: int
    required_count: int
    completion_rate: float
    present_items: list[CompletenessItem]
    missing_items: list[CompletenessItem]


class KnowledgeStatusResponse(BaseModel):
    raw_document_count: int
    supported_document_count: int
    indexed: bool
    indexed_document_count: int
    indexed_chunk_count: int
    embedding_backend: str
    raw_documents_dir: str
    chroma_dir: str
