from fastapi import APIRouter
from app.schemas.onboarding import (
    AnalyzeRequestWithWebsite,
    AnalyzeRequestWithoutWebsite,
    GrantAnalysisResult
)
from app.services.grant_readiness_service import (
    analyze_with_website,
    analyze_without_website
)

router = APIRouter(prefix="/onboarding", tags=["Onboarding"])


@router.post("/analyze/with-website", response_model=GrantAnalysisResult)
def analyze_with_website_endpoint(payload: AnalyzeRequestWithWebsite):
    return analyze_with_website(payload)


@router.post("/analyze/without-website", response_model=GrantAnalysisResult)
def analyze_without_website_endpoint(payload: AnalyzeRequestWithoutWebsite):
    return analyze_without_website(payload)
