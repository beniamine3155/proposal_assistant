
import json
from openai import OpenAI
from app.config import OPENAI_API_KEY
from app.data.org_store import get_organization_analysis
from app.data.grant_store import get_grant_analysis

client = OpenAI(api_key=OPENAI_API_KEY)

TGCI_PROPOSAL_PROMPT = """
You are a TGCI-trained grants professional.

TASK:
Generate a full proposal draft that follows
The Grantsmanship Center (TGCI) proposal framework.

IMPORTANT RULES (STRICT):
- Use TGCI knowledge ONLY for structure, tone, and logic
- NEVER invent data, programs, metrics, budgets, or outcomes
- Use ONLY information explicitly provided
- If a section lacks data, write high-level and factual
- Do NOT cite TGCI or training materials

TGCI PROPOSAL STRUCTURE:
1. Executive Summary
2. Introduction to the Organization
3. Statement of Need / Problem
4. Program Description (Methods & Activities)
5. Goals and Objectives
6. Evaluation Plan
7. Organizational Capacity
8. Sustainability Plan
9. Budget Summary
10. Conclusion

INPUT CONTEXT:
- Organization analysis
- Grant opportunity alignment analysis

BUDGET HANDLING RULES (VERY IMPORTANT):
- If explicit budget data (amounts, line items) is provided, summarize it accurately.
- If NO budget data is provided:
  - Infer ONLY high-level budget categories based on the described program activities.
  - Allowed categories include (but are not limited to):
    Personnel, Program Costs, Training, Materials, Evaluation, Administration.
  - Do NOT invent dollar amounts.
  - Use "TBD" for all cost fields.
  - Provide brief factual descriptions explaining what each category would cover.
- If even categories cannot be reasonably inferred, write a descriptive narrative
  explaining expected cost areas without listing categories.



OUTPUT FORMAT (JSON ONLY):
{
  "executive_summary": "",
  "organization_background": "",
  "problem_statement": "",
  "program_description": "",
  "goals_and_objectives": "",
  "evaluation_plan": "",
  "organizational_capacity": "",
  "sustainability_plan": "",
  "budget_summary": {
    "line_items": [
        {
        "category": "",
        "description": "",
        "estimated_cost": ""
        }
    ],
    "total_estimated_budget": ""
    }
  "conclusion": ""

}
"""

def normalize_proposal_output(raw_output: dict, session_id: str):
    budget = raw_output.get("budget_summary", {})

    # Normalize line items
    normalized_line_items = []
    if isinstance(budget, dict):
        for item in budget.get("line_items", []):
            normalized_line_items.append({
                "category": item.get("category", ""),
                "description": item.get("description", ""),
                "estimated_cost": item.get("estimated_cost", "")
            })

    return {
        "executive_summary": raw_output.get("executive_summary", ""),
        "introduction_to_organization": raw_output.get("organization_background", ""),
        "problem_statement": raw_output.get("problem_statement", ""),
        "goals_and_objectives": raw_output.get("goals_and_objectives", ""),
        "methods_and_activities": raw_output.get("program_description", ""),
        "evaluation_plan": raw_output.get("evaluation_plan", ""),
        "sustainability_plan": raw_output.get("sustainability_plan", ""),
        "budget_summary": {
            "line_items": normalized_line_items,
            "total_estimated_budget": budget.get("total_estimated_budget", "")
        },
        "conclusion": raw_output.get("conclusion", ""),
        "session_id": session_id
    }






def generate_proposal(session_id: str):
    org_data = get_organization_analysis(session_id)
    if not org_data:
        raise ValueError("Invalid session_id")

     # Convert datetime to ISO string
    org_data_serializable = org_data.copy()
    if "created_at" in org_data_serializable:
        org_data_serializable["created_at"] = org_data_serializable["created_at"].isoformat()

    analysis = org_data.get("analysis", {})

    context = {
        "organization": analysis.get("organization", {}),
        "grant": analysis.get("grant", {}),
        "task": "Generate Proposal following TGCI standards"
    }

    response = client.chat.completions.create(
        model="gpt-4.1",
        messages=[
            {"role": "system", "content": TGCI_PROPOSAL_PROMPT},
            {"role": "user", "content": json.dumps(context, default=str)}
        ],
        temperature=0.2
    ) 

    proposal = json.loads(response.choices[0].message.content)
    
 
    return normalize_proposal_output(proposal, session_id)
