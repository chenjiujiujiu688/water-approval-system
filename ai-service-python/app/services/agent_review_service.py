from __future__ import annotations

import re
from datetime import date, datetime
from pathlib import Path

from app.schemas.agent import AgentIssue, AgentReviewRequest, AgentReviewResponse
from app.services.document_parser import DocumentParser
from app.services.mcp_tool_bridge import McpToolBridge


class InitialReviewAgent:
    def __init__(self) -> None:
        self.parser = DocumentParser()
        self.tools = McpToolBridge()

    def review(self, request: AgentReviewRequest) -> AgentReviewResponse:
        parsed_files = self._parse_files(request)
        submitted_materials = [file.original_name for file in request.files]
        completeness = self.tools.call_check_completeness(submitted_materials)
        knowledge = self.tools.call_knowledge_search(self._build_query(request), top_k=5)

        issues: list[AgentIssue] = []
        issues.extend(self._check_required_fields(request))
        issues.extend(self._check_completeness(completeness))
        issues.extend(self._check_file_content(parsed_files))
        issues.extend(self._check_business_rules(request, parsed_files, knowledge))

        review_status = "APPROVED" if not issues else "NEEDS_REVISION"
        risk_level = self._risk_level(issues)
        knowledge_sources = self._knowledge_sources(knowledge)
        summary = self._build_summary(request, review_status, risk_level, issues, completeness)
        suggestions = self._build_suggestions(issues)

        return AgentReviewResponse(
            application_id=request.application_id,
            review_status=review_status,
            risk_level=risk_level,
            summary=summary,
            suggestions=suggestions,
            issues=issues,
            knowledge_sources=knowledge_sources,
            completeness_rate=float(completeness.get("completion_rate", 0.0)),
            reviewed_at=datetime.now().isoformat(timespec="seconds"),
        )

    def _parse_files(self, request: AgentReviewRequest) -> dict[str, str]:
        parsed: dict[str, str] = {}
        for file in request.files:
            path = Path(file.storage_path)
            if not path.exists():
                parsed[file.original_name] = f"附件文件不存在: {file.storage_path}"
                continue
            try:
                parsed[file.original_name] = self.parser.parse_file(path).content
            except Exception as exc:
                parsed[file.original_name] = f"附件解析失败: {exc}"
        return parsed

    def _build_query(self, request: AgentReviewRequest) -> str:
        return (
            f"取水许可申请初审规则。用途：{request.water_usage}；"
            f"地点：{request.water_location}；期限：{request.application_period}；"
            "需要提交哪些材料，哪些内容需要合规检查？"
        )

    def _check_required_fields(self, request: AgentReviewRequest) -> list[AgentIssue]:
        checks = {
            "申请标题": request.title,
            "申请人姓名": request.applicant_name,
            "所属单位": request.organization_name,
            "联系电话": request.contact_phone,
            "取水用途": request.water_usage,
            "取水地点": request.water_location,
            "申请期限": request.application_period,
        }
        issues = []
        for field_name, value in checks.items():
            if not value or not str(value).strip():
                issues.append(
                    AgentIssue(
                        category="内容规范",
                        severity="HIGH",
                        message=f"{field_name}为空或未填写。",
                        suggestion=f"请补充{field_name}后重新提交。",
                    )
                )

        if "其他" in request.water_usage and not (request.description and request.description.strip()):
            issues.append(
                AgentIssue(
                    category="内容规范",
                    severity="MEDIUM",
                    message="取水用途选择或填写为“其他”，但未补充具体用途说明。",
                    suggestion="请在补充说明中写明具体取水用途和使用场景。",
                )
            )
        return issues

    def _check_completeness(self, completeness: dict) -> list[AgentIssue]:
        issues = []
        for item in completeness.get("missing_items", []):
            issues.append(
                AgentIssue(
                    category="形式审查",
                    severity="HIGH",
                    message=f"缺少必备材料：{item.get('material_name')}",
                    suggestion=item.get("description", "请补齐该材料。"),
                )
            )
        return issues

    def _check_file_content(self, parsed_files: dict[str, str]) -> list[AgentIssue]:
        issues = []
        for filename, content in parsed_files.items():
            lowered_name = filename.lower()
            normalized_content = content.lower()
            if "身份证" in filename and ("driving license" in normalized_content or "驾驶证" in content):
                issues.append(
                    AgentIssue(
                        category="实质合规",
                        severity="HIGH",
                        message=f"文件名为身份证材料，但内容疑似驾驶证：{filename}",
                        suggestion="请上传真实身份证明材料，避免证照类型不一致。",
                        evidence=content[:180],
                    )
                )
            if "驾驶证" in filename or "driving license" in normalized_content or "机动车驾驶证" in content:
                issues.append(
                    AgentIssue(
                        category="实质合规",
                        severity="HIGH",
                        message=f"证件类型不符合身份证明要求：{filename}",
                        suggestion="取水许可申请应上传身份证或经办人身份证明，驾驶证不能替代身份证明材料。",
                        evidence=content[:180],
                    )
                )
            expired_period = self._find_expired_valid_period(content)
            if expired_period and self._is_identity_or_license_file(filename, content):
                issues.append(
                    AgentIssue(
                        category="实质合规",
                        severity="HIGH",
                        message=f"证照材料已过有效期：{filename}",
                        suggestion=(
                            f"系统识别到有效期截至 {expired_period}，请上传仍在有效期内的身份证明或营业执照材料。"
                        ),
                        evidence=content[:220],
                    )
                )
            if "营业执照" in filename and "ocr 解析失败" in content:
                issues.append(
                    AgentIssue(
                        category="非结构化文档",
                        severity="MEDIUM",
                        message=f"营业执照图片未能可靠识别：{filename}",
                        suggestion="请上传清晰营业执照扫描件或 PDF/DOCX 版本。",
                        evidence=content[:180],
                    )
                )
            if lowered_name.endswith((".jpg", ".jpeg", ".png")) and "未安装 OCR" in content:
                issues.append(
                    AgentIssue(
                        category="非结构化文档",
                        severity="MEDIUM",
                        message=f"图片材料未完成 OCR 识别：{filename}",
                        suggestion="请确认系统安装 OCR 引擎，或上传清晰 PDF/DOCX 材料。",
                    )
                )
        return issues

    def _is_identity_or_license_file(self, filename: str, content: str) -> bool:
        keywords = ("身份证", "营业执照", "法人证书", "证照", "居民身份证", "营业期限")
        return any(keyword in filename or keyword in content for keyword in keywords)

    def _find_expired_valid_period(self, content: str) -> str | None:
        for start_raw, end_raw in re.findall(
            r"(\d{4}[.\-/年]\d{1,2}[.\-/月]\d{1,2}日?)\s*[-至到]\s*(\d{4}[.\-/年]\d{1,2}[.\-/月]\d{1,2}日?)",
            content,
        ):
            end_date = self._parse_date(end_raw)
            if end_date and end_date < date.today():
                return end_date.isoformat()
        return None

    def _parse_date(self, value: str) -> date | None:
        parts = re.findall(r"\d+", value)
        if len(parts) < 3:
            return None
        try:
            return date(int(parts[0]), int(parts[1]), int(parts[2]))
        except ValueError:
            return None

    def _check_business_rules(
        self,
        request: AgentReviewRequest,
        parsed_files: dict[str, str],
        knowledge: dict,
    ) -> list[AgentIssue]:
        issues = []
        combined_text = "\n".join(parsed_files.values())
        if request.applicant_name and combined_text and request.applicant_name not in combined_text:
            issues.append(
                AgentIssue(
                    category="内容规范",
                    severity="LOW",
                    message="申请人姓名未在已解析附件中形成明显匹配。",
                    suggestion="请人工复核申请表、身份证明和营业执照中的主体信息是否一致。",
                )
            )

        if not knowledge.get("hits"):
            issues.append(
                AgentIssue(
                    category="合规审查",
                    severity="MEDIUM",
                    message="未从知识库检索到可用法规或办理依据。",
                    suggestion="请先确认知识库索引已构建，并补充取水许可相关法规材料。",
                )
            )
        return issues

    def _risk_level(self, issues: list[AgentIssue]) -> str:
        severities = {issue.severity for issue in issues}
        if "HIGH" in severities:
            return "HIGH"
        if "MEDIUM" in severities:
            return "MEDIUM"
        if "LOW" in severities:
            return "LOW"
        return "LOW"

    def _knowledge_sources(self, knowledge: dict) -> list[str]:
        sources = []
        for hit in knowledge.get("hits", []):
            source = hit.get("source", "")
            if source and source not in sources:
                sources.append(source)
        return sources

    def _build_summary(
        self,
        request: AgentReviewRequest,
        review_status: str,
        risk_level: str,
        issues: list[AgentIssue],
        completeness: dict,
    ) -> str:
        status_text = "通过" if review_status == "APPROVED" else "需补正"
        return (
            f"Agent 已完成申请《{request.title}》的初审。"
            f"结论：{status_text}；风险等级：{risk_level}；"
            f"材料完整率：{completeness.get('completion_rate', 0.0):.0%}；"
            f"发现问题 {len(issues)} 项。"
        )

    def _build_suggestions(self, issues: list[AgentIssue]) -> str:
        if not issues:
            return "材料完整性和基础合规性初审未发现明显问题，可进入人工复核。"
        return "\n".join(
            f"{index}. [{issue.category}] {issue.message} 建议：{issue.suggestion}"
            for index, issue in enumerate(issues, start=1)
        )


agent = InitialReviewAgent()
