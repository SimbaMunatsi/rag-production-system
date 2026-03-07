class PromptInjectionDetector:

    BLOCK_PATTERNS = [
        "ignore previous instructions",
        "reveal system prompt",
        "bypass safety",
        "act as system"
    ]

    def detect(self, query: str) -> bool:

        query_lower = query.lower()

        for pattern in self.BLOCK_PATTERNS:
            if pattern in query_lower:
                return True

        return False