import os
import json
import asyncio
from pydantic import BaseModel, Field
from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from app.core.config import settings

# Import your existing ingestion modules
from app.ingestion.document_loader import DocumentLoader
from app.ingestion.document_cleaner import DocumentCleaner

# 1. Define the exact JSON structure we need for Ragas/DeepEval
class QAPair(BaseModel):
    question: str = Field(description="A clear, specific question based on the text.")
    ground_truth: str = Field(description="The exact, factual answer based ONLY on the text.")

class SyntheticDataset(BaseModel):
    items: list[QAPair]

async def generate_dataset(num_chunks_to_process=10):
    print("========================================")
    print("🧠 Generating Synthetic Golden Dataset...")
    print("========================================")

    # 1. Load a sample of your actual documents
    print("Loading Constitution documents...")
    loader = DocumentLoader("data/raw")
    raw_docs = loader.load()
    
    cleaner = DocumentCleaner()
    docs = cleaner.clean(raw_docs)
    
    # We don't need to process the whole book, just a solid sample
    sample_docs = docs[:num_chunks_to_process]
    
    # 2. Set up the Teacher LLM with strict JSON output
    # Using gpt-4o because the "Teacher" needs to be highly accurate
    llm = ChatOpenAI(
        model="gpt-4o", 
        temperature=0.2,
        api_key=settings.OPENAI_API_KEY # <-- Add the explicit key here
    )
    structured_llm = llm.with_structured_output(SyntheticDataset)
    
    prompt = PromptTemplate.from_template(
        "You are an expert legal examiner creating a test for law students.\n"
        "Read the following excerpt from the Zimbabwe Constitution.\n"
        "Generate 2 complex, highly specific question-and-answer pairs based STRICTLY on this text.\n"
        "The questions should test deep understanding, not just keyword matching.\n\n"
        "Excerpt:\n{context}"
    )
    
    chain = prompt | structured_llm
    
    final_dataset = {
        "question": [],
        "ground_truth": [],
        "contexts": [] # Ragas needs the context that generated the truth
    }

    print(f"Generating questions from {len(sample_docs)} document chunks...")
    
    # 3. Generate the questions
    for i, doc in enumerate(sample_docs):
        print(f"Processing chunk {i+1}/{len(sample_docs)}...")
        try:
            result = await chain.ainvoke({"context": doc.page_content})
            
            for item in result.items:
                final_dataset["question"].append(item.question)
                # Ragas expects ground_truth and contexts to be lists of strings
                final_dataset["ground_truth"].append([item.ground_truth])
                final_dataset["contexts"].append([doc.page_content])
                
        except Exception as e:
            print(f"Skipped chunk {i+1} due to error: {e}")

    # 4. Save to disk
    os.makedirs("tests/data", exist_ok=True)
    output_path = "tests/data/golden_dataset.json"
    
    with open(output_path, "w") as f:
        json.dump(final_dataset, f, indent=4)
        
    print(f"\n✅ Successfully generated {len(final_dataset['question'])} test cases!")
    print(f"💾 Saved to {output_path}")

if __name__ == "__main__":
    asyncio.run(generate_dataset())