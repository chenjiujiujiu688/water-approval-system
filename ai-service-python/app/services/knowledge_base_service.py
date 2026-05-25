from __future__ import annotations

import json
import time
from functools import lru_cache

from chromadb.config import Settings as ChromaSettings
from langchain_chroma import Chroma
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter

from app.config import settings
from app.services.document_parser import DocumentParser
from app.services.embedding_factory import build_embeddings_provider


class KnowledgeBaseService:
    def __init__(self) -> None:
        self.parser = DocumentParser()
        self.embeddings, self.embedding_backend = build_embeddings_provider()
        self.splitter = RecursiveCharacterTextSplitter(
            chunk_size=settings.chunk_size,
            chunk_overlap=settings.chunk_overlap,
            separators=["\n\n", "\n", "。", "；", "，", " "],
        )
        self._ensure_directories()

    def build_index(self, force_rebuild: bool = True) -> dict:
        self._ensure_directories()
        parsed_documents = self.parser.parse_directory(settings.raw_documents_dir)
        if not parsed_documents:
            raise ValueError("知识库原始目录为空，请先放入 PDF、DOCX、TXT 或 MD 文档。")

        documents: list[Document] = []
        for parsed in parsed_documents:
            base_document = Document(
                page_content=parsed.content,
                metadata={
                    "source": parsed.source_name,
                    "source_path": str(parsed.path),
                    "file_type": parsed.file_type,
                },
            )
            split_docs = self.splitter.split_documents([base_document])
            for index, chunk in enumerate(split_docs):
                chunk.metadata["chunk_index"] = index
            documents.extend(split_docs)

        collection_name = self._next_collection_name() if force_rebuild else self._active_collection_name()
        vector_store = self._create_vector_store(collection_name=collection_name)
        vector_store.add_documents(documents)

        payload = {
            "indexed": True,
            "collection_name": collection_name,
            "document_count": len(parsed_documents),
            "chunk_count": len(documents),
            "embedding_backend": self.embedding_backend,
            "source_files": [document.source_name for document in parsed_documents],
        }
        settings.index_state_path.write_text(
            json.dumps(payload, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )
        return payload

    def search(self, query: str, top_k: int = 4) -> dict:
        if not settings.chroma_dir.exists():
            raise ValueError("知识库尚未构建，请先调用 /knowledge/index 建立向量库。")

        vector_store = self._create_vector_store(collection_name=self._active_collection_name())
        results = vector_store.similarity_search_with_score(query, k=top_k)
        hits = []
        for document, distance_score in results:
            similarity_score = round(1 / (1 + float(distance_score)), 4)
            hits.append(
                {
                    "content": document.page_content,
                    "source": document.metadata.get("source", ""),
                    "source_path": document.metadata.get("source_path", ""),
                    "file_type": document.metadata.get("file_type", ""),
                    "chunk_index": int(document.metadata.get("chunk_index", 0)),
                    "similarity_score": similarity_score,
                    "distance_score": round(float(distance_score), 4),
                }
            )

        return {
            "query": query,
            "total": len(hits),
            "embedding_backend": self.embedding_backend,
            "hits": hits,
        }

    def get_status(self) -> dict:
        self._ensure_directories()
        raw_files = list(settings.raw_documents_dir.iterdir()) if settings.raw_documents_dir.exists() else []
        supported_files = [
            file_path
            for file_path in raw_files
            if file_path.is_file() and file_path.suffix.lower() in self.parser.supported_suffixes
        ]

        state = {
            "indexed": False,
            "indexed_document_count": 0,
            "indexed_chunk_count": 0,
        }
        if settings.index_state_path.exists():
            stored = json.loads(settings.index_state_path.read_text(encoding="utf-8"))
            state["indexed"] = bool(stored.get("indexed", False))
            state["indexed_document_count"] = int(stored.get("document_count", 0))
            state["indexed_chunk_count"] = int(stored.get("chunk_count", 0))

        return {
            "raw_document_count": len(raw_files),
            "supported_document_count": len(supported_files),
            "indexed": state["indexed"],
            "indexed_document_count": state["indexed_document_count"],
            "indexed_chunk_count": state["indexed_chunk_count"],
            "embedding_backend": self.embedding_backend,
            "raw_documents_dir": str(settings.raw_documents_dir),
            "chroma_dir": str(settings.chroma_dir),
        }

    def _ensure_directories(self) -> None:
        settings.knowledge_base_root.mkdir(parents=True, exist_ok=True)
        settings.raw_documents_dir.mkdir(parents=True, exist_ok=True)
        settings.checklist_dir.mkdir(parents=True, exist_ok=True)

    def _active_collection_name(self) -> str:
        if settings.index_state_path.exists():
            stored = json.loads(settings.index_state_path.read_text(encoding="utf-8"))
            return stored.get("collection_name") or settings.collection_name
        return settings.collection_name

    def _next_collection_name(self) -> str:
        return f"{settings.collection_name}-{int(time.time())}"

    def _create_vector_store(self, collection_name: str) -> Chroma:
        client_settings = ChromaSettings(
            anonymized_telemetry=False,
            is_persistent=True,
            persist_directory=str(settings.chroma_dir),
        )
        return Chroma(
            collection_name=collection_name,
            persist_directory=str(settings.chroma_dir),
            client_settings=client_settings,
            embedding_function=self.embeddings,
        )


@lru_cache(maxsize=1)
def get_knowledge_base_service() -> KnowledgeBaseService:
    return KnowledgeBaseService()
