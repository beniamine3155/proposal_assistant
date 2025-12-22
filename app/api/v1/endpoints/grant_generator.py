from fastapi import APIRouter, Form
from typing import List
from app.services.grant_generator_service import generate_top_grants
from app.schemas.grant_fetch import GrantOpportunity, GrantResponse
from app.data.org_store import get_organization_analysis, save_organization_analysis
import uuid

router = APIRouter(prefix="/grant", tags=["Grant Generator"])


@router.post("/generate", response_model=GrantResponse)
async def generate_grants_endpoint(session_id: str = Form(...)):
    grants = await generate_top_grants(session_id=session_id, top_n=3)

    # Store grants temporarily inside org session
    org_data = get_organization_analysis(session_id)
    if not org_data:
        raise ValueError("Invalid org session")
    org_data["grant_options"] = grants  # each grant now has grant_id

    return GrantResponse(
        grants=[GrantOpportunity(**g) for g in grants]
    )


# @router.post("/generate", response_model=GrantResponse)
# async def generate_grants_endpoint(session_id: str = Form(...)):
#     grants = await generate_top_grants(session_id=session_id, top_n=3)

#     # Save grant options TEMPORARILY in org session
#     org_data = get_organization_analysis(session_id)
#     if not org_data:
#         raise ValueError("Invalid org session")
#     org_data["grant_options"] = grants

#     return GrantResponse(
#         grants=[
#             GrantOpportunity(
#                 session_id=g["session_id"],  # <-- REQUIRED
#                 grant_id=g["grant_id"],
#                 title=g["title"],
#                 focus_area=g["focus_area"],
#                 eligibility=g["eligibility"],
#                 funding_amount=g["funding_amount"],
#                 duration=g["duration"],
#                 rationale=g["rationale"]
#             )
#             for g in grants
#         ]
#     )



@router.post("/select")
def select_grant(
    org_session_id: str = Form(...),
    grant_id: str = Form(...)
):
    org_data = get_organization_analysis(org_session_id)
    if not org_data:
        raise ValueError("Invalid org session")

    selected_grant = next(
        (g for g in org_data.get("grant_options", []) if g["grant_id"] == grant_id),
        None
    )

    if not selected_grant:
        raise ValueError("Invalid grant_id")

    # 🔹 Save a new session combining org + selected grant
    new_session_id = str(uuid.uuid4())

    save_organization_analysis(
        new_session_id,
        payload={"source": "SELECTED_GRANT"},
        analysis={
            "organization": org_data,
            "grant": selected_grant
        }
    )

    return {"session_id": new_session_id}
