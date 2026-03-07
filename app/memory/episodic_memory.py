import datetime


class EpisodicMemory:

    def __init__(self):

        self.events = []

    def store_event(self, user_query, answer):

        self.events.append({
            "timestamp": datetime.datetime.now(),
            "query": user_query,
            "answer": answer
        })

    def get_recent_events(self, limit=5):

        return self.events[-limit:]