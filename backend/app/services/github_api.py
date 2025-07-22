import httpx

BASE_URL = "https://api.github.com"

async def call_github(method: str, path: str, token: str, **kwargs):
    headers = {
        "Authorization": f"Bearer {token}",
        "Accept": "application/vnd.github+json",
    }
    async with httpx.AsyncClient(timeout=10) as client:
        resp = await client.request(method, BASE_URL + path, headers=headers, **kwargs)
        resp.raise_for_status()
        return resp.json() if resp.content else {"status": "ok"}