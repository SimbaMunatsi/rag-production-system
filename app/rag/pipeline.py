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
        guardrails,
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

        # 1. Validate input
        safe_query = self.guardrails.validate_input(query)

        # 2. Build memory context
        memory_context = self.memory.build_context(safe_query)

        # 3. Retrieve documents
        docs = self.retriever.retrieve(safe_query)

        # 4. Rerank documents
        docs = self.reranker.rerank(safe_query, docs)

        # 5. Compress documents
        context = self.compressor.compress(docs)
        context_text = "\n\n".join(context)

        # 6. Build final prompt
        prompt = self.prompt_builder.build(
            query=safe_query,
            context=context_text,
            memory=memory_context
        )

        # 7. Generate answer from final prompt
        answer = self.generator.generate(prompt)

        # 8. Validate output
        safe_answer = self.guardrails.validate_output(safe_query, answer)

        # 9. Update memory
        self.memory.update(safe_query, safe_answer)

        # 10. Format sources
        sources = self.source_formatter.format(docs)

        return {
            "answer": safe_answer,
            "sources": sources
        }