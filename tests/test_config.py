import os
from src.config import Config

def test_config_initialization_with_defaults(monkeypatch):
    """Test that default values are set when environment variables are missing."""
    monkeypatch.delenv("GEMINI_API_KEY", raising=False)
    monkeypatch.delenv("NGROK_AUTH_TOKEN", raising=False)
    monkeypatch.delenv("GEMINI_MODEL", raising=False)
    monkeypatch.delenv("LOG_LEVEL", raising=False)
    monkeypatch.delenv("PORT", raising=False)

    test_config = Config()
    assert test_config.gemini_api_key == ""
    assert test_config.ngrok_auth_token == ""
    assert test_config.gemini_model == "gemini-3.5-flash"
    assert test_config.log_level == "INFO"
    assert test_config.port == 8501
    assert not test_config.is_api_configured

def test_config_initialization_with_env_vars(monkeypatch):
    """Test that custom environment variables are correctly parsed."""
    monkeypatch.setenv("GEMINI_API_KEY", "test-api-key")
    monkeypatch.setenv("NGROK_AUTH_TOKEN", "test-ngrok-token")
    monkeypatch.setenv("GEMINI_MODEL", "gemini-3.5-flash-lite")
    monkeypatch.setenv("LOG_LEVEL", "DEBUG")
    monkeypatch.setenv("PORT", "9000")

    test_config = Config()
    assert test_config.gemini_api_key == "test-api-key"
    assert test_config.ngrok_auth_token == "test-ngrok-token"
    assert test_config.gemini_model == "gemini-3.5-flash-lite"
    assert test_config.log_level == "DEBUG"
    assert test_config.port == 9000
    assert test_config.is_api_configured
