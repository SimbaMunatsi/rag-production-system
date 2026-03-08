class QueryRewriter:

    def rewrite(self, query, memory):
        conversation = memory.get("conversation", [])

        if not conversation:
            return query

        user_messages = [
            item["content"]
            for item in conversation
            if item["role"] == "user"
        ]

        if not user_messages:
            return query

        last_user_message = user_messages[-1]

        vague_terms = {"it", "its", "they", "them", "that", "those", "these", "this"}

        query_words = set(query.lower().replace("?", "").replace(".", "").split())

        if query_words.intersection(vague_terms):
            return f"In the context of '{last_user_message}', {query}"

        return query