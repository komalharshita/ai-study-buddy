import pytest
from unittest.mock import MagicMock, patch
from src.core.gemini_client import GeminiClient, GeminiClientError

def test_client_init_without_key_raises_error():
    """Verify that calling generate without an API key raises GeminiClientError."""
    client = GeminiClient(api_key="")
    with pytest.raises(GeminiClientError) as exc_info:
        client.generate("hello")
    assert "key is not configured" in str(exc_info.value)

@patch("google.generativeai.configure")
@patch("google.generativeai.GenerativeModel")
def test_client_generate_empty_prompt_raises(mock_model_class, mock_configure):
    """Verify that an empty or whitespace-only prompt is rejected before hitting the API."""
    client = GeminiClient(api_key="mock-api-key")
    with pytest.raises(GeminiClientError) as exc_info:
        client.generate("   ")
    assert "cannot be empty" in str(exc_info.value)
    mock_model_class.assert_not_called()

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
def test_client_api_key_override_is_temporary(mock_model_class, mock_configure):
    """Verify that a per-call API key override does not permanently replace the instance key."""
    mock_model_instance = MagicMock()
    mock_response = MagicMock()
    mock_response.text = "This is a mock explanation."
    mock_model_instance.generate_content.return_value = mock_response
    mock_model_class.return_value = mock_model_instance

    client = GeminiClient(api_key="mock-api-key")

    # First call with a temporary override key
    client.generate("Explain SQL Joins", api_key_override="override-key")

    # A subsequent call without the override must revert to the original key
    mock_configure.reset_mock()
    client.generate("Explain SQL Joins")
    mock_configure.assert_called_with(api_key="mock-api-key")
