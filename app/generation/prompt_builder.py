class PromptBuilder:

    def build(self, query, context, memory):
        conversation = memory.get("conversation", [])
        semantic = memory.get("semantic", [])

        conversation_text = "\n".join(
            f"{item['role']}: {item['content']}" for item in conversation
        )

        semantic_text = "\n".join(semantic)

        return f"""
You are a helpful assistant.

Conversation History:
{conversation_text}

Semantic Memory:
{semantic_text}

Retrieved Context:
{context}

User Question:
{query}
"""