from pydantic import BaseModel, HttpUrl, Field
from typing import List, Optional


class AnalyzeRequest(BaseModel):
    url: Optional[HttpUrl] = None
    raw_text: Optional[str] = None
    keywords: Optional[List[str]] = None
    analyst_questions: Optional[List[str]] = None
