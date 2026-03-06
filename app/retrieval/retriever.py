from app.core.vector_store import get_vector_store
from app.retrieval.base_retriever import BaseRetriever


class Retriever(BaseRetriever):

    def __init__(self, k: int = 4):

        self.vector_store = get_vector_store()
        self.k = k

    def retrieve(self, query: str):

        docs = self.vector_store.similarity_search(query, k=self.k)

        return docs