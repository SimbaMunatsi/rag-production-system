from .input_filter import InputFilter
from .pii_filter import PIIFilter
from .hallucination_check import HallucinationChecker


class GuardrailManager:

    def __init__(self):

        self.input_filter = InputFilter()
        self.pii_filter = PIIFilter()
        self.hallucination = HallucinationChecker()

    def validate_input(self, query):

        return self.input_filter.validate(query)

    def validate_output(self, answer, context):

        if self.pii_filter.contains_pii(answer):
            raise ValueError("PII detected in output")

        if not self.hallucination.grounded(answer, context):
            raise ValueError("Possible hallucination")

        return answer