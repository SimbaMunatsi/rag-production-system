from app.memory.base_memory import BaseMemory


class ConversationMemory(BaseMemory):

    def __init__(self):

        self.history = []

    def add(self, query, answer):

        self.history.append({
            "query": query,
            "answer": answer
        })

    def get_history(self):

        return self.history