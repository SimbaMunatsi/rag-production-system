class Reranker:

    def rerank(self, query, docs):

        scored_docs = []

        for doc in docs:
            score = self.score(query, doc.page_content)
            scored_docs.append((score, doc))

        scored_docs.sort(key=lambda x: x[0], reverse=True)

        reranked_docs = [doc for score, doc in scored_docs]

        return reranked_docs


    def score(self, query, text):

        # simple example scoring
        return text.lower().count(query.lower())