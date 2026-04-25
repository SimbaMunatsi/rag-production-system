from app.retrieval.hybrid_retriever import HybridRetriever
from app.retrieval.reranker import Reranker
from app.retrieval.context_compressor import ContextCompressor
from app.retrieval.query_rewriter import QueryRewriter
from app.generation.prompt_builder import PromptBuilder
from app.generation.generator import Generator
from app.rag.pipeline import RAGPipeline
from app.generation.source_formatter import SourceFormatter
from app.guardrails.guardrails import Guardrails
from app.memory.memory_manager import get_memory
from app.core.vector_store import get_vector_store

def create_rag_pipeline(corpus_documents):
    """
    corpus_documents: A list of LangChain Document objects representing 
    the entire constitution. This is required to build the BM25 keyword index.
    """
    
    # Initialize the Weighted Hybrid Retriever
    retriever = HybridRetriever(documents=corpus_documents)
    
    reranker = Reranker()
    compressor = ContextCompressor()
    query_rewriter = QueryRewriter()
    prompt_builder = PromptBuilder()
    generator = Generator()
    source_formatter = SourceFormatter()
    guardrails = Guardrails()
    vector_store = get_vector_store()

    def memory_getter(session_id):
        return get_memory(session_id, vector_store)

    rag = RAGPipeline(
        retriever=retriever,
        reranker=reranker,
        compressor=compressor,
        prompt_builder=prompt_builder,
        generator=generator,
        memory_getter=memory_getter,
        source_formatter=source_formatter,
        guardrails=guardrails,
        query_rewriter=query_rewriter,
    )

    return rag