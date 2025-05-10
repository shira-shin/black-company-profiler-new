# tests/test_fetch.py

import os
import pytest
import respx
import httpx
import asyncio

from server.services.fetch_official import fetch_official

@respx.mock
@pytest.mark.asyncio
async def test_fetch_official_list_and_data(monkeypatch):
    # 環境変数を設定（モック用）
    monkeypatch.setenv("ESTAT_APP_ID", "DUMMY_ID")

    # e-Stat list API のモック
    list_url = (
        "https://api.e-stat.go.jp/rest/3.0/app/json/getStatsList"
        "?appId=DUMMY_ID&searchWord=TestCorp&startPosition=1&countGetData=1"
    )
    respx.get(list_url).mock(
        return_value=httpx.Response(
            200,
            json={
                "GET_STATS_LIST": {
                    "STATISTICAL_DATA": [
                        {"@statsDataId": "TEST1234"}
                    ]
                }
            }
        )
    )

    # e-Stat data API のモック
    data_url = (
        "https://api.e-stat.go.jp/rest/3.0/app/json/getStatsData"
        "?appId=DUMMY_ID&statsDataId=TEST1234"
    )
    respx.get(data_url).mock(
        return_value=httpx.Response(200, json={"foo": "bar"})
    )

    # 実行＆アサート
    result = await fetch_official("TestCorp")
    assert result == {"foo": "bar"}
