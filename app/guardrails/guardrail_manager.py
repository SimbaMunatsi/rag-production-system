from app.guardrails.input_filter import InputFilter
from app.guardrails.pii_filter import PIIFilter
from app.guardrails.hallucination import HallucinationChecker

class GuardrailManager:
    def __init__(self):
        self.input_filter = InputFilter()
        self.pii_filter = PIIFilter()
        self.hallucination_checker = HallucinationChecker()

    async def validate_input(self, query: str) -> str:
        return await self.input_filter.validate(query)

    async def validate_output(self, query: str, answer: str, context_text: str) -> str:
        # 1. Check for PII leakage
        if self.pii_filter.contains_pii(answer):
            return "I cannot provide this answer as it contains sensitive personal data."

        # 2. Check for Hallucinations (Grounding Score)
        grounding_score = await self.hallucination_checker.check(answer, context_text)
        
        # We set a threshold of 0.8 to allow for paraphrasing but reject fabrication
        if grounding_score < 0.8:
            return "I could not find enough relevant support in the Zimbabwe Constitution to answer that confidently."

        return answer