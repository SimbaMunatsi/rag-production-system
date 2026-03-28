class ContextCompressor:

    def compress(self, documents):

        compressed = []

        for doc in documents:

            text = doc.page_content

            # simple truncation
            compressed.append(text[:1000])

        return compressed