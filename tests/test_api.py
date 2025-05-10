# tests/test_api.py

import pytest
from fastapi.testclient import TestClient
from server.main import app

@pytest.fixture
def client():
    return TestClient(app)

def test_profile_endpoint(monkeypatch, client):
    # Mock fetch_official
    async def fake_fetch_official(company, statsDataId=None):
        return {
            "GET_STATS_DATA": {
                "STATISTICAL_DATA": {
                    "RESULTS_OVER_TIME": {
                        "TIME_PERIOD": [
                            {"@timeCode":"2020","C1":"100","C2":"0.10","C3":"0.8"},
                            {"@timeCode":"2021","C1":"150","C2":"0.15","C3":"1.0"},
                        ]
                    }
                }
            }
        }
    monkeypatch.setattr(
        "server.services.fetch_official.fetch_official",
        fake_fetch_official
    )

    # Mock fetch_search
    async def fake_fetch_search(company):
        return "Dummy background info"
    monkeypatch.setattr(
        "server.services.fetch_search.fetch_search",
        fake_fetch_search
    )

    # Call endpoint with required fields
    resp = client.post(
        "/profile",
        json={
            "company": "TestCorp",
            "preset": "default",
            "statsDataId": ""
        }
    )
    assert resp.status_code == 200

    data = resp.json()
    # 必須キーがすべて含まれていることだけを確認
    for key in ("company", "score", "rank", "comment", "breakdown"):
        assert key in data
