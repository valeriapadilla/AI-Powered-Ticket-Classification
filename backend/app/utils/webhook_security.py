import hmac, hashlib, os

def verify_signature(payload: bytes, signature: str | None) -> bool:
    SECRET = os.getenv("GH_WEBHOOK_SECRET", "")

    if not signature or not SECRET:
        return False
    try:
        algo, sig = signature.split("=", 1)
    except ValueError:
        return False
    if algo != "sha256":
        return False
    mac = hmac.new(SECRET.encode(), msg=payload, digestmod=hashlib.sha256)
    return hmac.compare_digest(mac.hexdigest(), sig)