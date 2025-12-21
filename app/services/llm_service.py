from openai import OpenAI
from app.config import OPENAI_API_KEY
from app.services.tgci_knowledge import load_tgci_knowledge
import json

client = OpenAI(api_key=OPENAI_API_KEY)

tgci_knowledge = load_tgci_knowledge()


TGCI_ORG_PROFILE_PROMPT = """
Extract and structure the organization's factual profile
using ONLY the provided information.

STRICT RULES:
- Do NOT invent facts
- Do NOT evaluate readiness
- If information is missing, write high-level factual language

Generate:
- mission_statement
- programs
- achievements
- budget_statement
- evaluation

Return JSON ONLY.
"""


TGCI_READINESS_PROMPT = """
You are a TGCI-trained grant readiness evaluator.

Your task is to assess organizational grant readiness using TGCI principles.
Do NOT invent facts. Base evaluation ONLY on provided information.

CLASSIFICATION RULES (VERY IMPORTANT):

1. GRANT_READY
- Mission is clear and specific
- Programs are clearly defined
- Evidence of impact OR a strong track record is present
- Organizational maturity is demonstrated

2. NEEDS_MINOR_IMPROVEMENTS
- Mission is clear
- Programs or services are conceptually defined
- Some organizational capacity is evident
- Impact data, evaluation details, or maturity are limited or missing

3. NOT_READY
- Mission is unclear or too generic
- Programs are undefined or absent
- No organizational structure or capacity is evident

EVALUATE:
- Mission clarity
- Program definition
- Evidence of impact
- Organizational maturity

Return JSON ONLY in the following format:

{
  "status": "GRANT_READY | NEEDS_MINOR_IMPROVEMENTS | NOT_READY",
  "score": 0-100,
  "gaps": [],
  "recommendations": []
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
    # ---------- STEP 1: ALWAYS generate organizational profile ----------
    profile_response = client.chat.completions.create(
        model="gpt-4.1",
        messages=[
            {
                "role": "system",
                "content": f"""
You are a TGCI-trained grants professional.

Use TGCI knowledge ONLY to structure content,
never to invent facts.

TGCI KNOWLEDGE:
{tgci_knowledge}
"""
            },
            {"role": "system", "content": TGCI_ORG_PROFILE_PROMPT},
            {"role": "user", "content": str(context)}
        ],
        temperature=0.2
    )

    raw_profile = json.loads(profile_response.choices[0].message.content)
    generated_output = normalize_generated_output(raw_profile)

    # ---------- STEP 2: Readiness evaluation ----------
    readiness_response = client.chat.completions.create(
        model="gpt-4.1",
        messages=[
            {
                "role": "system",
                "content": f"""
You are a TGCI-trained grant readiness evaluator.

Use TGCI knowledge ONLY to judge readiness.

TGCI KNOWLEDGE:
{tgci_knowledge}
"""
            },
            {"role": "system", "content": TGCI_READINESS_PROMPT},
            {
                "role": "user",
                "content": json.dumps(
                    {
                        "organization_profile": generated_output,
                        "raw_context": context
                    }
                )
            }
        ],
        temperature=0.2
    )

    readiness = json.loads(readiness_response.choices[0].message.content)

    # Normalize status
    status = readiness["status"].strip().upper()
    if status not in ["GRANT_READY", "NEEDS_MINOR_IMPROVEMENTS", "NOT_READY"]:
        status = "NEEDS_MINOR_IMPROVEMENTS"

    return {
        "status": status,
        "score": readiness["score"],
        "gaps": readiness["gaps"],
        "recommendations": readiness["recommendations"],
        "generated_output": generated_output   # ✅ ALWAYS PRESENT
    }

