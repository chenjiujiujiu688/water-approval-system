from app.schemas.review import MockReviewRequest, MockReviewResponse


def generate_mock_review(request: MockReviewRequest) -> MockReviewResponse:
    return MockReviewResponse(
        application_id=request.application_id,
        review_status="MOCK_APPROVED",
        risk_level="LOW",
        summary=(
            f"申请《{request.title}》已完成节点一/节点二阶段的模拟初审，"
            "当前主要用于验证前后端联通、知识库检索接口和 AI 服务基础能力。"
        ),
        suggestions=(
            "建议在节点三中接入真实审核流程，将知识库检索、"
            "材料完整性校验结果与 Agent 决策流程整合。"
        ),
        future_extension_note=(
            "Node 2 ready: LangChain, ChromaDB, MCP knowledge_search, "
            "MCP check_completeness. Node 3 agent orchestration is not enabled yet."
        ),
    )
