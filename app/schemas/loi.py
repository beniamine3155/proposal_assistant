from pydantic import BaseModel
from uuid import UUID
from typing import Optional

class LOIResponse(BaseModel):
    session_id: UUID
    introduction: str
    organizational_summary: str
    project_overview: str
    funding_request: Optional[str]
    closing_statement: str
