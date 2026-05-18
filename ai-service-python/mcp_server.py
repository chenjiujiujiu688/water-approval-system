from __future__ import annotations

import anyio
import mcp.types as types
from mcp.server import NotificationOptions, Server
from mcp.server.stdio import stdio_server

from app.services.future_extensions import (
    check_completeness as run_check_completeness,
    knowledge_search as run_knowledge_search,
)

server = Server("water-approval-knowledge-mcp")


def tool_definitions() -> list[types.Tool]:
    return [
        types.Tool(
            name="knowledge_search",
            description="根据问题从涉水审批知识库中检索相关法规或材料片段。",
            inputSchema={
                "type": "object",
                "properties": {
                    "query": {"type": "string", "description": "用户检索问题"},
                    "top_k": {
                        "type": "integer",
                        "description": "返回结果数量",
                        "default": 4,
                    },
                },
                "required": ["query"],
            },
        ),
        types.Tool(
            name="check_completeness",
            description="对照材料检查清单，判断申请材料是否完整。",
            inputSchema={
                "type": "object",
                "properties": {
                    "application_type": {
                        "type": "string",
                        "description": "申请类型",
                        "default": "default",
                    },
                    "materials": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": "已提交材料名称列表",
                    },
                },
                "required": ["materials"],
            },
        ),
    ]


@server.list_tools()
async def list_tools() -> list[types.Tool]:
    return tool_definitions()


@server.call_tool()
async def call_tool(name: str, arguments: dict) -> list[types.TextContent]:
    if name == "knowledge_search":
        result = run_knowledge_search(
            query=arguments.get("query", ""),
            top_k=int(arguments.get("top_k", 4)),
        )
    elif name == "check_completeness":
        result = run_check_completeness(
            {
                "application_type": arguments.get("application_type", "default"),
                "materials": arguments.get("materials", []),
            }
        )
    else:
        raise ValueError(f"Unknown tool: {name}")

    return [types.TextContent(type="text", text=str(result))]


async def main() -> None:
    async with stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream,
            write_stream,
            server.create_initialization_options(
                notification_options=NotificationOptions(),
            ),
        )


if __name__ == "__main__":
    anyio.run(main)
