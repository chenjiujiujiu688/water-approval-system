from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class Settings:
    project_root: Path = Path(__file__).resolve().parents[1]
    knowledge_base_root: Path = project_root / "knowledge-base"
    raw_documents_dir: Path = knowledge_base_root / "raw"
    checklist_dir: Path = knowledge_base_root / "checklists"
    chroma_dir: Path = knowledge_base_root / "chroma"
    index_state_path: Path = knowledge_base_root / "index_state.json"
    checklist_file: Path = checklist_dir / "application_checklist.json"
    collection_name: str = os.getenv("KNOWLEDGE_COLLECTION_NAME", "water-approval-knowledge")
    embedding_model_name: str = os.getenv(
        "EMBEDDING_MODEL_NAME",
        "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2",
    )
    embedding_model_path: str = os.getenv("EMBEDDING_MODEL_PATH", "")
    allow_remote_embedding_download: bool = (
        os.getenv("ALLOW_REMOTE_EMBEDDING_DOWNLOAD", "0").lower() in {"1", "true", "yes"}
    )
    embedding_device: str = os.getenv("EMBEDDING_DEVICE", "cpu")
    chunk_size: int = int(os.getenv("CHUNK_SIZE", "450"))
    chunk_overlap: int = int(os.getenv("CHUNK_OVERLAP", "80"))


settings = Settings()
