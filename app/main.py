from fastapi import FastAPI
from app.api.v1.endpoints.onboarding import router as analyze_router
from app.api.v1.endpoints.grant_opportunity import router as opportunity_router

app = FastAPI()

# Include the analyze endpoint
app.include_router(analyze_router)
app.include_router(opportunity_router)
