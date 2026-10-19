from abc import ABC, abstractmethod
class LLMClient(ABC):
    def __init__(self, base_url: str, api_key: str):
        self.base_url = base_url
        self.api_key = api_key

    @abstractmethod
    def get_model(self, model_name):
        pass
    
    @abstractmethod
    def chat(self, model_name, messages):
        pass
    
    @abstractmethod
    def completion(self, model_name, prompt):
        pass
    
    @abstractmethod
    def embeddings(self, model_name, input):
        pass
    
    @abstractmethod
    def images(self, model_name, prompt):
        pass
