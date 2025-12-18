from app.services.llm_service import run_ai_analysis

def analyze_with_website(payload):
    context = {
        "scenario": "WITH_WEBSITE",
        "website_name": payload.website_name,
        "url": payload.url,
        "mission": payload.mission
    }
    return run_ai_analysis(context)


def analyze_without_website(payload):
    context = {
        "scenario": "WITHOUT_WEBSITE",
        "mission": payload.mission,
        "core_purpose": payload.core_purpose,
        "type_of_work": payload.type_of_work,
        "goals_aspirations": payload.goals_aspirations
    }
    return run_ai_analysis(context)
