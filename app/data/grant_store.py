# app/data/grant_store.py
from typing import Dict
from datetime import datetime

GRANT_ANALYSIS_STORE: Dict[str, dict] = {}

def save_grant_analysis(session_id: str, analysis: dict):
    GRANT_ANALYSIS_STORE[session_id] = {
        "analysis": analysis,
        "created_at": datetime.utcnow()
    }

def get_grant_analysis(session_id: str):
    return GRANT_ANALYSIS_STORE.get(session_id)
