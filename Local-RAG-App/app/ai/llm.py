"""Ollama chat and model listing."""
from __future__ import annotations

import ollama

from app.config import Settings


class LLMService:
    """Run chat completions and list models through Ollama."""

    def __init__(self, settings: Settings) -> None:
        self._settings = settings

    def list_chat_models(self) -> list[str]:
        data = ollama.list()
        models = data.get("models", []) if isinstance(data, dict) else data.models

        names: list[str] = []
        for model in models:
            if isinstance(model, dict):
                name = model.get("model") or model.get("name")
            else:
                name = getattr(model, "model", None)
            if name and "embed" not in name.lower():
                names.append(name)
        return sorted(names)

    def chat(self, prompt: str, model: str | None = None) -> str:
        response = ollama.chat(
            model=model or self._settings.chat_model,
            messages=[{"role": "user", "content": prompt}],
        )
        return response["message"]["content"]
