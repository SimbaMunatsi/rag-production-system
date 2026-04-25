from flashrank import Ranker, RerankRequest

class Reranker:
    def __init__(self):
        # Initializes a lightweight ONNX cross-encoder model.
        # It will download a tiny (~30MB) model on the first run.
        self.ranker = Ranker(model_name="ms-marco-MiniLM-L-12-v2")

    def rerank(self, query, docs, top_n=4):
        if not docs:
            return []

        # FlashRank expects a specific dictionary format, so we map our LangChain docs
        passages = [
            {
                "id": i, # Store the original index so we can retrieve the document later
                "text": doc.page_content, 
                "meta": doc.metadata
            } 
            for i, doc in enumerate(docs)
        ]

        # Create the request and execute the rerank
        rerankrequest = RerankRequest(query=query, passages=passages)
        results = self.ranker.rerank(rerankrequest)

        # FlashRank returns a sorted list of dictionaries with scores.
        # We use the 'id' we attached earlier to grab the original LangChain Document objects.
        reranked_docs = []
        for result in results[:top_n]:
            original_index = result["id"]
            reranked_docs.append(docs[original_index])

        return reranked_docs