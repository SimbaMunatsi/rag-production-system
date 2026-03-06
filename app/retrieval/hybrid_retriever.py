from langchain_community.retrievers import BM25Retriever
from app.core.vector_store import get_vector_store


class HybridRetriever:

    def __init__(self, documents, k=10):

        self.vector_store = get_vector_store()

        self.keyword_retriever = BM25Retriever.from_documents(
            documents
        )

        self.keyword_retriever.k = k

        self.k = k


    def retrieve(self, query):

        vector_results = self.vector_store.similarity_search(query, k=self.k)

        keyword_results = self.keyword_retriever.get_relevant_documents(query)

        combined = vector_results + keyword_results

        # remove duplicates
        unique_docs = list({doc.page_content: doc for doc in combined}.values())

        return unique_docs