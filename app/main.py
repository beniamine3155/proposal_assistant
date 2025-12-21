# main.py
from fastapi import FastAPI
from app.api.v1.endpoints.onboarding import router as analyze_router
from app.api.v1.endpoints.grant_opportunity import router as opportunity_router
from app.api.v1.endpoints.loi import router as loi_router
from app.api.v1.endpoints.proposal import router as proposal_router
from app.api.v1.endpoints.grant_generator import router as grant_router

app = FastAPI(title="TGCI Proposal Assistant")

# Root endpoint for health check or welcome
@app.get("/")
def root():
    return {"message": "Welcome to the TGCI Proposal Assistant API"}

app.include_router(analyze_router)
app.include_router(opportunity_router)
app.include_router(grant_router)  
app.include_router(loi_router)
app.include_router(proposal_router)
       