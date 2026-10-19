from openai import OpenAI
from .llm_client import LLMClient
class OllamaClient(LLMClient):
    def __init__(self, base_url="http://localhost:11434/v1", api_key="ollama", model_name=None):
        super().__init__(base_url, api_key)
        self.client = OpenAI(base_url=base_url, api_key=api_key)
        self.model_name = model_name or "llama3.2:3b"
    
    def get_model(self, model_name):
        return self.client.models.get(model_name)
    
    def chat(self, messages, **kwargs):
        return self.client.chat.completions.create(
            model=self.model_name,
            messages=messages,
            **kwargs,
        )
    
    def completion(self, prompt, model_name=None):
        return self.client.completions.create(model=self.model_name, prompt=prompt)
    
    def embeddings(self, input, model_name=None):
        return self.client.embeddings.create(model=self.model_name, input=input)
    def images(self, prompt, model_name=None):
        return self.client.images.generate(model=model_name, prompt=prompt)