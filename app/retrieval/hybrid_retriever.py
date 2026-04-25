from langchain_community.retrievers import BM25Retriever
from app.core.vector_store import get_vector_store
from app.retrieval.base_retriever import BaseRetriever

class HybridRetriever(BaseRetriever):
    def __init__(self, documents, k=8, rrf_k=60):
        self.vector_store = get_vector_store()
        # BM25 requires the document corpus loaded into memory
        self.keyword_retriever = BM25Retriever.from_documents(documents)
        self.keyword_retriever.k = k
        self.k = k
        self.rrf_k = rrf_k # Constant used in RRF formula (typically 60)

    async def retrieve(self, query):
        # Feature 2: Async retrieval
        # Note: Depending on your vector store, you might use asimilarity_search
        vector_results = await self.vector_store.asimilarity_search(query, k=self.k)
        
        # BM25 is purely CPU bound and fast, standard invoke is fine
        keyword_results = self.keyword_retriever.invoke(query)

        # Feature 3: Reciprocal Rank Fusion (Weighted Hybrid Search)
        doc_scores = {}
        content_to_doc = {}

        # Score Vector Results
        for rank, doc in enumerate(vector_results):
            content = doc.page_content
            content_to_doc[content] = doc
            doc_scores[content] = doc_scores.get(content, 0.0) + 1.0 / (self.rrf_k + rank)

        # Score BM25 Results
        for rank, doc in enumerate(keyword_results):
            content = doc.page_content
            content_to_doc[content] = doc
            doc_scores[content] = doc_scores.get(content, 0.0) + 1.0 / (self.rrf_k + rank)

        # Sort documents by their combined RRF score
        sorted_contents = sorted(doc_scores.keys(), key=lambda x: doc_scores[x], reverse=True)
        
        # Return the top K uniquely weighted documents
        return [content_to_doc[content] for content in sorted_contents[:self.k]]