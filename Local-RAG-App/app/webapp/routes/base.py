"""Base class for HTML and API routers."""
from __future__ import annotations

from fastapi import APIRouter
from fastapi.templating import Jinja2Templates

from app.container import ServiceContainer


class BaseRouter:
    """Register routes on a shared APIRouter instance."""

    prefix: str = ""
    tags: list[str] = []

    def __init__(self, services: ServiceContainer) -> None:
        self.services = services
        self.router = APIRouter(prefix=self.prefix, tags=self.tags)
        self.templates = Jinja2Templates(
            directory=str(services.settings.templates_dir),
        )
        self.register_routes()

    def register_routes(self) -> None:
        raise NotImplementedError
