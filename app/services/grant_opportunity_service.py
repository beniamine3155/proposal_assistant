from app.services.llm_service import client
from app.schemas.grant_opportunity import GrantOpportunityAnalysis, GrantOpportunityDetails
import json

import io
import pdfplumber
from docx import Document



TGCI_GRANT_ANALYSIS_PROMPT = """
You are a TGCI-trained grants evaluator.

IMPORTANT RULES (STRICT):
1. First, determine whether the provided text contains a REAL GRANT OPPORTUNITY.
2. A REAL GRANT OPPORTUNITY must include AT LEAST ONE of the following:
   - Application deadline
   - Eligibility criteria
   - Funding description or grant amount
   - Application or submission instructions
3. If NONE of the above are clearly present, then:
   - DO NOT analyze alignment
   - DO NOT infer strengths or weaknesses
   - Return EMPTY fields
   - Set status = NOT_ALIGNED

ONLY IF the text IS a real grant opportunity:
- Compare the organization profile (mission, programs, achievements) with the grant opportunity
- Apply TGCI grantsmanship principles
- Extract factual grant details ONLY if explicitly stated
- Do NOT guess or hallucinate missing details

if the organization is fit with the grant opportunity then
Return JSON ONLY in the following format:

{
  "key_strengths": "",
  "areas_for_improvement": "",
  "extracted_details": {
    "founder_name": "",
    "focus_area": "",
    "deadline": "",
    "eligibility": "",
    "attachment_required": "",
    "application_format": ""
  },
  "status": "NOT_ALIGNED | POSSIBLY_ALIGNED | STRONG_FIT"
}

ADDITIONAL CONSTRAINTS:
- If status is NOT_ALIGNED:
  - key_strengths MUST be empty string
  - areas_for_improvement MUST be empty string
  - ALL extracted_details fields MUST be empty strings
- NEVER invent or assume missing information
- Use concise, professional TGCI language
"""



def extract_text_from_file(file_bytes: bytes) -> str:
    """
    Extracts text from uploaded PDF or DOCX file.
    file_bytes: content of the uploaded file
    Returns extracted text as string.
    """
    # Try PDF first
    try:
        with pdfplumber.open(io.BytesIO(file_bytes)) as pdf:
            text = ""
            for page in pdf.pages:
                text += page.extract_text() + "\n"
        if text.strip():
            return text
    except Exception:
        pass  # Not a PDF, try DOCX next

    # Try DOCX
    try:
        doc = Document(io.BytesIO(file_bytes))
        text = "\n".join([p.text for p in doc.paragraphs if p.text.strip()])
        if text.strip():
            return text
    except Exception:
        pass

    # If unable to extract, return empty string
    return ""


def analyze_grant_opportunity(input_data):
    # Prepare text input from user
    if input_data.rfp_file:
        opportunity_text = extract_text_from_file(input_data.rfp_file)  # Implement PDF/DOCX parser
    elif input_data.opportunity_url:
        opportunity_text = f"Grant opportunity from URL: {input_data.opportunity_url}"
    else:
        opportunity_text = input_data.opportunity_text

    # Call OpenAI to analyze alignment
    ai_response = client.chat.completions.create(
        model="gpt-4.1",
        messages=[
            {"role": "system", "content": TGCI_GRANT_ANALYSIS_PROMPT},
            {"role": "user", "content": opportunity_text}
        ],
        temperature=0.2
    )

    raw_output = json.loads(ai_response.choices[0].message.content)

    # Build Pydantic response
    details = GrantOpportunityDetails(**raw_output.get("extracted_details", {}))
    return GrantOpportunityAnalysis(
        key_strengths=raw_output.get("key_strengths"),
        areas_for_improvement=raw_output.get("areas_for_improvement"),
        extracted_details=details,
        status=raw_output.get("status")
    )
