import pytest
from unittest.mock import MagicMock, patch
from google.genai import errors
from src.core.gemini_client import GeminiClient, GeminiClientError

def test_client_init_without_key_raises_error():
    """Verify that calling generate without an API key raises GeminiClientError."""
    client = GeminiClient(api_key="")
    with pytest.raises(GeminiClientError) as exc_info:
        client.generate("hello")
    assert "key is not configured" in str(exc_info.value)

@patch("src.core.gemini_client.genai.Client")
def test_client_generate_success(mock_client_class):
    """Verify standard content generation flow under normal API execution."""
    mock_api_client = MagicMock()
    mock_response = MagicMock()
    mock_response.text = "This is a mock explanation."
    mock_api_client.models.generate_content.return_value = mock_response
    mock_client_class.return_value = mock_api_client

    client = GeminiClient(api_key="mock-api-key")
    result = client.generate("Explain SQL Joins")
    
    mock_client_class.assert_called_with(api_key="mock-api-key")
    mock_api_client.models.generate_content.assert_called_once()
    assert result == "This is a mock explanation."

@patch("src.core.gemini_client.genai.Client")
def test_client_generate_unexpected_failure(mock_client_class):
    """Verify that unexpected exceptions are wrapped in GeminiClientError."""
    mock_api_client = MagicMock()
    mock_api_client.models.generate_content.side_effect = Exception("API connection timed out")
    mock_client_class.return_value = mock_api_client

    client = GeminiClient(api_key="mock-api-key")
    with pytest.raises(GeminiClientError) as exc_info:
        client.generate("Explain SQL Joins")
        
    assert "unexpected error" in str(exc_info.value)

@patch("src.core.gemini_client.genai.Client")
def test_client_generate_rate_limit(mock_client_class):
    """Verify that HTTP 429 ClientErrors surface as a rate-limit message."""
    mock_api_client = MagicMock()
    mock_api_client.models.generate_content.side_effect = errors.ClientError(429, {})
    mock_client_class.return_value = mock_api_client

    client = GeminiClient(api_key="mock-api-key")
    with pytest.raises(GeminiClientError) as exc_info:
        client.generate("Explain SQL Joins")

    assert "Rate limit exceeded" in str(exc_info.value)

@patch("src.core.gemini_client.genai.Client")
def test_client_generate_invalid_request(mock_client_class):
    """Verify that HTTP 400 ClientErrors surface as an invalid-request message."""
    mock_api_client = MagicMock()
    mock_api_client.models.generate_content.side_effect = errors.ClientError(400, {})
    mock_client_class.return_value = mock_api_client

    client = GeminiClient(api_key="mock-api-key")
    with pytest.raises(GeminiClientError) as exc_info:
        client.generate("Explain SQL Joins")

    assert "Invalid API request" in str(exc_info.value)

@patch("src.core.gemini_client.genai.Client")
def test_client_generate_auth_failure(mock_client_class):
    """Verify that HTTP 401/403 ClientErrors surface as an authentication message."""
    mock_api_client = MagicMock()
    mock_api_client.models.generate_content.side_effect = errors.ClientError(401, {})
    mock_client_class.return_value = mock_api_client

    client = GeminiClient(api_key="mock-api-key")
    with pytest.raises(GeminiClientError) as exc_info:
        client.generate("Explain SQL Joins")

    assert "Authentication failed" in str(exc_info.value)

@patch("src.core.gemini_client.genai.Client")
def test_client_generate_server_error(mock_client_class):
    """Verify that ServerErrors surface as a temporarily-unavailable message."""
    mock_api_client = MagicMock()
    mock_api_client.models.generate_content.side_effect = errors.ServerError(503, {})
    mock_client_class.return_value = mock_api_client

    client = GeminiClient(api_key="mock-api-key")
    with pytest.raises(GeminiClientError) as exc_info:
        client.generate("Explain SQL Joins")

    assert "temporarily unavailable" in str(exc_info.value)