from pydantic import BaseModel
from typing import List
from uuid import UUID

class GrantOpportunity(BaseModel):
    session_id: UUID
    title: str
    focus_area: str
    eligibility: str
    funding_amount: str
    duration: str
    rationale: str

class GrantResponse(BaseModel):
    grants: List[GrantOpportunity]
