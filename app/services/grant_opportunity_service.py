# app/services/grant_opportunity_service.py
from openai import OpenAI
from app.config import OPENAI_API_KEY
from app.schemas.grant_opportunity import GrantOpportunityAnalysis, GrantOpportunityDetails
from app.data.org_store import get_organization_analysis, save_organization_analysis

import requests
import json
import uuid
import io
import pdfplumber
from docx import Document
from bs4 import BeautifulSoup
import openai
import re

# Set your OpenAI API key
client = OpenAI(api_key=OPENAI_API_KEY)

TGCI_GRANT_ANALYSIS_PROMPT = """
You are a TGCI-trained grants evaluator.

YOUR TASK HAS THREE STEPS (DO NOT SKIP ANY STEP):

STEP 1 — GRANT DETECTION
Determine whether the provided text represents a REAL GRANT OPPORTUNITY,
RFP, funding call, or application notice.

A REAL GRANT OPPORTUNITY MAY:
- Explicitly state funding, eligibility, deadline, or application steps
- OR clearly IMPLY them through program descriptions, calls for applicants,
  or funding announcements

If the text is ONLY informational, promotional, or unrelated to funding,
then it is NOT a real grant opportunity.

STEP 2 — GRANT NORMALIZATION (CRITICAL)
If the text IS a real or implied grant opportunity:
- Rewrite the grant opportunity into a CLEAN, STRUCTURED description
- Preserve ONLY information that is present or clearly implied
- Do NOT invent facts
- Do NOT add assumptions

This normalized understanding MUST be used for analysis.

STEP 3 — TGCI ALIGNMENT ANALYSIS
Using the ORGANIZATION PROFILE and the NORMALIZED GRANT DESCRIPTION:

- Compare mission, programs, and goals
- Apply TGCI grantsmanship principles
- Identify alignment strengths and gaps
- Extract factual grant details IF present or clearly implied

OUTPUT RULES (STRICT):

Return JSON ONLY in the following format:

{
  "key_strengths": "",
  "areas_for_improvement": "",
  "extracted_details": {
    "funder_name": "",
    "focus_area": "",
    "deadline": "",
    "eligibility": "",
    "attachment_required": "",
    "application_format": ""
  },
  "status": "NOT_ALIGNED | POSSIBLY_ALIGNED | STRONG_FIT"
}

STATUS RULES:
- NOT_ALIGNED:
  - Use ONLY if the text is clearly NOT a grant opportunity
  - key_strengths MUST be empty
  - areas_for_improvement MUST be empty
  - ALL extracted_details MUST be empty
- POSSIBLY_ALIGNED:
  - Use if the grant exists but alignment is partial or unclear
- STRONG_FIT:
  - Use if there is clear mission and program alignment

ADDITIONAL CONSTRAINTS:
- NEVER hallucinate missing information
- DO NOT require explicit deadlines or funding amounts if the grant is implied
- Use concise, professional TGCI language
- Consider PDFs, webpages, Google Docs, and online notices as valid inputs
"""



def clean_text(text: str) -> str:
    """Remove excessive line breaks, multiple spaces, non-ASCII chars"""
    text = re.sub(r'\n+', '\n', text)
    text = re.sub(r'\s+', ' ', text)
    return text.strip()


def extract_text_from_file(file_bytes: bytes) -> str:
    """Extract text from PDF or DOCX files"""
    # PDF
    try:
        with pdfplumber.open(io.BytesIO(file_bytes)) as pdf:
            text = "".join([page.extract_text() or "" for page in pdf.pages])
        if text.strip():
            return text
    except Exception:
        pass

    # DOCX
    try:
        doc = Document(io.BytesIO(file_bytes))
        text = "\n".join([p.text for p in doc.paragraphs if p.text.strip()])
        if text.strip():
            return text
    except Exception:
        pass

    return ""


def get_text_from_url(url: str) -> str:
    """
    Download content from a URL and return text.
    Handles PDF, DOCX, Google Docs (export as PDF), or public web page text.
    """
    try:
        # Google Docs export as PDF
        if "docs.google.com/document" in url:
            if not url.endswith("/export?format=pdf"):
                url = url.replace("/edit", "/export?format=pdf")

        resp = requests.get(url, timeout=15)
        resp.raise_for_status()
        content_type = resp.headers.get("Content-Type", "").lower()

        # PDF
        if "pdf" in content_type or url.lower().endswith(".pdf"):
            return extract_text_from_file(resp.content)

        # Word
        elif "word" in content_type or url.lower().endswith((".docx", ".doc")):
            return extract_text_from_file(resp.content)

        # Fallback: HTML page
        elif "html" in content_type or url.lower().endswith(".html"):
            soup = BeautifulSoup(resp.text, "html.parser")
            texts = [t.get_text(separator=" ", strip=True) for t in soup.find_all(['p','h1','h2','h3','li'])]
            return "\n".join(texts)

        else:
            return resp.text

    except Exception:
        return f"Grant opportunity reference: {url}"


def create_combined_session(org_session_id: str, grant_analysis: dict) -> str:
    """Save combined organization + grant analysis into org_store"""
    org_data = get_organization_analysis(org_session_id)
    if not org_data:
        raise ValueError("Invalid org session")

    new_session_id = str(uuid.uuid4())

    combined_payload = {
        "organization": org_data,
        "grant": grant_analysis
    }

    save_organization_analysis(
        new_session_id,
        payload={"source": "UPLOADED_GRANT"},
        analysis=combined_payload
    )

    return new_session_id


def analyze_grant_opportunity(input_data, session_id: str):
    """
    Main function to analyze grant opportunity.
    Supports PDF/Word files, Google Docs URLs, public webpages, or plain text.
    """
    # 1. Load organization profile
    org_data = get_organization_analysis(session_id)
    if not org_data:
        raise ValueError("Invalid or expired session_id")

    # 2. Prepare grant opportunity text
    if getattr(input_data, "rfp_file", None):
        opportunity_text = clean_text(extract_text_from_file(input_data.rfp_file))
    elif getattr(input_data, "opportunity_url", None):
        opportunity_text = clean_text(get_text_from_url(input_data.opportunity_url))
    else:
        opportunity_text = clean_text(getattr(input_data, "opportunity_text", ""))

    # 3. Build context for LLM
    context = {
        "organization": org_data,
        "grant_opportunity": opportunity_text
    }

    # 4. Call OpenAI
    ai_response = client.chat.completions.create(
        model="gpt-5",
        messages=[
            {"role": "system", "content": TGCI_GRANT_ANALYSIS_PROMPT},
            {"role": "user", "content": json.dumps(context, indent=2, default=str)}
        ]
        
    )

    raw_output = json.loads(ai_response.choices[0].message.content)


    details = GrantOpportunityDetails(**raw_output.get("extracted_details", {}))
    analysis = GrantOpportunityAnalysis(
        key_strengths=raw_output.get("key_strengths"),
        areas_for_improvement=raw_output.get("areas_for_improvement"),
        extracted_details=details,
        status=raw_output.get("status")
    )

    new_session_id = create_combined_session(
        org_session_id=session_id,
        grant_analysis=analysis.dict()
    )

    return {
        "combined_session_id": new_session_id,
        "analysis": analysis.dict()
    }


