import pytest
from unittest.mock import MagicMock, patch
from google.api_core import exceptions
from src.core.gemini_client import GeminiClient, GeminiClientError

def test_client_init_without_key_raises_error():
    """Verify that calling generate without an API key raises GeminiClientError."""
    client = GeminiClient(api_key="")
    with pytest.raises(GeminiClientError) as exc_info:
        client.generate("hello")
    assert "key is not configured" in str(exc_info.value)

@patch("google.generativeai.configure")
@patch("google.generativeai.GenerativeModel")
def test_client_generate_success(mock_model_class, mock_configure):
    """Verify standard content generation flow under normal API execution."""
    mock_model_instance = MagicMock()
    mock_response = MagicMock()
    mock_response.text = "This is a mock explanation."
    mock_model_instance.generate_content.return_value = mock_response
    mock_model_class.return_value = mock_model_instance

    client = GeminiClient(api_key="mock-api-key")
    result = client.generate("Explain SQL Joins")
    
    mock_configure.assert_called_with(api_key="mock-api-key")
    mock_model_class.assert_called_once()
    assert result == "This is a mock explanation."

@patch("google.generativeai.configure")
@patch("google.generativeai.GenerativeModel")
def test_client_generate_api_failure(mock_model_class, mock_configure):
    """Verify that standard SDK exceptions are wrapped in GeminiClientError."""
    mock_model_instance = MagicMock()
    mock_model_instance.generate_content.side_effect = Exception("API connection timed out")
    mock_model_class.return_value = mock_model_instance

    client = GeminiClient(api_key="mock-api-key")
    with pytest.raises(GeminiClientError) as exc_info:
        client.generate("Explain SQL Joins")
        
    assert "unexpected error" in str(exc_info.value)

@patch("google.generativeai.configure")
@patch("google.generativeai.GenerativeModel")
def test_client_generate_model_not_found(mock_model_class, mock_configure):
    """Verify that a retired/unknown model ID surfaces an actionable message."""
    mock_model_instance = MagicMock()
    mock_model_instance.generate_content.side_effect = exceptions.NotFound(
        "models/gemini-1.5-flash is not found for API version v1beta"
    )
    mock_model_class.return_value = mock_model_instance

    client = GeminiClient(api_key="mock-api-key")
    with pytest.raises(GeminiClientError) as exc_info:
        client.generate("Explain SQL Joins")

    assert "retired" in str(exc_info.value)
    assert "GEMINI_MODEL" in str(exc_info.value)
