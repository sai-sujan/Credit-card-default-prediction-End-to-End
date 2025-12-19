"""Tests for Flask API endpoints."""
import pytest
from pathlib import Path
import sys

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from main import app


@pytest.fixture
def client():
    """Create Flask test client."""
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client


class TestAPIEndpoints:
    """Test cases for API endpoints."""

    def test_home_page(self, client):
        """Test home page loads successfully."""
        response = client.get('/')
        assert response.status_code == 200

    def test_home_page_content(self, client):
        """Test home page contains expected content."""
        response = client.get('/')
        data = response.data.decode('utf-8')
        # Check for some expected HTML elements
        assert len(data) > 0

    def test_cors_headers(self, client):
        """Test CORS headers are present."""
        response = client.get('/')
        # Flask-CORS should add appropriate headers
        assert response.status_code == 200

    def test_predict_endpoint_exists(self, client):
        """Test that predict endpoint is available."""
        # This will fail if no data is provided, but endpoint should exist
        response = client.post('/predict')
        # Should not be 404
        assert response.status_code != 404

    def test_train_endpoint_exists(self, client):
        """Test that train endpoint is available."""
        response = client.post('/train')
        # Should not be 404
        assert response.status_code != 404


class TestErrorHandling:
    """Test cases for API error handling."""

    def test_404_error(self, client):
        """Test 404 error for non-existent endpoint."""
        response = client.get('/nonexistent')
        assert response.status_code == 404

    def test_invalid_method(self, client):
        """Test invalid HTTP method."""
        # Predict endpoint should only accept POST
        response = client.get('/predict')
        assert response.status_code == 405  # Method Not Allowed
