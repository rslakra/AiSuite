"""Ollama embedding service."""
from __future__ import annotations

import ollama

from app.config import Settings


class EmbeddingService:
    """Generate vector embeddings through a local Ollama model."""

    def __init__(self, settings: Settings) -> None:
        self._settings = settings

    def embed(self, text: str, model: str | None = None) -> list[float]:
        response = ollama.embeddings(
            model=model or self._settings.embed_model,
            prompt=text,
        )
        return response["embedding"]
