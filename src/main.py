import logging
import json
from pathlib import Path
from datetime import datetime

from file_utils import get_image_files
from transcription import transcribe_raw_pages, categorize_topics, transcribe_topics
from config import BASE_FOLDER, OUTPUT_FOLDER

def save_topic_transcription(topic, transcription, folder: Path, dest_folder: Path):
    """
    Saves the transcription for a topic to a JSON file in dest_folder.
    """
    safe_name = "".join(c for c in topic.name if c.isalnum() or c in (' ', '-', '_')).strip()
    safe_name = safe_name.replace(' ', '_').lower()
    output_path = dest_folder / f"{safe_name}.json"
    output_data = {
        "topic_transcription": transcription.model_dump() if hasattr(transcription, "model_dump") else transcription,
        "metadata": {
            "source_pages": topic.pages,
            "created_at": datetime.now().isoformat(),
            "class": folder.name
        }
    }
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(output_data, f, indent=2, ensure_ascii=False)

def process_folder(folder: Path):
    """
    Process a folder of images by transcribing and categorizing its contents.
    Skips if folder (:= class) already exists in destination

    1. Gets image files from folder
    2. Transcribes them one by one to text
    3. Classifies them into topics from raw text for better transcription
    4. Transcribes topics and writes them to output folder
    5. Writes them to output folder
    
    Args:
        folder (Path): Path to the folder containing images to process.
    """
    logger = logging.getLogger(__name__)
    folder = folder.resolve()
    dest_folder = (OUTPUT_FOLDER / folder.name).resolve()

    # Skip if output already exists.
    if dest_folder.exists() and any(dest_folder.iterdir()):
        logger.info("Folder %s already processed. Skipping.", folder)
        return

    dest_folder.mkdir(parents=True, exist_ok=True)
    logger.info("Processing folder: %s, saving outputs to: %s", folder, dest_folder)
    
    # 1. Get image files in the current folder.
    image_files = get_image_files(folder)

    # 2. Transcribe all pages in this folder.
    pages_transcribed = transcribe_raw_pages(image_files, folder)
    
    # 3. Categorize the transcriptions into topics.
    topics = categorize_topics(pages_transcribed)

    # 4. Transcribe each topic.
    topic_transcriptions = transcribe_topics(topics, folder)

    # 5. Save the transcriptions to the output folder.
    for topic, transcription in topic_transcriptions:
        try:
            logger.info("Saving transcription for topic: %s", topic.name)
            save_topic_transcription(topic, transcription, folder, dest_folder)
        except Exception as e:
            logger.error("Failed to save transcription for topic %s: %s", topic.name, e)

def main():
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)

    # Process each subfolder in the base folder
    base_folder = BASE_FOLDER.resolve()
    for subfolder in base_folder.iterdir():
        if subfolder.is_dir():
            try:
                process_folder(subfolder)
            except Exception as e:
                logger.error("Error processing folder %s: %s", subfolder, e)

if __name__ == "__main__":
    main()

