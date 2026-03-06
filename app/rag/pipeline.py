class RAGPipeline:

    def __init__(
        self,
        retriever,
        reranker,
        compressor,
        prompt_builder,
        generator,
        memory,
        source_formatter
    ):

        self.retriever = retriever
        self.reranker = reranker
        self.compressor = compressor
        self.prompt_builder = prompt_builder
        self.generator = generator
        self.memory = memory
        self.source_formatter = source_formatter


    def run(self, query):

        docs = self.retriever.retrieve(query)

        docs = self.reranker.rerank(query, docs)

        context = self.compressor.compress(docs)

        context_text = "\n\n".join(context)

        prompt = self.prompt_builder.build(query, context_text)

        answer = self.generator.generate(prompt)

        self.memory.add(query, answer)

        sources = self.source_formatter.format(docs)

        return {
            "answer": answer,
            "sources": sources
        }