from pydantic import BaseModel
from typing import List, Optional
from uuid import UUID

class BudgetLineItem(BaseModel):
    category: Optional[str] = ""
    description: Optional[str] = ""
    estimated_cost: Optional[str] = ""

class BudgetSummary(BaseModel):
    line_items: List[BudgetLineItem] = []
    total_estimated_budget: Optional[str] = ""

class ProposalResponse(BaseModel):
    session_id: UUID
    executive_summary: str
    introduction_to_organization: str
    problem_statement: str
    goals_and_objectives: str
    methods_and_activities: str
    evaluation_plan: str
    sustainability_plan: str
    budget_summary: BudgetSummary
    conclusion: str
