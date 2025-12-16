from pydantic import BaseModel
from typing import Optional

class AnalyzeRequestWithWebsite(BaseModel):
    website_name: str
    url: str
    mission: str

class AnalyzeRequestWithoutWebsite(BaseModel):
    mission: str
    core_purpose: str
    type_of_work: str
    goals_aspirations: str
