from __future__ import annotations

import sys
import tempfile
from pathlib import Path

import win32com.client
from docx import Document as WordDocument


def convert_doc_to_text(path: Path) -> str:
    with tempfile.TemporaryDirectory() as temp_dir:
        temp_docx = Path(temp_dir) / f"{path.stem}.docx"
        word = win32com.client.DispatchEx("Word.Application")
        word.Visible = False
        word.DisplayAlerts = 0
        try:
            document = word.Documents.Open(str(path), False, True, False)
            document.SaveAs(str(temp_docx), FileFormat=16)
            document.Close(False)
        finally:
            word.Quit()

        document = WordDocument(str(temp_docx))
        return "\n".join(paragraph.text for paragraph in document.paragraphs if paragraph.text.strip())


if __name__ == "__main__":
    source = Path(sys.argv[1]).resolve()
    print(convert_doc_to_text(source))
