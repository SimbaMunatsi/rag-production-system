from app.guardrails.guardrail_manager import GuardrailManager

class RAGPipeline:

    def __init__(
        self,
        retriever,
        reranker,
        compressor,
        prompt_builder,
        generator,
        memory,
        source_formatter,
        guardrails
    ):

        self.retriever = retriever
        self.reranker = reranker
        self.compressor = compressor
        self.prompt_builder = prompt_builder
        self.generator = generator
        self.memory = memory
        self.source_formatter = source_formatter
        self.guardrails = guardrails


    def run(self, query):

        # input validation
        safe_query = self.guardrails.validate_input(query)

        docs = self.retriever.retrieve(query)

        docs = self.reranker.rerank(query, docs)

        context = self.compressor.compress(docs)

        context_text = "\n\n".join(context)

        prompt = self.prompt_builder.build(query, context_text)

        answer = self.generator.generate(prompt)

        self.memory.add(query, answer)

        sources = self.source_formatter.format(docs)

        # output validation
        safe_answer = self.guardrails.validate_output(answer, docs)

        return {
            "answer": answer,
            "sources": sources
        }