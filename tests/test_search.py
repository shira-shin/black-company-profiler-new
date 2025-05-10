# tests/test_search.py

import pytest
from openai import OpenAIError
import server.services.fetch_search as fs

class DummyResponse:
    def __init__(self, result):
        self.result = result

@pytest.mark.asyncio
async def test_fetch_search_success(monkeypatch):
    # モックした create() を用意
    async def fake_create(model, input, tools):
        return DummyResponse(f"Mocked summary for [{input}]")
    # 差し替え
    monkeypatch.setattr(fs.client.responses, 'create', fake_create)

    result = await fs.fetch_search("TestCorp")
    assert "Mocked summary for" in result
    assert "TestCorp" in result

@pytest.mark.asyncio
async def test_fetch_search_error(monkeypatch):
    async def fake_create(model, input, tools):
        raise OpenAIError("API failure")
    monkeypatch.setattr(fs.client.responses, 'create', fake_create)

    result = await fs.fetch_search("TestCorp")
    # エラー時は空文字
    assert result == ""
