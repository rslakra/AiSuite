"""Dependency injection container for application services."""
from __future__ import annotations

from app.ai.embeddings import EmbeddingService
from app.ai.llm import LLMService
from app.ai.rag import RAGService
from app.ai.text import TextProcessor
from app.ai.vector_store import VectorStore
from app.config import Settings


class ServiceContainer:
    """Wire and expose all AI and application services."""

    def __init__(self, settings: Settings | None = None) -> None:
        self.settings = settings or Settings.from_env()
        self.settings.ensure_dirs()
        self.text = TextProcessor(self.settings)
        self.embeddings = EmbeddingService(self.settings)
        self.vector_store = VectorStore(self.settings, self.embeddings)
        self.llm = LLMService(self.settings)
        self.rag = RAGService(self.settings, self.text, self.vector_store, self.llm)


container = ServiceContainer()
