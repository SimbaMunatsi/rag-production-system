from app.guardrails.prompt_injection import PromptInjectionDetector

class InputFilter:
    def __init__(self):
        self.detector = PromptInjectionDetector()

    async def validate(self, query: str) -> str:
        is_injection = await self.detector.detect(query)
        if is_injection:
            # Raising a ValueError allows FastAPI to catch it and return a 400 response
            raise ValueError("Blocked: Potential prompt injection detected.")
        return query