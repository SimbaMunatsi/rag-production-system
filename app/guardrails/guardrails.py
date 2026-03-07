class Guardrails:
    def validate_input(self, query: str) -> str:
        return query

    def validate_output(self, query: str , answer: str) -> str:
        return answer