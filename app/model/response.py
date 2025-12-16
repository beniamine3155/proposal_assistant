from pydantic import BaseModel
from typing import Optional

class AnalyzeResponse(BaseModel):
    mission_statement: Optional[str] = None
    programs: Optional[str] = None
    achievements: Optional[str] = None
    budget_statement: Optional[str] = None
    evaluation: Optional[str] = None
