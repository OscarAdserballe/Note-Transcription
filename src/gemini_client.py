import os
import time
import logging
from pathlib import Path
from typing import Any, List, Union
import PIL.Image

from google import genai

from config import BASE_LLM_MODEL

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

class GeminiFiles:
    """
    A client for interacting with the Gemini API with automatic retry on timeouts.
    """
    def __init__(self, response_schema: Any, model_name: str = BASE_LLM_MODEL):
        self.api_key = os.getenv("GEMINI_API_KEY")
        if not self.api_key:
            raise ValueError("GEMINI_API_KEY environment variable is not set.")
        self.client = genai.Client(api_key=self.api_key)
        self.model_name = model_name
        self.response_schema = response_schema

    def _call_api_with_retry(self, contents: List[Any], config: dict, retries: int = 3, delay: int = 5):
        for attempt in range(retries):
            try:
                response = self.client.models.generate_content(
                    model=self.model_name,
                    contents=contents,
                    config=config
                )
                return response
            except Exception as e:
                # If a timeout error is detected in the exception message, retry.
                if attempt < retries - 1:
                    logger.warning("API timeout detected (attempt %d/%d). Retrying in %d seconds...", attempt+1, retries, delay)
                    time.sleep(delay)
                    continue
                logger.exception("API call failed: %s", e)
                raise

    def prompt_with_image(self, prompt: str, image_paths: Union[Path, List[Path]]) -> Any:
        """
        Sends a prompt along with one or more images to the Gemini API and returns the parsed response.
        """
        try:
            if isinstance(image_paths, Path):
                image_paths = [image_paths]

            images = []
            for path in image_paths:
                try:
                    image = PIL.Image.open(path)
                    images.append(image)
                except Exception as e:
                    logger.error("Failed to open image %s: %s", path, e)
                    continue

            contents = [prompt] + images
            config = {
                "response_mime_type": "application/json",
                "response_schema": self.response_schema
            }
            response = self._call_api_with_retry(contents, config)
            return response.parsed
        except Exception as e:
            logger.exception("Error in prompt_with_image: %s", e)
            raise

    def query(self, prompt: str) -> Any:
        """
        Sends a text prompt to the Gemini API and returns the parsed response.
        """
        try:
            config = {
                "response_mime_type": "application/json",
                "response_schema": self.response_schema
            }
            response = self._call_api_with_retry([prompt], config)
            return response.parsed
        except Exception as e:
            logger.exception("Error in query: %s", e)
            raise
