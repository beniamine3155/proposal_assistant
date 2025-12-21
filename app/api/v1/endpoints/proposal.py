from fastapi import APIRouter, Form
from app.schemas.proposal import ProposalResponse
from app.services.proposal_service import generate_proposal

router = APIRouter(prefix="/proposal", tags=["Proposal"])

@router.post("/generate", response_model=ProposalResponse)
def generate_proposal_endpoint(session_id: str = Form(...)):
    return generate_proposal(session_id)
