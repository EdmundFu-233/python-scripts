"""Simple JWT implementation"""
import json
import base64
import hashlib
import hmac
import time

def b64url_encode(data: bytes) -> str:
    return base64.urlsafe_b64encode(data).rstrip(b'=').decode()

def b64url_decode(data: str) -> bytes:
    padding = 4 - len(data) % 4
    if padding != 4:
        data += '=' * padding
    return base64.urlsafe_b64decode(data)

def create_token(payload: dict, secret: str) -> str:
    header = {"alg": "HS256", "typ": "JWT"}
    header_b64 = b64url_encode(json.dumps(header).encode())
    payload_b64 = b64url_encode(json.dumps(payload).encode())
    signature = hmac.new(secret.encode(), f"{header_b64}.{payload_b64}".encode(),
                        hashlib.sha256).digest()
    sig_b64 = b64url_encode(signature)
    return f"{header_b64}.{payload_b64}.{sig_b64}"

def verify_token(token: str, secret: str) -> dict:
    parts = token.split('.')
    if len(parts) != 3:
        return None
    header_b64, payload_b64, sig_b64 = parts
    expected_sig = hmac.new(secret.encode(), f"{header_b64}.{payload_b64}".encode(),
                           hashlib.sha256).digest()
    actual_sig = b64url_decode(sig_b64)
    if not hmac.compare_digest(expected_sig, actual_sig):
        return None
    return json.loads(b64url_decode(payload_b64))

if __name__ == "__main__":
    payload = {"user": "zhihao", "exp": int(time.time()) + 3600}
    token = create_token(payload, "secret123")
    print(f"Token: {token}")
    decoded = verify_token(token, "secret123")
    print(f"Decoded: {decoded}")
