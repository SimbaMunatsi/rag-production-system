from app.memory.conversation_memory import ConversationMemory
from app.memory.semantic_memory import SemanticMemory
from app.memory.episodic_memory import EpisodicMemory


class MemoryManager:

    def __init__(self, semantic_store):

        self.conversation = ConversationMemory()
        self.semantic = SemanticMemory(semantic_store)
        self.episodic = EpisodicMemory()

    def build_context(self, query):

        conversation_context = self.conversation.get_context()

        semantic_context = self.semantic.retrieve_facts(query)

        return {
            "conversation": conversation_context,
            "semantic": semantic_context
        }

    def update(self, query, answer):

        self.conversation.add("user", query)
        self.conversation.add("assistant", answer)

        self.episodic.store_event(query, answer)