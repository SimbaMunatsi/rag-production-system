from deepeval.metrics import AnswerRelevancyMetric
from deepeval.test_case import LLMTestCase
from deepeval import evaluate

#from app.rag.pipeline import RAGPipeline
from app.rag.service import create_rag_pipeline
def run_deepeval():

    #rag = RAGPipeline()
    rag = create_rag_pipeline()

    test_case = LLMTestCase(
        input="What is the role of the Constitutional Court?",
        actual_output=rag.run("What is the role of the Constitutional Court?")["answer"],
        expected_output="The Constitutional Court is the highest court on constitutional matters."
    )

    metric = AnswerRelevancyMetric()

    evaluate([test_case], [metric])