from google import genai
from google.genai import types, errors
from src.config import config
from src.core.persona import AIPersona
from src.logger import logger

class GeminiClientError(Exception):
    """Custom exception class for Gemini API client errors."""
    pass

class GeminiClient:
    """Wrapper class for interacting with the Google Gemini Generative AI API."""
    
    def __init__(self, api_key: str = None):
        """
        Initializes the Gemini Client.
        
        Args:
            api_key: Optional API key. If not provided, falls back to config or environment.
        """
        self._api_key = api_key or config.gemini_api_key
        self._client = None
        
        if self._api_key:
            self._configure_client(self._api_key)

    def _configure_client(self, api_key: str):
        """Configures the google-genai client with the API key."""
        try:
            self._client = genai.Client(api_key=api_key)
            logger.info("Gemini API successfully configured.")
        except Exception as e:
            self._client = None
            logger.error(f"Failed to configure Gemini API: {str(e)}")
            raise GeminiClientError(f"Configuration failed: {str(e)}")

    def generate(self, prompt: str, system_instruction: str = None, api_key_override: str = None) -> str:
        """
        Generates content from the Gemini API.
        
        Args:
            prompt: The user-facing prompt or query.
            system_instruction: Guidelines directing the model's behavior/persona.
            api_key_override: A temporary API key to override the instance key (e.g. from UI input).
            
        Returns:
            The generated text string response.
            
        Raises:
            GeminiClientError: If generation fails due to network, auth, or rate limit issues.
        """
        # Determine which API key to use
        active_key = api_key_override or self._api_key
        if not active_key:
            logger.error("Attempted to generate content without an API key.")
            raise GeminiClientError("Gemini API key is not configured. Please add it in your .env file or input it in the sidebar.")
        
        # If API key changed or the client is not yet configured, configure it now
        if api_key_override or self._client is None:
            self._configure_client(active_key)
            if api_key_override:
                self._api_key = active_key

        model_name = config.gemini_model
        logger.debug(f"Calling Gemini model '{model_name}' with prompt length {len(prompt)}")
        
        # Set up generation config
        sys_instruction = system_instruction or AIPersona.SYSTEM_INSTRUCTION
        generation_config = types.GenerateContentConfig(
            temperature=0.7,
            top_p=0.95,
            max_output_tokens=2048,
            system_instruction=sys_instruction,
        )

        try:
            response = self._client.models.generate_content(
                model=model_name,
                contents=prompt,
                config=generation_config,
            )
            
            if not response.text:
                logger.warning("Empty response received from Gemini API.")
                raise GeminiClientError("The AI generated an empty response. Please try modifying your query.")
                
            logger.debug("Successfully received response from Gemini API.")
            return response.text.strip()
            
        except errors.ClientError as e:
            logger.error(f"Gemini API client error (code {e.code}): {str(e)}")
            if e.code == 400:
                raise GeminiClientError(f"Invalid API request: {str(e)}")
            if e.code == 429:
                raise GeminiClientError("Rate limit exceeded. Please wait a few moments before trying again.")
            if e.code in (401, 403):
                raise GeminiClientError("Authentication failed. Please verify your Gemini API key is correct.")
            raise GeminiClientError(f"Gemini API Error: {str(e)}")
        except errors.ServerError as e:
            logger.error(f"Gemini API server error: {str(e)}")
            raise GeminiClientError("The Gemini API is temporarily unavailable. Please try again shortly.")
        except Exception as e:
            logger.error(f"Unexpected error in Gemini client: {str(e)}")
            raise GeminiClientError(f"An unexpected error occurred: {str(e)}")