from app.services.llm_service import client, TGCI_GRANT_ANALYSIS_PROMPT
from app.schemas.grant_opportunity import GrantOpportunityAnalysis, GrantOpportunityDetails
import json

import io
import pdfplumber
from docx import Document


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
