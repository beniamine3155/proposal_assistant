import json
import re
import uuid
from openai import AsyncOpenAI
from app.config import OPENAI_API_KEY
from app.data.org_store import get_organization_analysis, save_organization_analysis
from app.services.grant_api_service import fetch_sample_grants

client = AsyncOpenAI(api_key=OPENAI_API_KEY)

PROMPT = """
You are a professional grant strategist.

INPUT:
1. Organization profile (mission, programs, achievements)
2. Sample grant opportunities

TASK:
- Analyze how well the organization aligns with potential funders
- Analyze strengths, gaps, and mission alignment
- CREATE 3 new grant opportunities based on organization profile if sample grants are missing
- Do NOT copy sample grants
- Each grant must look realistic and funder-driven

OUTPUT ONLY VALID JSON:

{
  "grants": [
    {
      "title": "",
      "funder": "",
      "focus": "",
      "deadline": "",
      "award": "",
      "alignment": ""
    }
  ]
}
"""


def normalize_grant_output(raw_output: dict, org_session_id: str) -> list:
    """
    Convert AI-generated grant fields into your GrantResponse schema
    and assign a unique grant_id to each grant. 
    Use the **organization session id** for all grants.
    """
    normalized_grants = []
    for g in raw_output.get("grants", []):
        normalized_grants.append({
            "grant_id": str(uuid.uuid4()),  # unique for each grant
            "session_id": org_session_id,   # same for all 3 grants
            "title": g.get("title", ""),
            "focus_area": g.get("focus", ""),
            "eligibility": g.get("funder", ""),
            "funding_amount": g.get("award", ""),
            "duration": g.get("deadline", ""),
            "rationale": g.get("alignment", "")
        })
    return normalized_grants



async def generate_top_grants(session_id: str, sample_grants: list = None, top_n: int = 3) -> list:
    """
    Generate top N grant opportunities with their own session IDs
    using the organization info from the provided session_id.
    """
    # Load organization profile
    org_data = get_organization_analysis(session_id)
    if not org_data:
        raise ValueError("Invalid session_id")

    org_profile = org_data["analysis"].get("generated_output", {})

    # Fetch sample grants if none provided
    if sample_grants is None:
        sample_grants = await fetch_sample_grants()

    # Only take top_n sample grants for AI context
    payload = f"""
ORGANIZATION PROFILE:
{json.dumps(org_profile, indent=2)}

SAMPLE GRANTS:
{json.dumps(sample_grants[:top_n], indent=2)}
"""

    # Call AI
    response = await client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "Return JSON only, no explanations."},
            {"role": "user", "content": PROMPT + payload}
        ],
        temperature=0.3
    )

    raw = response.choices[0].message.content.strip()
    cleaned = re.sub(r"```json|```", "", raw).strip()
    raw_output = json.loads(cleaned)

    # Normalize output and assign session_id
    normalized_grants = normalize_grant_output(raw_output, org_session_id=session_id)

    # Return only top N grants
    return normalized_grants[:top_n]
