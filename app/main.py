from fastapi import FastAPI
from app.api.v1.endpoints.analyze import router as analyze_router

app = FastAPI()

# Include the analyze endpoint
app.include_router(analyze_router)
