# 涉水审批智能审核系统 - 节点一项目基础架构

本项目用于完成《方向模块课程实践》中“涉水审批智能审核系统”的节点一任务。当前版本只实现项目基础架构、页面交互、后端占位接口、数据库结构和团队协作文档，不提前实现节点二、节点三中的真实知识库、MCP、Agent 审核逻辑。

## 1. 项目目录结构

```text
water-approval-system/
├── frontend/                 # Vue 3 前端
├── backend-java/             # Spring Boot 3.x 主后端
├── ai-service-python/        # FastAPI AI 服务
├── database/                 # 数据库初始化脚本
├── docs/                     # 团队分工等文档
├── .gitignore
└── README.md
```

## 2. 节点一完成内容

- AI 开发环境说明：已在本 README 中补充 Codex 等 AI 工具推荐与使用方式。
- 前端页面：已完成申请列表、新建申请、初审结果 3 个页面。
- Java Web 框架：已完成 Spring Boot 项目、RESTful API、CORS、文件上传、本地存储、Python 调用占位 Service。
- Python 开发环境：已完成 FastAPI 启动文件、依赖文件、健康检查和模拟初审接口。
- 结构化数据库：已提供 `users`、`applications`、`application_files`、`review_results` 表结构。
- 团队分工与 Git：已补充 `docs/team.md` 和 Git 提交规范示例。

## 3. 推荐 AI 辅助开发环境

### 3.1 推荐工具

- Codex：适合快速生成课程项目骨架、接口代码、README、测试样例。
- ChatGPT / OpenAI API：适合辅助撰写接口文档、调试思路、重构建议。
- GitHub Copilot：适合在 IDE 中补全常规前后端代码。

### 3.2 在本项目中的推荐使用方式

1. 用 Codex 初始化目录结构、接口骨架和课程设计说明文档。
2. 用 AI 辅助生成表单、DTO、实体类、SQL 脚本等重复性内容。
3. 用 AI 检查命名一致性、接口字段、README 部署步骤。
4. 节点二、节点三阶段可继续用 AI 辅助接入 LangChain、ChromaDB、MCP Server。

### 3.3 Codex 使用建议

适用于本项目的典型提问方式：

- “为 Spring Boot 增加涉水申请上传接口，并保存附件到本地 uploads 目录”
- “为 Vue 3 生成申请列表、新建申请、初审结果三个页面”
- “为 FastAPI 预留知识库检索和完整性校验工具接口，但不要实现真实逻辑”
- “补充课程设计 README、数据库初始化脚本和 Git 提交规范”

建议开发流程：

1. 人工先确定字段、页面与接口边界。
2. 使用 AI 快速生成基础代码。
3. 人工检查字段、业务流程、注释和运行命令。
4. 每完成一个模块就单独提交 Git。

## 4. 技术栈说明

### 前端

- Vue 3
- Vue Router 4
- Axios
- Vite

### Java 后端

- Spring Boot 3.3.x
- Spring Web
- Spring Data JPA
- SQLite / MySQL 可切换
- Maven

### Python AI 服务

- Python 3.8+
- FastAPI
- Uvicorn
- Pydantic

## 5. 环境要求

- Node.js 18+
- Java 17+
- Maven 3.9+
- Python 3.8+
- MySQL 8.x（可选）

## 6. 运行方式

### 6.1 前端启动

```bash
cd frontend
npm install
npm run dev
```

默认地址：

- [http://localhost:5173](http://localhost:5173)

如果 PowerShell 拦截 `npm`，请改用：

```bash
npm.cmd run dev
```

### 6.2 Java 后端启动

```bash
cd backend-java
mvn spring-boot:run
```

默认地址：

- [http://localhost:8080](http://localhost:8080)

### 6.3 Python AI 服务启动

```bash
cd ai-service-python
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
uvicorn main:app --reload --port 8001
```

默认地址：

- [http://localhost:8001](http://localhost:8001)

## 7. 前后端与 AI 服务接口说明

### 7.1 前端调用 Java 后端

- `POST /api/applications`：新建申请并上传多个附件
- `GET /api/applications`：获取申请列表
- `GET /api/applications/{id}`：获取申请详情
- `GET /api/applications/{id}/review`：获取初审结果占位数据

### 7.2 Java 预留调用 Python 服务

当前 `PythonAiClient` 暂时只返回模拟审核结果，后续节点将替换为真实 HTTP 调用：

- Python 健康检查：`GET /health`
- Python 模拟初审：`POST /review/mock`

## 8. 数据库配置方法

### 8.1 默认方案：SQLite

本项目默认使用 SQLite，便于课程设计快速启动，无需额外安装数据库。

默认数据库文件：

- `backend-java/data/water_approval.db`

默认配置文件：

- `backend-java/src/main/resources/application.yml`

### 8.2 切换到 MySQL

1. 创建数据库，例如 `water_approval_system`
2. 执行 `database/init_mysql.sql`
3. 修改 `backend-java/src/main/resources/application-mysql.yml`
4. 使用如下命令启动：

```bash
cd backend-java
mvn spring-boot:run "-Dspring-boot.run.profiles=mysql"
```

## 9. 数据库表结构说明

当前节点一已覆盖以下基础表：

- `users`：存储申请人或经办人基础信息
- `applications`：存储取水申请主体信息
- `application_files`：存储附件信息
- `review_results`：存储初审结果

初始化脚本：

- `database/init_sqlite.sql`
- `database/init_mysql.sql`

## 10. 节点一扩展预留点

当前只做占位，不实现真实 AI 审核逻辑，但已预留后续扩展接口：

- Python 后续接入 LangChain：`ai-service-python/app/services/future_extensions.py`
- Python 后续接入 ChromaDB：`ai-service-python/app/services/future_extensions.py`
- Python 后续实现 MCP Server：`ai-service-python/app/services/future_extensions.py`
- Python 后续实现 `knowledge_search` 和 `check_completeness` 工具：`ai-service-python/app/services/future_extensions.py`
- Java 后续通过 HTTP 调用 Python 真实初审接口：`backend-java/src/main/java/com/waterapproval/service/PythonAiClient.java`
- 前端后续展示真实初审结果列表：`frontend/src/views/ReviewResultView.vue`

## 11. Git 提交规范

建议采用 Conventional Commits 风格：

- `feat`：新功能
- `fix`：修复问题
- `docs`：文档更新
- `refactor`：重构
- `style`：样式调整
- `chore`：工程配置

推荐提交粒度：

1. 一个功能点对应一次提交。
2. 前端、后端、Python、数据库、文档尽量分开提交。
3. 每次提交前确认项目可运行或至少结构完整。

### 示例提交信息

- `feat(frontend): 初始化 Vue 页面与路由结构`
- `feat(backend): 初始化 Spring Boot 申请接口与 CORS 配置`
- `feat(ai): 初始化 FastAPI 健康检查与模拟审核接口`
- `feat(db): 添加用户、申请、附件、初审结果表结构`
- `docs: 添加团队分工、运行说明与 Git 提交规范`

## 12. 团队分工建议

团队分工文档见：

- [docs/team.md](./docs/team.md)

## 13. 课程检查建议

教师检查节点一时，建议重点演示：

1. 前端 3 个页面跳转与表单填写。
2. 新建申请页面上传多个附件并提交。
3. Java 后端返回申请列表、申请详情、初审结果。
4. Python FastAPI 健康检查和模拟审核接口可访问。
5. 数据库脚本、团队分工、Git 提交规范齐全。
