from abc import ABC, abstractmethod
import json
from pathlib import Path
from typing import Any

from models.llm_client import LLMClient

class BaseExperiment(ABC):
    """Common plumbing for an experiment that runs against 
    one LLM client
    Attributes:
        client: The injected LLM adapter. Experiments depend on this 
        abstraction only, never on a concrete provider class.
    """

    def __init__(self, client: LLMClient):
        self.client = client

    def send(self, message: list[dict[str, str]], **kwargs: Any) -> str:
        """Send a message to the model and return the reply text.
        
        The only method that knows the provider's response object shape.
        If an adapter returns something different, change it here alone.
        Args:
            message: Chat messages in OpenAI format.
            ***kwargs: Extra options forwarded to the adapter(temperature, response_format, and so on)
        Returns:
            The assistan's reply, or an empty string if none was produced.
        """
        response = self.client.chat(message, **kwargs)
        return response.choices[0].message.content if response.choices else ""
    
    @staticmethod
    def load_json(path: Path) -> list[dict[str, Any]]:
        """Load a JSON dataset from disk.
        Args:
            path: Absolute path to a JSON file holding a list of objects.
        Returns:
            The parsed list of case dicts.
        Raises:
            FileNotFoundError: If the file does not exist.
            ValueError: If the file is not a non-empty Json array
        """
        if not path.exists():
            raise FileNotFoundError(f"data not found: {path}")
        with path.open(encoding="utf-8") as handle:
            data = json.load(handle)
        if not isinstance(data, list) or not data:
            raise ValueError(f"{path.name} must be a non-empty JSON array")
        return data

    @abstractmethod
    def run(self):
        """Execute the experiment and print its report""" 