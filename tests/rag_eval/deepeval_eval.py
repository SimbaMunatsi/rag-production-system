from deepeval.metrics import AnswerRelevancyMetric
from deepeval.test_case import LLMTestCase
from deepeval import evaluate

#from app.rag.pipeline import RAGPipeline
from app.rag.service import create_rag_pipeline
def run_deepeval():

    #rag = RAGPipeline()
    rag = create_rag_pipeline()

    test_case = LLMTestCase(
        input="What is Artificial Intelligence (AI)?",
        actual_output=rag.run("What is Artificial Intelligence (AI)?")["answer"],
        expected_output="Artificial Intelligence is the ability of machines to imitate human intelligence, specifically the cognitive problem-solving capabilities such as learning, reasoning, and creating."
    )

    metric = AnswerRelevancyMetric()

    evaluate([test_case], [metric])