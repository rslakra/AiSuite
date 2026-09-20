"""Retrieval-augmented generation pipeline."""
from __future__ import annotations

from app.ai.llm import LLMService
from app.ai.text import TextProcessor
from app.ai.vector_store import VectorStore
from app.config import Settings


class RAGService:
    """Index documents and answer questions with retrieved context."""

    def __init__(
        self,
        settings: Settings,
        text: TextProcessor,
        vector_store: VectorStore,
        llm: LLMService,
    ) -> None:
        self._settings = settings
        self._text = text
        self._vector_store = vector_store
        self._llm = llm

    def index_file(self, filepath: str) -> int:
        content = self._text.extract(filepath)
        chunks = self._text.chunk(content)
        if not chunks:
            raise ValueError(
                "Couldn't read any text from that file. "
                "If it's a scanned PDF (just images), it has no selectable text."
            )
        return self._vector_store.index_chunks(chunks)

    def retrieve(self, question: str, k: int | None = None) -> list[str]:
        return self._vector_store.query(question, k=k)

    def answer(self, question: str, model: str | None = None) -> str:
        chunks = self.retrieve(question)
        if not chunks:
            return "No document loaded yet. Upload a file first, then ask away."

        context = "\n\n".join(chunks)
        prompt = self._settings.format_rag_prompt(context=context, question=question)
        return self._llm.chat(prompt, model=model or self._settings.chat_model)

    def has_document(self) -> bool:
        return self._vector_store.has_documents()
