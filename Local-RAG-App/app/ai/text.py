"""Document parsing and text chunking."""
from __future__ import annotations

from pypdf import PdfReader

from app.config import Settings


class TextProcessor:
    """Extract plain text from supported files and split it into chunks."""

    def __init__(self, settings: Settings) -> None:
        self._settings = settings

    def extract(self, filepath: str) -> str:
        if filepath.lower().endswith(".pdf"):
            reader = PdfReader(filepath)
            return "\n".join(page.extract_text() or "" for page in reader.pages)
        with open(filepath, "r", encoding="utf-8", errors="ignore") as handle:
            return handle.read()

    def chunk(self, text: str) -> list[str]:
        size = self._settings.chunk_size
        overlap = self._settings.chunk_overlap
        text = text.strip()
        if not text:
            return []

        chunks: list[str] = []
        start = 0
        step = max(size - overlap, 1)
        while start < len(text):
            chunk = text[start : start + size].strip()
            if chunk:
                chunks.append(chunk)
            start += step
        return chunks
