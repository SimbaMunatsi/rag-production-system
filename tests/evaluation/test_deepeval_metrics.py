import pytest
from deepeval import assert_test
from deepeval.test_case import LLMTestCase
from deepeval.metrics import HallucinationMetric

@pytest.mark.eval
def test_for_hallucinations():
    # 1. Simulate the pipeline output
    input_query = "Can the President of Zimbabwe be removed?"
    actual_output = "Yes, the President can be removed by a joint resolution of the Senate and National Assembly."
    retrieved_context = ["The President may be removed from office for serious misconduct by a joint resolution passed by at least two-thirds of the total membership of Parliament."]
    
    # 2. Create the test case
    test_case = LLMTestCase(
        input=input_query,
        actual_output=actual_output,
        context=retrieved_context
    )
    
    # 3. Define the metric (Fail if hallucination score is > 0.3)
    metric = HallucinationMetric(threshold=0.3)
    
    # 4. DeepEval's native pytest integration
    assert_test(test_case, [metric])