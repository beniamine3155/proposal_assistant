from pydantic import BaseModel, Field
from typing import Optional, List, Literal, Union
from uuid import UUID

# -------- INPUT SCHEMAS --------

class AnalyzeRequestWithWebsite(BaseModel):
    website_name: str = Field(...)
    url: str = Field(...)
    mission: str = Field(...)

class AnalyzeRequestWithoutWebsite(BaseModel):
    mission: str = Field(...)
    core_purpose: str = Field(...)
    type_of_work: str = Field(...)
    goals_aspirations: str = Field(...)

# -------- OUTPUT SCHEMAS --------

class AnalyzeResponse(BaseModel):
    mission_statement: Optional[str] = None
    programs: Optional[Union[str, List[dict]]] = None
    achievements: Optional[Union[str, List[str]]] = None
    budget_statement: Optional[str] = None
    evaluation: Optional[str] = None


class GrantAnalysisResult(BaseModel):
    session_id: UUID = Field(...)   # ✅ ADD THIS LINE

    status: Literal[
        "GRANT_READY",
        "NEEDS_MINOR_IMPROVEMENTS",
        "NOT_READY"
    ] = Field(...)

    score: int = Field(...)
    gaps: List[str] = Field(...)
    recommendations: List[str] = Field(...)
    generated_output: Optional[AnalyzeResponse] = None
