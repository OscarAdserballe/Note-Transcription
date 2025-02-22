import os
from pathlib import Path
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

def get_image_files(folder: Path) -> list:
    """
    Recursively finds all image files under the given folder.
    Returns a list of paths relative to the folder.
    """
    image_files = []
    try:
        for root, _, files in os.walk(folder):
            root_path = Path(root)
            for file in files:
                if file.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp')):
                    # Store the relative path to the base folder.
                    relative_path = root_path.relative_to(folder) / file
                    image_files.append(relative_path)
        return image_files
    except Exception as e:
        logger.exception("Error scanning folder %s: %s", folder, e)
        raise
