import os
from dotenv import load_dotenv
from src.logger import logger

# Load environment variables from .env file if it exists
load_dotenv()

# Current stable Gemini model. Older IDs (gemini-1.5-flash, gemini-2.0-flash)
# have been retired by Google and now fail with HTTP 404.
DEFAULT_GEMINI_MODEL = "gemini-3.5-flash"

class Config:
    """Configuration loader and validator for the AI Learning Buddy application."""
    
    def __init__(self):
        # 1. API Keys and Credentials
        self.gemini_api_key = os.getenv("GEMINI_API_KEY", "").strip()
        self.ngrok_auth_token = os.getenv("NGROK_AUTH_TOKEN", "").strip()
        
        # 2. Model Settings
        self.gemini_model = os.getenv("GEMINI_MODEL", DEFAULT_GEMINI_MODEL).strip()
        
        # 3. Server Settings
        self.log_level = os.getenv("LOG_LEVEL", "INFO").strip()
        try:
            self.port = int(os.getenv("PORT", "8501"))
        except ValueError:
            self.port = 8501

        logger.debug("Configuration initialized.")
        if not self.gemini_api_key:
            logger.warning("GEMINI_API_KEY is not defined in the environment. User must provide it via UI.")

    @property
    def is_api_configured(self) -> bool:
        """Returns True if the Google Gemini API key is configured."""
        return len(self.gemini_api_key) > 0

# Global configuration instance
config = Config()
