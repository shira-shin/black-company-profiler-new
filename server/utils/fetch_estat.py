import os
import httpx

# 1) Ensure you have the correct e-Stat endpoint in .env:
#    ESTAT_URL=https://api.e-stat.go.jp/rest/3.0/app/json/getStatsData
ESTAT_URL = os.getenv("ESTAT_URL")

async def fetch_estat(statsDataId: str):
    """
    Fetch e-Stat statistics data with a 30-second timeout.
    Returns a dict of parsed metrics or empty dict on error/timeout.
    """
    if not statsDataId or ESTAT_URL is None:
        return {}

    params = {
        "appId": statsDataId,
        # e-Stat requires statsDataId param, not appId key name; adjust accordingly:
        "statsDataId": statsDataId,
        "metaGetFlg": "Y",
        "cntGetFlg": "N",
    }

    # 30 seconds for connect & read
    timeout = httpx.Timeout(30.0, read=30.0)
    async with httpx.AsyncClient(timeout=timeout) as client:
        try:
            r = await client.get(ESTAT_URL, params=params)
            r.raise_for_status()
        except httpx.ReadTimeout:
            # timeout → no data
            return {}
        except httpx.HTTPError:
            # any HTTP error → no data
            return {}

    # parse JSON
    data = r.json()
    stats = data.get("GET_STATS_DATA", {}).get("STATISTICAL_DATA", {})
    # Example extraction (update to actual response paths):
    try:
        growth = float(stats["RESULT_INF"]["UnitMeasure"]["@growthRatePct"])
        margin = float(stats["RESULT_INF"]["UnitMeasure"]["@profitMarginPct"])
    except Exception:
        growth = 0.0
        margin = 0.0

    return {
        "growthRatePct": growth,
        "profitMarginPct": margin,
    }
