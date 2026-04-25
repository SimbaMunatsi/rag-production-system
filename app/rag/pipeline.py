class RAGPipeline:
    def __init__(self, retriever, reranker, compressor, prompt_builder, generator, memory_getter, source_formatter, guardrails, query_rewriter):
        self.retriever = retriever
        self.reranker = reranker
        self.compressor = compressor
        self.prompt_builder = prompt_builder
        self.generator = generator
        self.memory_getter = memory_getter
        self.source_formatter = source_formatter
        self.guardrails = guardrails
        self.query_rewriter = query_rewriter

    # Add 'db' to the runtime parameters
    async def run(self, query, session_id, db):
        # 1. Initialize memory with the active database session
        memory = self.memory_getter(db, session_id)

        safe_query = await self.guardrails.validate_input(query)
        
        # 2. Await the new async agentic memory retrieval
        memory_context = await memory.build_context(safe_query)

        standalone_query = self.query_rewriter.rewrite(
            query=safe_query,
            memory=memory_context
        )

        docs = await self.retriever.retrieve(standalone_query)
        docs = self.reranker.rerank(standalone_query, docs)

        if not docs:
            return {
                "answer": "I could not find enough relevant support in the Zimbabwe Constitution to answer that confidently.",
                "sources": []
            }

        context = self.compressor.compress(docs)
        context_text = "\n\n".join(context).strip()

        if not context_text:
            context_text = "\n\n".join(
                [doc.page_content for doc in docs if hasattr(doc, "page_content")]
            ).strip()

        prompt = self.prompt_builder.build(
            query=standalone_query,
            context=context_text,
            memory=memory_context
        )

        answer = await self.generator.generate(prompt)
        
        safe_answer = await self.guardrails.validate_output(
            query=standalone_query, 
            answer=answer, 
            context_text=context_text
        )

        # 3. Update memory (Sync for Postgres, Async for Agentic Vector Reflection)
        memory.update_sync(safe_query, safe_answer)
        await memory.update_async(safe_query, safe_answer)

        sources = self.source_formatter.format(docs)

        return {
            "answer": safe_answer,
            "sources": sources
        }