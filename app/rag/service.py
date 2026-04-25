from app.retrieval.hybrid_retriever import HybridRetriever
from app.retrieval.reranker import Reranker
from app.generation.prompt_builder import PromptBuilder
from app.generation.generator import Generator
from app.rag.pipeline import RAGPipeline
from app.retrieval.query_rewriter import QueryRewriter
from app.retrieval.context_compressor import ContextCompressor
from app.generation.source_formatter import SourceFormatter
from app.guardrails.guardrails import Guardrails
from app.memory.memory_manager import get_memory_manager 

def create_rag_pipeline(corpus_documents=None):
    retriever = HybridRetriever(documents=corpus_documents)
    reranker = Reranker()
    compressor = ContextCompressor()
    prompt_builder = PromptBuilder()
    generator = Generator()
    source_formatter = SourceFormatter()
    guardrails = Guardrails()
    query_rewriter = QueryRewriter()

    return RAGPipeline(
        retriever=retriever,
        reranker=reranker,
        compressor=compressor,
        prompt_builder=prompt_builder,
        generator=generator,
        memory_getter=get_memory_manager, 
        source_formatter=source_formatter,
        guardrails=guardrails,
        query_rewriter=query_rewriter
    )