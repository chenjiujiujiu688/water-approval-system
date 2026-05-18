from app.services.completeness_service import get_completeness_service
from app.services.knowledge_base_service import get_knowledge_base_service


def knowledge_search(query: str, top_k: int = 4) -> dict:
    return get_knowledge_base_service().search(query=query, top_k=top_k)


def check_completeness(payload: dict) -> dict:
    application_type = payload.get("application_type", "default")
    materials = payload.get("materials", [])
    return get_completeness_service().check_materials(
        application_type=application_type,
        materials=materials,
    )


class McpServerPlaceholder:
    def describe(self) -> dict:
        return {
            "implemented": True,
            "server_name": "water-approval-knowledge-mcp",
            "tools": ["knowledge_search", "check_completeness"],
            "stage_note": "Node 2 MCP tools are ready. Node 3 agent flow is still reserved.",
        }
