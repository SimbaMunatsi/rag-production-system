import pytest

from deepeval.metrics.hallucination.hallucination import HallucinationMetric
from deepeval.metrics.hallucination.schema import HallucinationVerdict
from deepeval.metrics.hallucination.template import HallucinationTemplate
from deepeval.test_case import LLMTestCase


class DummyHallucinationMetric(HallucinationMetric):
    def __init__(self, **kwargs):
        # Avoid real model initialization for unit tests.
        self.threshold = kwargs.get("threshold", 0.5)
        self.model = None
        self.using_native_model = True
        self.evaluation_model = "DummyModel"
        self.include_reason = kwargs.get("include_reason", False)
        self.async_mode = kwargs.get("async_mode", False)
        self.strict_mode = kwargs.get("strict_mode", False)
        self.verbose_mode = kwargs.get("verbose_mode", False)
        self.evaluation_template = kwargs.get("evaluation_template", HallucinationTemplate)


def test_hallucination_metric_when_grounded():
    """Test hallucination detection for grounded constitutional answer."""
    metric = DummyHallucinationMetric(include_reason=False, async_mode=False)

    # Mock verdicts: all agree (no hallucination)
    metric._generate_verdicts = lambda actual_output, contexts: [
        HallucinationVerdict(verdict="yes", reason="Output agrees with context on amendment process.")
    ]

    test_case = LLMTestCase(
        input="How can the Constitution be amended?",
        actual_output="The Constitution may be amended by a bill passed by at least two-thirds of Parliament and approved by two-thirds of the Senate.",
        context=["Section 328 of the Constitution provides that the Constitution may be amended by a bill passed by at least two-thirds of the members of Parliament and approved by at least two-thirds of the members of the Senate."],
    )

    score = metric.measure(
        test_case,
        _show_indicator=False,
        _in_component=False,
        _log_metric_to_confident=False,
    )

    assert score == 0.0  # No hallucinations
    assert metric.success is True


def test_hallucination_metric_when_hallucinated():
    """Test hallucination detection for unsupported constitutional claim."""
    metric = DummyHallucinationMetric(include_reason=False, async_mode=False)

    # Mock verdicts: contradicts context (hallucination)
    metric._generate_verdicts = lambda actual_output, contexts: [
        HallucinationVerdict(verdict="no", reason="Output claims amendment requires presidential approval, but context states only Parliament and Senate.")
    ]

    test_case = LLMTestCase(
        input="How can the Constitution be amended?",
        actual_output="The Constitution can be amended with presidential approval and a simple majority in Parliament.",
        context=["Section 328 of the Constitution provides that the Constitution may be amended by a bill passed by at least two-thirds of the members of Parliament and approved by at least two-thirds of the members of the Senate."],
    )

    score = metric.measure(
        test_case,
        _show_indicator=False,
        _in_component=False,
        _log_metric_to_confident=False,
    )

    assert score == 1.0  # Full hallucination
    assert metric.success is False


def test_hallucination_metric_with_weak_context():
    """Test hallucination detection when context is irrelevant."""
    metric = DummyHallucinationMetric(include_reason=False, async_mode=False)

    # Mock verdicts: context doesn't support legal claims (hallucination)
    metric._generate_verdicts = lambda actual_output, contexts: [
        HallucinationVerdict(verdict="no", reason="Context discusses weather, not constitutional rights.")
    ]

    test_case = LLMTestCase(
        input="What are the political rights in Zimbabwe?",
        actual_output="Citizens have the right to free elections and form political parties.",
        context=["The weather in Harare is generally warm and sunny throughout the year."],
    )

    score = metric.measure(
        test_case,
        _show_indicator=False,
        _in_component=False,
        _log_metric_to_confident=False,
    )

    assert score == 1.0  # Hallucination due to unsupported claims
    assert metric.success is False


# TODO: For production evaluation, configure a real model:
# - Set DEEPEVAL_MODEL environment variable or pass model parameter
# - Example: model="gpt-4" or use LocalModel for local LLM
# - Ensure model supports the required evaluation prompts
# - Consider async_mode=True for better performance
