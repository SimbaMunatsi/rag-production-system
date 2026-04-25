import datetime
import math
import asyncio
from typing import List
from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from langchain_postgres.vectorstores import PGVector

from app.core.config import settings
from app.core.vector_store import get_vector_store

class AgenticMemory:
    def __init__(self, session_id: str):
        self.session_id = session_id
        self.llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)
        
        # Initialize the vector store for the agentic memory collection
        self.vector_store = get_vector_store()
        self.vector_store.collection_name = "user_agentic_memory"
        
        # --- THE FIX: Explicitly create the collection if it doesn't exist ---
        self.vector_store.create_collection()

        self.reflection_prompt = PromptTemplate.from_template(
            "You are a memory consolidation agent. Analyze the following conversation turn.\n"
            "Extract ONLY permanent facts, preferences, or significant events about the user.\n"
            "If there is nothing significant to remember, output exactly 'NONE'.\n"
            "User: {query}\n"
            "Assistant: {answer}\n"
            "Memory Fact:"
        )

    async def reflect_and_store(self, query: str, answer: str):
        """Asynchronously extracts facts and stores them in pgvector via thread offloading."""
        chain = self.reflection_prompt | self.llm
        result = await chain.ainvoke({"query": query, "answer": answer})
        
        fact = result.content.strip()
        if fact != "NONE":
            await asyncio.to_thread(
                self.vector_store.add_texts,
                texts=[fact],
                metadatas=[{
                    "session_id": self.session_id,
                    "timestamp": datetime.datetime.utcnow().isoformat()
                }]
            )

    async def retrieve_relevant_facts(self, query: str, k: int = 3) -> str:
        """Retrieves facts using vector similarity combined with time decay via thread offloading."""
        try:
            results = await asyncio.to_thread(
                self.vector_store.similarity_search_with_relevance_scores,
                query, 
                k=k * 3, 
                filter={"session_id": self.session_id}
            )
        except ValueError as e:
            # Fallback: If for some reason the collection is completely empty and LangChain 
            # still throws the "Collection not found" error during the search, we catch it 
            # and just return no facts.
            if "Collection not found" in str(e):
                return ""
            raise e

        if not results:
            return ""

        scored_facts = []
        now = datetime.datetime.utcnow()

        for doc, similarity_score in results:
            fact_time = datetime.datetime.fromisoformat(doc.metadata["timestamp"])
            days_old = (now - fact_time).days

            decay_rate = 0.05
            time_decay_factor = math.exp(-decay_rate * days_old)
            
            final_score = similarity_score * time_decay_factor
            
            scored_facts.append((final_score, doc.page_content))

        scored_facts.sort(key=lambda x: x[0], reverse=True)
        top_facts = [fact for score, fact in scored_facts[:k]]

        return "\n".join(top_facts)