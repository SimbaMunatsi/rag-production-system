from app.retrieval.retriever import Retriever
from app.retrieval.reranker import Reranker
from app.retrieval.context_compressor import ContextCompressor
from app.generation.prompt_builder import PromptBuilder
from app.generation.generator import Generator
from app.memory.conversation_memory import ConversationMemory
from app.generation.source_formatter import SourceFormatter
from app.rag.pipeline import RAGPipeline
from app.guardrails.guardrails import Guardrails


def create_rag_pipeline():

    retriever = Retriever()

    reranker = Reranker()

    compressor = ContextCompressor()

    prompt_builder = PromptBuilder()

    generator = Generator()

    memory = ConversationMemory()

    source_formatter = SourceFormatter()

    guardrails = Guardrails()

    rag = RAGPipeline(
    retriever=retriever,
    reranker=reranker,
    compressor=compressor,
    prompt_builder=prompt_builder,
    generator=generator,
    memory=memory,
    source_formatter=source_formatter,
    guardrails = guardrails
    )

    return rag