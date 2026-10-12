"""Web UI and JSON API routes."""
from __future__ import annotations

import logging
from pathlib import Path

from fastapi import File, Request, UploadFile
from fastapi.responses import HTMLResponse, JSONResponse
from pydantic import BaseModel

from app.webapp.routes.base import BaseRouter

logger = logging.getLogger(__name__)


class ChatRequest(BaseModel):
    question: str = ""
    model: str = ""


class AppRouter(BaseRouter):
    """Web UI and JSON API for document upload and chat."""

    def register_routes(self) -> None:
        self.router.add_api_route(
            "/",
            self.home,
            methods=["GET"],
            response_class=HTMLResponse,
        )
        self.router.add_api_route("/api/models", self.api_models, methods=["GET"])
        self.router.add_api_route("/upload", self.upload, methods=["POST"])
        self.router.add_api_route("/chat", self.chat, methods=["POST"])

    async def home(self, request: Request):
        return self.templates.TemplateResponse(
            request=request,
            name="index.html",
            context={"has_document": self.services.rag.has_document()},
        )

    async def api_models(self):
        try:
            models = self.services.llm.list_chat_models()
            return {"models": models, "default": self.services.settings.chat_model}
        except Exception:
            return JSONResponse(
                status_code=503,
                content={"models": [], "error": "Couldn't reach Ollama."},
            )

    async def upload(self, file: UploadFile = File(...)):
        settings = self.services.settings
        if not file.filename:
            return JSONResponse(status_code=400, content={"error": "No file selected."})

        filename = self._safe_filename(file.filename)
        if not self._allowed(filename, settings.allowed_extensions):
            return JSONResponse(
                status_code=400,
                content={"error": "Use a .pdf, .txt, or .md file."},
            )

        path = settings.upload_dir / filename
        contents = await file.read()
        if len(contents) > settings.max_upload_bytes:
            return JSONResponse(
                status_code=400,
                content={"error": "File is too large (max 25 MB)."},
            )

        path.write_bytes(contents)

        try:
            chunk_count = self.services.rag.index_file(str(path))
        except ValueError as exc:
            logger.warning(
                "Invalid uploaded file '%s': %s",
                filename,
                exc,
                exc_info=True,
            )
            return JSONResponse(status_code=400, content={"error": "Invalid file content."})
        except Exception as exc:
            logger.exception("Unexpected error while processing uploaded file '%s': %s", filename, exc)
            return JSONResponse(
                status_code=500,
                content={"error": "Couldn't process the file right now."},
            )

        return {"filename": filename, "chunks": chunk_count}

    async def chat(self, payload: ChatRequest):
        settings = self.services.settings
        question = payload.question.strip()
        model = payload.model.strip() or settings.chat_model
        if not question:
            return JSONResponse(status_code=400, content={"error": "Ask a question first."})

        try:
            reply = self.services.rag.answer(question, model)
        except Exception:
            return JSONResponse(
                status_code=500,
                content={"error": "Couldn't get an answer right now."},
            )

        return {"answer": reply}

    @staticmethod
    def _allowed(filename: str, allowed_extensions: frozenset[str]) -> bool:
        return Path(filename).suffix.lower() in allowed_extensions

    @staticmethod
    def _safe_filename(filename: str) -> str:
        return Path(filename).name.replace("\x00", "")
