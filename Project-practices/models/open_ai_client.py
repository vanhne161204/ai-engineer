from openai import OpenAI
from .llm_client import LLMClient


class OpenAIClient(LLMClient):
    def __init__(self, api_key=None, model_name=None):
        super().__init__("https://api.openai.com/v1", api_key or "")
        self.client = OpenAI(api_key=api_key)
        self.model_name = model_name or "gpt-4o-mini"

    def get_model(self, model_name):
        return self.client.models.get(model_name)
    
    def chat(self, messages, **kwargs):
        return self.client.chat.completions.create(
            model=self.model_name,
            messages=messages,
            **kwargs,
        )
    
    def completion(self, model_name, prompt):
        return self.client.completions.create(model=model_name, prompt=prompt)
    
    def embeddings(self, model_name, input):
        return self.client.embeddings.create(model=model_name, input=input)
    
    def images(self, model_name, prompt):
        return self.client.images.generate(model=model_name, prompt=prompt)