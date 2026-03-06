from app.retrieval.retriever import Retriever

def test_retrieval_returns_documents():

    retriever = Retriever()

    docs = retriever.retrieve("What is Artificial Intelligence?")

    assert len(docs) > 0