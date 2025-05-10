import httpx
from urllib.parse import quote

# Wikipedia REST API summary endpoint
WIKI_SUMMARY_URL = "https://ja.wikipedia.org/api/rest_v1/page/summary/"

async def fetch_wikipedia(company: str):
    """
    Wikipedia REST API から企業概要の抜粋を取得。
    日本語文字列が正しくエンコードされなかった場合やAPIエラー時には空文字を返す。
    """
    if not company:
        return {"summary": ""}

    # 企業名を URL エンコード
    encoded = quote(company, safe='')
    url = f"{WIKI_SUMMARY_URL}{encoded}"
    headers = {
        "Accept": "application/json",
        "User-Agent": "BlackCompanyProfiler/1.0",
    }

    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(url, headers=headers)
            response.raise_for_status()
            data = response.json()
            return {"summary": data.get("extract", "")}  
        except httpx.HTTPStatusError:
            # 404 やその他ステータスエラー
            return {"summary": ""}
        except Exception:
            # ネットワークエラーやJSON解析エラー
            return {"summary": ""}
