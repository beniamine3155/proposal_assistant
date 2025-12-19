from openai import OpenAI
from app.config import OPENAI_API_KEY
from app.services.tgci_knowledge import load_tgci_knowledge
import json

client = OpenAI(api_key=OPENAI_API_KEY)

tgci_knowledge = load_tgci_knowledge()

TGCI_READINESS_PROMPT = """
You are a TGCI-trained grant readiness evaluator.

Evaluate whether the organization is ready for grant funding
based ONLY on the information explicitly provided.

Evaluate:
- Mission clarity
- Program definition
- Evidence of impact
- Organizational maturity

STRICT RULES:
- Do NOT assume missing information
- Do NOT infer capacity beyond stated facts
- Penalize unclear, vague, or aspirational-only statements

Return JSON ONLY:
{
  "status": "GRANT_READY | NEEDS_MINOR_IMPROVEMENTS | NOT_READY",
  "score": 0-100,
  "gaps": [],
  "recommendations": []
}

"""

TGCI_GENERATION_PROMPT = """
The organization has been determined to be GRANT READY.

Generate proposal-ready content using ONLY the information
explicitly provided in the organization profile.

STRICT RULES:
- Do NOT invent programs, budgets, metrics, or achievements
- If information is missing, write in high-level but factual language
- Use TGCI grantsmanship tone and structure
- No assumptions, no fictional data

Generate:
- mission_statement
- programs
- achievements
- budget_statement
- evaluation

Return JSON ONLY.
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
        messages = [
    {
        "role": "system",
        "content": f"""
You are a TGCI-trained evaluator.

You have internal knowledge of TGCI books, training materials,
and grantsmanship frameworks.

Use the following TGCI KNOWLEDGE ONLY to:
- judge correctness
- evaluate maturity
- validate structure and patterns

DO NOT quote or reference this knowledge explicitly.

TGCI KNOWLEDGE:
{tgci_knowledge}
"""
    },
    {
        "role": "system",
        "content": TGCI_READINESS_PROMPT
    },
    {
        "role": "user",
        "content": str(context)
    }
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
    {
        "role": "system",
        "content": f"""
You are generating content using TGCI grantsmanship standards.

Use TGCI knowledge ONLY for:
- tone
- structure
- evaluation logic

Never invent facts.
Never embellish missing data.

TGCI KNOWLEDGE:
{tgci_knowledge}
"""
    },
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