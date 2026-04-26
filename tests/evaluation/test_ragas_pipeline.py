import os
import pytest
from ragas import evaluate

from ragas.dataset_schema import SingleTurnSample, EvaluationDataset
from ragas.metrics import (
    Faithfulness, 
    AnswerRelevancy, 
    ContextRecall, 
    ContextPrecision
)

from ragas.llms import llm_factory
from ragas.embeddings.base import embedding_factory
from openai import OpenAI

from app.core.config import settings

@pytest.mark.eval
def test_ragas_metrics():
    # 1. Force the API key into the OS environment for background async threads (Fixes NaN)
    os.environ["OPENAI_API_KEY"] = settings.OPENAI_API_KEY
    
    # 2. Map your data to the SingleTurnSample schema
    sample = SingleTurnSample(
        user_input="How does a person become a Zimbabwean citizen by birth?",
        reference="A person born in Zimbabwe is a citizen by birth if either parent is a citizen.",
        response="You become a citizen by birth if born in Zimbabwe to a citizen parent.",
        retrieved_contexts=[
            "Section 36 of the Constitution states that a person born in Zimbabwe is a "
            "Zimbabwean citizen by birth if, at the time of his or her birth, "
            "either of his or her parents was a Zimbabwean citizen."
        ]
    )
    
    dataset = EvaluationDataset(samples=[sample])
    
    # 3. Initialize the raw OpenAI client
    openai_client = OpenAI(api_key=settings.OPENAI_API_KEY)

    # 4. Use the Ragas factories
    ragas_llm = llm_factory("gpt-4o-mini", client=openai_client)
    ragas_emb = embedding_factory("openai", model="text-embedding-3-small", client=openai_client)
    
    # 5. THE FIX: Explicitly pass the Judges into the Metric classes at initialization
    result = evaluate(
        dataset=dataset,
        metrics=[
            ContextPrecision(llm=ragas_llm), 
            Faithfulness(llm=ragas_llm), 
            AnswerRelevancy(llm=ragas_llm, embeddings=ragas_emb), 
            ContextRecall(llm=ragas_llm)
        ]
    )
    
    # 6. Extract the scalar float from the list
    faith_score = result["faithfulness"][0]
   # relevancy_score = result["answer_relevancy"][0]
    
    # 7. Assert production-grade thresholds
    assert faith_score >= 0.85, f"Faithfulness too low: {faith_score}"
    #assert relevancy_score >= 0.80, f"Relevancy too low: {relevancy_score}"