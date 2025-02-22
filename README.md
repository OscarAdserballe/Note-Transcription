# Note Transcription: From Handwritten Pages to Digital Insights

## Overview
Note Transcription is a Python tool that converts your handwritten note images into structured digital transcriptions. It transcribes individual pages, groups them into topics, and outputs detailed JSON files for easy review.

## Features
- **Folder-Based Processing**: Organizes input images by subfolder (e.g. class, project) and mirrors the structure in the output
- **Page Transcription**: Converts handwritten pages into text
- **Topic Classification**: Groups transcribed pages into topics based on content
- **Detailed Topic Transcription**: Enhances topics with a secondary transcription for richer insights
- **Configurable Paths**: Set your base and output folders in `src/config.py`

## Process
1. Scan a folder for image files
2. Transcribe each image to text
3. Categorize transcriptions into topics
4. Transcribe each topic for enriched output
5. Save transcriptions as JSON files in the output folder

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/Note-Transcription.git
   cd Note-Transcription
   ```

2. Install Poetry (if not already installed):
   - Follow instructions at [Poetry Installation](https://python-poetry.org/docs/#installation)

3. Install dependencies:
   ```bash
   poetry install
   ```

4. Set your Gemini API key:
   ```bash
   export GEMINI_API_KEY="your_gemini_api_key_here"
   ```

## Usage
Simply run the main script to process your notes:
```bash
poetry run python src/main.py

**Note**: Make sure the `BASE_FOLDER` (input) and `OUTPUT_FOLDER` (output) are correctly defined in `src/config.py`.
