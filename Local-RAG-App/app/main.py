"""Local RAG App — application entry point."""
import uvicorn

from app.application import app, create_app
from app.config import settings

__all__ = ["app", "create_app"]

if __name__ == "__main__":
    uvicorn.run(
        "app.main:app",
        host=settings.host,
        port=settings.port,
        reload=True,
    )
