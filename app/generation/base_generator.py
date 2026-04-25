from abc import ABC, abstractmethod

class BaseGenerator(ABC):
    @abstractmethod
    async def generate(self, prompt: str):
        pass