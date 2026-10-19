from __future__ import annotations

import os

from models.llm_client import LLMClient
from models.ollama_client import OllamaClient
from models.open_ai_client import OpenAIClient


def get_client(provider: str, model_name: str | None = None) -> LLMClient:
    """Create the configured LLM client for the selected provider."""
    if provider == "openai":
        return OpenAIClient(model_name=model_name)
    if provider == "ollama":
        return OllamaClient(model_name=model_name)
    raise ValueError(f"Unsupported provider: {provider}")


class ModelRepo:
    def __init__(self, client: LLMClient, models: dict, default_model: str):
        self.client = client
        self.models = models
        self.default_model = default_model

    def resolve_model(self, model_name: str) -> str:
        name = model_name or self.default_model
        return self.models.get(name, name)

    def chat(self, messages, model_name=None):
        return self.client.chat(self.resolve_model(model_name), messages)
