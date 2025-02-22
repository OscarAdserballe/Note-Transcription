import os
from pathlib import Path

# Environment variable: ensure your GEMINI_API_KEY is set.
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if GEMINI_API_KEY is None:
    raise ValueError("GEMINI_API_KEY environment variable is not set.")

# Base folder containing all handwritten note images.
BASE_FOLDER = Path("~/Google Drive/My Drive/Handwritten Notes").expanduser().resolve()

# Output folder to save transcriptions.
OUTPUT_FOLDER = Path("~/Google Drive/My Drive/Transcriptions").expanduser().resolve()

BASE_LLM_MODEL = "gemini-2.0-flash"
ADVANCED_LLM_MODEL = "gemini-exp-1206"

