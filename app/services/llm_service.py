from openai import OpenAI
from app.config import OPENAI_API_KEY, MODEL_NAME
import json

client = OpenAI(api_key=OPENAI_API_KEY)



TGCI_READINESS_PROMPT = """
You are a TGCI-trained grant readiness evaluator.

Step 1: Determine if the organization is ready for grant funding.

Evaluate:
- Mission clarity
- Program definition
- Evidence of impact
- Organizational maturity

Return JSON:
{
  "status": "GRANT_READY | NEEDS_MINOR_IMPROVEMENTS | NOT_READY",
  "score": 0-100,
  "gaps": [],
  "recommendations": []
}
"""

TGCI_GENERATION_PROMPT = """
The organization is GRANT READY.

Generate proposal-ready content:

- mission_statement
- programs
- achievements
- budget_statement
- evaluation

Write in professional grantsmanship language.
Return JSON only.
"""

TGCI_GRANT_ANALYSIS_PROMPT = """
You are a TGCI-trained grants evaluator.

Compare the organization’s profile (mission, programs, achievements) with the provided grant opportunity text.

Return a JSON object:

{
  "key_strengths": "Text describing alignment strengths",
  "areas_for_improvement": "Text describing gaps or weaknesses",
  "extracted_details": {
      "founder_name": "...",
      "focus_area": "...",
      "deadline": "...",
      "eligibility": "...",
      "attachment_required": "...",
      "application_format": "..."
  },
  "status": "NOT_ALIGNED | POSSIBLY_ALIGNED | STRONG_FIT"
}
"""


def normalize_generated_output(gen_output: dict) -> dict:
    if not gen_output:
        return None
    output = gen_output.copy()
    
    # Convert lists to single string
    for key in ["programs", "achievements"]:
        value = output.get(key)
        if isinstance(value, list):
            # Join strings or dicts into readable string
            if all(isinstance(item, dict) for item in value):
                output[key] = "\n".join([f"{item.get('name')}: {item.get('description')}" for item in value])
            else:
                output[key] = "\n".join(value)
    return output


def run_ai_analysis(context: dict):
    ai_response = client.chat.completions.create(
        model="gpt-4.1",
        messages=[
            {"role": "system", "content": TGCI_READINESS_PROMPT},
            {"role": "user", "content": str(context)}
        ],
        temperature=0.2
    )

    response_content = ai_response.choices[0].message.content
    readiness = json.loads(response_content)

    # Normalize status
    status = readiness["status"].strip().upper()
    if status not in ["GRANT_READY", "NEEDS_MINOR_IMPROVEMENTS", "NOT_READY"]:
        if "MINOR" in status:
            status = "NEEDS_MINOR_IMPROVEMENTS"
        else:
            status = "NOT_READY"

    readiness["status"] = status

    # Generate content if ready
    generated_output = None
    if status == "GRANT_READY":
        ai_response2 = client.chat.completions.create(
            model="gpt-4.1",
            messages=[
                {"role": "system", "content": TGCI_GENERATION_PROMPT},
                {"role": "user", "content": str(context)}
            ],
            temperature=0.2
        )
        raw_output = json.loads(ai_response2.choices[0].message.content)
        generated_output = normalize_generated_output(raw_output)


    return {
        "status": readiness["status"],
        "score": readiness["score"],
        "gaps": readiness["gaps"],
        "recommendations": readiness["recommendations"],
        "generated_output": generated_output
    }