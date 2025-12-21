import json
from openai import OpenAI
from app.config import OPENAI_API_KEY
from app.data.org_store import get_organization_analysis
from app.data.grant_store import get_grant_analysis

client = OpenAI(api_key=OPENAI_API_KEY)


TGCI_LOI_PROMPT = """
You are a TGCI-trained grants professional.

TASK:
Generate a Letter of Intent (LOI) that follows
The Grantsmanship Center (TGCI) standards.

IMPORTANT RULES (STRICT):
- Use TGCI knowledge ONLY for structure, tone, and sequencing
- Do NOT invent programs, outcomes, budgets, or partnerships
- Use ONLY the organization profile and grant analysis provided
- If information is missing, write conservatively and factually
- Do NOT cite or reference TGCI explicitly

LOI STRUCTURE (TGCI STANDARD):
1. Introduction / Purpose
2. Organizational Overview
3. Statement of Need / Problem
4. Project Overview
5. Alignment with Funder Priorities
6. Funding Request (if available)
7. Closing Statement

INPUT CONTEXT:
- Organization analysis (session-based)
- Grant opportunity analysis

OUTPUT FORMAT (JSON ONLY):
{
  "introduction": "",
  "organizational_summary": "",
  "problem_statement": "",
  "project_overview": "",
  "alignment_statement": "",
  "funding_request": "",
  "closing_statement": ""
}
"""

def normalize_loi_output(raw_output: dict, session_id: str):
    return {
        "introduction": raw_output.get("introduction", ""),
        "organizational_summary": raw_output.get("organizational_summary", ""),
        "problem_statement": raw_output.get("problem_statement", ""),
        "project_overview": raw_output.get("project_overview", ""),
        "alignment_statement": raw_output.get("alignment_statement", ""),
        "funding_request": raw_output.get("funding_request", ""),
        "closing_statement": raw_output.get("closing_statement", ""),
        "session_id": session_id
    }


def generate_loi(session_id: str):
    org_data = get_organization_analysis(session_id)
    if not org_data:
        raise ValueError("Invalid session_id")

    # Convert datetime to ISO string
    org_data_serializable = org_data.copy()
    if "created_at" in org_data_serializable:
        org_data_serializable["created_at"] = org_data_serializable["created_at"].isoformat()

    

    context = {
        "organization": org_data_serializable,
        "task": "Generate LOI following TGCI standards"
    }

    response = client.chat.completions.create(
        model="gpt-4.1",
        messages=[
            {"role": "system", "content": TGCI_LOI_PROMPT},
            {"role": "user", "content": json.dumps(context, default=str)}
        ],
        temperature=0.2
    )

    raw_loi = json.loads(response.choices[0].message.content)
    return normalize_loi_output(raw_loi, session_id)

