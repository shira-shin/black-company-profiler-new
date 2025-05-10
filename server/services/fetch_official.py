import os
import httpx
from server.utils.retry import retry_client

async def fetch_official(company: str, statsDataId: str = None) -> dict:
    """
    企業名からe-StatのstatsDataIdを動的に読み込み検索し、該当データを取得します。
    statsDataIdを指定すれば直接取得。未指定時は企業名で検索を行います。
    """
    # 環境変数を都度取得することでテストのmonkeypatchが効くように
    app_id = os.getenv('ESTAT_APP_ID')
    if not app_id:
        raise ValueError("ESTAT_APP_ID is not set in environment")

    async with retry_client() as client:
        # statsDataId未指定時はリストAPIから取得
        if not statsDataId:
            list_url = (
                f"https://api.e-stat.go.jp/rest/3.0/app/json/getStatsList"
                f"?appId={app_id}"
                f"&searchWord={company}"
                f"&startPosition=1&countGetData=1"
            )
            resp_list = await client.get(list_url)
            resp_list.raise_for_status()
            data_list = resp_list.json()
            try:
                statsDataId = data_list['GET_STATS_LIST']['STATISTICAL_DATA'][0]['@statsDataId']
            except Exception:
                raise ValueError(f"No statsDataId found for '{company}' via e-Stat list API")

        # 直接データ取得
        data_url = (
            f"https://api.e-stat.go.jp/rest/3.0/app/json/getStatsData"
            f"?appId={app_id}&statsDataId={statsDataId}"
        )
        resp_data = await client.get(data_url)
        resp_data.raise_for_status()
        return resp_data.json()
