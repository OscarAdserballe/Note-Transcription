import re
import json
from config import OBSIDIAN_FOLDER, OUTPUT_FOLDER
from objects import TopicTranscription, Metadata

def clean_filename(s: str) -> str:
    """
    Clean the input string to make it safe for use as a filename.
    - Strips leading/trailing whitespace.
    - Replaces spaces with underscores.
    - Removes any characters that are not alphanumeric, underscores, or hyphens.
    """
    s = s.strip()
    s = re.sub(r'\s+', '_', s)
    return re.sub(r'[^\w\-]', '', s)

def create_obsidian_file(topic_transcription: TopicTranscription, metadata: Metadata):
    # Sanitize the title and class name for file and folder names.
    safe_title = clean_filename(topic_transcription.title)
    safe_class_name = clean_filename(metadata.class_name)

    yaml_front_matter = f"""---
title: "{topic_transcription.title}"
tags: {topic_transcription.keywords}
keywords: {topic_transcription.keywords}
created_at: "{metadata.created_at}"
source_pages: {metadata.source_pages}
class: "{metadata.class_name}"
---
"""

    body = f"""# Problem Space

{topic_transcription.problem_space}

# Summary

{topic_transcription.summary}

# Content

{topic_transcription.content}

# Examples
"""
    # Append each example
    for ex in topic_transcription.examples:
        body += f"\n- {ex}\n"

    body += f"""\n# Reflection

{topic_transcription.reflection}

# Questions
"""
    # Append each question
    for q in topic_transcription.questions:
        body += f"\n- {q}\n"

    obsidian_note = yaml_front_matter + body

    # Construct the target folder and file using sanitized names.
    new_folder = OBSIDIAN_FOLDER / "not_yet_classified" / safe_class_name
    new_folder.mkdir(parents=True, exist_ok=True)

    new_file = new_folder / f"{safe_title}_{safe_class_name}.md"

    # Only create a new file if it doesn't already exist.
    if new_file.exists():
        print(f"File {new_file} already exists. Skipping file creation.")
    else:
        with open(new_file, "w") as f:
            f.write(obsidian_note)

if __name__ == "__main__":
    for i in OUTPUT_FOLDER.iterdir():
        try:
            for j in i.iterdir():
                try:
                    with open(j, "r") as f:
                        data = json.load(f)
                        topic_transcription = TopicTranscription(**data["topic_transcription"])
                        metadata = Metadata(**data["metadata"])
                        create_obsidian_file(topic_transcription, metadata)
                except Exception as e:
                    print(f"Error loading {i}/{j}: {e}")
                    continue
        except Exception as e:
            print(f"Error loading {i}: {e}")
            continue

