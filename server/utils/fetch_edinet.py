import os
import httpx

# EDINET API の新ドメインを優先的に使用
EDINET_URL = os.getenv("EDINET_API_URL") or "https://disclosure2d.edinet-fsa.go.jp/api/v1/documents.json"

async def fetch_edinet(ticker: str):
    """
    EDINET APIから有価証券報告書メタデータを取得。
    - ticker: 東証ティッカー（文字列）
    """
    if not ticker:
        return []

    params = {"type": 2, "code": ticker}
    headers = {"User-Agent": "Mozilla/5.0"}

    async with httpx.AsyncClient() as client:
        # まず新ドメインで試す
        response = await client.get(EDINET_URL, params=params, headers=headers)
        if response.status_code == 403:
            # 新ドメインで403が出たら旧ドメインを試す
            fallback = "https://disclosure.edinet-fsa.go.jp/api/v1/documents.json"
            response = await client.get(fallback, params=params, headers=headers)
        response.raise_for_status()
        data = response.json().get("results", [])

    # 結果を整形して返却
    return [
        {"docID": d.get("docID"), "name": d.get("docDescription"), "date": d.get("docDate")} 
        for d in data
    ]
