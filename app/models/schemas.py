from pydantic import BaseModel
from typing import List, Optional

class UploadResponse(BaseModel):
    message: str

class Source(BaseModel):
    source: str
    text: str

class ChatResponse(BaseModel):
    answer: str
    sources: List[Source]