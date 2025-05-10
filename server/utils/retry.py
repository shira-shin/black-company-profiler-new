import httpx
from httpx import AsyncClient
import asyncio

class RetryClient(AsyncClient):
    """
    HTTPX AsyncClient wrapper with simple retry on GET requests.
    """
    def __init__(self, *args, **kwargs):
        # default timeouts: connect and read
        kwargs.setdefault('timeout', (5.0, 15.0))
        super().__init__(*args, **kwargs)

    async def get(self, url: str, **kwargs) -> httpx.Response:
        last_err = None
        for _ in range(3):
            try:
                resp = await super().get(url, **kwargs)
                resp.raise_for_status()
                return resp
            except Exception as e:
                last_err = e
                await asyncio.sleep(2)
        # All attempts failed
        raise last_err

# Alias so import retry_client still works
retry_client = RetryClient
