class SourceFormatter:

    def format(self, documents):

        sources = []

        for doc in documents:

            sources.append({
                "content": doc.page_content[:200],
                "metadata": doc.metadata
            })

        return sources