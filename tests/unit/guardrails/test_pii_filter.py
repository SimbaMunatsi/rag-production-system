import pytest

from app.guardrails.pii_filter import PIIFilter
from tests.fixtures.sample_queries import VALID_CONSTITUTIONAL_QUESTIONS


class TestPIIFilter:

    @pytest.fixture
    def pii_filter(self):
        """Create PIIFilter instance."""
        return PIIFilter()

    def test_contains_pii_email_addresses(self, pii_filter):
        """Test detection of email addresses."""
        texts_with_emails = [
            "Contact me at user@example.com for more info.",
            "My email is test.email+tag@domain.co.uk",
            "Send to admin@constitution.gov.zw please."
        ]

        for text in texts_with_emails:
            assert pii_filter.contains_pii(text) is True, f"Should detect email in: {text}"

    # def test_contains_pii_phone_numbers(self, pii_filter):
    #     """Test detection of phone numbers."""
    #     texts_with_phones = [
    #         "Call me at +263772123456",
    #         "My number is 0772123456",
    #         "Contact: +1-555-123-4567",
    #         "Phone: 263772123456"
    #     ]

    #     for text in texts_with_phones:
    #         assert pii_filter.contains_pii(text) is True, f"Should detect phone in: {text}"

    def test_contains_pii_no_pii(self, pii_filter):
        """Test that text without PII passes."""
        texts_without_pii = [
            "What is section 67 about?",
            "The Constitution provides for political rights.",
            "Section 328 covers amendments.",
            "Zimbabwe is a unitary republic."
        ]

        for text in texts_without_pii:
            assert pii_filter.contains_pii(text) is False, f"Should not detect PII in: {text}"

    def test_contains_pii_constitutional_queries(self, pii_filter):
        """Test that valid constitutional questions pass PII check."""
        for query in VALID_CONSTITUTIONAL_QUESTIONS:
            assert pii_filter.contains_pii(query) is False, f"Constitutional query should pass: {query}"

    def test_contains_pii_empty_text(self, pii_filter):
        """Test PII detection with empty text."""
        assert pii_filter.contains_pii("") is False

    def test_contains_pii_whitespace_only(self, pii_filter):
        """Test PII detection with whitespace-only text."""
        assert pii_filter.contains_pii("   \n\t  ") is False
