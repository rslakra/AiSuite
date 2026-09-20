"""ChromaDB vector store."""
from __future__ import annotations

import chromadb

from app.ai.embeddings import EmbeddingService
from app.config import Settings


class VectorStore:
    """Persist and query document chunk embeddings in ChromaDB."""

    def __init__(self, settings: Settings, embeddings: EmbeddingService) -> None:
        self._settings = settings
        self._embeddings = embeddings
        self._client = chromadb.PersistentClient(path=str(settings.chroma_dir))

    def _fresh_collection(self):
        try:
            self._client.delete_collection(self._settings.collection_name)
        except Exception:
            pass
        return self._client.get_or_create_collection(self._settings.collection_name)

    def _collection(self):
        return self._client.get_or_create_collection(self._settings.collection_name)

    def index_chunks(self, chunks: list[str]) -> int:
        collection = self._fresh_collection()
        vectors = [self._embeddings.embed(chunk) for chunk in chunks]
        ids = [f"chunk-{index}" for index in range(len(chunks))]
        collection.add(ids=ids, documents=chunks, embeddings=vectors)
        return len(chunks)

    def query(self, question: str, k: int | None = None) -> list[str]:
        collection = self._collection()
        question_vector = self._embeddings.embed(question)
        results = collection.query(
            query_embeddings=[question_vector],
            n_results=k or self._settings.top_k,
        )
        return results["documents"][0] if results["documents"] else []

    def count(self) -> int:
        try:
            return self._collection().count()
        except Exception:
            return 0

    def has_documents(self) -> bool:
        return self.count() > 0
