from fastapi import APIRouter, UploadFile, Form
from app.schemas.grant_opportunity import GrantOpportunityInput, GrantOpportunityAnalysis
from app.services.grant_opportunity_service import analyze_grant_opportunity


router = APIRouter(prefix="/grant", tags=["Grant Opportunity"])

@router.post("/analyze", response_model=GrantOpportunityAnalysis)
async def analyze_grant_opportunity_endpoint(
    rfp_file: UploadFile = None,
    opportunity_url: str = Form(None),
    opportunity_text: str = Form(None)
):
    input_data = GrantOpportunityInput(
        rfp_file=await rfp_file.read() if rfp_file else None,
        opportunity_url=opportunity_url,
        opportunity_text=opportunity_text
    )
    return analyze_grant_opportunity(input_data)
