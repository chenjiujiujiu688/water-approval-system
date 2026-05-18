from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from docx import Document as WordDocument
from pypdf import PdfReader


@dataclass
class ParsedDocument:
    path: Path
    source_name: str
    file_type: str
    content: str


class DocumentParser:
    supported_suffixes = {".pdf", ".docx", ".txt", ".md"}

    def parse_directory(self, directory: Path) -> list[ParsedDocument]:
        documents: list[ParsedDocument] = []
        if not directory.exists():
            return documents

        for path in sorted(directory.iterdir()):
            if path.is_file() and path.suffix.lower() in self.supported_suffixes:
                documents.append(self.parse_file(path))
        return documents

    def parse_file(self, path: Path) -> ParsedDocument:
        suffix = path.suffix.lower()
        if suffix == ".pdf":
            content = self._parse_pdf(path)
        elif suffix == ".docx":
            content = self._parse_docx(path)
        else:
            content = path.read_text(encoding="utf-8")

        return ParsedDocument(
            path=path,
            source_name=path.name,
            file_type=suffix.lstrip("."),
            content=self._normalize_text(content),
        )

    def _parse_pdf(self, path: Path) -> str:
        reader = PdfReader(str(path))
        return "\n".join(page.extract_text() or "" for page in reader.pages)

    def _parse_docx(self, path: Path) -> str:
        document = WordDocument(str(path))
        return "\n".join(paragraph.text for paragraph in document.paragraphs if paragraph.text.strip())

    def _normalize_text(self, text: str) -> str:
        cleaned_lines = [line.strip() for line in text.splitlines()]
        return "\n".join(line for line in cleaned_lines if line)
