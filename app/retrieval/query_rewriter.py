from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate

class QueryRewriter:
    def __init__(self):
        # We use a fast, cheap model for query rewriting
        self.llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)
        self.prompt = PromptTemplate.from_template(
            "You are an expert search query formulator for a legal database.\n"
            "Your task is to rewrite the user's latest query into a standalone, highly searchable query "
            "using the provided conversation history and known facts.\n\n"
            "Conversation History:\n{conversation}\n\n"
            "Known Facts about the user:\n{semantic}\n\n"
            "Latest Query: {query}\n\n"
            "If the latest query is already standalone and clear, just return it exactly as is. "
            "Output ONLY the rewritten query."
        )

    def rewrite(self, query: str, memory: dict) -> str:
        # 1. Safely extract the new memory strings
        conv_history = memory.get("conversation", "")
        semantic_facts = memory.get("semantic", "")
        
        # 2. If there is no history at all (e.g., the very first query), skip the LLM call to save time
        if not conv_history and not semantic_facts:
            return query

        # 3. Ask the LLM to rewrite the query with the full context
        chain = self.prompt | self.llm
        
        # Since this is synchronous, we use standard invoke. 
        # (It runs fast enough that it won't bottleneck the async pipeline significantly)
        result = chain.invoke({
            "conversation": conv_history,
            "semantic": semantic_facts,
            "query": query
        })
        
        return result.content.strip()