# app/data/org_store.py
from typing import Dict
from datetime import datetime

# key can be org URL or org_id
ORG_ANALYSIS_STORE: Dict[str, dict] = {}

def save_organization_analysis(key: str, payload: dict, analysis: dict):
    """
    Save the analyzed organization data.
    """
    ORG_ANALYSIS_STORE[key] = {
        "payload": payload,         # input data (mission, website_name, etc.)
        "analysis": analysis,       # AI analysis result
        "created_at": datetime.utcnow()
    }

def get_organization_analysis(key: str):
    """
    Retrieve saved organization analysis.
    """
    return ORG_ANALYSIS_STORE.get(key)
