from langchain_core.prompts import PromptTemplate

class PromptBuilder:
    def __init__(self):
        # We structured the prompt with conditional behavioral rules
        self.template = PromptTemplate.from_template(
            "You are Bumbiro, a professional and helpful AI assistant specialized in the Constitution of Zimbabwe.\n\n"
            "Follow these rules strictly:\n"
            "1. CONVERSATION: If the user is greeting you, introducing themselves, or asking about your identity, respond politely, acknowledge any facts they share, and state your purpose. Do NOT use the legal fallback phrase.\n"
            "2. LEGAL QUERIES: If the user asks a substantive question about the law, government, or the Constitution, you MUST answer using ONLY the provided 'Context' and 'Known Facts'.\n"
            "3. MISSING CONTEXT: If a legal question cannot be answered using the provided context, you must state exactly: 'I could not find enough relevant support in the Constitution to answer that.' Do not guess or use outside knowledge.\n\n"
            "Context:\n{context}\n\n"
            "Known Facts about the user:\n{semantic}\n\n"
            "Conversation History:\n{conversation}\n\n"
            "User Query: {query}\n"
            "Assistant:"
        )

    def build(self, query: str, context: str, memory: dict) -> str:
        conversation_text = memory.get("conversation", "")
        semantic_text = memory.get("semantic", "")

        return self.template.format(
            context=context,
            semantic=semantic_text,
            conversation=conversation_text,
            query=query
        )