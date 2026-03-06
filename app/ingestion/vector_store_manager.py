from app.core.vector_store import get_vector_store


class VectorStoreManager:

    def __init__(self):

        self.vector_store = get_vector_store()

    def store(self, chunks):

        self.vector_store.add_documents(chunks)

        self.vector_store.persist()