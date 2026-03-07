class SemanticMemory:

    def __init__(self, vector_store):
        self.vector_store = vector_store

    def store_fact(self, fact):
        self.vector_store.add_texts([fact])

    def retrieve_facts(self, query):
        results = self.vector_store.similarity_search(query, k=3)
        return [doc.page_content for doc in results]