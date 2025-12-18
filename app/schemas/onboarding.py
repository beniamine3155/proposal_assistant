from pydantic import BaseModel, Field
from typing import Optional, List, Literal

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

from typing import Union

class AnalyzeResponse(BaseModel):
    mission_statement: Optional[str] = Field(None)
    programs: Optional[Union[str, List[dict]]] = Field(None)
    achievements: Optional[Union[str, List[str]]] = Field(None)
    budget_statement: Optional[str] = Field(None)
    evaluation: Optional[str] = Field(None)


class GrantAnalysisResult(BaseModel):
    status: Literal[
        "GRANT_READY",
        "NEEDS_MINOR_IMPROVEMENTS",
        "NOT_READY"
    ] = Field(...)
    score: int = Field(...)
    gaps: List[str] = Field(...)
    recommendations: List[str] = Field(...)
    generated_output: Optional[AnalyzeResponse] = Field(None)
