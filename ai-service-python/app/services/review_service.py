from app.schemas.review import MockReviewRequest, MockReviewResponse


def generate_mock_review(request: MockReviewRequest) -> MockReviewResponse:
    return MockReviewResponse(
        application_id=request.application_id,
        review_status="MOCK_APPROVED",
        risk_level="LOW",
        summary=(
            f"申请《{request.title}》已完成节点一模拟初审，"
            f"当前仅验证系统流程与接口联通。"
        ),
        suggestions="后续节点将接入真实知识库检索、材料完整性校验和智能体审核能力。",
        future_extension_note=(
            "Reserved for LangChain, ChromaDB, MCP Server, knowledge_search and "
            "check_completeness tools."
        ),
    )

