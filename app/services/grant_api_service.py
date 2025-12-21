# grant_api_service.py
import httpx
from app.config import GRANT_API_KEY, GRANT_API_URL

async def fetch_sample_grants() -> list:
    headers = {
        "Authorization": f"Bearer {GRANT_API_KEY}",
        "Content-Type": "application/json"
    }

    async with httpx.AsyncClient(timeout=10) as client:
        res = await client.get(GRANT_API_URL, headers=headers)
        res.raise_for_status()  # will raise if 4xx/5xx

        # Safely parse JSON
        try:
            data = res.json()
            if not isinstance(data, list):
                # fallback to empty list if unexpected structure
                return []
            return data
        except Exception:
            return []  # fallback to empty list if invalid JSON
