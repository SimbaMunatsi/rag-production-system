class IngestionPipeline:

    def __init__(
        self,
        loader,
        cleaner,
        chunker,
        vector_store
    ):

        self.loader = loader
        self.cleaner = cleaner
        self.chunker = chunker
        self.vector_store = vector_store

    def run(self):

        documents = self.loader.load()

        cleaned_docs = self.cleaner.clean(documents)

        chunks = self.chunker.chunk(cleaned_docs)

        self.vector_store.store(chunks)

        return len(chunks)