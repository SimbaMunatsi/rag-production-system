from langchain_openai import ChatOpenAI
from app.generation.base_generator import BaseGenerator

class Generator(BaseGenerator):
    def __init__(self):
        self.llm = ChatOpenAI(
            model="gpt-4o-mini",
            temperature=0
        )

    async def generate(self, prompt: str):
        # Feature 2: Async LLM generation
        response = await self.llm.ainvoke(prompt)
        return response.content