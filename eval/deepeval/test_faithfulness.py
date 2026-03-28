import pytest

from deepeval.metrics.faithfulness.faithfulness import FaithfulnessMetric
from deepeval.metrics.faithfulness.schema import FaithfulnessVerdict
from deepeval.metrics.faithfulness.template import FaithfulnessTemplate
from deepeval.test_case import LLMTestCase


class DummyFaithfulnessMetric(FaithfulnessMetric):
    def __init__(self, **kwargs):
        # Avoid loader model initialization for unit tests.
        self.threshold = kwargs.get("threshold", 0.5)
        self.model = None
        self.using_native_model = True
        self.include_reason = kwargs.get("include_reason", False)
        self.async_mode = kwargs.get("async_mode", False)
        self.strict_mode = kwargs.get("strict_mode", False)
        self.verbose_mode = kwargs.get("verbose_mode", False)
        self.evaluation_template = kwargs.get("evaluation_template", FaithfulnessTemplate)
        self.penalize_ambiguous_claims = kwargs.get("penalize_ambiguous_claims", False)
        self.truths_extraction_limit = kwargs.get("truths_extraction_limit", None)


def test_faithfulness_metric_when_faithful():
    metric = DummyFaithfulnessMetric(include_reason=False, async_mode=False)

    metric._generate_truths = lambda retrieval_context, multimodal: ["1+1 equals 2"]
    metric._generate_claims = lambda actual_output, multimodal: ["1+1 equals 2"]
    metric._generate_verdicts = lambda multimodal: [FaithfulnessVerdict(verdict="yes")]

    test_case = LLMTestCase(
        input="What is 1+1?",
        actual_output="1+1 equals 2",
        retrieval_context=["1+1 equals 2"],
    )

    score = metric.measure(
        test_case,
        _show_indicator=False,
        _in_component=False,
        _log_metric_to_confident=False,
    )

    assert score == 1.0
    assert metric.success is True


def test_faithfulness_metric_when_unfaithful():
    metric = DummyFaithfulnessMetric(include_reason=False, async_mode=False)

    metric._generate_truths = lambda retrieval_context, multimodal: ["1+1 equals 2"]
    metric._generate_claims = lambda actual_output, multimodal: ["1+1 equals 3"]
    metric._generate_verdicts = lambda multimodal: [
        FaithfulnessVerdict(verdict="no", reason="Claim is not supported by retrieval context")
    ]

    test_case = LLMTestCase(
        input="What is 1+1?",
        actual_output="1+1 equals 3",
        retrieval_context=["1+1 equals 2"],
    )

    score = metric.measure(
        test_case,
        _show_indicator=False,
        _in_component=False,
        _log_metric_to_confident=False,
    )

    assert score == 0.0
    assert metric.success is False
