from pydantic import BaseModel, Field
from typing import Optional, List, Literal

# ---------------- INPUT ----------------
class GrantOpportunityInput(BaseModel):
    rfp_file: Optional[bytes] = Field(None, description="Upload RFP file")
    opportunity_url: Optional[str] = Field(None, description="Paste opportunity URL")
    opportunity_text: Optional[str] = Field(None, description="Paste opportunity text")

# ---------------- OUTPUT ----------------
class GrantOpportunityDetails(BaseModel):
    funder_name: Optional[str] = Field(None)

    focus_area: Optional[str] = Field(None)
    deadline: Optional[str] = Field(None)
    eligibility: Optional[str] = Field(None)
    attachment_required: Optional[str] = Field(None)
    application_format: Optional[str] = Field(None)

class GrantOpportunityAnalysis(BaseModel):
    key_strengths: Optional[str] = Field(None)
    areas_for_improvement: Optional[str] = Field(None)
    extracted_details: Optional[GrantOpportunityDetails] = None
    status: Literal["NOT_ALIGNED", "POSSIBLY_ALIGNED", "STRONG_FIT"]
