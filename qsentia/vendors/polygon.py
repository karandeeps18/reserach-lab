import os, httpx
from typing import Dict, Any, Iterable, Optional
from tenacity import retry, wait_random_exponential, stop_after_attempt

BASE = "https://api.polygon.io"

class PolygonClient:
    def __init__(self, api_key: Optional[str] = None, timeout: float = 30.0):
        self.key = api_key or os.getenv("POLYGON_API_KEY")
        if not self.key:
            raise RuntimeError("POLYGON_API_KEY not set")
        self.client = httpx.Client(timeout=timeout)

    @retry(wait=wait_random_exponential(multiplier=1, max=20), stop=stop_after_attempt(6))
    def _get(self, path: str, params: Dict[str, Any]) -> Dict[str, Any]:
        params = {**params, "apiKey": self.key}
        r = self.client.get(f"{BASE}{path}", params=params)
        if r.status_code in (429, 500, 502, 503, 504):
            raise RuntimeError(f"Retryable {r.status_code}: {r.text[:120]}")
        r.raise_for_status()
        return r.json()

    # v2 aggregates (daily/minute)
    def agg_bars(self, symbol: str, multiplier: int, timespan: str, start: str, end: str) -> Iterable[Dict[str, Any]]:
        path = f"/v2/aggs/ticker/{symbol}/range/{multiplier}/{timespan}/{start}/{end}"
        params = {"adjusted": "true", "sort": "asc", "limit": 50000}
        data = self._get(path, params)
        for row in data.get("results", []) or []:
            yield row

    # v2 reference/news with pagination
    def news(self, symbol: str, start: str, end: str) -> Iterable[Dict[str, Any]]:
        path = "/v2/reference/news"
        params = {
            "ticker": symbol,
            "published_utc.gte": start,
            "published_utc.lte": end,
            "order": "asc",
            "limit": 100,
        }
        url = f"{BASE}{path}"
        while True:
            data = self._get(path if url.endswith(path) else url.replace(BASE, ""), params)
            for row in data.get("results", []) or []:
                yield row
            nxt = data.get("next_url")
            if not nxt:
                break
            # ensure apiKey on next_url by resetting params and using absolute path
            url = nxt
            params = {}  # key appended in _get