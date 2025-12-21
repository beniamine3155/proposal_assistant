from pydantic import BaseModel
from uuid import UUID

from pydantic import BaseModel
from typing import Optional

class BudgetSummary(BaseModel):
    category: Optional[str] = ""
    details: Optional[str] = ""
    estimated_cost: Optional[str] = ""


class ProposalResponse(BaseModel):
    session_id: UUID
    executive_summary: str
    introduction_to_organization: str
    problem_statement: str
    goals_and_objectives: str
    methods_and_activities: str
    evaluation_plan: str
    sustainability_plan: str
    budget_summary:  BudgetSummary
    conclusion: str
