import json
import re
from openai import OpenAI
from app.config import OPENAI_API_KEY
from app.utils.scraper import scrape_website

client = OpenAI(api_key=OPENAI_API_KEY)


def _ensure_string(value):
    """Convert any value to string, handling lists and dicts."""
    if isinstance(value, list):
        return ", ".join(str(item) for item in value)
    elif isinstance(value, dict):
        return json.dumps(value)
    elif value is None:
        return None
    else:
        return str(value)


def analyze_without_website(mission: str, core_purpose: str, type_of_work: str, goals_aspirations: str) -> dict:
    """
    Analyze proposal without website (using provided details only).
    """
    text_input = f"""
        Mission: {mission}
        Core Purpose: {core_purpose}
        Type of Work: {type_of_work}
        Goals and Aspirations: {goals_aspirations}
    """
    
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "system", 
                    "content": "You are a proposal writing assistant. You must respond with ONLY valid JSON, nothing else."
                },
                {
                    "role": "user", 
                    "content": f"""Analyze this proposal information and generate detailed responses for each field:

                    {text_input}

                    Return ONLY this JSON (no markdown, no extra text):
                    {{"mission_statement": "the core mission statement", "programs": "list of main programs or initiatives", "achievements": "expected achievements or outcomes", "budget_statement": "budget information or estimate", "evaluation": "evaluation of potential impact and effectiveness"}}"""
                }
            ],
            temperature=0.7
        )
        
        raw_response = response.choices[0].message.content.strip()
        print("Raw OpenAI Response:", raw_response)
        
        # Extract JSON from response (handles case where OpenAI adds markdown)
        json_match = re.search(r'\{.*\}', raw_response, re.DOTALL)
        if json_match:
            json_str = json_match.group(0)
            result = json.loads(json_str)
            return {
                "mission_statement": _ensure_string(result.get("mission_statement")) or mission,
                "programs": _ensure_string(result.get("programs")),
                "achievements": _ensure_string(result.get("achievements")),
                "budget_statement": _ensure_string(result.get("budget_statement")),
                "evaluation": _ensure_string(result.get("evaluation"))
            }
        else:
            raise ValueError("No valid JSON found in response")
            
    except json.JSONDecodeError as e:
        print(f"JSON parsing error: {str(e)}")
        raise
    except Exception as e:
        print(f"Error during analysis: {str(e)}")
        raise



def analyze_with_website(website_name: str, url: str, mission: str) -> dict:
    """
    Analyze proposal using website content.
    """
    scraped_content = scrape_website(url)
    
    if not scraped_content:
        raise ValueError(f"Could not scrape content from {url}")
    
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "system", 
                    "content": "You are a proposal writing assistant. Analyze website content and generate proposal details. Respond with ONLY valid JSON, nothing else."
                },
                {
                    "role": "user", 
                    "content": f"""Based on this website content, generate a comprehensive proposal analysis:

                    Website: {website_name}
                    Mission: {mission}
                    Content: {scraped_content[:2000]}

                    Return ONLY this JSON (no markdown, no extra text):
                    {{"mission_statement": "the mission statement", "programs": "list of programs from website", "achievements": "achievements mentioned", "budget_statement": "budget information if available", "evaluation": "evaluation of organization's impact"}}"""
                }
            ],
            temperature=0.7
        )
        
        raw_response = response.choices[0].message.content.strip()
        print("Raw OpenAI Response:", raw_response)
        
        # Extract JSON from response
        json_match = re.search(r'\{.*\}', raw_response, re.DOTALL)
        if json_match:
            json_str = json_match.group(0)
            result = json.loads(json_str)
            return {
                "mission_statement": _ensure_string(result.get("mission_statement")) or mission,
                "programs": _ensure_string(result.get("programs")),
                "achievements": _ensure_string(result.get("achievements")),
                "budget_statement": _ensure_string(result.get("budget_statement")),
                "evaluation": _ensure_string(result.get("evaluation"))
            }
        else:
            raise ValueError("No valid JSON found in response")
            
    except json.JSONDecodeError as e:
        print(f"JSON parsing error: {str(e)}")
        raise
    except Exception as e:
        print(f"Error during website analysis: {str(e)}")
        raise
