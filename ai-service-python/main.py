from fastapi import FastAPI

from app.routers.review import router as review_router

app = FastAPI(
    title="Water Approval AI Service",
    version="1.0.0",
    description="节点一阶段的 FastAPI 占位服务，后续可扩展为真实 AI 审核服务。",
)


@app.get("/health")
def health_check():
    return {"status": "ok", "message": "AI service is running"}


app.include_router(review_router)

