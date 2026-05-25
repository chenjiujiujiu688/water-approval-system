from __future__ import annotations

from app.services.future_extensions import check_completeness, knowledge_search


class McpToolBridge:
    def call_knowledge_search(self, query: str, top_k: int = 4) -> dict:
        return knowledge_search(query=query, top_k=top_k)

    def call_check_completeness(self, materials: list[str], application_type: str = "default") -> dict:
        return check_completeness(
            {
                "application_type": application_type,
                "materials": materials,
            }
        )
