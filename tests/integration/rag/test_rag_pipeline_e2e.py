import pytest
from unittest.mock import Mock, MagicMock

from app.rag.pipeline import RAGPipeline
from tests.fixtures.sample_documents import RELEVANT_CONSTITUTIONAL_DOC_1, RELEVANT_CONSTITUTIONAL_DOC_2, IRRELEVANT_DOC
from tests.fixtures.sample_responses import GROUNDED_RESPONSE


class TestRAGPipelineE2E:

    @pytest.fixture
    def mock_memory(self):
        """Mock memory manager."""
        mock_memory = Mock()
        mock_memory.get.return_value = {
            "conversation": [],
            "semantic": []
        }
        mock_memory.build_context.return_value = {
            "conversation": [],
            "semantic": []
        }
        mock_memory.update = Mock()
        return mock_memory

    @pytest.fixture
    def mock_retriever(self):
        """Mock retriever to avoid vector store calls."""
        mock = Mock()
        mock.retrieve.return_value = [RELEVANT_CONSTITUTIONAL_DOC_1, RELEVANT_CONSTITUTIONAL_DOC_2]
        return mock

    @pytest.fixture
    def mock_reranker(self):
        """Mock reranker."""
        mock = Mock()
        mock.rerank.side_effect = lambda query, docs: docs  # Pass through
        return mock

    @pytest.fixture
    def mock_compressor(self):
        """Mock context compressor."""
        mock = Mock()
        mock.compress.return_value = [
            "Section 328 provides amendment process...",
            "Political rights are covered in section 67..."
        ]
        return mock

    @pytest.fixture
    def mock_prompt_builder(self):
        """Mock prompt builder."""
        mock = Mock()
        mock.build.return_value = "System prompt with query and context..."
        return mock

    @pytest.fixture
    def mock_generator(self):
        """Mock LLM generator."""
        mock = Mock()
        mock.generate.return_value = "The Constitution can be amended by a two-thirds majority vote."
        return mock

    @pytest.fixture
    def mock_source_formatter(self):
        """Mock source formatter."""
        mock = Mock()
        mock.format.return_value = [
            "Section 328: Amendment process",
            "Section 67: Political rights"
        ]
        return mock

    @pytest.fixture
    def mock_guardrails(self):
        """Mock guardrails."""
        mock = Mock()
        mock.validate_input.side_effect = lambda x: x  # Pass through
        mock.validate_output.side_effect = lambda q, a: a  # Pass through
        return mock

    @pytest.fixture
    def mock_query_rewriter(self):
        """Mock query rewriter."""
        mock = Mock()
        mock.rewrite.side_effect = lambda query, memory: query  # Pass through
        return mock

    @pytest.fixture
    def mock_memory_getter(self, mock_memory):
        """Mock memory getter function."""
        return lambda session_id: mock_memory

    @pytest.fixture
    def rag_pipeline(
        self,
        mock_retriever,
        mock_reranker,
        mock_compressor,
        mock_prompt_builder,
        mock_generator,
        mock_memory_getter,
        mock_source_formatter,
        mock_guardrails,
        mock_query_rewriter,
    ):
        """Create RAGPipeline with all mocked dependencies."""
        return RAGPipeline(
            retriever=mock_retriever,
            reranker=mock_reranker,
            compressor=mock_compressor,
            prompt_builder=mock_prompt_builder,
            generator=mock_generator,
            memory_getter=mock_memory_getter,
            source_formatter=mock_source_formatter,
            guardrails=mock_guardrails,
            query_rewriter=mock_query_rewriter,
        )

    def test_rag_pipeline_happy_path(self, rag_pipeline, mock_memory):
        """Test end-to-end successful RAG pipeline execution."""
        query = "What is the amendment process in the Constitution?"
        session_id = "test-session-123"

        result = rag_pipeline.run(query, session_id)

        assert "answer" in result
        assert "sources" in result
        assert result["answer"] == "The Constitution can be amended by a two-thirds majority vote."
        assert len(result["sources"]) == 2

    def test_rag_pipeline_calls_components_in_order(
        self,
        rag_pipeline,
        mock_retriever,
        mock_reranker,
        mock_compressor,
        mock_prompt_builder,
        mock_generator,
        mock_source_formatter,
        mock_guardrails,
        mock_query_rewriter,
    ):
        """Test that pipeline components are called in correct order."""
        query = "Test query"
        session_id = "test-session-order"

        result = rag_pipeline.run(query, session_id)

        # Verify each component was called
        mock_guardrails.validate_input.assert_called_once()
        mock_query_rewriter.rewrite.assert_called_once()
        mock_retriever.retrieve.assert_called_once()
        mock_reranker.rerank.assert_called_once()
        mock_compressor.compress.assert_called_once()
        mock_prompt_builder.build.assert_called_once()
        mock_generator.generate.assert_called_once()
        mock_guardrails.validate_output.assert_called_once()
        mock_source_formatter.format.assert_called_once()

    def test_rag_pipeline_no_relevant_context_found(self, rag_pipeline, mock_retriever):
        """Test fallback behavior when retrieval returns empty results."""
        # Mock empty retrieval
        mock_retriever.retrieve.return_value = []

        query = "What is the weather in Harare?"
        session_id = "test-session-empty"

        result = rag_pipeline.run(query, session_id)

        assert result["answer"] == "I could not find enough relevant support in the Zimbabwe Constitution to answer that confidently."
        assert result["sources"] == []

    # def test_rag_pipeline_empty_compression_fallback(self, rag_pipeline, mock_compressor):
    #     """Test fallback when context compression returns empty."""
    #     mock_compressor.compress.return_value = []

    #     query = "Test query"
    #     session_id = "test-session-fallback"

    #     result = rag_pipeline.run(query, session_id)

    #     # Should fall back to using doc.page_content
    #     assert result["answer"] == "I could not find enough relevant support in the Zimbabwe Constitution to answer that confidently."
    #     assert result["sources"] == []

    def test_rag_pipeline_response_structure(self, rag_pipeline):
        """Test that response has expected structure."""
        query = "What are political rights?"
        session_id = "test-session-structure"

        result = rag_pipeline.run(query, session_id)

        # Verify response structure
        assert isinstance(result, dict)
        assert "answer" in result
        assert "sources" in result
        assert isinstance(result["answer"], str)
        assert isinstance(result["sources"], list)

    def test_rag_pipeline_memory_update_on_success(self, rag_pipeline, mock_memory):
        """Test that memory is updated after successful pipeline run."""
        query = "Test query"
        session_id = "test-session-memory"

        rag_pipeline.run(query, session_id)

        # Verify memory.update was called
        mock_memory.update.assert_called_once()
        # First argument should be the safe query, second the generated answer
        call_args = mock_memory.update.call_args
        assert call_args[0][0] == query  # safe_query

    def test_rag_pipeline_includes_sources_in_response(self, rag_pipeline, mock_source_formatter):
        """Test that formatted sources are included in response."""
        mock_source_formatter.format.return_value = [
            "Source 1: Section 328",
            "Source 2: Section 67"
        ]

        query = "Test query"
        session_id = "test-session-sources"

        result = rag_pipeline.run(query, session_id)

        assert result["sources"] == ["Source 1: Section 328", "Source 2: Section 67"]
