import pytest

from app.generation.prompt_builder import PromptBuilder
from tests.fixtures.sample_contexts import GROUNDED_CONSTITUTIONAL_CONTEXTS, EMPTY_CONTEXT


class TestPromptBuilder:

    @pytest.fixture
    def prompt_builder(self):
        """Create PromptBuilder instance."""
        return PromptBuilder()

    @pytest.fixture
    def sample_memory(self):
        """Sample memory structure for testing."""
        return {
            "conversation": [
                {"role": "user", "content": "What is section 67 about?"},
                {"role": "assistant", "content": "Section 67 covers political rights."}
            ],
            "semantic": ["Previous topics: political rights, equality"]
        }

    def test_build_includes_user_question(self, prompt_builder, sample_memory):
        """Test that the built prompt includes the user question."""
        query = "What is the amendment process?"
        context = GROUNDED_CONSTITUTIONAL_CONTEXTS[0]

        prompt = prompt_builder.build(query, context, sample_memory)

        assert "User Question:" in prompt
        assert query in prompt

    def test_build_includes_retrieved_context(self, prompt_builder, sample_memory):
        """Test that the built prompt includes the retrieved constitutional context."""
        query = "Test query"
        context = GROUNDED_CONSTITUTIONAL_CONTEXTS[0]

        prompt = prompt_builder.build(query, context, sample_memory)

        assert "Retrieved Context:" in prompt
        assert context in prompt

    def test_build_includes_grounding_instructions(self, prompt_builder, sample_memory):
        """Test that the built prompt includes grounding instructions."""
        query = "Test query"
        context = GROUNDED_CONSTITUTIONAL_CONTEXTS[0]

        prompt = prompt_builder.build(query, context, sample_memory)

        # Check for key instruction phrases
        assert "You are an AI assistant specialized in answering questions about the Zimbabwe Constitution" in prompt
        assert "Answer using only the provided context" in prompt
        assert "Do not use outside knowledge" in prompt
        assert "Be precise, clear, and grounded in the provided constitutional context" in prompt

    def test_build_handles_empty_context(self, prompt_builder, sample_memory):
        """Test that the prompt handles empty context safely."""
        query = "What is the amendment process?"
        context = EMPTY_CONTEXT

        prompt = prompt_builder.build(query, context, sample_memory)

        # Should still include the query and instructions
        assert "User Question:" in prompt
        assert query in prompt
        assert "Retrieved Context:" in prompt
        # Context section should be present but empty
        assert "Retrieved Context:\n\n" in prompt or "Retrieved Context:\n" in prompt

    def test_build_preserves_conversation_history(self, prompt_builder, sample_memory):
        """Test that conversation history is included in the prompt."""
        query = "Follow-up question"
        context = GROUNDED_CONSTITUTIONAL_CONTEXTS[0]

        prompt = prompt_builder.build(query, context, sample_memory)

        assert "Conversation History:" in prompt
        assert "user: What is section 67 about?" in prompt
        assert "assistant: Section 67 covers political rights." in prompt

    def test_build_preserves_semantic_memory(self, prompt_builder, sample_memory):
        """Test that semantic memory is included in the prompt."""
        query = "Test query"
        context = GROUNDED_CONSTITUTIONAL_CONTEXTS[0]

        prompt = prompt_builder.build(query, context, sample_memory)

        assert "Semantic Memory:" in prompt
        assert "Previous topics: political rights, equality" in prompt

    def test_build_includes_special_cases(self, prompt_builder, sample_memory):
        """Test that special case instructions are included."""
        query = "Test query"
        context = GROUNDED_CONSTITUTIONAL_CONTEXTS[0]

        prompt = prompt_builder.build(query, context, sample_memory)

        assert "Special Cases:" in prompt
        assert "I am BUMBIRO" in prompt
        assert "The Constitution of Zimbabwe is the supreme law" in prompt
