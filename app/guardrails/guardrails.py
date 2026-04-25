from app.guardrails.guardrail_manager import GuardrailManager

class Guardrails:
    def __init__(self):
        self.manager = GuardrailManager()

    async def validate_input(self, query: str) -> str:
        return await self.manager.validate_input(query)

    async def validate_output(self, query: str, answer: str, context_text: str) -> str:
        return await self.manager.validate_output(query, answer, context_text)