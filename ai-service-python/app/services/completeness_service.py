from __future__ import annotations

import json
import re
from functools import lru_cache

from app.config import settings


class CompletenessService:
    def __init__(self) -> None:
        if not settings.checklist_file.exists():
            raise FileNotFoundError(f"未找到检查清单文件: {settings.checklist_file}")
        self.checklists = json.loads(settings.checklist_file.read_text(encoding="utf-8"))

    def check_materials(self, application_type: str, materials: list[str]) -> dict:
        checklist = self.checklists.get(application_type) or self.checklists.get("default", [])
        normalized_input = {self._normalize_name(material) for material in materials}

        present_items = []
        missing_items = []

        for item in checklist:
            aliases = {self._normalize_name(alias) for alias in item.get("aliases", [])}
            aliases.add(self._normalize_name(item["material_name"]))
            target_list = present_items if aliases & normalized_input else missing_items
            target_list.append(
                {
                    "material_name": item["material_name"],
                    "description": item["description"],
                    "status": "present" if target_list is present_items else "missing",
                }
            )

        completion_rate = 0.0
        if checklist:
            completion_rate = round(len(present_items) / len(checklist), 4)

        return {
            "application_type": application_type,
            "submitted_count": len(materials),
            "required_count": len(checklist),
            "completion_rate": completion_rate,
            "present_items": present_items,
            "missing_items": missing_items,
        }

    def _normalize_name(self, value: str) -> str:
        return re.sub(r"\s+", "", value).lower()


@lru_cache(maxsize=1)
def get_completeness_service() -> CompletenessService:
    return CompletenessService()
