import base64
import json
import time

def base64url_encode(data: bytes) -> str:
    return base64.urlsafe_b64encode(data).rstrip(b'=').decode('utf-8')

def base64url_decode(data: str) -> bytes:
    padding = '=' * (-len(data) % 4)
    return base64.urlsafe_b64decode(data + padding)

def create_unsigned_jwt(payload: dict) -> str:
    header = {"alg": "none", "typ": "JWT"}
    payload["iat"] = int(time.time())
    header_enc = base64url_encode(json.dumps(header).encode())
    payload_enc = base64url_encode(json.dumps(payload).encode())
    return f"{header_enc}.{payload_enc}."

def decode_unsigned_jwt(token: str) -> dict:
    parts = token.strip('.').split('.')
    if len(parts) != 2:
        raise ValueError("Invalid unsigned JWT format.")
    header = json.loads(base64url_decode(parts[0]))
    payload = json.loads(base64url_decode(parts[1]))
    return {"header": header, "payload": payload}
