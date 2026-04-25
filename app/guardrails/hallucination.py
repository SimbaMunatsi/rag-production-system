from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate

class HallucinationChecker:
    def __init__(self):
        self.llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)
        self.prompt = PromptTemplate.from_template(
            "You are an evaluator grading a system's answer.\n"
            "Given the context below, determine if the answer is completely grounded in the factual context.\n\n"
            "Context: {context}\n"
            "Answer: {answer}\n\n"
            "Score the grounding from 0.0 to 1.0, where 1.0 means fully grounded and 0.0 means a complete hallucination. "
            "Respond with ONLY the float number."
        )

    async def check(self, answer: str, context_text: str) -> float:
        chain = self.prompt | self.llm
        try:
            response = await chain.ainvoke({
                "context": context_text, 
                "answer": answer
            })
            return float(response.content.strip())
        except ValueError:
            # Failsafe: if the LLM outputs text instead of a float, assume hallucination
            return 0.0