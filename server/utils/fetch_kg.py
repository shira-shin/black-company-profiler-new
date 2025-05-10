import os, httpx

API_KEY = os.getenv("GOOGLE_KG_API_KEY")
KG_URL  = "https://kgsearch.googleapis.com/v1/entities:search"

async def fetch_kg(company: str):
    params = {"query": company, "key": API_KEY, "limit": 1}
    async with httpx.AsyncClient() as client:
        r = await client.get(KG_URL, params=params)
        r.raise_for_status()
        items = r.json().get("itemListElement", [])
    if not items:
        return {}
    ent = items[0]["result"]
    return {
        "name":        ent.get("name"),
        "description": ent.get("description"),
        "url":         ent.get("detailedDescription", {}).get("url"),
    }
