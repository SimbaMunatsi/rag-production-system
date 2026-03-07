class ConversationMemory:

    def __init__(self, window_size=5):
        self.window_size = window_size
        self.history = []

    def add(self, role, message):

        self.history.append({
            "role": role,
            "content": message
        })

        if len(self.history) > self.window_size:
            self.history.pop(0)

    def get_context(self):

        return self.history