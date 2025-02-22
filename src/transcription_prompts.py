FIRST_TRANSCRIPTION_PROMPT = """
Task:
Transcribe the following handwritten notes as clearly as possible.

First, go thorugh the content and make sure you understand the content.
Sometimes it's only fragments of texts, but try to make sense of it as a whole.
Then, transcribe the content into its entirety. 
With equations and the sort, please write them out in full and in Latex.

You should return a JSON object with the following structure:

Page = {
    'content' : str
}

Return: Page
"""

SECOND_TRANSCRIPTION_PROMPT = """
Task:
Transcribe the following handwritten notes with the dual purpose of capturing their original content and enhancing understanding for deeper learning and recollection. Your transcription should maintain the notes’ original ideas and structure while enriching them with reflective insights and probing questions.

Instructions:

1. Overview and Initial Processing:
   - Write a concise 1-2 sentence summary capturing the main ideas of the notes.
   - Provide a list of keywords that best encapsulate the core topics.
   - Identify the problem space and context, relating the material to broader academic themes.

2. Detailed Content Transcription:
   - Transcribe all text, mathematical equations, and diagrams accurately.
   - Use Markdown for text formatting and KaTeX for all equations and symbols.
   - For diagrams or illustrations, include a detailed textual description of each element, explaining their relationships and significance.

3. Enhancing Understanding and Reflection:
   - Add a 'reflection' section where you note personal insights, connections to prior knowledge, or observations about the material.
   - Incorporate a 'questions' section with 2-3 thought-provoking questions that encourage further exploration or critical thinking about the content.
   - Provide 2-3 detailed examples that illustrate or extend key ideas from the notes, even if these examples are not originally present.

4. Structure, Coherence, and Self-Explanation:
   - Preserve the original structure by maintaining sections, headings, and subheadings.
   - Keep it at the level of the notes, and no lower in terms of difficulty. It's always with the aim of enhancing understanding for deeper learning and recollection.
   - Ensure the transcription is coherent; use context clues to fill in any gaps without compromising accuracy.
   - Where appropriate, include brief self-explanations that clarify the rationale or underlying concepts behind major points.

5. Output Format:
   - Produce the final transcription as a JSON object using single quotes for string values.
   - Follow this structure exactly:

TopicTranscription = {
    'title' : str,
    'keywords' : List[str],
    'summary' : str,
    'content' : str,
    'problem_space' : str,
    'examples' : List[str],
    'reflection' : str,
    'questions' : List[str]
}

Return: Note

Remember:
The goal is not to reproduce every word verbatim, but to capture the essential meaning, context, and significance of the notes while providing added value through reflection and inquiry to enhance long-term learning and recollection.
"""

CATEGORIZE_PROMPT = """
You will be categorizing a number of notes into appropriate content.
Currently, the problem is that the notes are scattered after an upload process, and you need to identify the pages that belong together based on the topics they revolve around.

The order in which you receive the notes can sometimes be informative, but it should not be taken as a given.
The minimum unit we're working with is a single page per topic, but a topic can span multiple pages. Aim for around 1-3 pages per topic.

You will be provided with a set of notes in the form of images, one per page, along with some metadata.
When citing the pages, it should always be in terms of their filenames provided before each page.


For each topic just provide
1) the name of the topic,
2) a brief description, and
3) a list of pages that belong to that topic based on what they're prefaced with after "Page: "

Topic = {
    'name' : str,
    'description' : str,
    'pages' : List[str]
}

Return: List[Topic]
"""

