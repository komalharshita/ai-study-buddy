import os
import google.generativeai as genai
from google.api_core import exceptions
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
        self._configured = False
        
        if self._api_key:
            self._configure_api(self._api_key)

    def _configure_api(self, api_key: str):
        """Configures the google-generativeai package with the API key."""
        try:
            genai.configure(api_key=api_key)
            self._configured = True
            logger.info("Gemini API successfully configured.")
        except Exception as e:
            self._configured = False
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
        
        # If API key changed or not yet configured, configure it now
        if api_key_override or not self._configured:
            self._configure_api(active_key)
            if api_key_override:
                self._api_key = active_key

        model_name = config.gemini_model
        logger.debug(f"Calling Gemini model '{model_name}' with prompt length {len(prompt)}")
        
        # Set up generation config
        # NOTE: temperature/top_p are intentionally not sent. Recent Gemini
        # models no longer accept sampling parameters and reject requests that
        # include them (HTTP 400), so the model defaults are used instead.
        generation_config = {
            "max_output_tokens": 2048,
        }

        # Build model arguments
        model_kwargs = {
            "model_name": model_name,
            "generation_config": generation_config,
        }
        
        # Inject system instructions if provided, otherwise default to persona guidelines
        sys_instruction = system_instruction or AIPersona.SYSTEM_INSTRUCTION
        model_kwargs["system_instruction"] = sys_instruction

        try:
            model = genai.GenerativeModel(**model_kwargs)
            response = model.generate_content(prompt)
            
            if not response.text:
                logger.warning("Empty response received from Gemini API.")
                raise GeminiClientError("The AI generated an empty response. Please try modifying your query.")
                
            logger.debug("Successfully received response from Gemini API.")
            return response.text.strip()
            
        except exceptions.InvalidArgument as e:
            logger.error(f"Invalid argument to Gemini API: {str(e)}")
            raise GeminiClientError(f"Invalid API request: {str(e)}")
        except exceptions.ResourceExhausted as e:
            logger.error(f"Gemini API rate limit exceeded: {str(e)}")
            raise GeminiClientError("Rate limit exceeded. Please wait a few moments before trying again.")
        except exceptions.PermissionDenied as e:
            logger.error(f"Gemini API permission denied: {str(e)}")
            raise GeminiClientError("Authentication failed. Please verify your Gemini API key is correct.")
        except exceptions.NotFound as e:
            logger.error(f"Gemini API model not found: {str(e)}")
            raise GeminiClientError(
                f"The configured model '{model_name}' was not found or has been retired. "
                "Update GEMINI_MODEL in your .env file to a currently supported model."
            )
        except exceptions.GoogleAPICallError as e:
            logger.error(f"General Gemini API call error: {str(e)}")
            raise GeminiClientError(f"Gemini API Error: {str(e)}")
        except Exception as e:
            logger.error(f"Unexpected error in Gemini client: {str(e)}")
            raise GeminiClientError(f"An unexpected error occurred: {str(e)}")
