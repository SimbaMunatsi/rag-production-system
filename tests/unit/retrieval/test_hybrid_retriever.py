import pytest
from unittest.mock import Mock, patch

from app.retrieval.hybrid_retriever import HybridRetriever
from tests.fixtures.sample_documents import SAMPLE_DOCUMENTS


class TestHybridRetriever:

    @pytest.fixture
    def mock_vector_store(self):
        """Mock vector store to avoid real embeddings."""
        mock_store = Mock()
        mock_store.similarity_search.return_value = SAMPLE_DOCUMENTS[:2]  # Return first 2 docs
        return mock_store

    @pytest.fixture
    def mock_keyword_retriever(self):
        """Mock keyword retriever to avoid BM25 computation."""
        mock_retriever = Mock()
        mock_retriever.get_relevant_documents.return_value = SAMPLE_DOCUMENTS[1:3]  # Return docs 1 and 2
        return mock_retriever

    @pytest.fixture
    def hybrid_retriever(self, mock_vector_store, mock_keyword_retriever):
        """Create HybridRetriever with mocked dependencies."""
        with patch('app.retrieval.hybrid_retriever.get_vector_store', return_value=mock_vector_store), \
             patch('langchain_community.retrievers.BM25Retriever.from_documents', return_value=mock_keyword_retriever):
            retriever = HybridRetriever(documents=SAMPLE_DOCUMENTS, k=4)
            return retriever

    def test_retrieve_normal_success(self, hybrid_retriever, mock_vector_store, mock_keyword_retriever):
        """Test successful retrieval combining vector and keyword results."""
        query = "What is the amendment process?"

        results = hybrid_retriever.retrieve(query)

        # Verify both retrievers were called
        mock_vector_store.similarity_search.assert_called_once_with(query, k=4)
        mock_keyword_retriever.get_relevant_documents.assert_called_once_with(query)

        # Should return unique documents (vector: docs 0,1; keyword: docs 1,2 -> unique: docs 0,1,2)
        assert len(results) == 3
        assert results[0].page_content == SAMPLE_DOCUMENTS[0].page_content
        assert results[1].page_content == SAMPLE_DOCUMENTS[1].page_content
        assert results[2].page_content == SAMPLE_DOCUMENTS[2].page_content

    def test_retrieve_empty_vector_results(self, hybrid_retriever, mock_vector_store, mock_keyword_retriever):
        """Test behavior when vector search returns empty results."""
        mock_vector_store.similarity_search.return_value = []

        query = "Some query"
        results = hybrid_retriever.retrieve(query)

        # Should still return keyword results
        assert len(results) == 2  # keyword returns docs 1 and 2
        assert results[0].page_content == SAMPLE_DOCUMENTS[1].page_content
        assert results[1].page_content == SAMPLE_DOCUMENTS[2].page_content

    def test_retrieve_empty_keyword_results(self, hybrid_retriever, mock_vector_store, mock_keyword_retriever):
        """Test behavior when keyword search returns empty results."""
        mock_keyword_retriever.get_relevant_documents.return_value = []

        query = "Some query"
        results = hybrid_retriever.retrieve(query)

        # Should still return vector results
        assert len(results) == 2  # vector returns docs 0 and 1
        assert results[0].page_content == SAMPLE_DOCUMENTS[0].page_content
        assert results[1].page_content == SAMPLE_DOCUMENTS[1].page_content

    def test_retrieve_k_parameter(self, mock_vector_store, mock_keyword_retriever):
        """Test that k parameter is passed correctly to vector search."""
        with patch('app.retrieval.hybrid_retriever.get_vector_store', return_value=mock_vector_store), \
             patch('langchain_community.retrievers.BM25Retriever.from_documents', return_value=mock_keyword_retriever):
            retriever = HybridRetriever(documents=SAMPLE_DOCUMENTS, k=6)

        query = "Test query"
        retriever.retrieve(query)

        # Verify k=6 was passed to vector search
        mock_vector_store.similarity_search.assert_called_once_with(query, k=6)

    def test_retrieve_removes_duplicates(self, hybrid_retriever, mock_vector_store, mock_keyword_retriever):
        """Test that duplicate documents are removed from combined results."""
        # Make both retrievers return the same document
        mock_vector_store.similarity_search.return_value = [SAMPLE_DOCUMENTS[0]]
        mock_keyword_retriever.get_relevant_documents.return_value = [SAMPLE_DOCUMENTS[0]]

        query = "Duplicate test"
        results = hybrid_retriever.retrieve(query)

        # Should return only one instance
        assert len(results) == 1
        assert results[0].page_content == SAMPLE_DOCUMENTS[0].page_content
