from fastapi import APIRouter, Form
from app.schemas.loi import LOIResponse
from app.services.loi_service import generate_loi

router = APIRouter(prefix="/loi", tags=["LOI"])

@router.post("/generate", response_model=LOIResponse)
def generate_loi_endpoint(session_id: str = Form(...)):
    return generate_loi(session_id)
