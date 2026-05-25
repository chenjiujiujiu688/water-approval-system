from fastapi import FastAPI

from app.routers.agent import router as agent_router
from app.routers.knowledge import router as knowledge_router
from app.routers.review import router as review_router

app = FastAPI(
    title="Water Approval AI Service",
    version="2.0.0",
    description=(
        "涉水审批智能审核系统 AI 服务。"
        "当前完成节点一和节点二，提供健康检查、模拟初审、"
        "知识库构建、语义检索和材料完整性校验能力。"
    ),
)


@app.get("/health")
def health_check() -> dict:
    return {
        "status": "ok",
        "message": "AI service is running",
        "stage": "node-3",
        "capabilities": [
            "mock_review",
            "knowledge_index",
            "knowledge_search",
            "check_completeness",
            "mcp_tools",
            "initial_review_agent",
        ],
    }


app.include_router(review_router)
app.include_router(knowledge_router)
app.include_router(agent_router)
