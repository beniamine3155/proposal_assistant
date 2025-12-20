import requests
from bs4 import BeautifulSoup


def scrape_website(url: str) -> str:
    """
    Deterministically extract public website text.
    NO AI here.
    """
    try:
        resp = requests.get(url, timeout=10, headers={
            "User-Agent": "Mozilla/5.0"
        })
        resp.raise_for_status()
    except Exception:
        return ""

    soup = BeautifulSoup(resp.text, "html.parser")

    # Remove noise
    for tag in soup(["script", "style", "nav", "footer", "header"]):
        tag.decompose()

    paragraphs = [p.get_text(" ", strip=True) for p in soup.find_all("p")]
    text = " ".join(paragraphs)

    return text[:12000]  # HARD LIMIT to prevent hallucination
