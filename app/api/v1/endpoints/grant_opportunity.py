from fastapi import APIRouter, UploadFile, Form, File
from app.schemas.grant_opportunity import GrantOpportunityInput,  GrantOpportunityAnalyzeResponse
from app.services.grant_opportunity_service import analyze_grant_opportunity

router = APIRouter(prefix="/grant", tags=["Grant Opportunity"])

@router.post("/analyze", response_model=GrantOpportunityAnalyzeResponse)
async def analyze_grant_opportunity_endpoint(
    session_id: str = Form(...),
    rfp_file: UploadFile | None = File(None),
    opportunity_url: str | None = Form(None),
    opportunity_text: str | None = Form(None)
):
    input_data = GrantOpportunityInput(
        rfp_file=await rfp_file.read() if rfp_file else None,
        opportunity_url=opportunity_url,
        opportunity_text=opportunity_text
    )

    return analyze_grant_opportunity(
        input_data=input_data,
        session_id=session_id
    )
