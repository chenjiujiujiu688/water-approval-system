from __future__ import annotations

import hashlib
from typing import Iterable
from pathlib import Path

from langchain_core.embeddings import Embeddings
from langchain_huggingface import HuggingFaceEmbeddings

from app.config import settings


class SimpleHashEmbeddings(Embeddings):
    def __init__(self, dimension: int = 384) -> None:
        self.dimension = dimension

    def embed_documents(self, texts: list[str]) -> list[list[float]]:
        return [self._embed_text(text) for text in texts]

    def embed_query(self, text: str) -> list[float]:
        return self._embed_text(text)

    def _embed_text(self, text: str) -> list[float]:
        vector = [0.0] * self.dimension
        for token in self._tokenize(text):
            digest = hashlib.sha256(token.encode("utf-8")).digest()
            for index, value in enumerate(digest):
                vector[(index * 13 + value) % self.dimension] += value / 255.0

        norm = sum(item * item for item in vector) ** 0.5 or 1.0
        return [item / norm for item in vector]

    def _tokenize(self, text: str) -> Iterable[str]:
        return (token for token in text.replace("\n", " ").split(" ") if token)


def build_embeddings_provider() -> tuple[Embeddings, str]:
    local_model_path = _resolve_local_model_path()
    if local_model_path is not None:
        embeddings = HuggingFaceEmbeddings(
            model_name=str(local_model_path),
            model_kwargs={
                "device": settings.embedding_device,
                "local_files_only": True,
            },
            encode_kwargs={"normalize_embeddings": True},
        )
        return embeddings, str(local_model_path)

    if not settings.allow_remote_embedding_download:
        return SimpleHashEmbeddings(), "simple-hash-fallback"

    try:
        embeddings = HuggingFaceEmbeddings(
            model_name=settings.embedding_model_name,
            model_kwargs={"device": settings.embedding_device},
            encode_kwargs={"normalize_embeddings": True},
        )
        return embeddings, settings.embedding_model_name
    except Exception:
        return SimpleHashEmbeddings(), "simple-hash-fallback"


def _resolve_local_model_path() -> Path | None:
    if settings.embedding_model_path:
        candidate = Path(settings.embedding_model_path)
        if candidate.exists():
            return candidate

    model_cache_root = (
        Path.home()
        / ".cache"
        / "huggingface"
        / "hub"
        / "models--sentence-transformers--paraphrase-multilingual-MiniLM-L12-v2"
        / "snapshots"
    )
    if not model_cache_root.exists():
        return None

    for snapshot_dir in sorted(model_cache_root.iterdir(), reverse=True):
        if snapshot_dir.is_dir():
            return snapshot_dir
    return None
