from .prompt_injection import PromptInjectionDetector


class InputFilter:

    def __init__(self):
        self.detector = PromptInjectionDetector()

    def validate(self, query: str):

        if self.detector.detect(query):
            raise ValueError("Prompt injection detected")

        return query