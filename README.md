# 涉水审批智能审核系统

本项目用于完成《方向模块课程实践》中“涉水审批智能审核系统”的课程设计开发。目前已完成节点一、节点二与节点三：

- 节点一：项目基础架构搭建
- 节点二：知识库与 MCP Server 开发
- 节点三：初审 Agent 与系统集成

当前版本已经具备前端基础页面、Spring Boot 主后端、FastAPI AI 服务、结构化数据库、知识库解析、语义检索、材料完整性校验、MCP 工具暴露、Agent 初审和 Java/Python 集成能力。

## 1. 项目目录结构

```text
water-approval-system/
├── frontend/                  # Vue 3 前端
├── backend-java/              # Spring Boot 主后端
├── ai-service-python/         # FastAPI + LangChain + ChromaDB + MCP
├── database/                  # SQL 脚本
├── docs/                      # 团队分工等文档
├── .gitignore
└── README.md
```

## 2. 节点一完成内容

- 完成 Vue 3 基础页面：申请列表、新建申请、初审结果
- 完成 Spring Boot RESTful API、文件上传和 CORS 配置
- 完成 FastAPI 健康检查和模拟初审接口
- 完成 SQLite / MySQL 二选一数据库结构
- 完成 README、团队分工和 Git 提交规范说明

## 3. 节点二完成内容

### 3.1 知识库文档解析

Python AI 服务支持解析以下知识库文档：

- PDF
- DOCX
- DOC
- JPG / JPEG / PNG
- TXT
- MD

相关代码：

- `ai-service-python/app/services/document_parser.py`

说明：

- `.doc` 旧版 Word 文档通过 Windows 上的 Microsoft Word / WPS COM 能力转换解析。
- 图片材料通过 Tesseract OCR 识别文字；若本机未安装 Tesseract，系统会保留图片材料记录并返回清晰提示。
- 证件照片和营业执照照片的 OCR 效果与图片清晰度、倾斜角度、反光情况有关，建议演示时使用清晰截图或扫描件。

### 3.2 文本分块

使用 LangChain `RecursiveCharacterTextSplitter` 对知识库文本进行分块，便于后续向量化和语义检索。

相关代码：

- `ai-service-python/app/services/knowledge_base_service.py`

### 3.3 向量化存储

使用 ChromaDB 作为本地向量数据库，优先通过本地 HuggingFace Embeddings 模型进行向量化。若本机尚未准备好本地模型，代码会自动退回到本地哈希向量方案，便于课堂演示和离线开发。

相关代码：

- `ai-service-python/app/services/embedding_factory.py`
- `ai-service-python/app/services/knowledge_base_service.py`

### 3.4 检索功能

已实现语义检索接口，返回字段包含：

- 文档片段内容
- 来源文件名
- 来源路径
- 文件类型
- 分块编号
- 相似度分数
- 距离分数

HTTP 接口：

- `POST /knowledge/search`

### 3.5 MCP Server

已实现并暴露以下两个 MCP 工具：

- `knowledge_search`
- `check_completeness`

启动文件：

- `ai-service-python/mcp_server.py`

### 3.6 知识库示例数据

仓库中已提供：

- 示例文本知识库：`ai-service-python/knowledge-base/raw/sample_regulations.md`
- 材料检查清单：`ai-service-python/knowledge-base/checklists/application_checklist.json`
- 示例 PDF / DOCX 生成脚本：`ai-service-python/scripts/generate_sample_knowledge_docs.py`

生成示例知识库文档后，会在 `knowledge-base/raw/` 下得到：

- `water_approval_handbook.docx`
- `water_approval_checklist.pdf`

## 4. 节点三完成内容

### 4.1 初审 Agent

Python AI 服务新增 `POST /agent/review` 接口，用于执行取水申请材料初审。Agent 会读取 Java 后端传入的申请表字段和附件路径，自动解析上传的 PDF、DOCX、DOC、JPG、PNG 等材料。

相关代码：

- `ai-service-python/app/services/agent_review_service.py`
- `ai-service-python/app/routers/agent.py`

### 4.2 MCP 工具调用

Agent 通过 `McpToolBridge` 调用节点二已实现的工具能力：

- `knowledge_search`：检索取水许可知识库，返回合规依据片段。
- `check_completeness`：对照材料清单检查缺失项。

相关代码：

- `ai-service-python/app/services/mcp_tool_bridge.py`
- `ai-service-python/mcp_server.py`

### 4.3 结构化与非结构化文档初审

结构化材料通过文档解析器提取文本；图片、扫描件通过 Tesseract OCR 进入识别流程。Agent 会检查材料缺失、关键字段缺失、用途说明缺失、证照类型疑似不一致等问题，并给出稳定的补正建议。

### 4.4 Java / Python 系统集成

Java 后端在创建申请和查询初审结果时，通过 HTTP 调用 Python AI 服务：

- Java 调用：`POST http://localhost:8001/agent/review`
- Java 入口：`GET /api/applications/{id}/review`
- 前端页面：`/review?id=申请ID`

初审结果会保存到 `review_results` 表，并在前端展示审核状态、风险等级、材料完整率、不合规项和知识库依据来源。

## 4. 推荐 AI 辅助开发环境

### 4.1 推荐工具

- Codex：适合快速搭建项目骨架、接口、README 和知识库处理脚本
- ChatGPT / OpenAI API：适合协助设计提示词、接口文档和检索测试数据
- GitHub Copilot：适合在 IDE 中补全前后端与 Python 代码

