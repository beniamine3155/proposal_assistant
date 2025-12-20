from app.services.llm_service import run_ai_analysis
from app.services.website_scraper import scrape_website
from app.data.org_store import save_organization_analysis
import uuid


def analyze_with_website(payload):
    scraped_text = scrape_website(payload.url)

    context = {
        "scenario": "WITH_WEBSITE",
        "website_name": payload.website_name,
        "url": payload.url,
        "mission": payload.mission,
        "website_content": scraped_text
    }
    
    result = run_ai_analysis(context)
    
    # Generate a session UUID
    session_id = str(uuid.uuid4())
    result["session_id"] = session_id

    # Save analyzed organization with session_id as key
    save_organization_analysis(session_id, payload.dict(), result)
    
    return result






# def analyze_with_website(payload):
#     context = {
#         "scenario": "WITH_WEBSITE",
#         "website_name": payload.website_name,
#         "url": payload.url,
#         "mission": payload.mission
#     }
#     return run_ai_analysis(context)


def analyze_without_website(payload):
    context = {
        "scenario": "WITHOUT_WEBSITE",
        "mission": payload.mission,
        "core_purpose": payload.core_purpose,
        "type_of_work": payload.type_of_work,
        "goals_aspirations": payload.goals_aspirations
    }
    result = run_ai_analysis(context)

    # Generate a session UUID
    session_id = str(uuid.uuid4())
    result["session_id"] = session_id

    # Save analyzed organization with session_id as key
    save_organization_analysis(session_id, payload.dict(), result)
    
    return result