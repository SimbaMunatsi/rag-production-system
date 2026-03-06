from langchain_openai import ChatOpenAI
from app.generation.base_generator import BaseGenerator


class Generator(BaseGenerator):

    def __init__(self):

        self.llm = ChatOpenAI(
            model="gpt-4o-mini",
            temperature=0
        )

    def generate(self, prompt: str):

        response = self.llm.invoke(prompt)

        return response.content