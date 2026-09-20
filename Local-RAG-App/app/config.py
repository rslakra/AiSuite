"""Application settings and paths."""
from __future__ import annotations

import os
from dataclasses import dataclass, field
from pathlib import Path

from dotenv import load_dotenv

APP_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = APP_DIR.parent

DEFAULT_RAG_PROMPT = (
    "Use only the context below to answer the question. "
    "If the answer isn't in the context, say you don't know.\n\n"
    "Context:\n{context}\n\n"
    "Question: {question}"
)


def _load_env() -> None:
    env_file = PROJECT_ROOT / ".env"
    if env_file.exists():
        load_dotenv(env_file)


def _env(key: str, default: str = "") -> str:
    return (os.getenv(key) or default).strip()


def resolve_data_path(raw: str) -> Path:
    text = raw.strip().strip("\"'")
    expanded = os.path.expandvars(os.path.expanduser(text))
    path = Path(expanded)
    if not path.is_absolute():
        path = PROJECT_ROOT / path
    return path.resolve()


def parse_allowed_extensions(raw: str) -> frozenset[str]:
    if not raw.strip():
        return frozenset({".pdf", ".md", ".txt"})
    extensions: set[str] = set()
    for part in raw.split(","):
        text = part.strip().lower()
        if not text:
            continue
        if not text.startswith("."):
            text = f".{text}"
        extensions.add(text)
    return frozenset(extensions)


@dataclass(frozen=True)
class Settings:
    chat_model: str = "llama3:8b"
    embed_model: str = "nomic-embed-text"
    chunk_size: int = 500
    chunk_overlap: int = 100
    top_k: int = 3
    collection_name: str = "documents"
    max_upload_bytes: int = 25 * 1024 * 1024
    host: str = "0.0.0.0"
    port: int = 8080
    rag_prompt: str = DEFAULT_RAG_PROMPT
    app_data_dir: Path = field(default_factory=lambda: PROJECT_ROOT / "app_data")
    allowed_extensions: frozenset[str] = field(default_factory=lambda: frozenset({".pdf", ".md", ".txt"}))

    @property
    def upload_dir(self) -> Path:
        return self.app_data_dir / "uploads"

    @property
    def chroma_dir(self) -> Path:
        return self.app_data_dir / "chroma_store"

    @property
    def webapp_dir(self) -> Path:
        return APP_DIR / "webapp"

    @property
    def templates_dir(self) -> Path:
        return self.webapp_dir / "templates"

    @property
    def static_dir(self) -> Path:
        return self.webapp_dir / "static"

    def ensure_dirs(self) -> None:
        self.app_data_dir.mkdir(parents=True, exist_ok=True)
        self.upload_dir.mkdir(parents=True, exist_ok=True)
        self.chroma_dir.mkdir(parents=True, exist_ok=True)

    def format_rag_prompt(self, context: str, question: str) -> str:
        return self.rag_prompt.format(context=context, question=question)

    @classmethod
    def from_env(cls) -> Settings:
        _load_env()
        raw_prompt = _env("RAG_PROMPT")
        rag_prompt = raw_prompt.replace("\\n", "\n") if raw_prompt else DEFAULT_RAG_PROMPT
        raw_port = _env("PORT")
        port = int(raw_port) if raw_port.isdigit() else 8080
        raw_data_dir = _env("APP_DATA_DIR", "app_data") or "app_data"
        app_data_dir = resolve_data_path(raw_data_dir)
        allowed_extensions = parse_allowed_extensions(_env("ALLOWED_EXTENSIONS", ".pdf,.md,.txt"))
        chat_model = _env("CHAT_MODEL", "llama3:8b") or "llama3:8b"
        embed_model = _env("EMBED_MODEL", "nomic-embed-text") or "nomic-embed-text"
        return cls(
            chat_model=chat_model,
            embed_model=embed_model,
            rag_prompt=rag_prompt,
            port=port,
            app_data_dir=app_data_dir,
            allowed_extensions=allowed_extensions,
        )


settings = Settings.from_env()
