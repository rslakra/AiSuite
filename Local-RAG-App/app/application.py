"""FastAPI application factory."""
from __future__ import annotations

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from app.container import ServiceContainer, container
from app.webapp.routes import AppRouter


class LocalRAGApplication:
    """Build and configure the Local RAG FastAPI app."""

    def __init__(self, services: ServiceContainer | None = None) -> None:
        self.services = services or container
        self.app = FastAPI(
            title="Local RAG",
            description="Chat with your documents using Ollama — fully offline on your machine.",
            version="1.0.0",
        )
        self._mount_static()
        self._register_routes()

    def _mount_static(self) -> None:
        static_dir = self.services.settings.static_dir
        self.app.mount("/static", StaticFiles(directory=str(static_dir)), name="static")

    def _register_routes(self) -> None:
        app_router = AppRouter(self.services)
        self.app.include_router(app_router.router)

    def create(self) -> FastAPI:
        return self.app


def create_app(services: ServiceContainer | None = None) -> FastAPI:
    return LocalRAGApplication(services).create()


app = create_app()