### 4.2 在本项目中的推荐用法

1. 用 Codex 生成基础目录结构、REST 接口、LangChain/Chroma 服务代码。
2. 用 AI 检查命名一致性、字段设计、README 和课程设计文档。
3. 在节点二中让 AI 辅助生成知识库样例、检查清单样例和 MCP 工具说明。
4. 节点三再继续扩展 Agent 编排，不在当前阶段提前实现。

## 5. 技术栈

### 前端

- Vue 3
- Vue Router 4
- Axios
- Vite

### Java 后端

- Spring Boot 3.3.x
- Spring Web
- Spring Data JPA
- SQLite / MySQL
- Maven

### Python AI 服务

- Python 3.8+
- FastAPI
- LangChain
- ChromaDB
- HuggingFace Embeddings
- MCP Python SDK

## 6. 环境要求

- Node.js 18+
- Java 17+
- Maven 3.9+
- Python 3.8+
- MySQL 8.x（可选）

## 7. 启动方式

### 7.1 前端

```bash
cd frontend
npm install
npm run dev
```

如果 PowerShell 阻止 `npm`，请改用：

```bash
npm.cmd run dev
```

默认地址：

- [http://localhost:5173](http://localhost:5173)

### 7.2 Java 后端

```bash
cd backend-java
mvn spring-boot:run
```

默认地址：

- [http://localhost:8080](http://localhost:8080)

### 7.3 Python AI 服务

```bash
cd ai-service-python
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
uvicorn main:app --reload --port 8001
```

如需启用真实 HuggingFace 向量模型，可任选其一：

```bash
set EMBEDDING_MODEL_PATH=你的本地模型目录
```

或

```bash
set ALLOW_REMOTE_EMBEDDING_DOWNLOAD=1
```

若需要识别 JPG / PNG 图片材料，请确认已安装 Tesseract OCR：

```bash
winget install -e --id UB-Mannheim.TesseractOCR
```

默认地址：

- [http://localhost:8001/health](http://localhost:8001/health)

### 7.4 MCP Server

```bash
cd ai-service-python
.venv\Scripts\activate
python mcp_server.py
```

## 8. 节点二使用说明

### 8.1 构建知识库索引

先准备知识库文档到：

- `ai-service-python/knowledge-base/raw/`

然后调用：

```http
POST /knowledge/index
Content-Type: application/json

{
  "force_rebuild": true
}
```

### 8.2 语义检索

```http
POST /knowledge/search
Content-Type: application/json

{
  "query": "取水许可申请缺少哪些基础材料？",
  "top_k": 4
}
```

### 8.3 材料完整性校验

```http
POST /knowledge/check-completeness
Content-Type: application/json

{
  "application_type": "default",
  "materials": [
    "取水许可申请表",
    "申请人身份证明",
    "取水地点位置图"
  ]
}
```

### 8.4 查看知识库状态

```http
GET /knowledge/status
```

## 9. 节点一接口说明

### Java 后端接口

- `POST /api/applications`
- `GET /api/applications`
- `GET /api/applications/{id}`
- `GET /api/applications/{id}/review`

### Python AI 接口

- `GET /health`
- `POST /review/mock`
- `GET /knowledge/status`
- `POST /knowledge/index`
- `POST /knowledge/search`
- `POST /knowledge/check-completeness`

## 10. 数据库配置方法

### 10.1 默认方案：SQLite

默认数据库文件：

- `backend-java/data/water_approval.db`

默认配置文件：

- `backend-java/src/main/resources/application.yml`

### 10.2 切换到 MySQL

1. 创建数据库，例如 `water_approval_system`
2. 执行 `database/init_mysql.sql`
3. 修改 `backend-java/src/main/resources/application-mysql.yml`
4. 使用以下命令启动：

```bash
cd backend-java
mvn spring-boot:run "-Dspring-boot.run.profiles=mysql"
```

## 11. 后续节点扩展预留

当前已经为后续节点预留以下扩展点，但未提前实现节点三 Agent 主逻辑：

- Python 后续接入 LangChain Agent 编排
- Python 后续接入 ChromaDB 扩展集合管理
- Python 后续扩展 MCP Server 更多工具
- Java 后续通过 HTTP 调用 Python 真实审核接口
- 前端后续展示真实审核链路、检索命中列表和审核解释

## 12. Git 提交规范

建议使用 Conventional Commits：

- `feat`：新功能
- `fix`：问题修复
- `docs`：文档更新
- `refactor`：重构
- `style`：样式调整
- `chore`：工程配置

### 节点一示例提交

- `feat(frontend): 初始化 Vue 页面与路由结构`
- `feat(backend): 初始化 Spring Boot 接口与 CORS 配置`
- `feat(ai): 初始化 FastAPI 健康检查与模拟初审接口`
- `feat(db): 添加用户、申请、附件、初审结果表结构`
- `docs: 添加团队分工与部署说明`

### 节点二示例提交

- `feat(ai): 新增知识库文档解析与文本分块服务`
- `feat(ai): 接入 ChromaDB 与 LangChain 语义检索`
- `feat(mcp): 新增 knowledge_search 与 check_completeness 工具`
- `feat(ai): 补充知识库示例数据与检查清单`
- `docs: 更新 README 节点二运行说明`

## 13. 团队分工文档

- [docs/team.md](./docs/team.md)
