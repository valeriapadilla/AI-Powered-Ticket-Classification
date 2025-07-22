import os, time, httpx, jwt

APP_ID = os.getenv("GITHUB_APP_ID")
KEY_PEM = os.getenv("GITHUB_APP_PRIVATE_KEY_PATH")

def _read_key() -> bytes:
    with open(KEY_PEM, "rb") as f:
        return f.read()

def _generate_jwt() -> str:
    now = int(time.time())
    payload = {"iat": now - 60, "exp": now + 600, "iss": APP_ID}
    return jwt.encode(payload, _read_key(), algorithm="RS256")

async def get_installation_id(owner: str) -> int:
    jwt_token = _generate_jwt()
    headers = {
        "Authorization": f"Bearer {jwt_token}",
        "Accept": "application/vnd.github+json"
    }
    url = "https://api.github.com/app/installations"
    async with httpx.AsyncClient() as client:
        resp = await client.get(url, headers=headers)
        resp.raise_for_status()
        installations = resp.json()
        for inst in installations:
            if inst["account"]["login"].lower() == owner.lower():
                return inst["id"]
        raise Exception(f"No installation found for owner: {owner}")

async def get_installation_token(installation_id: int) -> str:
    jwt_token = _generate_jwt()
    headers = {
        "Authorization": f"Bearer {jwt_token}",
        "Accept": "application/vnd.github+json",
    }
    url = f"https://api.github.com/app/installations/{installation_id}/access_tokens"
    async with httpx.AsyncClient() as client:
        resp = await client.post(url, headers=headers)
        resp.raise_for_status()
        return resp.json()["token"]