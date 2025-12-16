from fastapi import APIRouter
from app.schemas.request import AnalyzeRequestWithWebsite, AnalyzeRequestWithoutWebsite
from app.model.response import AnalyzeResponse
from app.services.analyze_service import analyze_with_website, analyze_without_website

router = APIRouter()

@router.post("/analyze-with-website", response_model=AnalyzeResponse)
async def analyze_with_website_endpoint(data: AnalyzeRequestWithWebsite):
    analysis = analyze_with_website(data.website_name, data.url, data.mission)
    return AnalyzeResponse(**analysis)

@router.post("/analyze-without-website", response_model=AnalyzeResponse)
async def analyze_without_website_endpoint(data: AnalyzeRequestWithoutWebsite):
    analysis = analyze_without_website(data.mission, data.core_purpose, data.type_of_work, data.goals_aspirations)
    return AnalyzeResponse(**analysis)
