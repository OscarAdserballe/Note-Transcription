from pydantic import BaseModel, Field
from typing import List

class Page(BaseModel):
    content: str

class Topic(BaseModel):
    name: str
    description: str
    pages: List[str]

class TopicTranscription(BaseModel):
    title: str
    keywords: List[str]
    summary: str
    content: str
    problem_space: str
    examples: List[str]
    reflection: str
    questions: List[str]

class Metadata(BaseModel):
    source_pages: list[str]
    created_at: str
    class_name: str = Field(alias="class")
