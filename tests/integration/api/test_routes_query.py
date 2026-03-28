import pytest
from unittest.mock import Mock
from fastapi.testclient import TestClient

from app.api.main import app
from app.api.dependencies import get_rag_pipeline


class TestRoutesQuery:

    @pytest.fixture
    def mock_rag_pipeline(self):
        """Mock RAG pipeline to avoid real LLM/retrieval calls."""
        mock_pipeline = Mock()
        mock_pipeline.run.return_value = {
            "answer": "Section 67 covers political rights.",
            "sources": ["Section 67: Every citizen has political rights..."]
        }
        return mock_pipeline

    @pytest.fixture
    def client_with_overrides(self, mock_rag_pipeline):
        """Create TestClient with dependency overrides to mock RAG pipeline."""
        app.dependency_overrides[get_rag_pipeline] = lambda: mock_rag_pipeline
        client = TestClient(app)
        yield client
        app.dependency_overrides.clear()

    def test_query_happy_path(self, client_with_overrides):
        """Test successful POST request to /query endpoint."""
        payload = {
            "query": "What are political rights under section 67?",
            "session_id": "test-session-123"
        }

        response = client_with_overrides.post("/query", json=payload)

        assert response.status_code == 200
        data = response.json()
        assert "answer" in data
        assert "sources" in data
        assert data["answer"] == "Section 67 covers political rights."
        assert isinstance(data["sources"], list)

    def test_query_response_schema(self, client_with_overrides):
        """Test that response conforms to QueryResponse schema."""
        payload = {
            "query": "What is section 6?",
            "session_id": "test-session-456"
        }

        response = client_with_overrides.post("/query", json=payload)

        assert response.status_code == 200
        data = response.json()
        assert isinstance(data["answer"], str)
        assert isinstance(data["sources"], list)
        assert all(isinstance(src, str) for src in data["sources"])

    def test_query_missing_required_field_query(self, client_with_overrides):
        """Test that missing 'query' field returns validation error."""
        payload = {
            "session_id": "test-session-789"
        }

        response = client_with_overrides.post("/query", json=payload)

        assert response.status_code == 422  # Unprocessable Entity

    def test_query_missing_required_field_session_id(self, client_with_overrides):
        """Test that missing 'session_id' field returns validation error."""
        payload = {
            "query": "What is the Constitution?"
        }

        response = client_with_overrides.post("/query", json=payload)

        assert response.status_code == 422

    def test_query_empty_payload(self, client_with_overrides):
        """Test that empty JSON payload returns validation error."""
        response = client_with_overrides.post("/query", json={})

        assert response.status_code == 422

    def test_query_with_empty_sources(self, client_with_overrides, mock_rag_pipeline):
        """Test fallback behavior when retrieval returns no sources."""
        mock_rag_pipeline.run.return_value = {
            "answer": "I could not find enough relevant support in the Zimbabwe Constitution to answer that confidently.",
            "sources": []
        }

        payload = {
            "query": "What is the weather in Harare?",
            "session_id": "test-session-out-of-scope"
        }

        response = client_with_overrides.post("/query", json=payload)

        assert response.status_code == 200
        data = response.json()
        assert data["sources"] == []

    def test_query_dependency_receives_correct_params(self, client_with_overrides, mock_rag_pipeline):
        """Test that the RAG pipeline is called with correct parameters."""
        payload = {
            "query": "Test question",
            "session_id": "test-session-params"
        }

        client_with_overrides.post("/query", json=payload)

        mock_rag_pipeline.run.assert_called_once_with(
            query="Test question",
            session_id="test-session-params"
        )

    def test_health_endpoint(self, client_with_overrides):
        """Test that health endpoint works."""
        response = client_with_overrides.get("/health")

        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "ok"
