from fastapi import APIRouter, Form
from typing import List
from app.services.grant_generator_service import generate_top_grants
from app.schemas.grant_fetch import GrantOpportunity, GrantResponse

router = APIRouter(prefix="/grant", tags=["Grant Generator"])

@router.post("/generate", response_model=GrantResponse)
async def generate_grants_endpoint(session_id: str = Form(...)):
    grants = await generate_top_grants(session_id=session_id, top_n=3)
    grants_schema = [
        GrantOpportunity(
            session_id= g["session_id"],
            title=g["title"],
            focus_area=g["focus_area"],
            eligibility=g["eligibility"],
            funding_amount=g["funding_amount"],
            duration=g["duration"],
            rationale=g["rationale"]
        )
        for g in grants
    ]
    return GrantResponse(grants=grants_schema)

