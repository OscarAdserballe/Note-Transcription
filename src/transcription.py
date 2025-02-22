import logging
from pathlib import Path
from tqdm import tqdm

from gemini_client import GeminiFiles
from transcription_prompts import FIRST_TRANSCRIPTION_PROMPT, SECOND_TRANSCRIPTION_PROMPT, CATEGORIZE_PROMPT
from objects import Page, Topic, TopicTranscription

from config import BASE_LLM_MODEL, ADVANCED_LLM_MODEL

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

def transcribe_raw_pages(image_files: list, folder: Path) -> dict:
    """
    Transcribes all image files in the given folder.
    Returns a dict mapping the relative file path (as string) to its transcription.
    """
    gemini_pages = GeminiFiles(response_schema=Page)
    pages_transcribed = {}

    for relative_path in tqdm(image_files, desc="Transcribing pages"):
        try:
            file_path = (folder / relative_path).resolve()
            result = gemini_pages.prompt_with_image(FIRST_TRANSCRIPTION_PROMPT, file_path)
            pages_transcribed[str(relative_path)] = result.content
        except Exception as e:
            logger.error("Error transcribing page %s: %s", relative_path, e)
            continue
    return pages_transcribed

def categorize_topics(pages_transcribed: dict) -> list:
    """
    Categorizes transcribed pages into topics using the Gemini API.
    Returns a list of Topic objects.
    """
    # Initialize the Gemini client for topic categorization.
    gemini_topics = GeminiFiles(model_name=ADVANCED_LLM_MODEL, response_schema=list[Topic])
    
    # Build the prompt for categorization.
    content_to_categorize = ""
    for page_name, page_content in pages_transcribed.items():
        content_to_categorize += f"Page: {page_name}\n\n{page_content}\n\n"
    prompt = CATEGORIZE_PROMPT + "\n\nHere are the notes you need to categorize:\n\n" + content_to_categorize

    try:
        topics = gemini_topics.query(prompt)
        return topics
    except Exception as e:
        logger.exception("Error categorizing topics: %s", e)
        raise

def _transcribe_topic(topic: Topic, folder: Path) -> any:
    """
    Internal helper: processes all pages for a given topic from the provided folder,
    using the Gemini API to transcribe them. Returns the transcription output.
    """
    gemini = GeminiFiles(response_schema=TopicTranscription, model_name=ADVANCED_LLM_MODEL)
    try:
        # Build absolute paths for all pages in the topic.
        page_paths = [(folder / Path(page)).resolve() for page in topic.pages]
    except Exception as e:
        logger.error("Error constructing file paths for topic %s: %s", topic.name, e)
        raise

    try:
        output = gemini.prompt_with_image(
            prompt=SECOND_TRANSCRIPTION_PROMPT,
            image_paths=page_paths
        )
        return output
    except Exception as e:
        logger.exception("Error transcribing topic %s: %s", topic.name, e)
        raise

def transcribe_topics(topics: list, folder: Path) -> list:
    """
    Transcribes all topics in the provided list.
    Returns a list of tuples (topic, transcription_output).
    """
    results = []
    for topic in topics:
        try:
            output = _transcribe_topic(topic, folder)
            results.append((topic, output))
        except Exception as e:
            logger.error("Error transcribing topic %s: %s", topic.name, e)
    return results

