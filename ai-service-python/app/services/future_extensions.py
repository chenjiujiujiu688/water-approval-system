"""
后续节点扩展预留文件。

当前节点一只保留接口和目录结构，不实现真实逻辑。

可在后续阶段继续扩展：
1. LangChain 工作流编排
2. ChromaDB 向量知识库
3. MCP Server 对外工具服务
4. knowledge_search 工具
5. check_completeness 工具
"""


def knowledge_search(query: str) -> dict:
    return {
        "implemented": False,
        "message": "knowledge_search 将在后续节点实现。"
    }


def check_completeness(payload: dict) -> dict:
    return {
        "implemented": False,
        "message": "check_completeness 将在后续节点实现。"
    }


class McpServerPlaceholder:
    def describe(self) -> dict:
        return {
            "implemented": False,
            "message": "MCP Server 将在后续节点实现。"
        }

