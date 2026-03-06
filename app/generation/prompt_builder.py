class PromptBuilder:

    def build(self, query: str, context: str):

        prompt = f"""
You are an expert assistant.

Use ONLY the context below to answer the question.

If the answer is not in the context, say "I don't know".

Context:
{context}

Question:
{query}

Answer:
"""

        return prompt