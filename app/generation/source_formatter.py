class SourceFormatter:

    def format(self, docs):
        sources = []

        for doc in docs:
            source = doc.metadata.get("source", "unknown source")
            page = doc.metadata.get("page")

            if page is not None:
                sources.append(f"{source} (page {page})")
            else:
                sources.append(source)

        return sources